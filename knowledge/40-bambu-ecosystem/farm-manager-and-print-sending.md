# Bambu Farm Manager and how Bambu Studio sends a print

Applies to: both · Bambu Farm Manager Server 03.00.00.00 / Client 03.00.00 · Bambu Studio UI strings at tag v02.08.02.61
Verified: 2026-10-04

This note documents how the vendor tools send prints so you can do it yourself. In this library the AI never starts, sends, uploads or queues a print; the maker presses Print.

## Facts

### What Farm Manager is, and requirements
- Bambu Farm Manager is an application suite for managing multiple printers (live status, batch operations, firmware upgrades, job queue, multiple users), shipped as a Server app and a Client app. - [wiki: Bambu Farm Manager](https://wiki.bambulab.com/en/software/bambu-farm-manager)
- Commands and model files go to the printer only within the local network over an encrypted channel. - [wiki: Bambu Farm Manager](https://wiki.bambulab.com/en/software/bambu-farm-manager)
- Requirements: Windows 10 or higher; x86 64-bit CPU; printer on 2.4 GHz Wi-Fi; the client needs internet for server activation, printer verification and firmware downloads. Server and client need 2 GB RAM each; the server needs 4 GB disk. - [wiki: Bambu Farm Manager](https://wiki.bambulab.com/en/software/bambu-farm-manager), [wiki: Farm FAQ and troubleshooting](https://wiki.bambulab.com/en/software/bambu-farm-faq-troubleshoot)
- Minimum firmware: H2C 01.02.00.00 or later (support added in Farm Manager 2.4.0); P1P/P1S 01.07.00.00 or later; A2L 01.00.03.00 or later. - [wiki: Bambu Farm Manager](https://wiki.bambulab.com/en/software/bambu-farm-manager), [wiki: Farm release notes 2.4.0](https://wiki.bambulab.com/en/software/bambu-farm-release-notes/2-4-0)
- First use: pick a region, log in with a Bambu Lab account, then set a local administrator account for the farm server. The activation certificate is valid for six months and must be renewed. - [wiki: Bambu Farm Manager](https://wiki.bambulab.com/en/software/bambu-farm-manager), [wiki: Farm FAQ](https://wiki.bambulab.com/en/software/bambu-farm-faq-troubleshoot)
- Adding a printer needs: firmware at the target version, printer unbound from Handy ("Logged Out"), and LAN mode off on the printer. - [wiki: Bambu Farm Manager](https://wiki.bambulab.com/en/software/bambu-farm-manager)

### Grouping and queue (v3.0.0)
- v3.0.0 added real printer groups; the older tags remain as a marker to be phased out. - [wiki: Farm release notes 3.0.0](https://wiki.bambulab.com/en/software/bambu-farm-release-notes/3-0-0)
- Upload path: in Bambu Studio use "Export plate sliced file" and upload the `gcode.3mf`; only single-plate files are supported. - [wiki: Bambu Farm Manager](https://wiki.bambulab.com/en/software/bambu-farm-manager), [BambuStudio.pot string catalog](https://github.com/bambulab/BambuStudio/blob/v02.08.02.61/bbl/i18n/BambuStudio.pot)
- "Queue Task" lets you set a repeat count and targets: "All Compatible Models (Default)", "Specify Printer Group" or "Specify Specific Printers". A "Top Priority" toggle moves a task to the front; the queue supports drag-to-reorder and filtering. - [wiki: Farm features](https://wiki.bambulab.com/en/software/bambu-farm-features), [wiki: Farm release notes 3.0.0](https://wiki.bambulab.com/en/software/bambu-farm-release-notes/3-0-0)
- The older Features page says the queue syncs to the printer screen; as of 3.0.0, printer-side queue sync is no longer supported for P1S/P1P/A1/A1 mini. - [wiki: Farm release notes 3.0.0](https://wiki.bambulab.com/en/software/bambu-farm-release-notes/3-0-0)
- Filament handling is matching, not inventory: the loaded filament type and quantity must meet the file's needs or the printer is not recommended. v2.4.0 replaced manual spool selection with Automatic Filament Matching. No Farm page describes a stock feature. - [wiki: Farm release notes 3.0.0](https://wiki.bambulab.com/en/software/bambu-farm-release-notes/3-0-0), [wiki: Farm release notes 2.4.0](https://wiki.bambulab.com/en/software/bambu-farm-release-notes/2-4-0)

### Starting prints and batch control
- "Direct to Print" starts one or more idle printers whose model and nozzle diameter match the file. A task's green "Start" button appears once a compatible printer is free. - [wiki: Bambu Farm Manager](https://wiki.bambulab.com/en/software/bambu-farm-manager), [wiki: Farm features](https://wiki.bambulab.com/en/software/bambu-farm-features)
- "Start All" (v3.0.0) matches idle printers to tasks by priority, but you still click it, and a large AMS colour mismatch needs your judgement. It is not unattended. - [wiki: Farm release notes 3.0.0](https://wiki.bambulab.com/en/software/bambu-farm-release-notes/3-0-0)
- Batch controls: pause, cancel, resume, LED on/off, print speed, nozzle and bed temperature, unload filament, machine calibration, and batch firmware update (idle printers only). - [wiki: Farm features](https://wiki.bambulab.com/en/software/bambu-farm-features)

### Dashboard, licensing, network
- Utilisation = effective working time (downloading, preheating, printing; pauses excluded) divided by recorded time; 30 days of data are kept. - [wiki: Farm release notes 2.4.0](https://wiki.bambulab.com/en/software/bambu-farm-release-notes/2-4-0)
- Only the administrator can create or delete user accounts and reset passwords. - [wiki: Farm features](https://wiki.bambulab.com/en/software/bambu-farm-features)
- The FAQ says current functions are free and the software does not limit the number of printers; the EULA only says a fee "may" come later. Each account can activate up to five servers. - [wiki: Farm FAQ](https://wiki.bambulab.com/en/software/bambu-farm-faq-troubleshoot), [Farm Manager service agreement](https://bambulab.com/en/policies/bambu-farm-manager-service-agreement)
- Farm-managed printers stay on the LAN except for activation/renewal, printer verification, version checks and the opt-in UX program. Handy cannot control a printer added to Farm Manager, because it leaves Bambu Cloud. - [wiki: Farm FAQ](https://wiki.bambulab.com/en/software/bambu-farm-faq-troubleshoot)
- Running the Farm server and Bambu Studio on the same PC can cause a port conflict that stops Studio discovering printers Farm Manager has claimed. Ports: server TCP 8888 (HTTPS), TCP 1883 (MQTT), UDP 1900/1991/2021/2022 (discovery); printer TCP 3002 and TCP 443 (cloud). - [wiki: Farm FAQ](https://wiki.bambulab.com/en/software/bambu-farm-faq-troubleshoot)
- No Farm Manager page names Bambu Connect or the Authorization Control System. - [wiki: Farm FAQ](https://wiki.bambulab.com/en/software/bambu-farm-faq-troubleshoot)
- Fleet Hub is separate wired hardware with an mTLS HTTP API for up to 50 printers; a bound printer leaves Bambu Cloud. - [wiki: Fleet Hub](https://wiki.bambulab.com/en/acc/manual/fleet-hub)

### Bambu Studio: how a print is sent
- The X1 manual describes the flow as "Slice", "Print" and "Send". The Bambu Studio string catalog at tag v02.08.02.61 contains "Slice plate", "Print plate", "Print all", "Send all" and "Send" (the confirm button in the send dialog); there is no standalone "Slice" button string in that list. - [wiki: print from Bambu Studio (X1)](https://wiki.bambulab.com/en/x1/manual/print-from-bambu-studio), [BambuStudio.pot](https://github.com/bambulab/BambuStudio/blob/v02.08.02.61/bbl/i18n/BambuStudio.pot)
- Transfer path (X1 wording): the file goes directly if Studio finds the printer on the local network, otherwise through the cloud, unless LAN mode is on. - [wiki: print from Bambu Studio (X1)](https://wiki.bambulab.com/en/x1/manual/print-from-bambu-studio)
- Remote printing over Wi-Fi needs the Bambu Network Plugin; without it no job can be sent and the Device page is unavailable. - [wiki: remote control](https://wiki.bambulab.com/en/software/bambu-studio/remote-control)

## In practice
- For a batch: slice one plate per file ("Export plate sliced file"), check each printer is unbound from Handy, LAN mode off and firmware at the minimum, then use "Queue Task" or "Direct to Print". You press the button; the AI does not.
- Do not rely on the printer screen to show the Farm queue on P1/A1 models after 3.0.0.
- Put the Farm server on a separate machine from Bambu Studio to avoid the port conflict.
- When writing instructions, use the real labels "Slice plate" and "Print plate".

## Not verified / open questions
- The button labels come from the string catalog, not a screenshot with an H2C selected; that the strings are the top-bar labels is not verified on screen.
- Whether H2C or P1S storage changes the X1's direct-vs-cloud transfer path.
- The `.pot` file path is the published catalog at that tag; the exact string list was checked by text search.

Sources:
- https://wiki.bambulab.com/en/software/bambu-farm-manager - overview, requirements, firmware minimums, activation, upload, Direct to Print
- https://wiki.bambulab.com/en/software/bambu-farm-features - queue, batch control, roles
- https://wiki.bambulab.com/en/software/bambu-farm-faq-troubleshoot - requirements, certificate, free/no-limit, network, ports
- https://wiki.bambulab.com/en/software/bambu-farm-release-notes/3-0-0 - groups, queue sync removal, Start All
- https://wiki.bambulab.com/en/software/bambu-farm-release-notes/2-4-0 - H2C support, utilisation, filament matching
- https://wiki.bambulab.com/en/acc/manual/fleet-hub - Fleet Hub
- https://wiki.bambulab.com/en/x1/manual/print-from-bambu-studio - Slice/Print/Send flow, transfer path
- https://wiki.bambulab.com/en/software/bambu-studio/remote-control - network plugin requirement
- https://bambulab.com/en/policies/bambu-farm-manager-service-agreement - EULA pricing language
- https://github.com/bambulab/BambuStudio/blob/v02.08.02.61/bbl/i18n/BambuStudio.pot - UI strings "Slice plate", "Print plate", "Send", "Export plate sliced file"
