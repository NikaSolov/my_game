from pygame import *
import random
import uuid

font.init()
mixer.init()

width, height = 800, 600
window = display.set_mode((width, height))
display.set_caption("Пригоди гнома")
display.set_icon(image.load("images/icon.jpg"))
clock = time.Clock()
cadrs = 40

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, width, height):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, width, height):
        super().__init__(player_image, player_x, player_y, width, height)
        self.x_move = 0
        self.lives = 3
        self.dead = False
        self.poza_1_image = self.image
        self.poza_2_image = transform.scale(image.load("images/gnom/poza 3.png"), (width, height))
        self.poza_3_image = transform.scale(image.load("images/gnom/poza 3.png"), (width, height))
        self.hit_pouse = 0

    def update(self):
        if not self.dead:
            self.rect.x += self.x_move
            self.rect.x = max(0, min(self.rect.x, width - self.rect.width))
        if self.hit_pouse > 0:
            self.hit_pouse -= 1
            if self.hit_pouse == 0 and not self.dead:
                self.image = self.poza_1_image

    def got_hit(self):
        if self.hit_pouse == 0 and not self.dead:
            self.hit_pouse = cadrs
            self.image = self.poza_2_image
            self.lives -= 1
            if self.lives == 0:
                self.dead = True
                self.image = self.poza_3_image
            return True
        return False

class Enemy(GameSprite):
    def __init__(self, image_path, speed):
        x = random.randint(0, width - 50)
        y = random.randint(-150, -50)
        super().__init__(image_path, x, y, 50, 50)
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > height:
            self.rect.y = random.randint(-150, -50)
            self.rect.x = random.randint(0, width - 50)

class Count(GameSprite):
    def __init__(self, player_image, speed):
        player_x = random.randint(0, width - 40)
        player_y = random.randint(-300, -100)
        super().__init__(player_image, player_x, player_y, 40, 40)
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > height:
            self.rect.y = random.randint(-300, -100)
            self.rect.x = random.randint(0, width - 40)

class Button:
    def __init__(self, player_image, player_x, player_y, width, height):
        self.sprite = GameSprite(player_image, player_x, player_y, width, height)

    def draw(self):
        self.sprite.draw()

    def click(self, mouse_poza):
        return self.sprite.rect.collidepoint(mouse_poza)

MENU = "Menu"
LEVEL1 = "Level 1"
LEVEL2 = "Level 2"
WIN = "Win"
LOSE = "Lose"

back_menu = transform.scale(image.load("images/fon.jpg"), (width, height))
back_lvl1 = transform.scale(image.load("images/fon_lvl1.jpg"), (width, height))
back_lvl2 = transform.scale(image.load("images/fon_lvl2.jpg"), (width, height))

heart_image = transform.scale(image.load("images/heart.png"), (40, 30))

player = Player("images/gnom/poza 1.png", 10, height - 150, 120, 120)

stones = sprite.Group()
for p in range(5):
    stones.add(Enemy("images/stone.png", random.randint(1, 2)))

arrow = sprite.Group()
for v in range(5):
    arrow.add(Enemy("images/arrow.png", random.randint(1, 2)))

crystals = sprite.Group()
for q in range(2):
    crystals.add(Count("images/crystal.png", random.randint(3, 4)))

coins = sprite.Group()
for a in range(2):
    coins.add(Count("images/coins.png", random.randint(3, 4)))

button_start = Button("images/start.png", 300, 300, 200, 200)
button_next = Button("images/start.png", 300, 350, 200, 200)
button_restart = Button("images/restart.png", 250, 300, 300, 120)
button_music = Button("images/music.png", 10, 10, 100, 100)

collected = 0
target_lvl1 = 10
target_lvl2 = 15

music_on = False

current_level = LEVEL1

game_state = MENU

def load_music(track):
    mixer.music.load(track)
    mixer.music.play(-1)

