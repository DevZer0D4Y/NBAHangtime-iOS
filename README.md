# NBA Hangtime for iOS and Windows

A native iPhone, iPad and Windows port of Midway's **NBA Hangtime** (arcade, 1996). The original arcade program runs through an embedded [MAME 2003-Plus](https://github.com/libretro/mame2003-plus-libretro) core, with touch and controller support and a true widescreen mode.

**You need your own copy of the arcade ROM set (`nbahangt.zip`, revision L1.1). Game ROMs are not included.**

**[Releases](https://github.com/DevZer0D4Y/NBAHangtime-iOS/releases)** · [Changelog](CHANGELOG.md) · [Windows guide](desktop/README.md)

If you want to support me and remain up-to-date about this and other projects, you can in different ways:

Ko-Fi: https://ko-fi.com/dev_zer0

Discord: https://discord.gg/uFChheZEWX

YouTube: https://www.youtube.com/@develop_erZ

## Features

- The real arcade game, revision **L1.1 (04/16/96)**, with its original graphics, DCS sound and up to four players.
- **True widescreen.** During play, the game shows the full 512-pixel lines the arcade draws instead of the 400 its monitor displayed: more of the court and crowd, with nothing stretched. Player 1 and 4's status plates, the jump-ball meters and the arrows to off-screen players move to the new edges. Turn it off for the exact original.
- **Big and huge heads** for all four players, from the pause menu or with the arcade's own codes.
- On-screen touch controls with a floating stick, sprint at the stick's edge, haptics and a customizable layout. Spin, dunk and shove can each get a one-touch button.
- Controller support for up to four players: Xbox (Series X|S, One, Elite, and Xbox 360 on Windows), PlayStation, MFi and Switch Pro, with an NBA 2K-style default layout and remappable buttons, including the Xbox Share button and Elite paddles. The first two controllers play against each other.
- ROM import with a full check of all 26 files by checksum, whatever their names; missing or wrong files are listed.
- High scores, records and the arcade's operator settings are saved automatically. The game pauses when you switch apps or lock the phone.
- A Windows build with keyboard and gamepad support, remappable keys, fullscreen and drag-and-drop ROM loading.

## Requirements

- **iOS**: an iPhone or iPad running **iOS/iPadOS 16 or later**, and a sideloading tool to sign and install the IPA, such as ESign, AltStore, SideStore or Sideloadly.
- **Windows**: Windows 10 or 11, 64-bit.
- Your own **NBA Hangtime arcade ROM set, revision L1.1**, as a ZIP archive of 26 files: the program ROMs `htime54.bin` and `htime63.bin`, 20 graphics ROMs and 4 sound ROMs. [`ios/rom-manifest.json`](ios/rom-manifest.json) lists their names, sizes and CRC32 checksums. File names may differ, as each ROM is recognized by its checksum. *NBA Maximum Hangtime* and the home console versions are not supported.

A controller is recommended, but the game is fully playable with touch controls.

## Installation

### iPhone and iPad

1. Download `NBA-Hangtime-iOS.ipa` from the [latest release](https://github.com/DevZer0D4Y/NBAHangtime-iOS/releases) or [build it from source](#building).
2. Sign and install it with your sideloading tool. With ESign, import the IPA, then sign and install it inside ESign.
3. Open **NBA Hangtime**, tap **IMPORT nbahangt.zip** and pick your ROM archive in the Files app.
4. Tap **COIN**, then **START**.

You can also copy `nbahangt.zip` into **Files → On My iPhone → NBA Hangtime**, or into the app's folder from a computer (Finder's Files tab). The app loads it automatically at launch.

To update an existing installation, use the same signing identity and bundle identifier (`com.devz.nbahangtime`) so the app keeps its data.

### Windows

1. Download `NBA-Hangtime-Windows-x64.zip` from the [latest release](https://github.com/DevZer0D4Y/NBAHangtime-iOS/releases) and extract it.
2. Run `NBA Hangtime.exe`, then click **OPEN ROM ARCHIVE** or drag `nbahangt.zip` into the window.
3. Press **5** for a credit, then **1** to start.

The [Windows guide](desktop/README.md) covers the controls, settings and where your data is kept.

## Playing and settings

On iOS, tap **❚❚** to pause, or hold the controller's Menu button. The pause menu has four tabs:

| Tab | Settings |
|---|---|
| **GAME** | Resume, **HEADS** (normal, big or huge, for all four players), controller tutorial, restart the arcade |
| **DISPLAY** | **WIDESCREEN** (on by default); **SCREEN**: ARCADE (default), SQUARE or FULL; **PIXELS**: sharp or smooth |
| **TOUCH** | Touch controls (auto, on or off), floating or fixed stick, sprint at the stick's edge, button size, opacity, vibration, which extra buttons to show, and **CUSTOMIZE LAYOUT** |
| **GAMEPAD** | Remap every action to any controller button |

ARCADE keeps the arcade monitor's proportions (4:3, or about 16:9 in widescreen), SQUARE uses square pixels and FULL stretches the picture over the whole screen. On Windows, the same settings, HEADS included, are in the pause menu (**Esc**), with **F9** for widescreen, **F10** for the screen mode and **F11** for fullscreen.

### Controls

| Action | Touch | Controller | Keyboard (Windows) |
|---|---|---|---|
| Move | Stick | Left stick / D-pad | Arrow keys |
| Shoot / block | SHOOT | X | X |
| Pass / steal | PASS | A | C |
| Turbo | TURBO | RT / LT / RB | Z |
| Spin move | SPIN | B | A |
| Dunk (turbo + shoot) | DUNK (hidden by default) | Y | S |
| Shove (turbo + pass) | SHOVE (hidden by default) | LB | D |
| Coin | COIN | View / Back | 5 |
| Start | START | Menu / Start (tap) | 1 |
| Pause | ❚❚ | Hold Menu / Start, or the Xbox button | Esc |

The touch controls, the keyboard and the first controller play as player 1. Further controllers join as player 3, then player 2, then player 4, so two controllers play head to head and a third or fourth joins as a teammate.

### How widescreen works

The arcade draws every frame into video memory lines 512 pixels wide, but its monitor showed only 400 of them: 56 columns on each side were drawn and then hidden. In widescreen, the port shows the whole line while the court is up, and patches the L1.1 game program in memory when it loads (the ROM files are never changed) so that:

- objects are culled against the wider screen, and the court floor is drawn 512 pixels wide;
- the camera stops 56 pixels sooner at each end of the court, keeping the view inside the original artwork;
- player 1 and 4's status plates, the jump-ball meters and the arrows pointing to off-screen players sit at the new edges.

Menus and other screens stay 4:3 with black side bars. With widescreen off, the emulation is identical to the original. The patch locations come from the game's source code, published by [historicalsource](https://github.com/historicalsource/nba-hangtime).

## Status

Current version: **0.4.0 (build 5)**, the first public release. Only the arcade ROM set revision L1.1 is supported. See the [changelog](CHANGELOG.md) for the changes in each version.

## Building

Requires a Mac with **Xcode 16 or newer**, **Python 3**, **Git** and **Make**. The release build used Xcode 27.0.

The first build clones the pinned [MAME 2003-Plus](https://github.com/libretro/mame2003-plus-libretro) commit into the ignored `vendor/` folder and applies [`ios/scripts/core-ios.patch`](ios/scripts/core-ios.patch). Builds use two parallel jobs by default; set `HANGTIME_BUILD_JOBS` to change it.

### iOS

From the repository root:

```sh
xcodebuild -project ios/Hangtime.xcodeproj -scheme Hangtime -configuration Release \
  -sdk iphoneos -destination 'generic/platform=iOS' \
  -derivedDataPath ios/DerivedDataDevice CODE_SIGNING_ALLOWED=NO build
python3 ios/scripts/package-ipa.py
```

This writes an unsigned `dist/NBA-Hangtime-iOS.ipa`, ready for your sideloading tool. The packaging script refuses to include ROMs. You can also open `ios/Hangtime.xcodeproj` in Xcode, choose your team in Signing & Capabilities and run it on a device.

### Windows

Cross-compiled on the Mac with [LLVM-MinGW 20260616](https://github.com/mstorsjo/llvm-mingw/releases/tag/20260616) (`llvm-mingw-20260616-ucrt-macos-universal`) and [SDL2 2.32.10](https://github.com/libsdl-org/SDL/releases/tag/release-2.32.10) (`SDL2-devel-2.32.10-mingw`), both extracted into `vendor/`:

```sh
python3 desktop/build.py --windows
python3 desktop/package.py
```

This writes `dist/windows-x64/` and `dist/NBA-Hangtime-Windows-x64.zip`. On Windows itself, MSYS2 MinGW64 works too: `python3 desktop/build.py --windows --cc gcc --ar ar --sdl-prefix /mingw64`.

### Tests

After a first build has fetched the core:

```sh
python3 ios/tests/run-tests.py                               # ROM importer, core bridge and gamepad routing; no game files needed
python3 desktop/build.py                                     # native macOS build of the same frontend (brew install sdl2)
python3 desktop/tests/run-controller-tests.py                 # four virtual gamepads; no game files needed
python3 desktop/tests/run-game-test.py /path/to/nbahangt.zip   # runs the real game: video, audio and saved data
```

## Source layout

| Path | Contents |
|---|---|
| [`ios/Hangtime/`](ios/Hangtime/) | iOS app (Swift, UIKit): touch controls, gamepads, menus and settings, plus the C bridge to the core and the ROM importer shared with Windows |
| [`ios/scripts/`](ios/scripts/) | Core build, the MAME 2003-Plus patch with the Wolf-unit build setup, NVRAM saving and widescreen, and IPA packaging |
| [`desktop/`](desktop/) | SDL2 frontend for Windows (and macOS, for testing), build and packaging scripts, Windows guide |
| [`ios/tests/`](ios/tests/), [`desktop/tests/`](desktop/tests/) | ROM importer, core bridge and full-game tests |
| [`licenses/`](licenses/) | Third-party licenses |

## Credits

- [MAME 2003-Plus](https://github.com/libretro/mame2003-plus-libretro) and the MAME team, whose Midway Wolf-unit driver runs the game.
- [historicalsource/nba-hangtime](https://github.com/historicalsource/nba-hangtime), for publishing the game's original source, which made the widescreen mode possible.
- [SDL](https://www.libsdl.org) and [LLVM-MinGW](https://github.com/mstorsjo/llvm-mingw), for the Windows build.

## License

The port's own code (the iOS app, the Windows frontend, the bridge and the scripts) is licensed under the [MIT License](LICENSE). The MAME 2003-Plus core and the changes to it in `ios/scripts/core-ios.patch` are under the [MAME 2003-Plus license](licenses/MAME-2003-Plus-LICENSE.md), which forbids commercial use. Every build includes the core, so the IPA and the Windows package can't be sold either.

This is an unofficial fan project, not affiliated with or endorsed by Midway, Warner Bros. Games or the NBA. *NBA Hangtime* and its content belong to their respective owners, and NBA and team names and logos are trademarks of NBA Properties, Inc. and the teams. The app icon uses the game's cover art. No ROMs, game files, signing certificates or provisioning profiles are distributed with this source.

## Support and community

[Ko-Fi](https://ko-fi.com/dev_zer0) · [Discord](https://discord.gg/uFChheZEWX) · [YouTube](https://www.youtube.com/@develop_erZ)
