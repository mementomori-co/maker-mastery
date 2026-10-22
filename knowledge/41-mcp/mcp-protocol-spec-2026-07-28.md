# MCP protocol spec 2026-07-28: transports, features, deprecations, security

Applies to: any MCP client or server (protocol-level, not printer-specific) · MCP spec revision 2026-07-28
Verified: 2026-10-04

## Facts

### Revision and transports
- The current MCP spec revision is 2026-07-28: `/specification/latest` redirects to `/specification/2026-07-28`, and the schema lives at `schema/2026-07-28/schema.ts` in the `modelcontextprotocol/specification` repo. "Latest" moves with the next revision. - [MCP specification (latest)](https://modelcontextprotocol.io/specification/latest)
- The overview page describes the base protocol as stateless, with capabilities negotiated per request. - [MCP specification (latest)](https://modelcontextprotocol.io/specification/latest)
- Standard transports: stdio (newline-delimited messages over the standard streams of a subprocess the client launches) and Streamable HTTP (each message is an HTTP POST to one MCP endpoint; the reply is a JSON object or a request-scoped SSE stream). - [Transports](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports)
- The old HTTP+SSE transport is deprecated (SEP-2596; replaced by Streamable HTTP) and can be removed three months after SEP-2596 reaches Final. - [Deprecated features](https://modelcontextprotocol.io/specification/2026-07-28/deprecated)

### Features
- Server features: Tools (functions the model can execute), Resources (context and data for the user or model) and Prompts (templated messages and workflows for users). - [MCP specification (latest)](https://modelcontextprotocol.io/specification/latest)
- Elicitation (a server asking the user for more information) is a current client feature. A client that supports it must declare the `elicitation` capability in `_meta.io.modelcontextprotocol/clientCapabilities` on each request; that per-request declaration is new in 2026-07-28. - [Elicitation](https://modelcontextprotocol.io/specification/2026-07-28/client/elicitation)
- Sampling is deprecated as of 2026-07-28 (SEP-2577): new implementations "SHOULD NOT adopt it" and existing ones should call LLM provider APIs directly. Earliest removal is the first revision released on or after 2027-07-28. - [Sampling](https://modelcontextprotocol.io/specification/2026-07-28/client/sampling)
- Roots is deprecated as of 2026-07-28 (SEP-2577); implementations should pass directories or files through tool parameters, resource URIs or server configuration instead. Claude Code's MCP page still documents answering `roots/list`. - [Roots](https://modelcontextprotocol.io/specification/2026-07-28/client/roots), [Claude Code: MCP](https://code.claude.com/docs/en/mcp)
- Logging and Dynamic Client Registration are also deprecated in 2026-07-28 (DCR: migrate to Client ID Metadata Documents). - [Deprecated features](https://modelcontextprotocol.io/specification/2026-07-28/deprecated)
- `ToolAnnotations` fields and defaults: `readOnlyHint` false, `destructiveHint` true, `idempotentHint` false, `openWorldHint` true; the destructive and idempotent hints only mean something when `readOnlyHint` is false. The schema says clients should never decide tool use from annotations sent by untrusted servers. - [schema.ts (main branch, not pinned)](https://raw.githubusercontent.com/modelcontextprotocol/specification/main/schema/2026-07-28/schema.ts)

### Authorization and security
- Authorization is OPTIONAL. Implementations on the STDIO transport should not follow the authorization spec and should take credentials from the environment instead. Authorization servers must implement OAuth 2.1 for both confidential and public clients. - [Authorization](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization)
- Confused deputy: the consent cookie or session holding the `state` value must not be set until the user has approved the consent screen, and MCP proxy servers "MUST implement per-client consent". - [Security best practices](https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices)
- Token passthrough: "MCP servers MUST NOT accept any tokens that were not explicitly issued" for that server. - [Security best practices](https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices)
- State handle hijacking: servers with authorization must verify every inbound request and must not treat possession of a state handle as authentication. The section was named "Session Hijacking" on 2025-11-25 and earlier versions of the page. - [Security best practices](https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices)
- SSRF: MCP clients deployed to a server must consider SSRF risks when fetching OAuth-related URLs and mitigate them. - [Security best practices](https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices)

## In practice
- Treat Sampling, Roots, Logging and Dynamic Client Registration as legacy: do not design a new server around them. For file access, pass paths as tool parameters, resource URIs or server config.
- Never auto-approve a tool call because an untrusted server says `readOnlyHint: true`; the spec itself forbids that.
- For an OAuth-based server: set no consent cookie before the user approves, and give a proxy per-client consent, not one shared consent.
- A local stdio server (like the read-only audit server in [tools/mcp](../../tools/mcp/)) needs no OAuth: it takes what it needs from its environment and config.
- Cite the dated security page (`/docs/2026-07-28/...`), not the draft path, which will change at the next revision.

## Not verified / open questions
- `ToolAnnotations` was read from `schema.ts` on the `main` branch, not a pinned commit; re-fetch before relying on it.
- These facts describe the pages as fetched on the Verified date; the next spec revision may change any of them.

Sources:
- https://modelcontextprotocol.io/specification/latest - current revision, base-protocol claims, server features
- https://modelcontextprotocol.io/specification/2026-07-28/basic/transports - stdio and Streamable HTTP
- https://modelcontextprotocol.io/specification/2026-07-28/deprecated - HTTP+SSE, Logging, Dynamic Client Registration
- https://modelcontextprotocol.io/specification/2026-07-28/client/elicitation - elicitation capability declaration
- https://modelcontextprotocol.io/specification/2026-07-28/client/sampling - sampling deprecation and removal window
- https://modelcontextprotocol.io/specification/2026-07-28/client/roots - roots deprecation
- https://code.claude.com/docs/en/mcp - Claude Code still answers `roots/list`
- https://raw.githubusercontent.com/modelcontextprotocol/specification/main/schema/2026-07-28/schema.ts - ToolAnnotations fields and defaults
- https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization - OAuth 2.1 requirement, STDIO exemption
- https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices - confused deputy, token passthrough, state handle hijacking, SSRF
