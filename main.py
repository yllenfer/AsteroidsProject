
import arcade
import math
import random

# These are Global constants to use throughout the game
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

BULLET_RADIUS = 30
BULLET_SPEED = 10
BULLET_LIFE = 60

SHIP_TURN_AMOUNT = 3
SHIP_THRUST_AMOUNT = 0.25
SHIP_RADIUS = 30
SCREEN_TITLE = "ASTEROID"

INITIAL_ROCK_COUNT = 5

BIG_ROCK_SPIN = 1
BIG_ROCK_SPEED = 2
BIG_ROCK_RADIUS = 20

MEDIUM_ROCK_SPIN = -2
MEDIUM_ROCK_RADIUS = 5

SMALL_ROCK_SPIN = 5
SMALL_ROCK_RADIUS = 2


class Point:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0


class Velocity:
    def __init__(self):
        self.dx = 0.0
        self.dy = 0.0


class Flying:
    def __init__(self, img):
        self.center = Point()
        self.velocity = Velocity()
        self.radius = SHIP_RADIUS
        self.alive = True
        self.img = img
        self.texture = arcade.load_texture(self.img)
        self.width = self.texture.width
        self.height = self.texture.height
        self.angle = 0
        self.speed = 0
        self.direction = 1
        self.velocity.dx = math.sin(math.radians(self.direction)) * self.speed
        self.velocity.dy = math.cos(math.radians(self.direction)) * self.speed
        #just added this
        # self.score = 0

    def advance(self):
        self.center.x += self.velocity.dx
        self.center.y += self.velocity.dy
        self.wrapping_is_off_screen()

    def draw(self):
        arcade.draw_texture_rectangle(self.center.x, self.center.y, self.width, self.height, self.texture, self.angle,
                                      255)




    def wrapping_is_off_screen(self):
        if self.center.x > SCREEN_WIDTH:
            self.center.x = 0
        elif self.center.x < 0:
            self.center.x = SCREEN_WIDTH
        elif self.center.y > SCREEN_WIDTH:
            self.center.y = 0
        elif self.center.y < 0:
            self.center.y = SCREEN_WIDTH


class Asteroid(Flying):
    def __init__(self, img):
        super().__init__(img)
        self.radius = BIG_ROCK_RADIUS


class Small(Asteroid):
    def __init__(self):
        super().__init__(":resources:images/space_shooter/meteorGrey_small1.png")
        self.radius = SMALL_ROCK_RADIUS
        self.speed = BIG_ROCK_SPEED

    def break_apart(self, asteroids):
        self.alive = False


    def advance(self):
        super().advance()
        self.angle += SMALL_ROCK_SPIN


class Medium(Asteroid):
    def __init__(self):
        super().__init__(":resources:images/space_shooter/meteorGrey_med1.png")
        self.radius = MEDIUM_ROCK_RADIUS
        self.speed = BIG_ROCK_SPEED
        self.velocity.dx = math.sin(math.radians(self.direction)) * self.speed
        self.velocity.dy = math.cos(math.radians(self.direction)) * self.speed

    def advance(self):
        super().advance()
        self.angle += MEDIUM_ROCK_SPIN

    def break_apart(self, asteroids):
        small1 = Small()
        small1.center.x = self.center.x
        small1.center.y = self.center.y
        small1.velocity.dy = self.velocity.dy + 1.5
        small1.velocity.dx = self.velocity.dx + 1.5

        small2 = Medium()
        small2.center.x = self.center.x
        small2.center.y = self.center.y
        small2.velocity.dy = self.velocity.dy - 1.5
        small2.velocity.dx = self.velocity.dx - 1.5

        asteroids.append(small1)
        asteroids.append(small2)
        self.alive = False






class Large(Asteroid):
    def __init__(self):
        super().__init__(":resources:images/space_shooter/meteorGrey_big1.png")
        self.radius = BIG_ROCK_RADIUS
        self.center.x = random.randint(1, 50)
        self.center.y = random.randint(1, 150)
        self.direction = random.randint(1, 50)
        self.speed = BIG_ROCK_SPEED
        self.velocity.dx = math.cos(math.radians(self.direction)) * self.speed
        self.velocity.dy = math.cos(math.radians(self.direction)) * self.speed



    def break_apart(self, asteroids):
        med1 = Medium()
        med1.center.x = self.center.x
        med1.center.y = self.center.y
        med1.velocity.dy = self.velocity.dy + 2

        med2 = Medium()
        med2.center.x = self.center.x
        med2.center.y = self.center.y
        med2.velocity.dy = self.velocity.dy - 2

        small = Small()
        small.center.x = self.center.x
        small.center.y = self.center.y
        small.velocity.dy = self.velocity.dy + 5

        asteroids.append(med1)
        asteroids.append(med2)
        asteroids.append(small)
        self.alive = False


    def advance(self):
        super().advance()
        self.angle += BIG_ROCK_SPIN




