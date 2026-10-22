r"""slice_cli.py - slice a 3MF with the installed Bambu Studio command line and summarise the result.

What it does (the slicer is NEVER asked to print, send or upload anything; it only slices):
  1. Copies the input 3MF to <slice_workdir>\<stem>\in.3mf (slice_workdir comes from config\paths.yaml; a path without
     spaces is more reliable for the command line).
  2. Runs:  "<bambu_studio_exe>" --debug <N> --slice 0 --export-3mf out.3mf --outputdir <dir> in.3mf
     (--slice 0 = all plates; --debug 2 = warnings, 3 = info). stdout+stderr are captured to <dir>\cli.log.
  3. Reads <dir>\result.json (return_code, error_string, sliced_plates[] with feature_type_times, filaments, objects,
     warning_message) and greps cli.log for "got warnings". Some warnings do reach result.json warning_message
     (floating regions); the prime-tower clearance warning does not, and the CLI's stdout/stderr can be lost on Windows,
     so the log grep is not a check: run tools\tower_clearance.py, gcode_audit.py and audit_3mf.py as well.
  4. Prints a per-plate summary and exits 0 (clean), 1 (warnings found in log or result.json), 2 (slice failed).
  Work-folder lock: <dir>\.slice_cli.lock is created with O_EXCL and holds this process's PID. If another
  live slice_cli run holds <dir>, this run exits 2 without touching the folder (pass --outdir <unique dir> to run in
  parallel); a lock whose PID is dead is taken over. Before slicing, result.json, out.3mf and plate_*.gcode are removed.
  Orphan guard: on Windows the slicer runs in a Job object with KILL_ON_JOB_CLOSE, so it dies when this process
  dies; the lock also records the slicer's PID and start time and stays held while either process is alive.
  Remaining limit: two runs that find the same stale lock in the same instant can both take it over (not atomic).
  Gated-file guard: before the lock, every file this run would write or delete in <dir> (in.3mf, out.3mf, result.json,
  cli.log, existing plate_*.gcode) is resolved; if one already exists AND is a gated file - it matches
  **\projects\**\print\**\*_SLICED.3mf (case-insensitive) or lies anywhere inside a **\projects\**\print\ folder - the
  run exits 3 with a one-line reason and touches nothing, unless --allow-overwrite is given. The output names are fixed
  (out.3mf, plate_N.gcode), so in practice the guard fires when --outdir points into a print folder that already holds them.

Inputs: a 3MF; config\paths.yaml (bambu_studio_exe, slice_workdir) unless --exe / --outdir are given.
Outputs: <dir>\out.3mf, plate_N.gcode, result.json, cli.log; a summary on stdout (or --json).
Usage: .venv\Scripts\python.exe tools\slice_cli.py <file.3mf> [--debug 2] [--outdir DIR] [--exe PATH] [--timeout 1800] [--json] [--allow-overwrite]
Example: .venv\Scripts\python.exe tools\slice_cli.py examples\calibration-cube\cube.3mf --json
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import re
import shutil
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mm_config  # noqa: E402


def _cfg_path(key: str, fallback: str) -> str:
    """A path from config\\paths.yaml, or `fallback` when the key is empty (the check below then names the problem)."""
    try:
        return str(mm_config.path(key))
    except mm_config.MMConfigError:
        return fallback


DEFAULT_EXE = _cfg_path("bambu_studio_exe", "")
DEFAULT_TMP = _cfg_path("slice_workdir", os.path.join(str(mm_config.repo_root()), "work", "slice"))
LOCK_NAME = ".slice_cli.lock"
LOCK_YOUNG_S = 10.0  # an unreadable lock younger than this is treated as held (its owner may be mid-write)
GUARD_EXIT = 3
# gated files: **\projects\**\print\**\*_SLICED.3mf and "inside a **\projects\**\print\ folder", on the resolved path
GATED_SLICED_RE = re.compile(r"(?:^|[\\/])projects[\\/](?:[^\\/]+[\\/])*?print[\\/](?:[^\\/]+[\\/])*[^\\/]*_sliced\.3mf$", re.I)
PRINT_TREE_RE = re.compile(r"(?:^|[\\/])projects[\\/](?:[^\\/]+[\\/])*?print[\\/]", re.I)


def is_gated_sliced(path: str) -> bool:
    """True if the resolved path matches **\\projects\\**\\print\\**\\*_SLICED.3mf (case-insensitive)."""
    return bool(GATED_SLICED_RE.search(os.path.realpath(path)))


def run_destinations(workdir: str) -> list[str]:
    """Every file a run in `workdir` writes or deletes (the plate G-code count is unknown before slicing: existing
    plate_*.gcode are the ones that would be deleted and rewritten)."""
    fixed = [os.path.join(workdir, n) for n in ("in.3mf", "out.3mf", "result.json", "cli.log")]
    return fixed + sorted(glob.glob(os.path.join(glob.escape(workdir), "plate_*.gcode")))


def gated_overwrite(workdir: str) -> str | None:
    """One-line reason if a destination already exists and is gated, else None."""
    for p in run_destinations(workdir):
        if not os.path.exists(p):
            continue
        rp = os.path.realpath(p)
        if GATED_SLICED_RE.search(rp):
            why = "a gated *_SLICED.3mf under projects\\**\\print\\"
        elif PRINT_TREE_RE.search(rp):
            why = "a file inside a projects\\**\\print\\ folder"
        else:
            continue
        return (f"refused: {rp} already exists and is {why}; slice into a work folder (slice_workdir in "
                f"config\\paths.yaml, or --outdir), or pass --allow-overwrite")
    return None


def _pid_alive(pid: int, since: float | None = None) -> bool:
    """True if process `pid` exists. On Windows, a process created more than 2 s after `since` (the lock time) is a
    reused PID, so it counts as dead. os.kill(pid, 0) is not used on Windows: there it terminates the process."""
    if pid <= 0:
        return False
    if pid == os.getpid():
        return True
    if os.name != "nt":
        try:
            os.kill(pid, 0)
        except ProcessLookupError:
            return False
        except PermissionError:
            return True
        return True
    import ctypes
    from ctypes import wintypes
    k32 = ctypes.WinDLL("kernel32", use_last_error=True)
    k32.OpenProcess.restype = wintypes.HANDLE
    k32.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
    k32.GetExitCodeProcess.argtypes = [wintypes.HANDLE, ctypes.POINTER(wintypes.DWORD)]
    k32.GetProcessTimes.argtypes = [wintypes.HANDLE] + [ctypes.POINTER(wintypes.FILETIME)] * 4
    k32.CloseHandle.argtypes = [wintypes.HANDLE]
    h = k32.OpenProcess(0x1000, False, pid)  # PROCESS_QUERY_LIMITED_INFORMATION
    if not h:
        return ctypes.get_last_error() == 5  # ERROR_ACCESS_DENIED: the process exists but belongs to someone else
    try:
        code = wintypes.DWORD()
        if k32.GetExitCodeProcess(h, ctypes.byref(code)) and code.value != 259:  # 259 = STILL_ACTIVE
            return False
        if since is not None:
            c, e, kt, ut = (wintypes.FILETIME() for _ in range(4))
            if k32.GetProcessTimes(h, ctypes.byref(c), ctypes.byref(e), ctypes.byref(kt), ctypes.byref(ut)):
                created = ((c.dwHighDateTime << 32) | c.dwLowDateTime) / 1e7 - 11644473600.0
                if created > since + 2.0:
                    return False
        return True
    finally:
        k32.CloseHandle(h)


def _read_lock(path: str) -> tuple[dict | None, str]:
    try:
        with open(path, encoding="utf-8") as fh:
            raw = fh.read()
    except FileNotFoundError:
        return None, ""
    try:
        info = json.loads(raw)
        if not isinstance(info, dict):
            return None, raw
        info["pid"], info["time"] = int(info.get("pid") or 0), float(info.get("time") or 0)
        info["child_pid"], info["child_time"] = int(info.get("child_pid") or 0), float(info.get("child_time") or 0)
        return info, raw
    except (ValueError, TypeError):
        return None, raw


def acquire_lock(workdir: str, input_path: str) -> tuple[str | None, str]:
    """Create <workdir>\\.slice_cli.lock with O_EXCL. Returns (lock_path, note) on success, (None, message) if a live
    run holds the folder. A lock with a dead PID (or unreadable and older than LOCK_YOUNG_S) is taken over."""
    lock = os.path.join(workdir, LOCK_NAME)
    note = ""
    for _ in range(5):  # bounded: each retry follows a lock that vanished or was taken over between reads
        try:
            fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        except FileExistsError:
            info, raw = _read_lock(lock)
            if info is None and raw == "" and not os.path.exists(lock):
                continue  # released between open and read: try again
            if info is not None:
                pid, since = info["pid"], info["time"] or None
                if _pid_alive(pid, since):
                    return None, (f"another slice_cli run (PID {pid}, input {info.get('input')!r}) holds {workdir}; "
                                  f"pass --outdir <unique dir>")
                cpid, ctime = info["child_pid"], info["child_time"] or None
                if cpid and _pid_alive(cpid, ctime):
                    return None, (f"another slice_cli run (PID {pid}, input {info.get('input')!r}) holds {workdir}: "
                                  f"it is gone but its slicer (PID {cpid}) is still running; pass --outdir <unique dir>")
                why = f"PID {pid} is not running" + (f" and its slicer PID {cpid} is not running" if cpid else "")
            else:
                try:
                    age = time.time() - os.path.getmtime(lock)
                except FileNotFoundError:
                    continue
                if age < LOCK_YOUNG_S:
                    return None, f"another slice_cli run is creating its lock in {workdir}; pass --outdir <unique dir>"
                why = f"lock unreadable and {age:.0f}s old"
            _, raw_now = _read_lock(lock)
            if raw_now != raw:
                continue  # someone else took it over first: re-evaluate
            try:
                os.remove(lock)
            except FileNotFoundError:
                pass
            note = f"took over a stale lock in {workdir} ({why})"
            continue
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(json.dumps({"pid": os.getpid(), "time": time.time(), "input": input_path}))
        return lock, note
    return None, f"could not take the lock in {workdir} after 5 attempts; pass --outdir <unique dir>"


def release_lock(lock: str) -> None:
    """Remove the lock only if it still records this process (never delete another run's lock)."""
    info, _ = _read_lock(lock)
    if info is not None and info["pid"] == os.getpid():
        try:
            os.remove(lock)
        except FileNotFoundError:
            pass


def record_child(lock: str, child_pid: int, child_time: float) -> None:
    """Add the slicer's PID and start time to this process's lock, so the lock stays held while the slicer lives even if
    this process is killed (belt and braces for the Job object). Rewritten in place: a reader that catches it mid-write
    sees an unreadable, young lock, which counts as held."""
    info, _ = _read_lock(lock)
    if info is None or info["pid"] != os.getpid():
        return
    info["child_pid"], info["child_time"] = child_pid, child_time
    with open(lock, "w", encoding="utf-8") as fh:
        fh.write(json.dumps(info))


CREATE_SUSPENDED = 0x00000004
CREATE_BREAKAWAY_FROM_JOB = 0x01000000


def _k32():
    """kernel32 with the signatures the Job-object launcher needs (Windows only)."""
    import ctypes
    from ctypes import wintypes

    class BASIC(ctypes.Structure):  # JOBOBJECT_BASIC_LIMIT_INFORMATION
        _fields_ = [("PerProcessUserTimeLimit", ctypes.c_int64), ("PerJobUserTimeLimit", ctypes.c_int64),
                    ("LimitFlags", wintypes.DWORD), ("MinimumWorkingSetSize", ctypes.c_size_t),
                    ("MaximumWorkingSetSize", ctypes.c_size_t), ("ActiveProcessLimit", wintypes.DWORD),
                    ("Affinity", ctypes.c_size_t), ("PriorityClass", wintypes.DWORD), ("SchedulingClass", wintypes.DWORD)]

    class IO(ctypes.Structure):  # IO_COUNTERS
        _fields_ = [(n, ctypes.c_uint64) for n in ("ReadOperationCount", "WriteOperationCount", "OtherOperationCount",
                                                    "ReadTransferCount", "WriteTransferCount", "OtherTransferCount")]

    class EXTENDED(ctypes.Structure):  # JOBOBJECT_EXTENDED_LIMIT_INFORMATION
        _fields_ = [("BasicLimitInformation", BASIC), ("IoInfo", IO), ("ProcessMemoryLimit", ctypes.c_size_t),
                    ("JobMemoryLimit", ctypes.c_size_t), ("PeakProcessMemoryUsed", ctypes.c_size_t),
                    ("PeakJobMemoryUsed", ctypes.c_size_t)]

    class THREADENTRY32(ctypes.Structure):
        _fields_ = [("dwSize", wintypes.DWORD), ("cntUsage", wintypes.DWORD), ("th32ThreadID", wintypes.DWORD),
                    ("th32OwnerProcessID", wintypes.DWORD), ("tpBasePri", wintypes.LONG), ("tpDeltaPri", wintypes.LONG),
                    ("dwFlags", wintypes.DWORD)]

    k = ctypes.WinDLL("kernel32", use_last_error=True)
    k.CreateJobObjectW.restype = wintypes.HANDLE
    k.CreateJobObjectW.argtypes = [wintypes.LPVOID, wintypes.LPCWSTR]
    k.SetInformationJobObject.restype = wintypes.BOOL
    k.SetInformationJobObject.argtypes = [wintypes.HANDLE, ctypes.c_int, wintypes.LPVOID, wintypes.DWORD]
    k.AssignProcessToJobObject.restype = wintypes.BOOL
    k.AssignProcessToJobObject.argtypes = [wintypes.HANDLE, wintypes.HANDLE]
    k.TerminateJobObject.restype = wintypes.BOOL
    k.TerminateJobObject.argtypes = [wintypes.HANDLE, wintypes.UINT]
    k.OpenProcess.restype = wintypes.HANDLE
    k.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
    k.CreateToolhelp32Snapshot.restype = wintypes.HANDLE
    k.CreateToolhelp32Snapshot.argtypes = [wintypes.DWORD, wintypes.DWORD]
    k.Thread32First.restype = wintypes.BOOL
    k.Thread32First.argtypes = [wintypes.HANDLE, ctypes.POINTER(THREADENTRY32)]
    k.Thread32Next.restype = wintypes.BOOL
    k.Thread32Next.argtypes = [wintypes.HANDLE, ctypes.POINTER(THREADENTRY32)]
    k.OpenThread.restype = wintypes.HANDLE
    k.OpenThread.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
    k.ResumeThread.restype = wintypes.DWORD
    k.ResumeThread.argtypes = [wintypes.HANDLE]
    k.CloseHandle.restype = wintypes.BOOL
    k.CloseHandle.argtypes = [wintypes.HANDLE]
    return ctypes, k, EXTENDED, THREADENTRY32


def _new_kill_on_close_job():
    """Return (job_handle, "") or (None, reason). The job kills every process in it when its last handle closes, which
    the kernel does when this process exits for any reason, including TerminateProcess."""
    ctypes, k, EXTENDED, _ = _k32()
    job = k.CreateJobObjectW(None, None)
    if not job:
        return None, f"CreateJobObjectW failed (error {ctypes.get_last_error()})"
    info = EXTENDED()
    info.BasicLimitInformation.LimitFlags = 0x2000  # JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
    if not k.SetInformationJobObject(job, 9, ctypes.byref(info), ctypes.sizeof(info)):  # 9 = JobObjectExtendedLimitInformation
        err = ctypes.get_last_error()
        k.CloseHandle(job)
        return None, f"SetInformationJobObject failed (error {err})"
    return job, ""


def _assign(job, pid: int) -> int:
    """Assign process `pid` to `job`. Returns 0 on success, else the Windows error code."""
    ctypes, k, _, _ = _k32()
    h = k.OpenProcess(0x0100 | 0x0001, False, pid)  # PROCESS_SET_QUOTA | PROCESS_TERMINATE (what AssignProcessToJobObject needs)
    if not h:
        return ctypes.get_last_error() or -1
    try:
        return 0 if k.AssignProcessToJobObject(job, h) else (ctypes.get_last_error() or -1)
    finally:
        k.CloseHandle(h)


def _resume(pid: int) -> bool:
    """Resume every thread of a process created with CREATE_SUSPENDED (subprocess closes the primary-thread handle, so
    the threads are found with a Toolhelp snapshot). True if at least one thread was resumed and none failed."""
    ctypes, k, _, THREADENTRY32 = _k32()
    snap = k.CreateToolhelp32Snapshot(0x00000004, 0)  # TH32CS_SNAPTHREAD
    if not snap or snap == ctypes.c_void_p(-1).value:
        return False
    resumed, ok = 0, True
    try:
        te = THREADENTRY32()
        te.dwSize = ctypes.sizeof(THREADENTRY32)
        more = k.Thread32First(snap, ctypes.byref(te))
        while more:
            if te.th32OwnerProcessID == pid:
                th = k.OpenThread(0x0002, False, te.th32ThreadID)  # THREAD_SUSPEND_RESUME
                if not th or k.ResumeThread(th) == 0xFFFFFFFF:
                    ok = False
                else:
                    resumed += 1
                if th:
                    k.CloseHandle(th)
            more = k.Thread32Next(snap, ctypes.byref(te))
    finally:
        k.CloseHandle(snap)
    return ok and resumed > 0


def launch_in_job(cmd: list[str], log) -> tuple[subprocess.Popen, object, str]:
    """Start `cmd` (stdout+stderr to `log`) so that it cannot outlive this process. Returns (proc, job, status).
    Windows: the child is created suspended, assigned to a KILL_ON_JOB_CLOSE job (nested jobs work when this process is
    already in a job, Windows 8+), then resumed. If assignment fails, it is retried once with CREATE_BREAKAWAY_FROM_JOB;
    if that fails too, the child runs without a job, a WARN line goes to stderr and only the lock's child PID guards it."""
    def start(flags: int) -> subprocess.Popen:
        return subprocess.Popen(cmd, stdout=log, stderr=subprocess.STDOUT, creationflags=flags)

    if os.name != "nt":
        return start(0), None, "none: not Windows"
    job, why = _new_kill_on_close_job()
    if job is not None:
        _, k, _, _ = _k32()
        for flags, label in ((CREATE_SUSPENDED, "nested"), (CREATE_SUSPENDED | CREATE_BREAKAWAY_FROM_JOB, "breakaway")):
            try:
                proc = start(flags)
            except OSError as e:
                why = f"{label}: CreateProcess refused (error {getattr(e, 'winerror', None) or e.errno})"
                continue
            err = _assign(job, proc.pid)
            if err == 0:
                if _resume(proc.pid):
                    return proc, job, f"kill-on-close job ({label})"
                k.TerminateJobObject(job, 1)
                proc.wait()
                k.CloseHandle(job)
                raise OSError(f"slice_cli: could not resume the suspended slicer (PID {proc.pid}); it was killed")
            proc.kill()  # still suspended: nothing ran
            proc.wait()
            why = f"{label}: AssignProcessToJobObject failed (error {err})"
        k.CloseHandle(job)
    print(f"slice_cli: WARN the slicer runs without a kill-on-close job ({why}); if this process is killed the slicer "
          f"may outlive it, and the lock stays held until the slicer exits", file=sys.stderr)
    return start(0), None, f"none: {why}"


def close_job(job, kill: bool = False) -> None:
    if job is None:
        return
    _, k, _, _ = _k32()
    if kill:
        k.TerminateJobObject(job, 1)
    k.CloseHandle(job)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path")
    ap.add_argument("--debug", type=int, default=2)
    ap.add_argument("--outdir")
    ap.add_argument("--exe", default=DEFAULT_EXE)
    ap.add_argument("--timeout", type=int, default=1800)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--allow-overwrite", action="store_true",
                    help="allow writing over an existing gated file (*_SLICED.3mf or anything in projects\\**\\print\\)")
    a = ap.parse_args(argv[1:])

    stem = re.sub(r"[^A-Za-z0-9_-]+", "_", os.path.splitext(os.path.basename(a.path))[0])
    workdir = a.outdir or os.path.join(DEFAULT_TMP, stem)
    if not a.allow_overwrite:
        reason = gated_overwrite(workdir)
        if reason is not None:
            print(f"slice_cli: {reason}", file=sys.stderr)
            if a.json:
                print(json.dumps({"input": a.path, "workdir": workdir, "cmd": None, "exit_code": None, "elapsed_s": 0,
                                  "log": None, "log_warnings": [], "result_json": None, "return_code": None,
                                  "error_string": None, "plates": [], "verdict": "FAIL", "guard_error": reason},
                                 indent=1, ensure_ascii=False))
            return GUARD_EXIT
    if not a.exe or not os.path.isfile(a.exe):
        print(f"bambu-studio.exe not found at {a.exe!r}: set bambu_studio_exe in config\\paths.yaml or pass --exe", file=sys.stderr)
        return 2
    os.makedirs(workdir, exist_ok=True)
    lock, note = acquire_lock(workdir, a.path)
    if lock is None:
        print(f"slice_cli: {note}", file=sys.stderr)
        if a.json:
            print(json.dumps({"input": a.path, "workdir": workdir, "cmd": None, "exit_code": None, "elapsed_s": 0,
                              "log": None, "log_warnings": [], "result_json": None, "return_code": None,
                              "error_string": None, "plates": [], "verdict": "FAIL", "lock_error": note},
                             indent=1, ensure_ascii=False))
        else:
            print(f"slice: {a.path}\n  LOCKED: {note}\nVERDICT: FAIL")
        return 2
    if note:
        print(f"slice_cli: {note}", file=sys.stderr)
    try:
        return _slice(a, workdir, lock)
    finally:
        release_lock(lock)


