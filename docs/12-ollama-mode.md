# 12 - Ollama mode: run Maker Mastery on local or Ollama Cloud models

How to point Claude Code at [Ollama](https://ollama.com) instead of Anthropic, so Maker Mastery's rulebook, agents,
skills, hooks and tools run on an open model on your own GPU, or on an Ollama Cloud model. Back to the start:
[01 - What this is](01-what-this-is.md). Related: [02 - Install](02-install.md), [11 - Autonomous mode](11-autonomous-mode.md).

Every variable, setting key and UI label below is quoted from the official Ollama or Claude Code documentation, linked
next to it. Things seen on a real PC but not stated in any documentation are marked "(observed)", with the date and
version. Anything else is marked "(not verified)".

> **Read this first.**
> - **Anthropic does not support this.** Claude Code's own docs say Anthropic "doesn't support routing Claude Code to
>   non-Claude models through any gateway" ([Other LLM gateways](https://code.claude.com/docs/en/llm-gateway)). Ollama
>   supports it ([Ollama: Claude Code](https://docs.ollama.com/integrations/claude-code)). If something breaks in Ollama
>   mode, switch back to Claude ([section 7](#7-switch-back-to-claude)) before you report a Maker Mastery bug.
> - **Nothing about print safety changes.** No AI ever starts, sends, uploads or queues a print. The deny rules in
>   `.claude\settings.json` and the guard hook are part of Claude Code on your PC, not of the model, so they apply
>   whichever model answers.
> - **Open models are not Claude.** Expect weaker reasoning on hard tasks, and keep the independent-check rule: a
>   second agent checks everything before it is called ready. How much weaker for Maker Mastery work has not been
>   measured yet (not verified).

## Contents
1. [What Ollama mode is](#1-what-ollama-mode-is)
2. [Set up Ollama](#2-set-up-ollama)
3. [Check the server with ollama_check.py](#3-check-the-server-with-ollama_checkpy)
4. [Connect Claude Code](#4-connect-claude-code)
5. [Confirm it worked](#5-confirm-it-worked)
6. [What works and what does not](#6-what-works-and-what-does-not)
7. [Switch back to Claude](#7-switch-back-to-claude)
8. [Troubleshooting](#8-troubleshooting)
9. [Known flaws](#9-known-flaws)
10. [Sources](#10-sources)

---

## 1. What Ollama mode is

Claude Code normally sends every request to Anthropic. Ollama runs a local server with an Anthropic-compatible API
(`/v1/messages`), and Claude Code can be pointed at it with environment variables
([Ollama: Anthropic compatibility](https://docs.ollama.com/api/anthropic-compatibility)). Maker Mastery itself does not
change: the same `CLAUDE.md`, agents, skills, hooks and tools load as before.

| | Local model | Ollama Cloud model |
|---|---|---|
| Runs on | your GPU | Ollama's servers |
| Your prompts and files | stay on your PC (Claude Code still sends telemetry and some checks to Anthropic, see [section 6](#6-what-works-and-what-does-not)) | go to Ollama ([Ollama: Cloud](https://docs.ollama.com/cloud)) |
| Cost | none per request | per token, for example `glm-5.3:cloud` lists $1.40 input / $4.40 output per 1M tokens ([ollama.com/library/glm-5.3](https://ollama.com/library/glm-5.3)) |
| Needs | a GPU with enough memory for the model and its context window ([Ollama: context length](https://docs.ollama.com/context-length)) | an Ollama account and sign-in. The Free plan "Includes access to starter models"; to "unlock all models" you add credits or pick a paid plan ([ollama.com/pricing](https://ollama.com/pricing)). Whether `glm-5.3:cloud` is a starter model is not stated (not verified) |
| Anthropic account | not needed: a gateway credential replaces the claude.ai login ([Other LLM gateways](https://code.claude.com/docs/en/llm-gateway#subscriptions-and-gateways)); the command line ran with no sign-in at all (observed 2026-10-26, Linux); the VS Code route is not tested yet | not needed |

Model choices that Ollama tags with **tools** (Claude Code needs tool calling):

| Model | Where | Ollama tags | Notes |
|---|---|---|---|
| `qwen3.8:27b` | local | vision, tools, thinking ([library](https://ollama.com/library/qwen3.8)) | 18GB on the library page; `ollama list` shows 17 GB (observed 2026-10-26, Ollama 0.40.11). On a 24 GB RTX 4090 it ran 100% on the GPU at a 64k context, about 112 tokens/s warm (observed 2026-10-26, Ollama 0.40.11) |
| `qwen3.5:9b` | local | vision, tools, thinking ([library](https://ollama.com/library/qwen3.5)) | `ollama list` shows 6.6 GB (observed 2026-10-26, Ollama 0.40.11); for smaller GPUs. Speed and quality in Maker Mastery not measured (not verified) |
| `glm-5.3:cloud` | Ollama Cloud | tools, thinking, cloud; 1M context ([library](https://ollama.com/library/glm-5.3)) | No download, nothing on your GPU |

## 2. Set up Ollama

The app labels in steps 2 to 6 (including the slider's **64k** mark) are as seen in Ollama 0.40.11 on Windows 11
(observed 2026-10-26); Ollama's documentation shows the slider but not these exact labels.

1. Download and install Ollama for Windows from [ollama.com/download/windows](https://ollama.com/download/windows).
   If an older Ollama is running, quit it first (see [section 8](#8-troubleshooting)).
2. Open the **Ollama** app, click the sidebar icon at the top left, then **Settings**.
3. **Model location:** click **Browse** and pick a folder on a drive with room for your models. The app shows
   **Saved**.
4. **Context length:** move the slider to **64k** or higher. Ollama says tasks such as "agents, and coding tools should
   be set to at least 64000 tokens", and documents this slider in the app's settings
   ([Ollama: context length](https://docs.ollama.com/context-length)). Without it, Ollama picks 4k, 32k or 256k from
   your GPU memory (same page), which is too small on most GPUs.
5. **Cloud:** turn it on only if you want cloud models.
6. Quit Ollama (right-click the llama icon in the taskbar > **Quit Ollama**) and start it again from the Start menu, so
   the settings load.
7. In the VS Code terminal, download your model (skip this for a cloud model):

   ```powershell
   ollama pull qwen3.8:27b
   ```

   For a cloud model, sign in once instead: `ollama signin`
   ([Ollama: authentication](https://docs.ollama.com/api/authentication#signing-in)).

## 3. Check the server with ollama_check.py

From the project folder, in the VS Code terminal:

```powershell
.venv\Scripts\python.exe -B tools\ollama_check.py --model qwen3.8:27b
```

It asks the Ollama server on your PC five questions and only talks to `localhost`:

| Check | Passes when |
|---|---|
| O1 | the Ollama server answers |
| O2 | the model is installed (a cloud model only warns) |
| O3 | the model supports tool calling |
| O4 | the loaded model's context window is at least 64000 tokens (O5 loads the model first, so this reads the real value) |
| O5 | the Anthropic-compatible `/v1/messages` endpoint answers a one-token request |

On **VERDICT: OK** or **WARN** it prints the exact settings for the next section, with your model and the loaded context
window filled in. Exit code 0 means OK or WARN, 2 means FAIL. Fix
every FAIL first; each FAIL line says what to do. Full reference: [07 - Tools reference](07-tools-reference.md#ollama_checkpy).

## 4. Connect Claude Code

Claude Code reads these environment variables. Each one is documented in the linked page:

| Variable | Value | Why |
|---|---|---|
| `ANTHROPIC_BASE_URL` | `http://localhost:11434` | sends requests to Ollama ([Ollama: Claude Code](https://docs.ollama.com/integrations/claude-code)) |
| `ANTHROPIC_AUTH_TOKEN` | `ollama` | Ollama needs a token but ignores its value ([Ollama: Anthropic compatibility](https://docs.ollama.com/api/anthropic-compatibility)) |
| `ANTHROPIC_API_KEY` | empty | as in Ollama's manual setup ([Ollama: Claude Code](https://docs.ollama.com/integrations/claude-code)) |
| `ANTHROPIC_DEFAULT_OPUS_MODEL`, `ANTHROPIC_DEFAULT_SONNET_MODEL`, `ANTHROPIC_DEFAULT_HAIKU_MODEL` | your model | Maker Mastery's agents ask for `model: opus` or `model: sonnet`; these variables decide what those aliases resolve to ([Claude Code: model configuration](https://code.claude.com/docs/en/model-config)) |
| `CLAUDE_CODE_SUBAGENT_MODEL` | your model | the default for subagents that name no model ([Claude Code: model configuration](https://code.claude.com/docs/en/model-config)) |
| `CLAUDE_CODE_MAX_CONTEXT_TOKENS` | your loaded context length, for example `65536` | local models only: Claude Code does not recognize Ollama model names and otherwise assumes a 200k window, so it would not compact before the model's real 64k limit ([Claude Code: correct the window](https://code.claude.com/docs/en/model-config#correct-the-window-for-a-gateway-or-custom-model-id)) |

**Never put these in the project's `.claude\settings.json`.** That file is committed and shared
([Claude Code: connect to a gateway](https://code.claude.com/docs/en/llm-gateway-connect)). Use one of the two ways
below; both stay on your PC.

### A. The Claude Code panel in VS Code (recommended)

Claude Code's docs say the VS Code extension reads gateway variables from its `claudeCode.environmentVariables`
setting, which it checks before launching ([Claude Code: connect to a gateway, VS Code extension](https://code.claude.com/docs/en/llm-gateway-connect#vs-code-extension)).

1. In VS Code press **Ctrl+Shift+P**, type **Preferences: Open User Settings (JSON)** and press Enter.
2. Paste the two keys that `tools\ollama_check.py` printed inside the outer `{ }`. If the line above where you paste
   does not end with a comma, add one. For `qwen3.8:27b` loaded at 65536 tokens the two keys are:

   ```json
   "claudeCode.disableLoginPrompt": true,
   "claudeCode.environmentVariables": [
     { "name": "ANTHROPIC_BASE_URL", "value": "http://localhost:11434" },
     { "name": "ANTHROPIC_AUTH_TOKEN", "value": "ollama" },
     { "name": "ANTHROPIC_API_KEY", "value": "" },
     { "name": "ANTHROPIC_DEFAULT_OPUS_MODEL", "value": "qwen3.8:27b" },
     { "name": "ANTHROPIC_DEFAULT_SONNET_MODEL", "value": "qwen3.8:27b" },
     { "name": "ANTHROPIC_DEFAULT_HAIKU_MODEL", "value": "qwen3.8:27b" },
     { "name": "CLAUDE_CODE_SUBAGENT_MODEL", "value": "qwen3.8:27b" },
     { "name": "CLAUDE_CODE_MAX_CONTEXT_TOKENS", "value": "65536" }
   ]
   ```

   `claudeCode.disableLoginPrompt` skips the sign-in prompt "for third-party provider setups"
   ([Claude Code in VS Code: extension settings](https://code.claude.com/docs/en/vs-code)).
3. Save the file, then run **Developer: Reload Window** from **Ctrl+Shift+P**.
4. Open the Claude Code panel. Its model picker (**Switch model…** in the command menu, or `/model`) changes the model
   ([Claude Code in VS Code](https://code.claude.com/docs/en/vs-code)); whether it lists Ollama model names is not verified. Every agent
   that asks for `opus` or `sonnet` uses the model you set in the variables either way.

### B. One VS Code terminal, with the Claude Code command line

Needs the Claude Code command line ([02 - Install](02-install.md)). The variables last only for that terminal
([Claude Code: connect to a gateway](https://code.claude.com/docs/en/llm-gateway-connect)). Paste the PowerShell lines
`tools\ollama_check.py` printed, then start Claude Code with your model (the last line):

```powershell
$env:ANTHROPIC_BASE_URL = "http://localhost:11434"
$env:ANTHROPIC_AUTH_TOKEN = "ollama"
$env:ANTHROPIC_API_KEY = ""
$env:ANTHROPIC_DEFAULT_OPUS_MODEL = "qwen3.8:27b"
$env:ANTHROPIC_DEFAULT_SONNET_MODEL = "qwen3.8:27b"
$env:ANTHROPIC_DEFAULT_HAIKU_MODEL = "qwen3.8:27b"
$env:CLAUDE_CODE_SUBAGENT_MODEL = "qwen3.8:27b"
$env:CLAUDE_CODE_MAX_CONTEXT_TOKENS = "65536"
claude --model qwen3.8:27b
```

Ollama also has a one-line launcher, `ollama launch claude --model qwen3.8:27b`
([Ollama: Claude Code](https://docs.ollama.com/integrations/claude-code)). Whether it also maps the `opus` and
`sonnet` aliases that Maker Mastery's agents use is not documented (not verified), so for Maker Mastery use the lines
above.

## 5. Confirm it worked

1. In Claude Code, type `/status`. The **Status** tab should show an `Anthropic base URL` line with
   `http://localhost:11434`, and an `Auth token` line naming `ANTHROPIC_AUTH_TOKEN`
   ([Claude Code: connect to a gateway](https://code.claude.com/docs/en/llm-gateway-connect#confirm-in-claude-code)).
2. Ask: `Read CLAUDE.md and tell me the one rule about printing.` The answer should be the no-AI-print rule.
3. Ask for a subagent: `Use the librarian agent to list the categories in knowledge\INDEX.md.` While it runs,
   `ollama ps` in a second terminal shows your model loaded.

## 6. What works and what does not

| Feature | In Ollama mode | Source |
|---|---|---|
| Chat, file reads and edits, commands with the permission flow | works with tool-capable models | [Ollama: Claude Code](https://docs.ollama.com/integrations/claude-code) |
| Subagents (all 22 agents) | supported by Ollama; `model: opus` and `model: sonnet` resolve through the variables in section 4. A subagent run in Ollama mode has not been tried yet (not verified) | [Ollama: Claude Code](https://docs.ollama.com/integrations/claude-code), [Claude Code: model configuration](https://code.claude.com/docs/en/model-config) |
| Vision (renders, screenshots) | works with vision models such as `qwen3.8:27b` | [Ollama: Anthropic compatibility](https://docs.ollama.com/api/anthropic-compatibility) |
| Hooks: guard, session start, note check, run log | unchanged: hooks are commands Claude Code runs on your PC, not in the model | [Claude Code: hooks](https://code.claude.com/docs/en/hooks) |
| Deny rules for print, upload and start tools | unchanged: they are Claude Code permission rules | [.claude/settings.notes.md](../.claude/settings.notes.md) |
| `WebSearch` (the `researcher` and `fact-checker` agents rely on it) | "Tool-choice controls, deferred tools, and hosted web search are not fully supported."; Ollama offers web search through an MCP server and an Ollama API key instead | [Ollama: Anthropic compatibility](https://docs.ollama.com/api/anthropic-compatibility), [Ollama: web search](https://docs.ollama.com/capabilities/web-search) |
| `tool_choice` request field | not supported by Ollama | [Ollama: Anthropic compatibility](https://docs.ollama.com/api/anthropic-compatibility) |
| PDF files (`document` blocks), prompt caching, token counting (`count_tokens`) | not supported by Ollama, so datasheet PDFs cannot be sent and the long Maker Mastery system prompt is processed in full on every turn | [Ollama: Anthropic compatibility](https://docs.ollama.com/api/anthropic-compatibility) |
| Deferred tools (used for MCP tool search) | not fully supported | [Ollama: Anthropic compatibility](https://docs.ollama.com/api/anthropic-compatibility) |
| Extended thinking in Claude Code | may stay off: Claude Code turns features such as thinking on by matching the model ID, and the `_SUPPORTED_CAPABILITIES` variables that override this "take effect on third-party providers such as Amazon Bedrock"; through a gateway such as Ollama only `_NAME` and `_DESCRIPTION` do. Not tested here (not verified) | [Claude Code: model configuration](https://code.claude.com/docs/en/model-config) |
| Traffic to Anthropic | the model requests go to Ollama, but Claude Code still sends telemetry, version checks and release notes to Anthropic, and the WebFetch domain check still calls `api.anthropic.com` | [Claude Code: connect to a gateway](https://code.claude.com/docs/en/llm-gateway-connect#turn-off-traffic-outside-the-gateway-path) |
| Plan usage bars, voice dictation, the Web tab | not offered on a third-party setup | [Claude Code in VS Code](https://code.claude.com/docs/en/vs-code) |

**Keep traffic on your PC (optional):** add `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` with the value `1` to the
variables in section 4. It also turns off auto-updates, error reporting and `/feedback`, and any value, even `0`, turns
it on ([Claude Code: environment variables](https://code.claude.com/docs/en/env-vars)). The WebFetch domain check has
its own setting, `skipWebFetchPreflight` ([Claude Code: connect to a gateway](https://code.claude.com/docs/en/llm-gateway-connect#turn-off-traffic-outside-the-gateway-path)).
With auto-updates off, update Claude Code yourself.

**In practice:** run design, DFM, slicing, audits and print-qa in Ollama mode, and keep `/research-topic` and
`/verify-claim` on Claude until web search in Ollama mode is set up and checked. Every knowledge note still needs a
source link and an independent fact-check, whichever model wrote it.

## 7. Switch back to Claude

- **Panel (A):** delete the two `claudeCode.` keys from your user settings (this also removes the optional
  `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` if you added it there, which turns auto-updates back on), save, and reload
  the window. The sign-in
  screen comes back if you were never signed in.
- **Terminal (B):** close that terminal and open a new one; the variables lived only there. To clear them in the same
  terminal instead, remove all of them, not just the first two, or `opus`, `sonnet` and subagents would still ask
  Anthropic for your Ollama model name:

  ```powershell
  Remove-Item Env:ANTHROPIC_BASE_URL, Env:ANTHROPIC_AUTH_TOKEN, Env:ANTHROPIC_API_KEY, Env:ANTHROPIC_DEFAULT_OPUS_MODEL, Env:ANTHROPIC_DEFAULT_SONNET_MODEL, Env:ANTHROPIC_DEFAULT_HAIKU_MODEL, Env:CLAUDE_CODE_SUBAGENT_MODEL, Env:CLAUDE_CODE_MAX_CONTEXT_TOKENS, Env:CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC -ErrorAction SilentlyContinue
  ```

  Then start `claude` again. A gateway credential takes precedence over a saved claude.ai login; unset it and Claude Code
  goes back to the login ([Claude Code: connect to a gateway](https://code.claude.com/docs/en/llm-gateway-connect#conflicts-with-an-existing-login)).
- `/status` shows a `Login method` line again instead of `Anthropic base URL`.

## 8. Troubleshooting

| You see | Fix |
|---|---|
| `could not connect to a running Ollama instance` or `timed out waiting for server to start` | The Ollama app is not running. Start **Ollama** from the Start menu and try again (observed 2026-10-25, Ollama 0.33.1). |
| The installer stops with `DeleteFile failed; code 5. Access is denied.` on `ollama app.exe` | Ollama is still running. In PowerShell run `taskkill /F /IM "ollama app.exe"` and `taskkill /F /IM "ollama.exe"`, then click **Try again** (observed 2026-10-25, installer 0.40.11). |
| Models download to `%USERPROFILE%\.ollama\models` even though you set `OLLAMA_MODELS` | The app's **Settings > Model location** won over the environment variable. Set the folder there, quit and restart Ollama, and pull again (observed 2026-10-26, Ollama 0.40.11). |
| `Claude Code doesn't recognize the model "...", so it assumes a context window of 200k tokens` | Set `CLAUDE_CODE_MAX_CONTEXT_TOKENS` to your context length ([Claude Code: correct the window](https://code.claude.com/docs/en/model-config#correct-the-window-for-a-gateway-or-custom-model-id)). |
| `ollama_check.py` O4 FAIL: only 32768 tokens of context | Ollama app > **Settings > Context length** to 64k, quit and restart Ollama, check again. |
| The first answer after loading is very slow | The first run loads the model from disk. On the RTX 4090 above, the first run made 45 tokens/s and the second 112 tokens/s (observed 2026-10-26). Check the second run. |
| A request fails with `401` | `ANTHROPIC_AUTH_TOKEN` is not set, or a different credential won. Run `/status` ([Claude Code: connect to a gateway](https://code.claude.com/docs/en/llm-gateway-connect#how-the-credential-variable-maps-to-a-header)). |

## 9. Known flaws

- **Unsupported by Anthropic.** Routing Claude Code to non-Claude models is supported by Ollama, not by Anthropic. A
  Claude Code update could change how it works.
- **The VS Code panel setup (A) was not run end to end for this guide.** The variable names and the
  `claudeCode.environmentVariables` setting come from Claude Code's docs; the end-to-end test so far is the command
  line on Linux (below). The first Windows run is still to do.
- **Tested with a tiny model only.** Claude Code v2.1.310 was run against Ollama 0.40.11 on Linux with `qwen3.5:0.8b`
  on CPU: the request reached `/v1/messages`, the `opus` alias resolved to the Ollama model, and the 200k warning went
  away with `CLAUDE_CODE_MAX_CONTEXT_TOKENS` (2026-10-26). That small model answered a "reply PONG" test with "PING",
  so it is not good enough for real work; a subagent run on it was not tried.
- **Maker Mastery quality in Ollama mode is not measured.** No agent, skill or print-qa run has been compared between
  Claude and an open model yet.
- **Web search is not set up.** The research pipeline depends on `WebSearch`, which Ollama does not fully support; the
  MCP route in [Ollama: web search](https://docs.ollama.com/capabilities/web-search) is not tested here.
- **The `ollama launch claude` route is not checked** for the `opus` / `sonnet` alias mapping the agents need.
- **Context budget not measured.** How much of a 64k window the rulebook, the 22 agents and the skills use before your
  first question has not been measured; long sessions may compact often.
- **Not supported by Ollama, so not available in Ollama mode:** PDF `document` blocks, prompt caching, `count_tokens`,
  and full deferred-tool support.
- **Thinking may stay off** for Ollama model names, and the documented `_SUPPORTED_CAPABILITIES` override does not apply to a gateway such as Ollama (not tested).
- **Ollama app labels** in section 2 come from one Windows PC (observed), not from Ollama's documentation.
- **Cloud model access on the Free plan** is not checked for `glm-5.3:cloud`.

## 10. Sources

- https://docs.ollama.com/integrations/claude-code - `ollama launch claude`, manual setup variables, 64k+ context, capabilities list, direct cloud setup
- https://docs.ollama.com/api/anthropic-compatibility - `/v1/messages`, supported and unsupported fields (`tool_choice`), hosted web search not fully supported, the `ollama` placeholder token
- https://docs.ollama.com/cloud - cloud models, no download
- https://docs.ollama.com/api/authentication - `ollama signin`
- https://docs.ollama.com/context-length - "at least 64000 tokens" for agents and coding tools, the app slider, VRAM-based defaults
- https://docs.ollama.com/capabilities/web-search - web search API key, MCP server, 32k context advice
- https://ollama.com/library/qwen3.8 - tags vision, tools, thinking; 27b, 18GB
- https://ollama.com/library/qwen3.5 - tags vision, tools, thinking; sizes 0.8b to 122b
- https://ollama.com/library/glm-5.3 - tags tools, thinking, cloud; 1M context; $1.40 / $4.40 per 1M tokens
- https://ollama.com/pricing - Free plan: starter models; credits or a paid plan unlock all models
- https://code.claude.com/docs/en/llm-gateway - no Anthropic support for non-Claude models; gateway credentials replace the subscription login
- https://code.claude.com/docs/en/llm-gateway-connect - `ANTHROPIC_AUTH_TOKEN`, settings-file scopes, VS Code `claudeCode.environmentVariables`, `/status` lines, login precedence
- https://code.claude.com/docs/en/model-config - `ANTHROPIC_DEFAULT_*_MODEL`, `CLAUDE_CODE_SUBAGENT_MODEL`, the 200k assumption and `CLAUDE_CODE_MAX_CONTEXT_TOKENS`, `_SUPPORTED_CAPABILITIES` and where it applies
- https://code.claude.com/docs/en/env-vars - `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` and what it turns off
- https://code.claude.com/docs/en/vs-code - `disableLoginPrompt`, features not offered on third-party providers
- https://code.claude.com/docs/en/hooks - hooks are commands Claude Code runs on your machine
