# NBA Hangtime 0.4.3

iOS build 8 · Windows x64 · iOS 16 or later

## New in 0.4.3

- Add the NewPixie CRT filter on iOS and Windows. Enable or disable CRT FILTER from the iOS Display menu or Windows pause menu.
- Save the setting across launches; default to OFF. Apply changes immediately without restarting the game.
- Preserve the original pixel display with CRT off, and reset feedback when toggling or switching widescreen frame sizes.

## Changes since 0.4.0

- Fix Windows Xbox input by reading buttons, sticks and triggers through XInput. Gameplay, controller setup and menus use the same polled input state.
- Improve iOS controller event delivery, including Menu/Start and gamepad routing on iOS 18 and later.
- Keep controller slots stable across reordering and disconnects. Controllers join as Player 1, Player 3, Player 2 and Player 4.
- Align Player 1 and Player 4 possession indicators and scoring flashes with their status plates.
- Restore camera tracking at both near-side corners. Limit the inbound view separately so it stays inside the available scenery at both court ends.
- Preserve live settings changes, including switching head size during gameplay. Normal, big and huge head settings apply to all four players.
- Strip private build paths and debug metadata from release binaries. Check packages for ROMs, signing credentials and development artifacts.
- Include license notices and matching source references in both binary packages.

## Downloads

- `NBA-Hangtime-Windows-x64.zip`
- `NBA-Hangtime-iOS.ipa` (unsigned; sign using your sideloading tool)
- `NBA-Hangtime-0.4.3-source.zip`

Each archive has a companion SHA-256 checksum. Game ROMs are not included; the complete arcade L1.1 set is required. See `SOURCE.md` for source and distribution notices.

## Validation

Windows and iOS release builds succeeded. ROM importer, controller routing, native XInput decoding, controller remapping, camera bounds, live widescreen switching, core bridge and release hygiene tests passed.

Physical Xbox testing, visual confirmation of the revised inbound view and GPU rendering of the CRT effect remain unverified on Windows and iOS. The local build environment has no GPU/display access, so the graphics test harnesses could compile but could not run. If CRT is unavailable, the normal picture remains available.
