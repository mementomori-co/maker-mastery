# Live view limits and Camera Full Screen (Bambu Studio)
Applies to: both (the idle logic is printer-independent Studio code; the camera spec row is H2C only) · Bambu Studio 02.08.02.61 (source tag v02.08.02.61)
Verified: 2026-10-16

Everything below is a code reading of tag v02.08.02.61. Nothing was tested live (no 15-minute idle, no 5-minute stop, no full-screen capture); verify on your own setup.

## Facts
Idle stops (the two that end an unattended stream)
- Live view stops after 900 s (15 min) with no keyboard or mouse input on the PC. The check runs once a minute while playing, so the stop lands at 15-16 min. Input is the system-wide `GetLastInputInfo` on Windows. This is in the public-build branch (`BBL_RELEASE_TO_PUBLIC`). — [MediaPlayCtrl.cpp v02.08.02.61](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/MediaPlayCtrl.cpp)
- Preference "Keep liveview when printing." (Preferences > User > User Settings; tooltip: live view pauses after 15 minutes of PC inactivity unless checked, during printing). Default unchecked (config `liveview/auto_stop_liveview` = true, shown inverted). The 15-minute stop is skipped only while the printer reports it is printing. — [Preferences.cpp v02.08.02.61](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Preferences.cpp), [AppConfig.cpp v02.08.02.61](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/AppConfig.cpp), [MediaPlayCtrl.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/MediaPlayCtrl.cpp)
- The 15-minute stop message in source says the view was temporarily closed for no operation; the English translation file shipped with Studio may reword it ("no activity"). — [MediaPlayCtrl.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/MediaPlayCtrl.cpp); translation wording: not verified (no public source)
- When the printer is NOT printing, live view stops after 5 one-minute checks (about 4-5 min after the last check that saw printing), regardless of the preference. Message: "Temporarily closed because there is no printing for a while." The counter resets when playback starts. — [MediaPlayCtrl.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/MediaPlayCtrl.cpp)
- Both idle stops clear the auto-retry, so the feed stays stopped until someone clicks Play. — [MediaPlayCtrl.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/MediaPlayCtrl.cpp)
- Hiding the live-view panel stops the feed; showing it again restarts it after 2 s only while auto-retry is still armed, so not after either idle stop. — [MediaPlayCtrl.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/MediaPlayCtrl.cpp)
- A feed stuck in Loading/Initializing for 15 s or more is stopped with "Loading failed. Please check the network and try again." — [MediaPlayCtrl.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/MediaPlayCtrl.cpp)

Multiple viewers
- The "Multi-device/client simultaneous liveview is not supported" message is a conditional error (failure code 1 after the state was Playing). The wiki frames the limit as capacity: code -48 means the printer exceeded its service capacity (check for too many video connections), and code 1 means too many Studio/Handy clients use remote access. No source says the limit is exactly one viewer. — [MediaPlayCtrl.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/MediaPlayCtrl.cpp), [wiki: live-view FAQ](https://wiki.bambulab.com/en/software/bambu-studio/faq/live-view)
- On Windows, Studio plays the stream through Windows Media Player and the "BambuSource" DirectShow component from the network plugin; Windows Media Player renders with the d3d9 driver. — [wiki: live-view FAQ](https://wiki.bambulab.com/en/software/bambu-studio/faq/live-view)

Camera Full Screen window (what a screen-capture tool would capture)
- Window title "Camera Full Screen", created borderless, without a taskbar button and always on top. On Windows it drops out of topmost when it loses focus and returns when reactivated. Esc exits. Tooltips "Enter Camera Full Screen" / "Exit Camera Full Screen". — [StatusPanel.cpp v02.08.02.61](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/StatusPanel.cpp)
- Preference "Open full screen camera view on active monitor only." (Preferences > 3D tab), default on. When off (non-Apple) the window spans all monitors; when on it fills the monitor that holds Studio. — [Preferences.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Preferences.cpp), [StatusPanel.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/StatusPanel.cpp), [AppConfig.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/AppConfig.cpp)

H2C camera spec
- H2C store spec: Live View, Nozzle and Toolhead cameras built-in at 1920*1080; BirdsEye camera 3264*2448 (Laser Edition). Resolution only, no frame rate. — [H2C store page](https://us.store.bambulab.com/products/h2c)

## In practice
- For an unattended stream of a running print, tick Preferences > User > User Settings > "Keep liveview when printing." Without it, a PC with no input loses the feed at 15-16 min. Even with it, the feed stops about 5 min after printing ends and needs a click on Play.
- If you capture the live view or the "Camera Full Screen" window with streaming software, remember it is topmost only while focused, and a stopped feed stays stopped after the panel is shown again.
- Related: [go-live-virtual-camera.md](go-live-virtual-camera.md) (virtual camera route that does not use this window).

## Not verified / open questions
- Whether a paused print, post-print cooldown or calibration counts as "printing" for the idle logic.
- Whether `BBL_RELEASE_TO_PUBLIC` is set in the released build (assumed).
- Behaviour after Studio releases later than v02.08.02.61.
- The H2C limit on simultaneous viewers, and the H2C live-view frame rate.
- What "Camera Full Screen" shows after live view stops, and whether minimizing the main window affects it.

Sources:
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/MediaPlayCtrl.cpp — idle stops, retry, loading timeout, multi-client error
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/StatusPanel.cpp — Camera Full Screen window
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Preferences.cpp — preference labels and tooltips
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/AppConfig.cpp — preference defaults
- https://wiki.bambulab.com/en/software/bambu-studio/faq/live-view — playback stack, capacity error codes
- https://us.store.bambulab.com/products/h2c — H2C camera resolutions
