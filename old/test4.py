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
    trees = [Tree(-57), Tree(-35), Tree(-23), Tree(-3)]

    car = Player()

    running = 1

    while running: # game loop

        delta = clock.tick()/1000 + 0.00001

        for event in pg.event.get():
            if event.type == pg.QUIT: running = 0
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE: running = 0

        screen.fill((100,150,250))
        screen.blit(mountains_texture, (-65- car.angle*82,0))
        vertical  = 180

        draw_distance = 1
        y0, z0 = calc_yz(car.x+2)
        z_buffer = [999 for element in range(180)]
        
        while draw_distance < 120:
            last_vertical = vertical
            while vertical >= last_vertical and draw_distance < 120:
                draw_distance += draw_distance/150
                x = car.x + draw_distance
                y, z = calc_yz(x, car.y, z0)
                vertical = int(60+160/draw_distance + z/draw_distance)
            
            if draw_distance < 120:
                z_buffer[int(vertical)] = draw_distance

                scale = 1/draw_distance 
                road_slice = road_texture.subsurface((0, (x*10)%360,320, 1))
                color = (int(50-draw_distance/3),int(130-draw_distance), int(50-z/20+30*math.sin(x)))
                pg.draw.rect(screen, color, (0, vertical, 320, 1))
                render_element(screen, road_slice, 500*scale, 1, scale, x,  car.angle, car.y, z0, z_buffer)


        
        for tree_index in reversed(range(len(trees)-1)):
            scale = max(0.0001, 1/(trees[tree_index].x - car.x))
            render_element(screen, tree_sprite, 200*scale, 300*scale, scale, trees[tree_index].x,
                             car.angle, trees[tree_index].y +car.y, z0, z_buffer, car.y)

        for car_front_index in reversed(range(len(cars)-1)):
            scale = max(0.0001, 1/(cars[car_front_index].x - car.x))
            render_element(screen, car_sprite2, 100*scale, 80*scale, scale, cars[car_front_index].x,
                             car.angle, -70 +car.y, z0, z_buffer, car.y)

            cars[car_front_index].x -= .10*delta
        
        if cars[0].x < car.x+1:
            cars.pop(0)
            cars.append(Car_front(car.x))
        if trees[0].x < car.x+1:
            trees.pop(0)
            trees.append(Tree(trees[-1].x))
    
        screen.blit(car_sprite, (100, 120))
        
        pg.display.set_caption(str(int(1/delta)))
        car.controls(delta)
        if abs(car.y - y0 -100) > 280 and car.velocity > 5:
            car.velocity += -car.velocity*delta
            car.acceleration += -car.acceleration*delta
            pg.draw.circle(screen, (255,0,0), (300, 170), 3)
        
        pg.display.update()
        await asyncio.sleep(0)

def calc_yz(x, y_offset=0, z_offset=0):
    y = 200*math.sin(x/17) + 170*math.sin(x/8) - y_offset
    z = 200+80*math.sin(x/13)-120*math.sin(x/7) - z_offset

    return y, z


def render_element(screen, sprite, width, height, scale,
                    x,  car_angle, y_offset, z_offset, z_buffer, car_y=0):
    y, z = calc_yz(x, y_offset, z_offset)

    vertical = int(60+160*scale + z*scale)
    if vertical >= 1 and vertical < 180 and z_buffer[vertical-1] > 1/scale -10:
        horizontal = 160- 160*scale + y*scale +  car_angle*(vertical-150) #- car_y*scale 

        scaled_sprite = pg.transform.scale(sprite, (width, height))
        screen.blit(scaled_sprite, (horizontal,vertical-height+1))

class Player():
    def __init__(self):
        self.x = 0
        self.y = 300
        self.angle = 0
        self.velocity = 0
        self.acceleration = 0

    def controls(self, delta):
        pressed_keys = pg.key.get_pressed()
        self.acceleration += -0.5*self.acceleration *delta
        self.velocity += -0.5*self.velocity*delta

        if pressed_keys[pg.K_w] or pressed_keys[pg.K_UP]:
            if self.velocity > -1:
                self.acceleration  += 4*delta
            else:
                self.acceleration  = 0
                self.velocity += -self.velocity*delta
        elif pressed_keys[pg.K_s] or pressed_keys[pg.K_DOWN]:
            if self.velocity < 1:
                self.acceleration  -= delta
            else:
                self.acceleration  = 0
                self.velocity += -self.velocity*delta
        if pressed_keys[pg.K_a] or pressed_keys[pg.K_LEFT]:
            self.angle -= delta*self.velocity/10
        elif pressed_keys[pg.K_d] or pressed_keys[pg.K_RIGHT]:
            self.angle += delta*self.velocity/10
        self.velocity = max(-10,min(self.velocity, 20))
        self.angle = max(-0.8,(min(0.8, self.angle)))
        self.velocity += self.acceleration *delta
        self.x += self.velocity*delta*math.cos(self.angle)
        self.y += self.velocity*math.sin(self.angle)*delta*100

class Car_front():
    def __init__(self, distance):
        self.x = distance +100

class Tree():
    def __init__(self, distance):
        self.x = distance +random.randint(10, 50) + 0.5
        self.y = random.randint(500, 1500)*random.choice([-1,1])


if __name__ == "__main__":
    pg.init()
    asyncio.run(main())
    pg.quit()