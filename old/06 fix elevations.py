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
        car_x += delta*3

        for event in pg.event.get():
            if event.type == pg.QUIT: running = 0

        screen.fill((100,150,250))
        vertical = 180
        draw_distance = 1
        while draw_distance < 120:
            last_vertical = vertical
            while vertical >= last_vertical and draw_distance < 120:
                draw_distance += draw_distance/150
                x = car_x + draw_distance
                z = 200+80*math.sin(x/13)-120*math.sin(x/7)
                scale = 1/draw_distance

                vertical = int(60+160*scale + z*scale)
            if draw_distance < 120:
                y = 200*math.sin(x/17) + 170*math.sin(x/8)

                horizontal = 160-(160 - y)*scale

                road_slice = road_texture.subsurface((0, (10*x)%360,320, 1))
                scaled_slice = pg.transform.scale(road_slice, (500*scale, 1))
                color = (int(50-draw_distance/3),int(130-draw_distance), int(50-z/20+30*math.sin(x)))
                pg.draw.rect(screen, color, (0, vertical, 320, 1))
                screen.blit(scaled_slice, (horizontal, vertical))

        
        pg.display.update()
        await asyncio.sleep(0)


if __name__ == "__main__":
    pg.init()
    asyncio.run(main())
    pg.quit()