#ifndef HANGTIME_CORE_H
#define HANGTIME_CORE_H
#include <stdint.h>
#include <stddef.h>
#include <stdbool.h>
/* Core calls on main thread; audio consumer can run on the audio thread. */
bool ht_validate_rom(const char *path, char *report, size_t capacity);
bool ht_start(const char *path, const char *directory);
void ht_run(void);
bool ht_save_data(void);
void ht_stop(void);
void ht_reset(void);
void ht_set_buttons(unsigned player, uint16_t buttons);
const uint8_t *ht_pixels(void);
unsigned ht_width(void);
unsigned ht_height(void);
double ht_fps(void);
double ht_sample_rate(void);
/* Display aspect of the current frame: 4:3 for the arcade's 400 columns, wider in widescreen. */
double ht_aspect_ratio(void);
/* Widescreen shows the full 512-column bitmap during play (more of the court, not stretched).
   Can be set before or after ht_start; it applies at the next frame. */
void ht_set_widescreen(bool enable);
bool ht_widescreen(void);
/* Head size for all four players: 0 = as the game decides (codes), 1 = big, 2 = huge. */
void ht_set_heads(int mode);
const char *ht_error(void);
void ht_audio_read(float *left, float *right, unsigned frames);
void ht_audio_clear(void);
#endif
