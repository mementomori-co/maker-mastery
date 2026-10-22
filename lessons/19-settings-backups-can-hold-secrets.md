# Lesson 19: a settings backup can contain a secret

Area: agent and tool hygiene, security

| What happened | Root cause | Rule now |
|---|---|---|
| Streaming and app profile folders can hold stream keys and tokens, so a backup of such a folder can carry a secret. | Copying a whole profile folder copies every secret file inside it. Keeping the copy out of version control does not make storing it safe. | Never copy app profile or settings folders into a shared place (the repository, a shared drive, a scratch folder). Back up settings file by file and leave secret-bearing files where the application keeps them. |

How to check: before any backup or copy of application settings, list the files to be copied and remove any that hold keys, tokens or credentials.
