---
description: Fan out researchers on a topic, fact-check, and file verified notes
argument-hint: <topic>
---
Topic: $ARGUMENTS
1. Split the topic into 4-8 narrow questions. Launch one `researcher` agent per question in parallel; each writes its claims table to research\inbox\.
2. Send every returned claim to `fact-checker`, which re-derives each one without seeing the researcher's reasoning and writes to research\verified\.
3. `librarian` files the VERIFIED claims into the right knowledge\ category and updates its index.md, sources\registry.md and CURRICULUM.md.
4. Reply with: what was verified (with links), what could not be verified, and the next topic to study.
