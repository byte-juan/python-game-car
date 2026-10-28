import asyncio
import pygame as pg
import sys, platform
import random
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
    car_sprite = pg.image.load("assets/car.png").convert()
    car_sprite.set_colorkey((255,0,255))

    velocity = 0
    distance = 0
    
    total_time = 0

    running = 1
    offset =0
    while running: # game loop
        p_mouse = pg.mouse.get_pos()

        delta = clock.tick(60)/1000
        distance += delta*10

        for event in pg.event.get():
            if event.type == pg.QUIT: running = 0
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE: running = 0

        screen.fill((120,120,220))
        vertical  = 181
        last_vertical = 181.1
        x = distance +1
        draw_distance = 1
        for i in range(120):
            last_vertical = vertical
            while vertical >= last_vertical and draw_distance < 1000:
                draw_distance += 0.001 + i/1000
                # x = distance + 160/(120.1-i))
                x = distance + draw_distance
                y = 50*math.sin((x/10))
                z = 5*math.sin((x/5))
                #vertical = int(120-i+60+z)
                vertical = int(60+160/draw_distance+z)
                #vertical = int(180 - 2/draw_distance+z)
                print(x,y,z,vertical, draw_distance)
            if draw_distance > 100:
                break
            #vertical = last_vertical - 1

            scale = 1/draw_distance
            road_slice = road_texture.subsurface((0, (x*30)%360,320, 1))
            
            horizontal = 160- (p_mouse[0]) - 160*scale + y

            scaled_slice = pg.transform.scale(road_slice, (320*scale, 1))
            pg.draw.rect(screen, (int(50-i/3),int(130-i), int(20+z)), (0, vertical, 320, 1))
            screen.blit(scaled_slice, (horizontal,vertical))

        
        scale = abs((p_mouse[1]-60)/100)
        resized_car = pg.transform.scale_by(car_sprite, scale)
        screen.blit(resized_car, p_mouse)
        pg.display.update()

        await asyncio.sleep(0)

if __name__ == "__main__":
    pg.init()
    asyncio.run(main())
    pg.quit()