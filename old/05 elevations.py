import asyncio
import pygame as pg
import sys, platform
import math

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
        car_x += delta*300

        for event in pg.event.get():
            if event.type == pg.QUIT: running = 0

        screen.fill((100,150,250))

        for i in range(120):
            scale = (121-i)/120
            x = car_x + i/scale
            y = 200*math.sin(x/1170) + 170*math.sin(x/580)
            z = 100+40*math.sin(x/1113)-60*math.sin(x/237)
            horizontal = 160-(160 - y)*scale
            vertical = 180-i +z*scale
            road_slice = road_texture.subsurface((0, (0.1*x)%360,320, 1))
            scaled_slice = pg.transform.scale(road_slice, (320*scale, 1))
            color = (int(50-i/3),int(130-i), int(50-z/20+30*math.sin(x)))
            pg.draw.rect(screen, color, (0, vertical, 320, 1))
            screen.blit(scaled_slice, (horizontal, vertical))

        
        pg.display.update()
        await asyncio.sleep(0)


if __name__ == "__main__":
    pg.init()
    asyncio.run(main())
    pg.quit()