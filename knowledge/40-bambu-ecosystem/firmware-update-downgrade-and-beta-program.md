# Firmware update, downgrade, beta program and Bambu Studio minimum-firmware notes

Applies to: H2C | P1S | both · H2C firmware 01.02.00.00 (20260601) and P1 firmware 01.10.00.00 (20260330), the latest wiki entries when checked · Bambu Studio release notes 2.8.2.60 and 2.8.2.61
Verified: 2026-10-04

Firmware baselines and Authorization Control history are in [connection-modes-and-bambu-connect.md](connection-modes-and-bambu-connect.md). This note covers the update, downgrade and beta mechanics.

## Facts

### H2C 01.02.00.00
- New features include Filament Track Switch support (needs Bambu Studio 2.5.3.60 or later and Handy 3.18.0 or later), remote AMS drying, TPU (90A or harder) on the left nozzle, LAN printing without USB storage, foreign-object detection under the heatbed (Bambu Studio 2.5.3 or above), "Purify Air at Print End", and a "Stopping" state. - [wiki: H2C firmware release history](https://wiki.bambulab.com/en/h2c/manual/h2c-firmware-release-history)
- Known issue: PTFE-tube detachment detection is temporarily disabled. - [wiki: H2C firmware release history](https://wiki.bambulab.com/en/h2c/manual/h2c-firmware-release-history)
- A motor-noise optimisation needs motor-noise calibration after upgrading, and the calibration must be redone when rolling back from this version to 01.01.05.00 or earlier. The 01.01.05.00 entry has no such note. - [wiki: H2C firmware release history](https://wiki.bambulab.com/en/h2c/manual/h2c-firmware-release-history)

### P1 series
- 01.10.00.00 adds External Spool Multi-Color Printing (Bambu Studio 2.5.2.65 or higher), Automatic Drying Presets and Chamber Light Memory. - [wiki: P1P/P1S firmware release history](https://wiki.bambulab.com/en/p1/manual/p1p-firmware-release-history)
- A P1 printer below 01.09.01.00 must first take an offline upgrade to the "Bridge Firmware" (01.09.01.00). - [wiki: P1P/P1S firmware release history](https://wiki.bambulab.com/en/p1/manual/p1p-firmware-release-history)
- Recommended accessory firmware with 01.10.00.00: AMS 01.00.06.83; AMS HT 03.00.21.29; AMS 2 Pro 03.00.21.29. - [wiki: P1P/P1S firmware release history](https://wiki.bambulab.com/en/p1/manual/p1p-firmware-release-history)

### Downgrading (Bambu Handy, all models)
- The illustrated steps use an A1 but apply to all models: Device tab > menu icon > Settings > Firmware Version > "I want to update to a historical version" > pick a version > Update. You can choose the version the technical team recommends or the one before your current firmware. The printer restarts; run a calibration afterwards. - [wiki: firmware downgrade](https://wiki.bambulab.com/en/knowledge-sharing/firmware-downgrade)

### Beta firmware program
- The open beta offers firmware features before release, usually up to a month ahead; some beta features may not reach the official release. Joining means agreeing to the Beta Firmware Program Terms. - [wiki: firmware open beta](https://wiki.bambulab.com/en/software/bambu-firmware-open-beta)
- Join: turn on the "Beta firmware program" toggle, agree to the terms, restart the printer; a beta upgrade notification appears if a beta exists, and installed beta versions are marked "beta" in Handy, Studio and on the printer. (The page's step 4 in this section repeats the "leave" text and appears to be a copy error.) - [wiki: firmware open beta](https://wiki.bambulab.com/en/software/bambu-firmware-open-beta)
- Leave: turn the toggle off and restart; a notification offers the official release. Run a full calibration after downgrading. - [wiki: firmware open beta](https://wiki.bambulab.com/en/software/bambu-firmware-open-beta)
- Bambu Lab recommends avoiding beta firmware unless you plan to test new features; it can contain bugs that cause print failures. - [wiki: firmware open beta](https://wiki.bambulab.com/en/software/bambu-firmware-open-beta)

### Authorization-control firmware and Studio/Handy versions
- The January 2025 announcement says that after the authorization-controlled firmware update, Bambu Studio and Bambu Handy must be updated together or some controls may become unusable; Bambu Studio users otherwise see no impact, and users on older firmware can keep using old or new app versions. Its version numbers are X1-specific (firmware 01.08.03.00+, Studio 01.10.02.64+, Handy 2.17.0+). - [Bambu Lab blog: new authorization control system](https://blog.bambulab.com/firmware-update-introducing-new-authorization-control-system-2/)

### Update flow
- H2 series on screen: Confirm opens the Update section; Update starts it; do not cut power until it finishes. - [wiki: H2 firmware update](https://wiki.bambulab.com/en/h2/software/firmware-update)
- P1: an update can take 5-15 minutes depending on network speed; afterwards power off, wait 5 seconds, power on, and run a full calibration. The P1 microSD card is not hot-swappable and can corrupt if removed while running. - [wiki: P1 firmware upgrading](https://wiki.bambulab.com/en/p1/manual/firmware-upgrading)
- Offline update by microSD card and update package covers H2C, H2D, H2S, H2D Pro, P1 and P1S; expect 10-20 minutes. The linked H2 guide is titled "Offline Firmware Update Guide for H2 Series" despite an `/h2d/` URL. - [wiki: update firmware from SD card](https://wiki.bambulab.com/en/general/update-firmware-from-sd-card), [wiki: H2 offline firmware update](https://wiki.bambulab.com/en/h2d/manual/offline-firmware-update)

### Bambu Studio release notes and minimum firmware
- The 2.8.2.61 release note is a minor fix release (six fixes listed) with no minimum-firmware statement. - [wiki: release note 2.8.2.61](https://wiki.bambulab.com/en/software/bambu-studio/release/release-note-2-8-2-61)
- 2.8.2.60 states minimum firmware only for H2S (01.02.50.00), H2D (01.03.50.00) and A2L (01.01.01.00). It names the H2C (left toolhead only) for E3D High Flow nozzle support but gives no H2C firmware minimum. - [wiki: release note 2.8.2.60](https://wiki.bambulab.com/en/software/bambu-studio/release/release-note-2-8-2-60)

## In practice
- Before rolling an H2C back from 01.02.00.00 to 01.01.05.00 or earlier, plan to redo motor-noise calibration.
- An old P1 cannot jump straight to current firmware; take the Bridge Firmware first.
- Joining or leaving the beta ends in a restart and a calibration each time.
- For a firmware minimum, do not look on the 2.8.2.61 note; check 2.8.2.60 or a newer release note.
- With no internet, update from a microSD card using the SD-card index page.

## Not verified / open questions
- Whether the H2C has its own Studio/Handy version-lockstep rule for Authorization Control; the only sourced numbers are X1-specific.

Sources:
- https://wiki.bambulab.com/en/h2c/manual/h2c-firmware-release-history - H2C features, known issue, rollback warning
- https://wiki.bambulab.com/en/p1/manual/p1p-firmware-release-history - P1 features, Bridge Firmware, accessory firmware
- https://wiki.bambulab.com/en/knowledge-sharing/firmware-downgrade - Handy downgrade flow
- https://wiki.bambulab.com/en/software/bambu-firmware-open-beta - beta program
- https://blog.bambulab.com/firmware-update-introducing-new-authorization-control-system-2/ - Studio/Handy update rule (X1 numbers)
- https://wiki.bambulab.com/en/h2/software/firmware-update - H2 on-screen flow
- https://wiki.bambulab.com/en/p1/manual/firmware-upgrading - P1 timing and post-update steps
- https://wiki.bambulab.com/en/general/update-firmware-from-sd-card - offline update coverage
- https://wiki.bambulab.com/en/h2d/manual/offline-firmware-update - H2 offline guide title
- https://wiki.bambulab.com/en/software/bambu-studio/release/release-note-2-8-2-61 - no minimum firmware
- https://wiki.bambulab.com/en/software/bambu-studio/release/release-note-2-8-2-60 - minimum firmware for H2S/H2D/A2L
