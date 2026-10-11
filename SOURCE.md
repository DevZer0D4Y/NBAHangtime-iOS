# Source and distribution

NBA Hangtime 0.4.3 (iOS build 8) is an unofficial fan port.

Distribute the matching `NBA-Hangtime-0.4.3-source.zip` alongside the Windows ZIP and unsigned iOS IPA. The source archive contains the port and its patched MAME core, with build instructions in `README.md`.

Port source: https://github.com/DevZer0D4Y/NBAHangtime-iOS

Core source: https://github.com/libretro/mame2003-plus-libretro/tree/e05caba0aa33cae580d104c45c6caa6406617e3b

Core modifications: `ios/scripts/core-ios.patch` in the port source. The bundled core source already has this patch applied.

Windows SDL2 dependency source (2.32.10): https://github.com/libsdl-org/SDL/tree/release-2.32.10

The port's own code uses the MIT license (`LICENSE-MIT.txt` in binary packages; `LICENSE` in source). The included MAME core uses the non-commercial MAME 2003-Plus license (`MAME-LICENSE.md`). SDL2 uses the zlib license (`SDL-LICENSE.txt` in the Windows package). Keep these notices with redistributed packages. The included MAME license restricts commercial distribution and requires source availability.

NewPixie CRT by Mattias Gustavsson, with Slang adaptation by hunterk, uses the MIT license (`NewPixie-MIT.txt`). Its native Metal and OpenGL adapters are included in the matching source archive. Upstream: https://github.com/libretro/slang-shaders/tree/master/crt/shaders/newpixie

No game ROMs are included. Users must supply their own complete NBA Hangtime arcade L1.1 ROM archive. The iOS IPA is unsigned and must be signed before installation.
