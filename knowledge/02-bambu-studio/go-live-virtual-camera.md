# Go Live (virtual camera) in Bambu Studio
Applies to: H2C | P1S (see per-printer rows) · Bambu Studio 02.08.02.61 (source tag v02.08.02.61)
Verified: 2026-10-06

## Facts
What it is
- The wiki page "Streaming video of Bambu Printer" says Studio supplies a virtual camera stream to local RTP for broadcasting. It is a local feed, not a platform broadcaster. — [wiki: virtual camera](https://wiki.bambulab.com/en/software/bambu-studio/virtual-camera)
- UI path: select one printer, click the "Camera Setting" icon at the top-right of the video panel, then toggle "Go Live" (Device tab > Camera Setting > Go Live). It was introduced in v01.04.00.18. — [wiki: virtual camera](https://wiki.bambulab.com/en/software/bambu-studio/virtual-camera), [CameraPopup.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/CameraPopup.cpp) L68, [v01.04.00.18 notes](https://github.com/bambulab/BambuStudio/releases/tag/v01.04.00.18)
- Bambu chose OBS as the route to streaming services because it is popular and gives fine control over the stream. — [v01.04.00.18 notes](https://github.com/bambulab/BambuStudio/releases/tag/v01.04.00.18)
- Later fixes: v01.05.00.59 added Linux; v02.04.00.70 fixed OBS streaming on macOS/Linux; v02.05.00.67 fixed Go Live failing to enable because of a plugin loading error. — [GitHub releases API](https://api.github.com/repos/bambulab/BambuStudio/releases?per_page=100&page=1)
- Neither Studio nor Bambu Handy has an RTMP field, stream key or platform login; the platform connection is made in OBS. — [Handy wiki](https://wiki.bambulab.com/en/studio-handy/handy/bambu-handy-quick-start), [App Store](https://apps.apple.com/us/app/bambu-handy/id1625671285), [OBS overview](https://obsproject.com/kb/obs-studio-overview)

How it works
- It needs a separate download: Studio prompts that "Virtual Camera Tools" are required and offers to install them (`camera_tools.zip`). — [MediaPlayCtrl.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/MediaPlayCtrl.cpp) L701, L712-713
- Two detached helper processes under `%APPDATA%\BambuStudio\cameratools\`: `bambu_source.exe` piped into `ffmpeg.exe` (arguments from `ffmpeg.cfg`, which is not in the repository). — [MediaPlayCtrl.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/MediaPlayCtrl.cpp) L1252-1306
- Output is a local SDP/RTP stream described by `ffmpeg.sdp` in `%APPDATA%\BambuStudio\cameratools\`. — [wiki: virtual camera](https://wiki.bambulab.com/en/software/bambu-studio/virtual-camera)
- One virtual camera at a time: starting a stream from another printer stops the first. — [wiki: virtual camera](https://wiki.bambulab.com/en/software/bambu-studio/virtual-camera)
- Stopping: switch Go Live off. Closing Studio does NOT stop it; the tool keeps running in the background (exception: on the cloud Agora route the stream ends some time after Studio closes). A "Virtual Camera" icon at the top-right of the video panel shows it is running. — [wiki: virtual camera](https://wiki.bambulab.com/en/software/bambu-studio/virtual-camera), [MediaPlayCtrl.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/MediaPlayCtrl.cpp) L685-690, L796

The status icon and the gates
- The toolbar "Go Live" icon is a status picture, not a button: it has no click handler. It is shown only when the printer's `virtual_camera` flag is on; grey (in both themes) means not streaming, and a red element appears while streaming. — [StatusPanel.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/StatusPanel.cpp) L2097-2098, L2150-2165, L2977-2997, [monitor_vcamera_off.svg](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/images/monitor_vcamera_off.svg), [monitor_vcamera_on.svg](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/images/monitor_vcamera_on.svg)
- The real switch is "Go Live" in the Camera Setting popup, shown only when `virtual_camera && has_ipcam`; it toggles the stream. — [CameraPopup.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/CameraPopup.cpp) L312-323, [StatusPanel.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/StatusPanel.cpp) L5632-5648
- Gate 1, model flag: `virtual_camera` is true when the printer reports `ipcam.virtual_camera == "enabled"`, seeded from the printer profile. At this tag the H2C (`O1C.json`, `O1C2.json`), X1C, H2D, H2D Pro and H2S profiles enable it; the P1S profile (`C12.json`) has no `virtual_camera` key. — [DeviceManager.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/DeviceManager.cpp) L3462, [O1C.json](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/printers/O1C.json), [C12.json](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/printers/C12.json)
- Gate 2, camera present (`has_ipcam`, default true, overwritten by the printer). Gate 3, Virtual Camera Tools installed (`bambu_source.exe`, `ffmpeg.exe`, `ffmpeg.cfg` in the cameratools folder), otherwise the download prompt. Gate 4, one virtual camera at a time ("Another virtual camera is running"). — [MediaPlayCtrl.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/MediaPlayCtrl.cpp) L696-737, L1252-1266; [DeviceManager.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/DeviceManager.cpp) L646, L3429-3434
- Gate 5, LAN route: used when the printer reports a local liveview protocol, and is in LAN Only mode or has no remote protocol, and has a known LAN IP. The URL uses user `bblp` and the printer access code. Otherwise (gate 6) the cloud route via the network agent, with "tutk" by default or "agora" when the printer flags support; failure shows "Virtual camera initialize failed (Network unreachable)!". — [MediaPlayCtrl.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/MediaPlayCtrl.cpp) L739-746, L785-796; [DeviceManager.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/DeviceManager.cpp) L1210-1216, L3449-3467
- There is no X1-only check and no active-print gate in the Go Live code; the wiki's "Applicable models: X1, X1C and X1E" is documentation, not code. — [MediaPlayCtrl.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/MediaPlayCtrl.cpp), [DeviceManager.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/DeviceManager.cpp) L2455-2460
- Printer side: if LAN Only Liveview is off, Studio asks you to turn it on on the printer screen. The wiki's LAN-mode page (H2 series / P2S / X series) says to turn on LAN Only mode, then "LAN Only Liveview". Enabling Developer Mode also opens the live stream, among other services. — [MediaPlayCtrl.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/MediaPlayCtrl.cpp) L476, [wiki: LAN mode](https://wiki.bambulab.com/en/knowledge-sharing/enable-lan-mode), [wiki: Developer Mode](https://wiki.bambulab.com/en/knowledge-sharing/enable-developer-mode)
- The H2C firmware release history has no Go Live, virtual camera or RTSP entry, and no official Bambu page names the H2C as supported or unsupported. — [H2C firmware history](https://wiki.bambulab.com/en/h2c/manual/h2c-firmware-release-history)

Security
- While Go Live is on, `%APPDATA%\BambuStudio\cameratools\url.txt` holds the stream URL in plain text: the printer access code on the LAN route, or the cloud URL with its tokens. `encode_path` is a code-page conversion, not encryption. Treat that file as a secret: do not paste, sync or screenshot it. — [MediaPlayCtrl.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/MediaPlayCtrl.cpp) L754-758, L804-808; [utils.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/utils.cpp) L1080-1081

Which printers (official statements)
- Wiki: applicable models X1, X1C and X1E; live streaming is temporarily not supported on H2D, H2S and P2S in some unnamed regions. Neither H2C nor P1S is mentioned. — [wiki EN](https://wiki.bambulab.com/en/software/bambu-studio/virtual-camera), [wiki ZH](https://wiki.bambulab.com/zh/software/bambu-studio/virtual-camera)
- Camera specs: H2C live view camera 1920*1080 (no frame rate given); P1S chamber camera 1280 x 720 at 0.5 fps. — [H2C spec PDF](https://store.bblcdn.com/s7/default/d741f5a073c94245885065ff89a0b2da/H2C_Spec.pdf), [P1S store page](https://us.store.bambulab.com/products/p1s)

Documented route to a streaming platform
- OBS: add a Media Source, uncheck local file (the wiki notes OBS has trouble with local SDP), set the input to the `file:` path of `ffmpeg.sdp`, FFmpeg options `protocol_whitelist=file,udp,rtp`, and wait about a minute for a picture. Alternative on Windows: open `ffmpeg.sdp` in a VLC source. — [wiki: virtual camera](https://wiki.bambulab.com/en/software/bambu-studio/virtual-camera)
- Then in OBS choose a streaming service (or Custom server) and enter the stream key. — [OBS overview](https://obsproject.com/kb/obs-studio-overview), [OBS media sources](https://obsproject.com/kb/media-sources)
- Alternatives to Go Live in OBS: Window Capture (captures one window even if covered) and Video Capture Device (webcams, capture cards; DirectShow on Windows). — [OBS window capture](https://obsproject.com/kb/window-capture-sources), [OBS video capture](https://obsproject.com/kb/video-capture-sources)

## In practice
- H2C: no Bambu page names it for Go Live, but its profile enables the flag, and a GitHub issue about the H2C Go Live click doing nothing was closed as fixed by an update (community report plus contributor closure). — [issue #9514](https://github.com/bambulab/BambuStudio/issues/9514)
- P1S: a Bambu repository collaborator wrote in 2023 that Go Live is not supported on P1P/P1S because of low FPS; consistent with the 0.5 fps spec. — [issue #2099 comment](https://github.com/bambulab/BambuStudio/issues/2099#issuecomment-1648846844)
- A grey Go Live icon means the model gate passes and nothing is streaming; it is not a disabled control. Open Camera Setting and toggle Go Live; the first blocker is usually the Virtual Camera Tools download.
- Which route (LAN or cloud) your printer takes depends on what it reports; you cannot predict it from the profile alone.
- On the LAN route the access code sits in plain text in `url.txt`. Switch Go Live off when done, since closing Studio leaves the tool running.

## Not verified / open questions
- Frame rate, bitrate and RTP port of the stream (set in files inside `camera_tools.zip`).
- Community reports, none verified by Bambu: H2C RTSPS working in ffplay after enabling LAN Only Liveview without full LAN mode [forum](https://forum.bambulab.com/t/h2c-rtsp-for-camera/256148); H2D "nothing appears in OBS" [issue #6690](https://github.com/bambulab/BambuStudio/issues/6690); VLC showing one frame on Studio 2.8.2.61 [issue #12201](https://github.com/bambulab/BambuStudio/issues/12201); overlay request answered with "use OBS" [forum](https://forum.bambulab.com/t/go-live-video-overlay/232455); toggle issues on H2D/P2S [#9529](https://github.com/bambulab/BambuStudio/issues/9529), [#9501](https://github.com/bambulab/BambuStudio/issues/9501).
- go2rtc can take RTSP/RTSPS and publish over RTMP, so it could replace Studio for printers that expose RTSPS on the LAN; not documented by Bambu, and the P1-series camera uses a different TCP-TLS link on port 6000. — [go2rtc README](https://raw.githubusercontent.com/AlexxIT/go2rtc/master/README.md), [P1 wiki](https://wiki.bambulab.com/en/p1/troubleshooting/wifi-bt-liveview)
- Whether Go Live counts against the live-view client limit; audio; duration caps; which regions exclude H2D/H2S/P2S.

Sources:
- https://wiki.bambulab.com/en/software/bambu-studio/virtual-camera — what Go Live is, UI path, OBS setup, models, stopping
- https://wiki.bambulab.com/zh/software/bambu-studio/virtual-camera — same model list
- https://github.com/bambulab/BambuStudio/releases/tag/v01.04.00.18 — introduction, why OBS
- https://api.github.com/repos/bambulab/BambuStudio/releases?per_page=100&page=1 — later fixes
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/CameraPopup.cpp — switch label and condition
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/MediaPlayCtrl.cpp — helpers, routes, url.txt, stop behaviour
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/StatusPanel.cpp — status icon, popup wiring
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/DeviceManager.cpp — `virtual_camera`, `has_ipcam`, liveview protocols
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/utils.cpp — `encode_path`
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/printers/O1C.json — H2C flag (C12.json for P1S in the same folder)
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/images/monitor_vcamera_off.svg — icon colours
- https://wiki.bambulab.com/en/knowledge-sharing/enable-lan-mode — LAN Only Liveview
- https://wiki.bambulab.com/en/knowledge-sharing/enable-developer-mode — Developer Mode opens the live stream
- https://wiki.bambulab.com/en/h2c/manual/h2c-firmware-release-history — no Go Live entry
- https://wiki.bambulab.com/en/p1/troubleshooting/wifi-bt-liveview — P1 camera link
- https://wiki.bambulab.com/en/studio-handy/handy/bambu-handy-quick-start — Handy is view-only
- https://apps.apple.com/us/app/bambu-handy/id1625671285 — Handy listing
- https://store.bblcdn.com/s7/default/d741f5a073c94245885065ff89a0b2da/H2C_Spec.pdf — H2C camera spec
- https://us.store.bambulab.com/products/p1s — P1S camera spec
- https://obsproject.com/kb/obs-studio-overview — service and stream key in OBS
- https://obsproject.com/kb/media-sources — Media Source
- https://obsproject.com/kb/window-capture-sources — Window Capture
- https://obsproject.com/kb/video-capture-sources — Video Capture Device
- https://github.com/bambulab/BambuStudio/issues/9514 — H2C report (community)
- https://github.com/bambulab/BambuStudio/issues/2099 — P1/P1S not supported (collaborator comment)
- https://github.com/bambulab/BambuStudio/issues/6690 — community
- https://github.com/bambulab/BambuStudio/issues/12201 — community
- https://github.com/bambulab/BambuStudio/issues/9529 — community
- https://github.com/bambulab/BambuStudio/issues/9501 — community
- https://forum.bambulab.com/t/h2c-rtsp-for-camera/256148 — community
- https://forum.bambulab.com/t/go-live-video-overlay/232455 — community
- https://raw.githubusercontent.com/AlexxIT/go2rtc/master/README.md — go2rtc
