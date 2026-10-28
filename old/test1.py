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
    
    total_time = 0

    running = 1
    offset =0
    while running: # game loop

        delta = clock.tick(60)
        total_time += delta

        for event in pg.event.get():
            if event.type == pg.QUIT: running = 0
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE: running = 0
                if event.key == pg.K_d or event.key == pg.K_RIGHT:
                    offset -= delta
                if event.key == pg.K_a or event.key == pg.K_LEFT:
                    offset += delta

        screen.fill((120,120,220))
        offset = -100*math.sin((-total_time/10000))
        v_offset = 30*math.sin(-total_time/10000)
        
        pg.draw.circle(screen, (190, 110, 90), [50+offset, 50+v_offset], 20)
        
        for i in range(5):
            pg.draw.polygon(screen, (10-i*2, 25+i*20, 60+i*30), [[-100+offset+i*150, 200+v_offset],
                                                                 [200+offset+i*150, 10+i*50+v_offset],
                                                                 [400+offset+i*150, 200+v_offset]])

        last_vertical=0
        for i in range(150):
            distance = (120 - i)**3/15000
            scale = i/120
            road_slice = road_texture.subsurface((0, (-total_time/10-distance)%360,320, 1))
            scaled_slice = pg.transform.smoothscale(road_slice, (320*scale+1, 1))
            horizontal = offset+100*math.sin((-total_time/10000-distance/100))
            vertical = i+60+30*math.sin((-total_time/10000-distance/100))
            #for j in range(1):#int(max(1, last_vertical-vertical))):

            pg.draw.rect(screen, (int(30+i/3),int(20+i/2), 10), (0, vertical, 320, 1))
            screen.blit(scaled_slice, (160+horizontal-(320*scale+1)*0.5,vertical))
            if vertical - last_vertical > 1:
                pg.draw.rect(screen, (int(30+i/3), int(20+i/2), 10), (0, vertical-1, 320, 1))
                screen.blit(scaled_slice, (160+horizontal-(320*scale+1)*0.5,vertical-1))

            last_vertical = vertical
            if last_vertical >= 180:
                break
        
        #small_car_distance = (120 - total_time/100)**3/15000%80
        #small_car = pg.transform.scale_by(car_sprite, 1/small_car_distance)
        #print(small_car_distance)
        #screen.blit(small_car, (120+offset+100*math.sin((-0*total_time/10000-small_car_distance/10)), 120-small_car_distance))
        screen.blit(car_sprite, (120, 120))
        pg.display.update()

        await asyncio.sleep(0)

if __name__ == "__main__":
    pg.init()
    asyncio.run(main())
    pg.quit()