class Bullets(Flying):
    def __init__(self, ship_angle, ship_x, ship_y):
        super().__init__(":resources:images/space_shooter/laserBlue01.png")
        self.radius = BULLET_RADIUS
        self.life = BULLET_LIFE
        self.speed = BULLET_SPEED
        self.angle = ship_angle - 90
        self.center.x = ship_x
        self.center.y = ship_y



    def fire(self):
        self.velocity.dx -= math.sin(math.radians(self.angle + 90)) * BULLET_SPEED
        self.velocity.dy += math.cos(math.radians(self.angle + 90)) * BULLET_SPEED


    def advance(self):
        super().advance()
        self.life -= 1
        if self.life < 1:
            self.alive = False




class Ship(Flying):
    def __init__(self):
        super().__init__(":resources:images/space_shooter/playerShip3_orange.png")
        self.center.x = (SCREEN_WIDTH / 2)
        self.center.y = (SCREEN_HEIGHT / 2)
        self.radius = SHIP_RADIUS

    def left(self):
        self.angle += SHIP_TURN_AMOUNT
        if self.angle >= 360:
            self.angle = 0

    def right(self):
        self.angle -= SHIP_TURN_AMOUNT
        if self.angle < 0:
            self.angle = 360

    def thrust(self):
        self.velocity.dx -= math.cos(math.radians(self.angle)) * SHIP_THRUST_AMOUNT
        self.velocity.dy += math.cos(math.radians(self.angle)) * SHIP_THRUST_AMOUNT

    def slow_down(self):
        self.velocity.dx += math.cos(math.radians(self.angle)) * SHIP_THRUST_AMOUNT
        self.velocity.dy -= math.cos(math.radians(self.angle)) * SHIP_THRUST_AMOUNT


class Game(arcade.Window):


    def __init__(self, width, height, title):

        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.SMOKY_BLACK)

        self.held_keys = set()
        #score
        self.score = 0

        #sound
        self.laser_sound = arcade.load_sound(":resources:sounds/hurt5.wav")
        self.hit_sound1 = arcade.load_sound(":resources:sounds/explosion1.wav")

        #image
        self.smallShip = (":resources:images/space_shooter/playerShip2_orange.png")


        self.asteroids = []
        for asteroid in range(INITIAL_ROCK_COUNT):
            largeAsteroid = Large()
            self.asteroids.append(largeAsteroid)

        self.ship = Ship()
        self.bullets = []


    def on_draw(self):

        arcade.start_render()


        for asteroid in self.asteroids:
            asteroid.draw()

        for bullet in self.bullets:
            bullet.draw()

        self.ship.draw()


        self.draw_score()
        self.draw_game_over()
  #This method is drawing score in window
    def draw_score(self):
        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 70, arcade.color.WHITE, 13)

#This method checks if the ship is alive, and displays a message if not
    def draw_game_over(self):
        if self.ship.alive == False:
            gameOver = f"Game Over"
            arcade.draw_text(gameOver, 100, 150, arcade.color.RED, 100)
            # self.game_over.play()

  #This method removes objects once they are hit
    def removeObjets(self):
        for bullet in self.bullets:
            if not bullet.alive:
                self.bullets.remove(bullet)
        for asteroid in self.asteroids:
            if not asteroid.alive:
                self.asteroids.remove(asteroid)


#this method is in charged of checking if the radius
# of the ship and the radius of the asteroid collides
    def checkCollisions(self):
        for bullet in self.bullets:
            for asteroid in self.asteroids:
                    if bullet.alive and asteroid.alive:
                       distance_x = abs(asteroid.center.x - bullet.center.x)
                       distance_y = abs(asteroid.center.y - bullet.center.y)
                       max_dist = asteroid.radius + bullet.radius
                       if distance_x < max_dist and distance_y < max_dist:
                        asteroid.break_apart(self.asteroids)
                        bullet.alive = False
                        asteroid.alive = False
                        self.score += 1
                        #sounds when the asteroids are being hit
                        self.hit_sound1.play()






        for asteroid in self.asteroids:
            if self.ship.alive and asteroid.alive:
                distance_x = abs(asteroid.center.x - self.ship.center.x)
                distance_y = abs(asteroid.center.y - self.ship.center.y)
                max_dist = asteroid.radius + self.ship.radius
                if distance_x < max_dist and distance_y < max_dist:
                    self.ship.alive = False


    def update(self, delta_time):

        self.check_keys()

        for asteroid in self.asteroids:
            asteroid.advance()

        for bullet in self.bullets:
            bullet.advance()

            self.removeObjets()

            self.checkCollisions()

        self.ship.advance()

    def check_keys(self):

        if arcade.key.LEFT in self.held_keys:
            self.ship.left()

        if arcade.key.RIGHT in self.held_keys:
            self.ship.right()

        if arcade.key.UP in self.held_keys:
            self.ship.thrust()

        if arcade.key.DOWN in self.held_keys:
            self.ship.slow_down()


    def on_key_press(self, key: int, modifiers: int):

        if self.ship.alive:
            self.held_keys.add(key)

            if key == arcade.key.SPACE:


                bullet = Bullets(self.ship.angle, self.ship.center.x, self.ship.center.y)
                self.bullets.append(bullet)
                bullet.fire()
                arcade.play_sound(self.laser_sound)

    def on_key_release(self, key: int, modifiers: int):

        if key in self.held_keys:
            self.held_keys.remove(key)



window = Game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
arcade.run()