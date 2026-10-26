# Claude Code on Ollama (local and Ollama Cloud models)

Applies to: Claude Code v2.1.310 - Ollama 0.40.11 - Windows 11 (guide) and Linux (test run)
Verified: 2026-10-26

## Facts
- Ollama serves an Anthropic-compatible `/v1/messages` endpoint; Claude Code connects with `ANTHROPIC_BASE_URL=http://localhost:11434`, `ANTHROPIC_AUTH_TOKEN=ollama` and an empty `ANTHROPIC_API_KEY`. - [Ollama: Claude Code](https://docs.ollama.com/integrations/claude-code)
- The token is "required but ignored" by the local server. - [Ollama: Anthropic compatibility](https://docs.ollama.com/api/anthropic-compatibility)
- Ollama's guide asks for a 64k+ context window on local models used with Claude Code. - [Ollama: Claude Code](https://docs.ollama.com/integrations/claude-code)
- Ollama's context page says agents and coding tools "should be set to at least 64000 tokens"; without a setting it picks 4k, 32k or 256k from the GPU's memory, and the app has a context slider in its settings. - [Ollama: context length](https://docs.ollama.com/context-length)
- Not supported by Ollama's endpoint: `count_tokens`, `tool_choice`, `metadata`, prompt caching, batches, citations and PDF `document` blocks; "Tool-choice controls, deferred tools, and hosted web search are not fully supported." - [Ollama: Anthropic compatibility](https://docs.ollama.com/api/anthropic-compatibility)
- With `ANTHROPIC_BASE_URL` set, Claude Code still sends telemetry and other nonessential traffic to Anthropic; `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` turns it off, and the WebFetch domain check still calls `api.anthropic.com`. - [Claude Code: connect to a gateway](https://code.claude.com/docs/en/llm-gateway-connect#turn-off-traffic-outside-the-gateway-path)
- Anthropic "doesn't support routing Claude Code to non-Claude models through any gateway". - [Claude Code: other LLM gateways](https://code.claude.com/docs/en/llm-gateway)
- A gateway credential such as `ANTHROPIC_AUTH_TOKEN` takes the place of a claude.ai login while it is set. - [Claude Code: connect to a gateway](https://code.claude.com/docs/en/llm-gateway-connect#conflicts-with-an-existing-login)
- `ANTHROPIC_DEFAULT_OPUS_MODEL`, `ANTHROPIC_DEFAULT_SONNET_MODEL` and `ANTHROPIC_DEFAULT_HAIKU_MODEL` set what the `opus`, `sonnet` and `haiku` aliases resolve to; `CLAUDE_CODE_SUBAGENT_MODEL` is the default for subagents without a model. - [Claude Code: model configuration](https://code.claude.com/docs/en/model-config)
- For a model ID Claude Code does not recognize it assumes a 200k window; `CLAUDE_CODE_MAX_CONTEXT_TOKENS` sets the real one for IDs that do not start with `claude-`. - [Claude Code: correct the window](https://code.claude.com/docs/en/model-config#correct-the-window-for-a-gateway-or-custom-model-id)
- The VS Code extension reads gateway variables from `claudeCode.environmentVariables` in VS Code user settings; `~/.claude/settings.json` values do not reach its login check. - [Claude Code: connect to a gateway, VS Code extension](https://code.claude.com/docs/en/llm-gateway-connect#vs-code-extension)
- With the variables above and `--model opus`, a Claude Code v2.1.310 request reached Ollama 0.40.11's `/v1/messages` and was answered by the only installed model, `qwen3.5:0.8b`, so the alias resolved to the Ollama model; with `CLAUDE_CODE_MAX_CONTEXT_TOKENS=65536` the 200k warning did not appear (Linux, CPU, fresh config, no sign-in, 2026-10-26) - measured

## What it means in practice
- Maker Mastery's agents ask for `model: opus` or `model: sonnet`, so Ollama mode must set all three alias variables, or the agents ask Ollama for a Claude model name it does not have.
- Keep the knowledge pipeline (`/research-topic`, `/verify-claim`) on Claude until web search in Ollama mode is set up and checked.
- Full setup, checks and switch-back steps: [docs/12-ollama-mode.md](../../docs/12-ollama-mode.md). Readiness check: `tools\ollama_check.py`.

## Not verified / open questions
- The VS Code panel route has not been run end to end on Windows yet.
- Whether `ollama launch claude` sets the `opus` / `sonnet` alias variables is not documented.
- Answer quality of open models on Maker Mastery agents and skills has not been measured against Claude.

Sources:
- https://docs.ollama.com/integrations/claude-code - variables, 64k+ context, launcher
- https://docs.ollama.com/context-length - at least 64000 tokens, defaults by GPU memory, app slider
- https://docs.ollama.com/api/anthropic-compatibility - endpoint, unsupported fields, placeholder token
- https://code.claude.com/docs/en/llm-gateway - no Anthropic support for non-Claude models
- https://code.claude.com/docs/en/llm-gateway-connect - credential precedence, VS Code setting
- https://code.claude.com/docs/en/model-config - alias variables, subagent default, context window
