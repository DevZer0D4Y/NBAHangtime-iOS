# NBA Hangtime for Windows

The original 1996 Midway arcade game, running through an embedded MAME 2003-Plus core.

**You need your own copy of the arcade ROM set: `nbahangt.zip`, revision L1.1. No game files are included.**

## Quick start

1. Keep `NBA Hangtime.exe` and `SDL2.dll` in the same folder and run `NBA Hangtime.exe`.
2. Click **OPEN ROM ARCHIVE** (or press **O**), or drag `nbahangt.zip` into the window. The archive must hold all 26 files of the L1.1 set; file names may differ, as each ROM is recognised by its checksum. The app checks it, keeps a copy and opens it automatically from then on.
3. Press **5** for a credit, then **1** to start. With a controller, press **View** (Back), then **Menu** (Start).

If Windows shows "Windows protected your PC", click **More info › Run anyway**. The executable is not code-signed.

## Controls

Defaults, with an NBA 2K-style controller layout. Every action can be remapped in **CONTROLS**.

| Action | Keyboard | Controller |
| --- | --- | --- |
| Move | Arrow keys | D-pad / left stick |
| Shoot / block | X | X |
| Pass / steal | C | A |
| Turbo | Z | RT / LT / RB |
| Spin move | A | B |
| Dunk (turbo + shoot) | S | Y |
| Shove (turbo + pass) | D | LB |
| Coin | 5 | View / Back |
| Start | 1 | Menu / Start (tap) |
| Pause menu | Esc or P | Hold Menu / Start, or the Xbox button |
| Controls | F1 | Pause menu |
| Widescreen on/off | F9 | Pause menu |
| Screen mode | F10 | Pause menu |
| Fullscreen | F11 or Alt+Enter | Pause menu |

Xbox controllers (Xbox 360, One, Series X|S and Elite) work out of the box, as do other XInput and SDL-compatible gamepads; the Share button and the Elite paddles can be assigned to actions too.

The keyboard and the first controller play as player 1. Further controllers join as player 3, then player 2, then player 4, so the first two controllers play against each other. In menus, use the arrow keys or D-pad, Enter or A to confirm, Esc or B to go back. On the controls screen, Backspace or Y restores the defaults.

## Game

**HEADS** in the pause menu gives all four players big or huge heads (NORMAL, BIG or HUGE). The arcade's big and huge head codes also apply to all four players.

## Display

- **WIDESCREEN** (on by default) shows more of the court during play instead of stretching the picture. The arcade draws 512 pixels per line but its monitor showed only the middle 400; widescreen shows them all. Players 1 and 4's name plates and the jump-ball meters move to the new edges, and the camera stops slightly sooner at each end of the court so nothing outside the original artwork comes into view. Menus and other screens stay 4:3. With widescreen off, the game runs exactly as the arcade original.
- **SCREEN**: **ARCADE** keeps the arcade monitor's proportions (4:3, or about 16:9 in widescreen), **SQUARE** uses square pixels and **FULL** stretches the picture over the whole window.

## Your data

Settings, the copy of your ROM set and the arcade's saved data (high scores, records, operator settings) are kept in `%APPDATA%\HistoricalSource\Hangtime`. The game pauses when the window loses focus or a controller disconnects, and saves periodically, on pause and on exit. To use a different ROM set, close and reopen the app.

Command line: `"NBA Hangtime.exe" path\to\nbahangt.zip` starts with that archive, and `"NBA Hangtime.exe" --audit path\to\nbahangt.zip` reports whether a set is complete.

## Licenses

The MAME 2003-Plus core is distributed under the MAME license (`MAME-LICENSE.md`): non-commercial use only. SDL2 is under the zlib license (`SDL-LICENSE.txt`). This is an unofficial fan project, not affiliated with or endorsed by Midway, Warner Bros. Games or the NBA.
