# Lesson 16: Windows paths turn into control characters in shells and string literals

Area: agent and tool hygiene

This one lesson collects a family of failures that recurred many times.

| What happened | Root cause | Rule now |
|---|---|---|
| Text written with a Bash `printf`, `echo`, `sed` or heredoc came out with tabs, carriage returns and other control bytes where a Windows path had backslashes (for example `\t` in `...\tools\...`). A note's pointer stopped being a path. | In the agent's Bash tool on Windows, backslashes can be consumed before the shell runs, and `printf`, `sed a\` and `echo -e` then read what is left as escapes (`\t`, `\r`, octal `\0nn`). | Text that contains a Windows path goes into a file only through the Write/Edit tools, or through a script file that was itself written with the Write tool. Never through `printf`, `echo`, `sed` or a heredoc. |
| An inline `python -c "..."` edit, and scripts that held paths in normal Python strings, wrote backspace, vertical-tab and other bytes into files (`\b` in `\build`, `\v` in `\v2`, `\0` followed by digits as an octal escape). Python printed "SyntaxWarning: invalid escape sequence", which was ignored as noise. | In a normal Python string `\b \f \n \r \t \v \a` and octal escapes are real escapes. Some warnings are harmless (`\M`), which taught people to ignore all of them. | Any Python that writes Windows paths uses raw strings (`r"..."`) or forward slashes, even in comments that end up in a file. A `SyntaxWarning: invalid escape sequence` is a stop signal: fix the string before using the output. |
| A slicer was launched from a shell loop with a variable inside a quoted Windows path; the variable was not expanded and output landed in a folder literally named with `$`. | Shell quoting and backslash handling combined. | Build slicer paths in a Python script and print them before launching; never assemble them in a shell string. |
| `\uXXXX` escapes typed into Python source through an editing tool were saved as the real characters (line separators, zero-width joiners, direction overrides). | The editing tool decoded the escapes in its input. | Write non-ASCII in source as `chr(0x2028)` or similar; keep tool source files pure ASCII. |

How to check: after every scripted write, scan the file for control and format characters (Unicode categories Cc except tab/newline, Cf, Zl, Zp) and require a count of 0 before hand-off.

```python
import sys, unicodedata
text = open(sys.argv[1], encoding="utf-8", newline="").read().replace("\r\n", "\n")
bad = [(i, hex(ord(c))) for i, c in enumerate(text)
       if c not in "\t\n" and unicodedata.category(c) in ("Cc", "Cf", "Zl", "Zp")]
print(len(bad), bad[:20])
```
