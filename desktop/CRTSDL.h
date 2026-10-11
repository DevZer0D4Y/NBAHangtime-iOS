#include <SDL.h>
#include <stdint.h>
#include <stdbool.h>
bool crt_draw(SDL_Renderer *,SDL_Texture *,const uint8_t *,unsigned,unsigned,SDL_Rect,bool);
void crt_reset(void);
void crt_shutdown(void);