run = True

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_LEFT:
                player.x_move = -10
            elif e.key == K_RIGHT:
                player.x_move = 10
        elif e.type == KEYUP:
            if e.key in [K_LEFT, K_RIGHT]:
                player.x_move = 0
        elif e.type == MOUSEBUTTONDOWN and e.button == 1:
            mouse_pos = e.pos
            if game_state == MENU and button_start.click(mouse_pos):
                game_state = LEVEL1
                current_level = LEVEL1
                player.dead = False
                player.lives = 3
                collected = 0
                for s in stones:
                    s.rect.y = random.randint(-150, -50)
                    s.rect.x = random.randint(0, width - 50)
                for c in crystals:
                    c.rect.y = random.randint(-300, -100)
                    c.rect.x = random.randint(0, width - 40)
                if music_on:
                    load_music("sounds/music_lvl1.ogg")
            elif game_state == MENU and button_music.click(mouse_pos):
                music_on = not music_on
                if music_on:
                    load_music("sounds/music_menu.ogg")
                else:
                    mixer.music.stop()
            elif game_state == WIN and button_next.click(mouse_pos) and current_level == LEVEL1:
                game_state = LEVEL2
                current_level = LEVEL2
                player.dead = False
                player.lives = 3
                collected = 0
                for s in stones:
                    s.rect.y = random.randint(-150, -50)
                    s.rect.x = random.randint(0, width - 50)
                for c in crystals:
                    c.rect.y = random.randint(-300, -100)
                    c.rect.x = random.randint(0, width - 40)
                if music_on:
                    load_music("sounds/music_lvl2.ogg")
            elif game_state == WIN and current_level == LEVEL2 and button_next.click(mouse_pos):
                game_state = MENU
                if music_on:
                    load_music("sounds/music_menu.ogg")
            elif game_state == LOSE and button_restart.click(mouse_pos):
                game_state = LEVEL1
                current_level = LEVEL1
                player.dead = False
                player.lives = 3
                collected = 0
                for s in stones:
                    s.rect.y = random.randint(-150, -50)
                    s.rect.x = random.randint(0, width - 50)
                for c in crystals:
                    c.rect.y = random.randint(-300, -100)
                    c.rect.x = random.randint(0, width - 40)
                for a in arrow:
                    a.rect.y = random.randint(-150, -50)
                    a.rect.x = random.randint(0, width - 50)
                for c in coins:
                    c.rect.y = random.randint(-300, -100)
                    c.rect.x = random.randint(0, width - 40)
                if music_on:
                    load_music("sounds/music_lvl1.ogg")

    window.fill((50, 100, 200))

    if game_state == MENU:
        window.blit(back_menu, (0, 0))
        button_start.draw()
        button_music.draw()
    elif game_state == LEVEL1:
        window.blit(back_lvl1, (0, 0))
        player.update()
        player.draw()

        stones.update()
        stones.draw(window)

        crystals.update()
        crystals.draw(window)

        for s in stones:
            if s.rect.colliderect(player.rect):
                if player.got_hit():
                    break

        for c in crystals:
            if c.rect.colliderect(player.rect):
                collected += 1
                c.rect.y = random.randint(-300, -100)
                c.rect.x = random.randint(0, width - 40)

        for i in range(player.lives):
            window.blit(heart_image, (10 + i * 40, 10))

        font1 = font.SysFont("Arial", 30)
        text = font1.render("Coins: " + str(collected) + "/10", True, (255, 255, 255))
        window.blit(text, (width - 200, 10))

        if player.dead:
            game_state = LOSE
        elif collected >= target_lvl1:
            game_state = WIN

    elif game_state == WIN:
        window.blit(back_menu, (0, 0))
        font1 = font.SysFont("Arial", 60)
        text = font1.render("YOU WIN!", True, (255, 255, 0))
        window.blit(text, (250, 200))
        if current_level == LEVEL1:
            button_next.draw()
        else:
            button_next.draw()  # Відображаємо кнопку "Menu" для LEVEL2
    elif game_state == LOSE:
        window.blit(back_menu, (0, 0))
        font1 = font.SysFont("Arial", 60)
        text = font1.render("YOU LOSE!", True, (255, 0, 0))
        window.blit(text, (250, 200))
        button_restart.draw()
    elif game_state == LEVEL2:
        window.blit(back_lvl2, (0, 0))
        player.update()
        player.draw()

        arrow.update()
        arrow.draw(window)

        coins.update()
        coins.draw(window)

        for s in arrow:
            if s.rect.colliderect(player.rect):
                if player.got_hit():
                    break

        for c in coins:
            if c.rect.colliderect(player.rect):
                collected += 1
                c.rect.y = random.randint(-300, -100)
                c.rect.x = random.randint(0, width - 40)

        for i in range(player.lives):
            window.blit(heart_image, (10 + i * 40, 10))

        font1 = font.SysFont("Arial", 30)
        text = font1.render("Coins: " + str(collected) + "/15", True, (255, 255, 255))
        window.blit(text, (width - 200, 10))

        if player.dead:
            game_state = LOSE
        elif collected >= target_lvl2:
            game_state = WIN

    display.update()
    clock.tick(60)