def _slice(a: argparse.Namespace, workdir: str, lock: str) -> int:
    src = os.path.join(workdir, "in.3mf")
    shutil.copyfile(a.path, src)
    out3mf = "out.3mf"  # relative: the CLI writes it into --outputdir; a full path here made export fail (return_code -13)
    for stale in ["result.json", "out.3mf"] + [os.path.basename(g) for g in glob.glob(os.path.join(glob.escape(workdir), "plate_*.gcode"))]:
        p = os.path.join(workdir, stale)
        if os.path.exists(p):
            os.remove(p)
    cmd = [a.exe, "--debug", str(a.debug), "--slice", "0", "--export-3mf", out3mf, "--outputdir", workdir, src]
    out3mf_path = os.path.join(workdir, out3mf)
    log_path = os.path.join(workdir, "cli.log")
    t0 = time.time()
    with open(log_path, "w", encoding="utf-8", errors="replace") as log:
        log.write("CMD: " + " ".join(f'"{c}"' if " " in c else c for c in cmd) + "\n")
        log.flush()
        proc, job, job_status = launch_in_job(cmd, log)
        try:
            record_child(lock, proc.pid, time.time())
            try:
                exit_code = proc.wait(timeout=a.timeout)
            except subprocess.TimeoutExpired:
                close_job(job, kill=True)
                job = None
                if proc.poll() is None:
                    proc.kill()
                proc.wait()
                log.write(f"\nTIMEOUT after {a.timeout}s\n")
                exit_code = -1
        finally:
            if proc.poll() is None:  # an exception left the slicer running: take it down before the lock is released
                close_job(job, kill=True)
                job = None
                proc.kill()
                proc.wait()
            close_job(job)
        log.write(f"\nJOB: {job_status}\n")
    elapsed = round(time.time() - t0, 1)

    with open(log_path, encoding="utf-8", errors="replace") as fh:
        log_text = fh.read()
    log_warnings = [l.strip() for l in log_text.splitlines() if "got warnings" in l or "warning" in l.lower() and "Prime Tower" in l]

    result_path = os.path.join(workdir, "result.json")
    result = None
    if os.path.isfile(result_path):
        with open(result_path, encoding="utf-8") as fh:
            result = json.load(fh)

    summary = {
        "input": a.path, "workdir": workdir, "cmd": cmd, "exit_code": exit_code, "elapsed_s": elapsed,
        "log": log_path, "log_warnings": log_warnings, "result_json": result_path if result else None,
        "return_code": result.get("return_code") if result else None,
        "error_string": result.get("error_string") if result else None,
        "plates": [],
    }
    rj_warnings = 0
    for pl in (result or {}).get("sliced_plates", []) or []:
        ft = pl.get("feature_type_times") or {}
        fils = pl.get("filaments") or []
        wm = pl.get("warning_message") or ""
        if wm:
            rj_warnings += 1
        summary["plates"].append({
            "id": pl.get("id"),
            "total_s": round(pl.get("total_predication") or 0),
            "support_s": round(ft.get("Support", 0) + ft.get("Support interface", 0)),
            "prime_tower_s": round(ft.get("Prime tower", 0)),
            "flush_s": round(ft.get("Flush", 0)),
            "filament_g": [(f.get("filament_id"), round(f.get("total_used_g") or 0, 1)) for f in fils],
            "filament_change_times": pl.get("filament_change_times"),
            "objects": [o.get("name") for o in (pl.get("objects") or [])],
            "warning_message": wm,
        })

    if result is None or (result.get("return_code") not in (0, None)) or exit_code not in (0,):
        verdict, rc = "FAIL", 2
    elif log_warnings or rj_warnings:
        verdict, rc = "WARN", 1
    else:
        verdict, rc = "OK", 0
    summary["verdict"] = verdict

    if a.json:
        print(json.dumps(summary, indent=1, ensure_ascii=False))
    else:
        print(f"slice: {a.path}\n  exit={exit_code} return_code={summary['return_code']} error={summary['error_string']!r} elapsed={elapsed}s\n  log={log_path}")
        for p in summary["plates"]:
            print(f"  plate {p['id']}: total {p['total_s']}s support {p['support_s']}s prime-tower {p['prime_tower_s']}s flush {p['flush_s']}s changes {p['filament_change_times']} filaments {p['filament_g']} objects {p['objects']} warn={p['warning_message']!r}")
        for w in log_warnings:
            print(f"  [LOG WARNING] {w}")
        print(f"VERDICT: {verdict}")
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv))
