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
    mountains_texture = pg.image.load("assets/mountains.png").convert()
    car_sprite = pg.image.load("assets/car.png").convert()
    car_sprite2 = pg.image.load("assets/car2.png").convert()
    tree_sprite = pg.image.load("assets/tree.png").convert()
    car_sprite.set_colorkey((255,0,255))
    car_sprite2.set_colorkey((255,0,255))
    tree_sprite.set_colorkey((255,0,255))

    cars = [Car_front(-50), Car_front(-13), Car_front(7)]
    trees = [Tree(-57), Tree(-35), Tree(-20), Tree(-3)]


    distance, car_angle, car_y, car_vel, car_acc = 0,0,300,0,0

    running = 1
    offset =0
    while running: # game loop

        delta = clock.tick()/1000 + 0.00001

        for event in pg.event.get():
            if event.type == pg.QUIT: running = 0
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE: running = 0

        screen.fill((120,120,220))
        car_sin = math.sin(car_angle)
        screen.blit(mountains_texture, (-64-car_sin*90,0))
        vertical  = 180
        last_vertical = 181.1

        draw_distance = 1
        z0 = calc_z(distance)
        z_buffer = [999 for element in range(180)]
        
        for i in range(120):
            last_vertical = vertical
            while vertical >= last_vertical and draw_distance < 100:
                draw_distance += (1 + i)/500
                x = distance + draw_distance
                y = calc_y(x) - car_y#*scale 
                z = calc_z(x) -z0
                vertical = int(60+160/draw_distance + z/draw_distance)
            if draw_distance > 100:
                break
            z_buffer[int(vertical)] = draw_distance
            thickness = max(last_vertical - vertical, 1)

            scale = 1/(draw_distance)#+z/600)
            road_slice = road_texture.subsurface((0, (x*10)%360,320, 1))
            
            
            horizontal = 160- 160*scale + y*scale + car_sin*(vertical-150)

            scaled_slice = pg.transform.smoothscale(road_slice, (420*scale, thickness))
            pg.draw.rect(screen, (int(50-draw_distance/3),int(130-draw_distance), int(50-z/20+30*math.sin(x))), (0, vertical, 320, thickness))
            screen.blit(scaled_slice, (horizontal,vertical))
        
        for tree_index in reversed(range(len(trees)-1)):

                draw_distance2 = trees[tree_index].x - distance
                x2 = trees[tree_index].x
                y2 = calc_y(trees[tree_index].x) + trees[tree_index].y
                z2 = calc_z(trees[tree_index].x) -z0
                vertical2 = int(60+160/draw_distance2 + z2/draw_distance2)
                if vertical2 > 0 and vertical2 < 180 and (z_buffer[int(vertical2)] > draw_distance2-10 or draw_distance < 60):
                    scale2 = max(0.001, 1/draw_distance2)
                    horizontal2 = 160- 160*scale2 + y2*scale2 - car_y*scale2 + car_sin*(vertical2-150)
                    scaled_tree = pg.transform.scale_by(tree_sprite, scale2*15)
                    screen.blit(scaled_tree, (horizontal2,vertical2-300*scale2 ))


                #trees[tree_index].x -= 10*delta
            
        for car_front_index in reversed(range(len(cars)-1)):

                draw_distance2 = cars[car_front_index].x - distance
                x2 = cars[car_front_index].x
                y2 = calc_y(cars[car_front_index].x)
                z2 = calc_z(cars[car_front_index].x) -z0
                vertical2 = int(60+160/draw_distance2 + z2/draw_distance2)
                if vertical2 < 180 and z_buffer[int(vertical2)] > draw_distance2-5:
                    scale2 = 1/draw_distance2
                    horizontal2 = 160- 160*scale2 + (y2+60)*scale2 - car_y*scale2 + car_sin*(vertical2-150)
                    scaled_car = pg.transform.scale_by(car_sprite2, scale2*2)
                    screen.blit(scaled_car, (horizontal2,vertical2-50*scale2 ))
                cars[car_front_index].x -= 10*delta
        
        if cars[0].x < distance+1:
            cars.pop(0)
            cars.append(Car_front(distance))
        if trees[0].x < distance+1:
            trees.pop(0)
            trees.append(Tree(trees[-1].x))
    
        

        #screen.blit(car_sprite, (100+car_y-y0/2, 120))
        screen.blit(car_sprite, (100, 120))
        
        pg.display.set_caption(str(int(1/delta)))
        distance, car_angle, car_y, car_vel, car_acc = controls(distance, car_angle, car_y, car_vel, car_acc, delta)
        if abs(car_y - (100 + 200*math.sin((distance/17)) + 170*math.sin(distance/8))) > 180 and car_vel > 5:
            car_vel += -car_vel*delta
            car_acc += -car_acc*delta
            pg.draw.circle(screen, (255,0,0), (300, 170), 3)
        
        pg.display.update()
        await asyncio.sleep(0)

def calc_y(x):
    return 200*math.sin(x/17) + 170*math.sin(x/8)#+ 300*math.sin(x/7)

def calc_z(x):
    return 200+80*math.sin(x/13)-120*math.sin(x/7)

def controls(distance, car_angle, car_y, car_vel, car_acc, delta):
    pressed_keys = pg.key.get_pressed()
    car_acc += -0.1*car_acc*delta
    car_vel += -0.1*car_vel*delta
    #car_angle += -0.1*car_angle*delta
    if pressed_keys[pg.K_w] or pressed_keys[pg.K_UP]:
        if car_vel > -1:
            car_acc += delta
        else:
            car_acc = 0
            car_vel += -0.5*car_vel*delta
    elif pressed_keys[pg.K_s] or pressed_keys[pg.K_DOWN]:
        if car_vel < 1:
            car_acc -= delta
        else:
            car_acc = 0
            car_vel += -0.5*car_vel*delta
    if pressed_keys[pg.K_a] or pressed_keys[pg.K_LEFT]:
        car_angle -= delta*car_vel/10
    elif pressed_keys[pg.K_d] or pressed_keys[pg.K_RIGHT]:
        car_angle += delta*car_vel/10
    car_vel = max(-10,min(car_vel, 20))
    car_angle = max(-0.8,(min(0.8, car_angle)))
    car_vel += car_acc*delta
    distance += car_vel*delta*math.cos(car_angle)
    car_y += car_vel*math.sin(car_angle)*delta*100

    return distance, car_angle, car_y, car_vel, car_acc

class Car_front():
    def __init__(self, distance):
        self.x = distance +100

class Tree():
    def __init__(self, distance):
        self.x = distance +random.randint(100, 120)
        self.y = random.randint(500, 1500)*random.choice([-1,1])


if __name__ == "__main__":
    pg.init()
    asyncio.run(main())
    pg.quit()