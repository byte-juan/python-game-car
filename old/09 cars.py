import asyncio
import pygame as pg
import sys, platform
import math, random

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
    car_sprite.set_colorkey((255,0,255))
    car_sprite2 = pg.image.load("assets/car2.png").convert()
    car_sprite2.set_colorkey((255,0,255))
    tree_sprite = pg.image.load("assets/tree.png").convert()
    tree_sprite.set_colorkey((255,0,255))

    car = Player()

    running = 1
    cars = [Car(-50), Car(-23), Car(7)]
    trees = [Tree(-67), Tree(-55), Tree(-43), Tree(-33), Tree(-25), Tree(-13), Tree(-3)]

    while running: # game loop

        delta = clock.tick()/1000 + 0.00001
        car.controls(delta)        

        for event in pg.event.get():
            if event.type == pg.QUIT: running = 0

        screen.blit(mountains_texture, (-65- car.angle*82,0))#screen.fill((100,150,250))
        vertical = 180
        draw_distance = 1
        car.z = calc_z(car.x)
        z_buffer = [999 for element in range(180)]
        while draw_distance < 120:
            last_vertical = vertical
            while vertical >= last_vertical and draw_distance < 120:
                draw_distance += draw_distance/150
                x = car.x + draw_distance
                z = calc_z(x) - car.z
                scale = 1/draw_distance

                vertical = int(60+160*scale + z*scale)

            if draw_distance < 120:
                z_buffer[int(vertical)] = draw_distance
                road_slice = road_texture.subsurface((0, (x*10)%360,320, 1))
                color = (int(50-draw_distance/3),int(130-draw_distance), int(50-z/20+30*math.sin(x)))
                pg.draw.rect(screen, color, (0, vertical, 320, 1))
                render_element(screen, road_slice, 500*scale, 1, scale, x,  car, car.y, z_buffer)
        
        for index in reversed(range(len(trees)-1)):
            scale = max(0.0001, 1/(trees[index].x - car.x))
            render_element(screen, tree_sprite, 200*scale, 300*scale, scale, trees[index].x, car, trees[index].y+car.y, z_buffer)
        
        if trees[0].x < car.x+1:
            trees.pop(0)
            trees.append(Tree(trees[-1].x))

        for index in reversed(range(len(cars)-1)):
            scale = max(0.0001, 1/(cars[index].x - car.x))
            render_element(screen, car_sprite2, 100*scale, 80*scale, scale, cars[index].x, car, -70+car.y, z_buffer)
            cars[index].x -= 10*delta
        
        if cars[0].x < car.x+1:
            cars.pop(0)
            cars.append(Car(car.x))

                

        screen.blit(car_sprite, (100, 120))
        pg.display.update()
        await asyncio.sleep(0)

class Car():
    def __init__(self, distance):
        self.x = distance + random.randint(90, 110)

class Tree():
    def __init__(self, distance):
        self.x = distance +random.randint(10, 20) + 0.5
        self.y = random.randint(500, 1500)*random.choice([-1,1])

def calc_y(x):
    return 200*math.sin(x/17) + 170*math.sin(x/8)

def calc_z(x):
    return 200+80*math.sin(x/13)-120*math.sin(x/7)

def render_element(screen, sprite, width, height, scale, x, car, y, z_buffer):
    y = calc_y(x) - y
    z = calc_z(x) - car.z

    vertical = int(60+160*scale + z*scale)
    if vertical >= 1 and vertical < 180 and z_buffer[vertical-1] > 1/scale -10:
        horizontal = 160-(160 - y)*scale +  car.angle*(vertical-150)

        scaled_sprite = pg.transform.scale(sprite, (width, height))
        screen.blit(scaled_sprite, (horizontal, vertical-height+1))


class Player():
    def __init__(self):
        self.x = 0
        self.y = 300
        self.z = 0
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

if __name__ == "__main__":
    pg.init()
    asyncio.run(main())
    pg.quit()