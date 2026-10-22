# Security policy

## Reporting a problem privately

If you find a security problem (for example a tool that could send a print, leak a secret, write outside the folders it should, or run untrusted code), report it **privately**, not in a public issue.

Use GitHub's private vulnerability reporting:

1. Open the repository's **Advisories** page: `https://github.com/<owner>/maker-mastery/security/advisories`. (GitHub's
   reporting guide also starts from the repository's **Security and quality** tab; the button is offered there too.)
2. Click the **Report a vulnerability** button and fill in the form.
3. Click **Submit report**.

GitHub's guides: [Privately reporting a security vulnerability](https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/report-privately)
and, for where the button appears, [Configuring private vulnerability reporting for a repository](https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/configure-vulnerability-reporting/configure-for-a-repository).

> Maintainer setup: private vulnerability reporting must be switched on for the repository first. On the repository,
> **Settings**, then in the sidebar's "Security and quality" section **Advanced Security**, then **Enable** next to
> "Private vulnerability reporting" (labels as written in GitHub's guide:
> https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/configure-vulnerability-reporting/configure-for-a-repository).

Please include what you ran, what happened, and what you expected. The maintainers will reply in the advisory thread.

## Never paste secrets

**Never paste API keys, stream keys or printer access codes into issues.** The same goes for pull requests, discussions, screenshots, logs and 3MF or G-code files you attach. Also leave out serial numbers, IP addresses, account names and your home folder path.

Before you share any file from your machine, run the privacy scan described in [CONTRIBUTING.md](CONTRIBUTING.md). If you posted a secret by mistake, change it at its source (regenerate the key or code) first, then delete the post.

## The no-AI-print rule

**No AI ever starts, sends, uploads or queues a print.** Claude Code, every agent, skill, command, hook and tool in this repository may prepare and check print files, and may slice them. Only you press Print, in Bambu Studio, after you have reviewed the file yourself.

Any route around this rule (a tool, MCP server, hook or prompt that can start, send, upload or queue a print by any route, including LAN, cloud or a printer API) is treated as a security problem. Please report it privately as described above.

## Supported versions

Only the latest release receives fixes.
