# Lesson 20: no personal identifiers in request headers

Area: agent and tool hygiene, privacy

| What happened | Root cause | Rule now |
|---|---|---|
| A research agent put a personal identifier in the User-Agent of web requests. | Nothing in the agent's instructions forbade it. | Never put a personal identifier (email, name, account handle) in a User-Agent, request header, URL or payload sent to an outside service unless the maker asks. A User-Agent names the tool only. Every agent prompt that fetches over the network says so. |

How to check: read every script that sets request headers and confirm the User-Agent and other headers name only the tool.
