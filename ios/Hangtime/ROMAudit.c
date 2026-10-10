#include "HangtimeCore.h"
#include "unzip.h"
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
struct requirement { const char *name; unsigned size, crc; };
static const struct requirement required[] = {
    {"mhtu2.bin", 1048576, 0x3f0b0d0au},
    {"mhtu3.bin", 1048576, 0xec1db988u},
    {"mhtu4.bin", 1048576, 0xc7f847a3u},
    {"mhtu5.bin", 1048576, 0xef19316au},
    {"htime54.bin", 524288, 0xc2875d98u},
    {"htime63.bin", 524288, 0x6f4728c3u},
    {"mhtu133.bin", 1048576, 0x3163feedu},
    {"mhtu132.bin", 1048576, 0x428eaf44u},
    {"mhtu131.bin", 1048576, 0x5f7c5111u},
    {"mhtu130.bin", 1048576, 0xc7c0c514u},
    {"mhtu129.bin", 1048576, 0xb3d0daa0u},
    {"mhtu128.bin", 1048576, 0x3704ee69u},
    {"mhtu127.bin", 1048576, 0x4ea64d5au},
    {"mhtu126.bin", 1048576, 0x0c5c19b7u},
    {"mhtu125.bin", 1048576, 0x46c43d67u},
    {"mhtu124.bin", 1048576, 0xed495156u},
    {"mhtu123.bin", 1048576, 0xb48aa5dau},
    {"mhtu122.bin", 1048576, 0xb18cd181u},
    {"mhtu121.bin", 1048576, 0x5acb267au},
    {"mhtu120.bin", 1048576, 0x28e05f86u},
    {"mhtu119.bin", 1048576, 0xb4f604eau},
    {"mhtu118.bin", 1048576, 0xa257b973u},
    {"mhtu113.bin", 1048576, 0xd712a779u},
    {"mhtu112.bin", 1048576, 0x644e1bcau},
    {"mhtu111.bin", 1048576, 0x10d3b768u},
    {"mhtu110.bin", 1048576, 0x8575aeb2u},
};
bool ht_validate_rom(const char *path, char *report, size_t capacity) {
    if (!report || !capacity) return false;
    report[0] = 0;
    unzFile zip = unzOpen(path);
    if (!zip) { snprintf(report, capacity, "Invalid or unreadable ZIP archive."); return false; }
    bool found[sizeof(required)/sizeof(required[0])] = {false};
    int status = unzGoToFirstFile(zip);
    unsigned files = 0;
    while (status == UNZ_OK && ++files <= 1024) {
        unz_file_info info;
        if (unzGetCurrentFileInfo(zip, &info, NULL, 0, NULL, 0, NULL, 0) != UNZ_OK) break;
        for (unsigned i = 0; i < sizeof(required)/sizeof(required[0]); ++i) {
            if (info.crc != required[i].crc || info.uncompressed_size != required[i].size) continue;
            /* Read the payload too: central-directory checksums alone are untrusted. */
            if (unzOpenCurrentFile(zip) != UNZ_OK) continue;
            unsigned char buffer[16384]; unsigned total = 0; int n;
            while ((n = unzReadCurrentFile(zip, buffer, sizeof buffer)) > 0) { total += n; if (total > required[i].size) break; }
            int close_status = unzCloseCurrentFile(zip);
            if (n == 0 && total == required[i].size && close_status == UNZ_OK) found[i] = true;
        }
        status = unzGoToNextFile(zip);
    }
    unzClose(zip);
    unsigned missing = 0;
    for (unsigned i = 0; i < sizeof(required)/sizeof(required[0]); ++i) {
        if (!found[i]) {
            size_t used = strlen(report);
            if (used < capacity) snprintf(report + used, capacity - used, "%s%s (%08x)", missing ? "\n" : "Missing or invalid ROMs for NBA Hangtime L1.1:\n", required[i].name, required[i].crc);
            missing++;
        }
    }
    return missing == 0;
}
