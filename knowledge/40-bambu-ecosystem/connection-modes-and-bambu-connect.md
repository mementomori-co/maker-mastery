# Connection modes (Cloud / LAN Only / Developer Mode) and Bambu Connect

Applies to: H2C | P1S | both · H2C firmware 01.02.00.00 (20260601) and P1 firmware 01.10.00.00 (20260330), the latest wiki entries when checked
Verified: 2026-10-04

## Facts

### Developer Mode
- Enabling Developer Mode opens the MQTT channel, live stream and FTP, which the wiki says gives full control over the printer "and its network security". - [wiki: enable Developer Mode](https://wiki.bambulab.com/en/knowledge-sharing/enable-developer-mode)
- The enable order differs by model. H2 series (covers H2C): first enable LAN Only mode on the printer (and choose whether to enable LAN-mode liveview), then enable Developer Mode. P series (P1S): Settings > WLAN > LAN Only mode, then scroll to Developer Mode > Enable (the screen shows "ON"). - [wiki: enable Developer Mode](https://wiki.bambulab.com/en/knowledge-sharing/enable-developer-mode)
- A risk acknowledgement is required. H2 series: tick the confirmation that you have read the Important Notice, then select "Enable Developer Mode". P series: scroll to the end and click Enable. - [wiki: enable Developer Mode](https://wiki.bambulab.com/en/knowledge-sharing/enable-developer-mode)
- The page gives only "Enable" steps; it does not say how to turn Developer Mode off, and no page checked says whether it persists across a firmware update. - [wiki: enable Developer Mode](https://wiki.bambulab.com/en/knowledge-sharing/enable-developer-mode)
- In the H2/P2S/X-series section of the LAN Mode page (not the P1P/P1S section), Developer Mode is described as working for 3D printing parts only and letting third-party software manage print jobs. - [wiki: enable LAN Mode](https://wiki.bambulab.com/en/knowledge-sharing/enable-lan-mode)
- Developer Mode does not allow a Bambu Cloud connection, so it works only in LAN Mode. It works as in earlier firmware and needs no authorization verification. - [wiki: third-party integration](https://wiki.bambulab.com/en/software/third-party-integration)
- Bambu Lab's follow-up post: Standard Mode (the default) runs authorization in LAN mode through Bambu Connect without internet or an account. Developer Mode is optional, leaves MQTT, live stream and FTP open, and Bambu Lab will not provide customer support for it. The post names X1, P1, A1 and A1 Mini; the H2C's Developer Mode is documented on the wiki. - [Bambu Lab blog: updates and third-party integration with Bambu Connect](https://blog.bambulab.com/updates-and-third-party-integration-with-bambu-connect/) (2025-01-20)

### LAN Mode
- LAN Mode lets a printer work on the local network and talk to the slicer for sending files and monitoring without internet access. - [wiki: enable LAN Mode](https://wiki.bambulab.com/en/knowledge-sharing/enable-lan-mode)
- In LAN Mode you cannot start prints remotely from outside the local network, Bambu Handy is unavailable, and Print History is unavailable (list not split by model). - [wiki: enable LAN Mode](https://wiki.bambulab.com/en/knowledge-sharing/enable-lan-mode)
- Binding a LAN-mode printer in Bambu Studio: on H2/X models the printer shows a lock icon and you enter the printer's access code and click Confirm; the page also documents binding by IP address plus access code across subnets. On P1P/P1S the page says you use the printer normally once the connection is confirmed. - [wiki: enable LAN Mode](https://wiki.bambulab.com/en/knowledge-sharing/enable-lan-mode)

### Authorization Control System
- Restricted commands (cloud and normal LAN mode, not Developer Mode): binding/unbinding; firmware upgrades from other software (microSD update unaffected); remote video through the network plugin; starting a print via LAN or cloud from software other than Bambu Studio (needs Bambu Connect); controlling motion, temperature, fans, AMS settings and calibration. The rollout was X-series first, then P- and A-series; the page does not name the H2C. - [wiki: third-party integration](https://wiki.bambulab.com/en/software/third-party-integration)
- Not restricted: status updates such as MQTT pushes to Home Assistant; starting prints from an SD card; microSD firmware updates; other general operations. - [wiki: third-party integration](https://wiki.bambulab.com/en/software/third-party-integration)
- Third-party slicers using the network plugin (for example Orca Slicer) can start firmware updates, live view and file downloads once their maintainers integrate the latest plugin. - [wiki: third-party integration](https://wiki.bambulab.com/en/software/third-party-integration)
- The January 2025 announcement (written for X1 firmware 01.08.03.00+, Bambu Studio 01.10.02.64+, Handy 2.17.0+) listed the same restricted and unrestricted sets. It said Bambu Studio users see no impact, but Bambu Studio and Bambu Handy must be updated at the same time as the firmware or some controls may stop working. - [Bambu Lab blog: new authorization control system](https://blog.bambulab.com/firmware-update-introducing-new-authorization-control-system-2/)
- The same post: full control of printers via Home Assistant is no longer possible after the update (some information stays available). OrcaSlicer without Bambu Connect loses binding, starting prints, axis control and calibration, and keeps status monitoring and LED control. - [Bambu Lab blog: new authorization control system](https://blog.bambulab.com/firmware-update-introducing-new-authorization-control-system-2/)
- Users were given three options: stay on current firmware; update and use Bambu Lab's tools; or update and switch to Developer Mode. The post also lists seven claims it calls false (for example that printers would be remotely disabled, AMS restricted, third-party filament disabled or a subscription required); these are the vendor's own statements. - [Bambu Lab blog: updates and third-party integration](https://blog.bambulab.com/updates-and-third-party-integration-with-bambu-connect/)

### Bambu Connect
- Bambu Connect sends sliced G-code and 3MF files to the printer, so that printer commands go through verified channels. - [wiki: third-party integration](https://wiki.bambulab.com/en/software/third-party-integration)
- Features listed (beta, build v2.5.0-beta.15 for Windows x64 and macOS): Cloud Account Login, Printer Management, LAN Mode Connectivity (no internet or account needed on that path), File Import and Printing, Basic Printer Controls. Liveview is not yet supported. - [wiki: Bambu Connect](https://wiki.bambulab.com/en/software/bambu-connect)
- Platforms: Windows 10 or later (x86_64); macOS 13 or later (arm64 and x86_64); Linux in development. - [wiki: third-party integration](https://wiki.bambulab.com/en/software/third-party-integration)
- URL scheme for file import: `bambu-connect://import-file` with `path`, `name` and `version` (fixed `1.0.0`). - [wiki: third-party integration](https://wiki.bambulab.com/en/software/third-party-integration), [wiki: Bambu Connect](https://wiki.bambulab.com/en/software/bambu-connect)

### Bambu Handy
- `https://wiki.bambulab.com/en/software/bambu-handy` returned HTTP 404 when checked; there is no dedicated Handy page at that path. - [wiki: software/bambu-handy](https://wiki.bambulab.com/en/software/bambu-handy)
- The wiki Software index describes Handy as an all-in-one mobile app for Bambu Lab printers and links to `https://bambulab.com/download/app`. - [wiki: Software index](https://wiki.bambulab.com/en/software)
- Store listings when checked: iOS 4.1.1, Android 4.1.2; the Android package ID is `bbl.intl.bambulab.com`; the developer of record on both stores is "Shanghai Lunkuo Technology Co., Ltd". Versions change with every release. - [Apple App Store](https://apps.apple.com/us/app/bambu-handy/id1625671285), [Google Play](https://play.google.com/store/apps/details?id=bbl.intl.bambulab.com&hl=en_US)

### Firmware by printer (as checked)
- Farm Manager minimum firmware: H2C 01.02.00.00 or later; P1P/P1S 01.07.00.00 or later. - [wiki: Bambu Farm Manager](https://wiki.bambulab.com/en/software/bambu-farm-manager)
- H2C 01.02.00.00 (20260601) added starting prints over LAN without a USB storage device, and a "Purify Air at Print End" option. Its firmware log has no "Developer", "Authoriz" or "Bambu Connect" entry from 01.01.00.00 onward. - [wiki: H2C firmware release history](https://wiki.bambulab.com/en/h2c/manual/h2c-firmware-release-history)
- P1 01.08.02.00 (20250603) introduced Authorization Control (control commands from unauthorized software are rejected), while keeping Bambu Connect use, offline use, LAN file sending and downgrades possible; the same release added a Developer Mode entry in LAN Mode that disables Authorization Control. - [wiki: P1P/P1S firmware release history](https://wiki.bambulab.com/en/p1/manual/p1p-firmware-release-history)
- P1 01.10.00.00 (20260330) added External Spool Multi-Color Printing (needs Bambu Studio 2.5.2.65 or higher), Automatic Drying Presets, Chamber Light Memory and security patches. A printer below 01.09.01.00 must first take the offline Bridge Firmware (01.09.01.00). - [wiki: P1P/P1S firmware release history](https://wiki.bambulab.com/en/p1/manual/p1p-firmware-release-history)

## In practice
- Developer Mode means no Bambu Cloud, no Handy, no Print History, and an open FTP/MQTT/stream channel that Bambu Lab does not support. Treat it as an advanced, unsupported mode.
- Without Developer Mode or Bambu Connect, third-party software can still monitor status and toggle LEDs, but cannot bind, start a print, move axes or calibrate once Authorization Control is active.
- Bambu Connect does not need a cloud account for LAN-mode use.
- The H2C's own firmware log never mentions Authorization Control; do not assume it has or lacks it without a model-specific source.
- This library's stance: the AI never starts, sends, uploads or queues a print by any of these routes. The maker presses Print.

## Not verified / open questions
- Whether "Shanghai Lunkuo Technology Co., Ltd" is officially Bambu Lab; no Bambu-owned page checked states it.
- How to turn Developer Mode off, and whether it survives a firmware update.
- Whether Authorization Control applies to the H2C from its first firmware.
- LAN-mode spaghetti detection is described for the X1 only; do not carry it over to other models without a source.
- The UI steps are from wiki text; no screenshot confirmed them.

Sources:
- https://wiki.bambulab.com/en/knowledge-sharing/enable-developer-mode - Developer Mode: what it opens, enable flow per model
- https://wiki.bambulab.com/en/knowledge-sharing/enable-lan-mode - LAN Mode definition, limits, binding flow
- https://wiki.bambulab.com/en/software/third-party-integration - Authorization Control scope, Bambu Connect, platforms, URL scheme
- https://wiki.bambulab.com/en/software/bambu-connect - Bambu Connect beta features and URL scheme
- https://wiki.bambulab.com/en/software/bambu-farm-manager - Farm Manager minimum firmware
- https://wiki.bambulab.com/en/h2c/manual/h2c-firmware-release-history - H2C firmware history
- https://wiki.bambulab.com/en/p1/manual/p1p-firmware-release-history - P1 firmware history, Authorization Control, Bridge Firmware
- https://blog.bambulab.com/firmware-update-introducing-new-authorization-control-system-2/ - January 2025 announcement
- https://blog.bambulab.com/updates-and-third-party-integration-with-bambu-connect/ - Standard vs Developer Mode, options, denial list
- https://wiki.bambulab.com/en/software/bambu-handy - HTTP 404 when checked
- https://wiki.bambulab.com/en/software - Handy description on the Software index
- https://apps.apple.com/us/app/bambu-handy/id1625671285 - iOS listing
- https://play.google.com/store/apps/details?id=bbl.intl.bambulab.com&hl=en_US - Android listing
