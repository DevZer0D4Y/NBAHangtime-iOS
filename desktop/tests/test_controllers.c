/* Exercise the shipped SDL input path with four virtual Xbox-style gamepads. */
#define main hangtime_frontend_main
#include "../main.c"
#undef main
#include <assert.h>

int main(void) {
    SDL_SetHint(SDL_HINT_VIDEODRIVER,"dummy");
    SDL_SetHint(SDL_HINT_JOYSTICK_ALLOW_BACKGROUND_EVENTS,"1");
    assert(SDL_Init(SDL_INIT_VIDEO | SDL_INIT_GAMECONTROLLER)==0);
    window=SDL_CreateWindow("Controller tests",0,0,64,64,SDL_WINDOW_HIDDEN);
    assert(window);
    memcpy(keys,default_keys,sizeof keys); memcpy(pads,default_pads,sizeof pads);
    reset_players(false);
    SDL_Joystick *virtual[4];
    for (unsigned i=0;i<4;i++) {
        SDL_VirtualJoystickDesc desc={0};
        desc.version=SDL_VIRTUAL_JOYSTICK_DESC_VERSION;
        desc.type=SDL_JOYSTICK_TYPE_GAMECONTROLLER;
        desc.naxes=SDL_CONTROLLER_AXIS_MAX; desc.nbuttons=SDL_CONTROLLER_BUTTON_MAX;
        desc.vendor_id=0x045e; desc.product_id=0x02ea; desc.name="Virtual Xbox Controller";
        desc.button_mask=(1u<<SDL_CONTROLLER_BUTTON_MAX)-1;
        desc.axis_mask=(1u<<SDL_CONTROLLER_AXIS_MAX)-1;
        int device=SDL_JoystickAttachVirtualEx(&desc); assert(device>=0);
        virtual[i]=SDL_JoystickOpen(device); assert(virtual[i]);
        update_controllers(); assert(controllers[i]);
    }
    const unsigned expected[4]={0,2,1,3};
    for (unsigned i=0;i<4;i++) {
        assert(player_port[i]==expected[i]);
        assert(SDL_JoystickSetVirtualButton(virtual[i],SDL_CONTROLLER_BUTTON_X,1)==0);
        assert(SDL_JoystickSetVirtualButton(virtual[i],SDL_CONTROLLER_BUTTON_A,1)==0);
        assert(SDL_JoystickSetVirtualAxis(virtual[i],SDL_CONTROLLER_AXIS_LEFTX,-32768)==0);
        assert(SDL_JoystickSetVirtualButton(virtual[i],SDL_CONTROLLER_BUTTON_START,1)==0);
        SDL_PumpEvents(); input_poll();
        assert((next_frame(&players[i]) & (PAD_SHOOT|PAD_PASS|PAD_LEFT))==(PAD_SHOOT|PAD_PASS|PAD_LEFT));
        assert(SDL_JoystickSetVirtualButton(virtual[i],SDL_CONTROLLER_BUTTON_START,0)==0);
        SDL_PumpEvents(); input_poll();
        assert(next_frame(&players[i]) & PAD_START);
        for (unsigned j=0;j<4;j++) if (j!=i) assert(!players[j].start_pulse);
        SDL_JoystickSetVirtualButton(virtual[i],SDL_CONTROLLER_BUTTON_X,0);
        SDL_JoystickSetVirtualButton(virtual[i],SDL_CONTROLLER_BUTTON_A,0);
        SDL_JoystickSetVirtualAxis(virtual[i],SDL_CONTROLLER_AXIS_LEFTX,0);
        SDL_PumpEvents(); reset_players(false);
    }
    SDL_JoystickSetVirtualButton(virtual[0],SDL_CONTROLLER_BUTTON_X,1);
    SDL_PumpEvents(); input_poll(); assert(players[0].held[A_SHOOT]);
    assert(SDL_JoystickDetachVirtual(0)==0);
    SDL_PumpEvents(); update_controllers();
    assert(!controllers[0] && !players[0].held[A_SHOOT]);
    assert(controllers[1] && controllers[2] && controllers[3]);
    for (unsigned i=0;i<4;i++) {
        if (controllers[i]) SDL_GameControllerClose(controllers[i]);
        SDL_JoystickClose(virtual[i]);
    }
    SDL_DestroyWindow(window); SDL_Quit();
    puts("SDL controllers: four Xbox-style pads, gameplay buttons, movement, Start order and disconnect passed.");
    return 0;
}
