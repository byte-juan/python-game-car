import asyncio
import pygame as pg
import sys, platform

async def main():
    screen_size = [320, 180]

    if sys.platform == "emscripten":
        platform.window.canvas.style.imageRendering = "pixelated"
        screen = pg.display.set_mode(screen_size)
    else:
        screen = pg.display.set_mode(screen_size, pg.SCALED)

    clock = pg.Clock()
    clock.tick(); pg.time.wait(16)
    road_texture = pg.image.load("assets/road.png").convert()

    car_x = 0

    running = 1

    while running: # game loop

        delta = clock.tick()/1000 + 0.00001
        car_x += delta*100

        for event in pg.event.get():
            if event.type == pg.QUIT: running = 0

        screen.fill((100,150,250))

        for i in range(180):
            x = car_x + i
            road_slice = road_texture.subsurface((0, (x)%360,320, 1))
            screen.blit(road_slice, (0, 180-i))

        
        pg.display.update()
        await asyncio.sleep(0)


if __name__ == "__main__":
    pg.init()
    asyncio.run(main())
    pg.quit()