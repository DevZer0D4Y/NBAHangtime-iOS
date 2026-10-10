# Changelog

## 0.4.1 (build 6)

- Read Windows Xbox buttons, sticks and triggers directly through XInput. Controller setup and menu navigation now poll the same input state as gameplay, including when controller button events are unavailable.
- Declare iOS game-controller support and request gamepad event delivery through the GameController framework on iOS 18 and later.
- Restore the arcade camera's full horizontal travel in widescreen mode so players do not disappear into the near-side corners.


- Strip release executable debug metadata and local symbols that expose build paths. Audit release payloads for home-directory paths, private keys, signing files, ROMs and development artifacts before packaging.

- Route iOS controller events to the game instead of UIKit navigation, including Menu/Start presses.
- Keep controller player assignments stable when the system changes the controller list order or a controller disconnects. Clear disconnected inputs on Windows.
- Select the native XInput backend for Xbox controllers on Windows.
- Align player 1 and 4 possession indicators and scoring flashes with their status plates in widescreen mode.
- Add controller regression coverage for four-player input, Start, pause, reconnects and menu button suppression.

## 0.4.0 (build 5)

First public release.

- iPhone and iPad app (iOS 16+) and Windows x64 build, sharing one MAME 2003-Plus core and ROM importer.
- True widescreen: during play the full 512-pixel lines the arcade draws are shown, with player 1 and 4's status plates, the jump-ball meters and the off-screen player arrows at the new edges, and the camera kept inside the original artwork. Menus stay 4:3. On by default, can be switched during a game, and identical to the original when off.
- HEADS option in the pause menu: normal, big or huge heads for all four players. The arcade's big and huge head codes now apply to all four players too, instead of only the player who entered them.
- Xbox controller support (Series X|S, One and Elite, plus Xbox 360 on Windows), with Xbox button names, the Xbox button for pause, and the Share button and Elite paddles available for remapping.
- Controllers join as players 1, 3, 2 and 4, so the first two controllers play against each other.
- Screen modes ARCADE (default), SQUARE and FULL, with sharp or smooth pixels.
- Touch controls with a floating stick, sprint at the stick's edge, haptics, optional spin, dunk and shove buttons, and a customizable layout.
- Up to four controllers, with an NBA 2K-style default layout and remappable buttons.
- Windows: keyboard and gamepad remapping, pause menu, fullscreen, drag-and-drop ROM loading, app icon and version details.
- ROM import with a checksum check of all 26 files of the L1.1 set; high scores, records and operator settings saved automatically.
