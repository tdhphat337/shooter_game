try:
    import pygame
    import os
    import time
    import random
    pygame.font.init()
    pygame.mixer.init()

    WIDTH, HEIGHT = 750, 750
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Phát comeback kaka")

    # Load images
    RED_SPACE_SHIP = pygame.image.load(os.path.join( "pixel_ship_red_small.png"))
    GREEN_SPACE_SHIP = pygame.image.load(os.path.join( "pixel_ship_green_small.png"))
    BLUE_SPACE_SHIP = pygame.image.load(os.path.join( "pixel_ship_blue_small.png"))

    # Player player
    YELLOW_SPACE_SHIP = pygame.image.load(os.path.join( "main.png"))
    RED2_SPACE_SHIP = pygame.image.load(os.path.join( "main2.png"))
    #init the music
    pygame.mixer.music.load("nhacnen.mp3")
    pygame.mixer.music.play(-1)
    # Lasers
    RED_LASER = pygame.image.load(os.path.join( "pixel_laser_red.png"))
    GREEN_LASER = pygame.image.load(os.path.join( "pixel_laser_green.png"))
    BLUE_LASER = pygame.image.load(os.path.join( "pixel_laser_blue.png"))
    YELLOW_LASER = pygame.image.load(os.path.join( "pixel_laser_yellow.png"))
    RED2_LASER = pygame.image.load(os.path.join( "pixel_laser_red.png"))
    YELLOW2_LASER = pygame.image.load(os.path.join( "pixel_laser_yellow.png"))
    # Background
    BG = pygame.transform.scale(pygame.image.load(os.path.join( "space.png")), (WIDTH, HEIGHT))
    BG2 = pygame.transform.scale(pygame.image.load(os.path.join( "images.png")), (WIDTH, HEIGHT))

    class Laser:
        def __init__(self, x, y, img):
            self.x = x
            self.y = y
            self.img = img
            self.mask = pygame.mask.from_surface(self.img)

        def draw(self, window):window.blit(self.img, (self.x, self.y))
        def move(self,vel):self.y += vel
        def off_screen(self, height):return not(self.y <= height and self.y >= 0)
        def collision(self, obj):return collide(self, obj)
    class Ship:
        COOLDOWN = 30
        def __init__(self, x, y, health=100):
            self.x = x
            self.y = y
            self.health = health
            self.ship_img = None
            self.laser_img = None
            self.lasers = []
            self.cool_down_counter = 0

        def draw(self, window):
            window.blit(self.ship_img, (self.x, self.y))
            for laser in self.lasers:laser.draw(window)
        def move_lasers(self, vel, obj):
            self.cooldown()
            for laser in self.lasers:
                laser.move(vel)
                if laser.off_screen(HEIGHT):
                    self.lasers.remove(laser)
                elif laser.collision(obj):
                    obj.health -= 10
                    self.lasers.remove(laser)
        def cooldown(self):
            if self.cool_down_counter >= self.COOLDOWN:self.cool_down_counter = 0
            elif self.cool_down_counter > 0:self.cool_down_counter += 1
        def shoot(self):
            if self.cool_down_counter == 0:
                laser = Laser(self.x, self.y, self.laser_img)
                self.lasers.append(laser)
                self.cool_down_counter = 1
        def get_width(self):return self.ship_img.get_width()
        def get_height(self):return self.ship_img.get_height()

    class Player(Ship):
        def __init__(self, x, y, health=100):
            super().__init__(x, y, health)
            self.ship_img = YELLOW_SPACE_SHIP
            self.laser_img = YELLOW2_LASER
            self.mask = pygame.mask.from_surface(self.ship_img)
            self.max_health = health
        def move_lasers(self, vel, objs):
            self.cooldown()
            for laser in self.lasers:
                laser.move(vel)
                if laser.off_screen(HEIGHT):
                    self.lasers.remove(laser)
                else:
                    for obj in objs:
                        if laser.collision(obj):
                            objs.remove(obj)
                            if laser in self.lasers:
                                self.lasers.remove(laser)
        def draw(self, window):
            super().draw(window)
            self.healthbar(window)
        def healthbar(self, window):
            pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
            pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10))
    class Player2(Ship):
        def __init__(self, x, y, health=100):
            super().__init__(x, y, health)
            self.ship_img = RED2_SPACE_SHIP
            self.laser_img = RED2_LASER
            self.mask = pygame.mask.from_surface(self.ship_img)
            self.max_health = health
        def move_lasers(self, vel, objs):
            self.cooldown()
            for laser in self.lasers:
                laser.move(vel)
                if laser.off_screen(HEIGHT):
                    self.lasers.remove(laser)
                else:
                    for obj in objs:
                        if laser.collision(obj):
                            objs.remove(obj)
                            if laser in self.lasers:
                                self.lasers.remove(laser)
        def draw(self, window):
            super().draw(window)
            self.healthbar(window)
        def healthbar(self, window):
            pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
            pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10))
    class Enemy(Ship):
        COLOR_MAP = {
                    "red": (RED_SPACE_SHIP, RED_LASER),
                    "green": (GREEN_SPACE_SHIP, GREEN_LASER),
                    "blue": (BLUE_SPACE_SHIP, BLUE_LASER)
                    }
        def __init__(self, x, y, color, health=100):
            super().__init__(x, y, health)
            self.ship_img, self.laser_img = self.COLOR_MAP[color]
            self.mask = pygame.mask.from_surface(self.ship_img)
        def move(self, vel):self.y += vel
        def shoot(self):
            if self.cool_down_counter == 0:
                laser = Laser(self.x-20, self.y, self.laser_img)
                self.lasers.append(laser)
                self.cool_down_counter = 1
    def collide(obj1, obj2):
        offset_x = obj2.x - obj1.x
        offset_y = obj2.y - obj1.y
        return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None
    def main():
        run = True
        FPS = 60
        level = 0
        lives = 20
        main_font = pygame.font.SysFont("comicsans", 50)
        lost_font = pygame.font.SysFont("comicsans", 60)

        enemies = []
        wave_length = 5
        enemy_vel = 1
        laser_vel_enemy=2

        player_vel = 6
        laser_vel = 10

        player = Player(200, 630)
        player2 = Player2(400, 630)
        clock = pygame.time.Clock()
        lost = False
        lost_count = 0

        def redraw_window():
            WIN.blit(BG, (0,0))
            # draw text
            lives_label = main_font.render(f"Lives: {lives}", 1, (255,255,255))
            level_label = main_font.render(f"Level: {level}", 1, (255,255,255))
            WIN.blit(lives_label, (10, 10))
            WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))
            for enemy in enemies: enemy.draw(WIN)
            player.draw(WIN)
            player2.draw(WIN)
            if lost:
                lost_label = lost_font.render("You Lost!!", 1, (255,255,255))
                WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))
            pygame.display.update()
        while run:
            clock.tick(FPS)
            redraw_window()
            if lives <= 0 or player.health <= 0 or player2.health <= 0:
                lost = True
                lost_count += 1
            if lost:
                if lost_count > FPS * 3:
                    run = False
                else:continue
            if len(enemies) == 0:
                level += 1
                wave_length += 5
                laser_vel_enemy+=1
                for i in range(wave_length):
                    enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), random.choice(["red", "blue", "green"]))
                    enemies.append(enemy)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:quit()
            keys = pygame.key.get_pressed()
            #xử lý sự kiện cho người chơi 1
            if keys[pygame.K_a] and player.x - player_vel > 0: player.x -= player_vel# left
            if keys[pygame.K_a] and player.x - player_vel > 0: player.x -= 0
            if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH: player.x += player_vel# right
            if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH: player.x += 0
            if keys[pygame.K_w] and player.y - player_vel > 0: player.y -= player_vel# up
            if keys[pygame.K_w] and player.y - player_vel > 0: player.y -= 0
            if keys[pygame.K_s] and player.y + player_vel + player.get_height() + 15 < HEIGHT: player.y += player_vel# down
            if keys[pygame.K_s] and player.y + player_vel + player.get_height() + 15 < HEIGHT: player.y += 0
                
            if keys[pygame.K_SPACE]:
                laser_sound = pygame.mixer.Sound("laser.mp3") # Thay đổi đường dẫn tới file âm thanh của bạn
                laser_sound.play()
                player.shoot()
            #xử lý sự kiện cho người chơi 2
            if keys[pygame.K_LEFT] and player2.x - player_vel > 0: player2.x -= player_vel# left
            if keys[pygame.K_LEFT] and player2.x - player_vel > 0: player2.x -= 0
            if keys[pygame.K_RIGHT] and player2.x + player_vel + player.get_width() < WIDTH: player2.x += player_vel# right
            if keys[pygame.K_RIGHT] and player2.x + player_vel + player.get_width() < WIDTH: player2.x += 0
            if keys[pygame.K_UP] and player2.y - player_vel > 0: player2.y -= player_vel# up
            if keys[pygame.K_UP] and player2.y - player_vel > 0: player2.y -= 0
            if keys[pygame.K_DOWN] and player2.y + player_vel + player.get_height() + 15 < HEIGHT: player2.y += player_vel# down
            if keys[pygame.K_DOWN] and player2.y + player_vel + player.get_height() + 15 < HEIGHT: player2.y += 0
                
            if keys[pygame.K_RCTRL]:
                laser_sound = pygame.mixer.Sound("laser.mp3") # Thay đổi đường dẫn tới file âm thanh của bạn
                laser_sound.play()
                player2.shoot()
            # kiểm tra sự va chạm giữa player1 và enemy
            for enemy in enemies[:]:
                enemy.move(enemy_vel)
                enemy.move_lasers(laser_vel_enemy, player)
                if random.randrange(0, 2*60) == 1:enemy.shoot()
                if collide(enemy, player):
                    player.health -= 5
                    enemies.remove(enemy)
                elif enemy.y + enemy.get_height() > HEIGHT:
                    lives -= 1
                    enemies.remove(enemy)
            player.move_lasers(-laser_vel, enemies)
            # kiểm tra sự va chạm giữa player2 và enemy
            for enemy in enemies[:]:
                enemy.move(enemy_vel)
                enemy.move_lasers(laser_vel_enemy, player2)
                if random.randrange(0, 2*60) == 1:enemy.shoot()
                if collide(enemy, player2):
                    player2.health -= 5
                    enemies.remove(enemy)
                elif enemy.y + enemy.get_height() > HEIGHT:
                    lives -= 1
                    enemies.remove(enemy)
            player2.move_lasers(-laser_vel, enemies)
    def single_player_game():
        run = True
        FPS = 60
        level = 0
        lives = 20
        main_font = pygame.font.SysFont("comicsans", 50)
        lost_font = pygame.font.SysFont("comicsans", 60)

        enemies = []
        wave_length = 5
        enemy_vel = 1
        laser_vel_enemy=2

        player_vel = 6
        laser_vel = 10

        player = Player(350, 630)
        clock = pygame.time.Clock()
        lost = False
        lost_count = 0

        def redraw_window():
            WIN.blit(BG, (0,0))
            # draw text
            lives_label = main_font.render(f"Lives: {lives}", 1, (255,255,255))
            level_label = main_font.render(f"Level: {level}", 1, (255,255,255))
            WIN.blit(lives_label, (10, 10))
            WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))
            for enemy in enemies: enemy.draw(WIN)
            player.draw(WIN)
            if lost:
                lost_label = lost_font.render("You Lost!!", 1, (255,255,255))
                WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))
            pygame.display.update()
        while run:
            clock.tick(FPS)
            redraw_window()
            if lives <= 0 or player.health <= 0:
                lost = True
                lost_count += 1
            if lost:
                if lost_count > FPS * 3:
                    run = False
                else:continue
            if len(enemies) == 0:
                level += 1
                wave_length += 5
                laser_vel_enemy+=1
                for i in range(wave_length):
                    enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), random.choice(["red", "blue", "green"]))
                    enemies.append(enemy)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:quit()
            keys = pygame.key.get_pressed()
            #xử lý sự kiện cho người chơi 1
            if keys[pygame.K_a] and player.x - player_vel > 0: player.x -= player_vel# left
            if keys[pygame.K_a] and player.x - player_vel > 0: player.x -= 0
            if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH: player.x += player_vel# right
            if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH: player.x += 0
            if keys[pygame.K_w] and player.y - player_vel > 0: player.y -= player_vel# up
            if keys[pygame.K_w] and player.y - player_vel > 0: player.y -= 0
            if keys[pygame.K_s] and player.y + player_vel + player.get_height() + 15 < HEIGHT: player.y += player_vel# down
            if keys[pygame.K_s] and player.y + player_vel + player.get_height() + 15 < HEIGHT: player.y += 0
                
            if keys[pygame.K_SPACE]:
                laser_sound = pygame.mixer.Sound("laser.mp3") # Thay đổi đường dẫn tới file âm thanh của bạn
                laser_sound.play()
                player.shoot()
            # kiểm tra sự va chạm giữa player1 và enemy
            for enemy in enemies[:]:
                enemy.move(enemy_vel)
                enemy.move_lasers(laser_vel_enemy, player)
                if random.randrange(0, 2*60) == 1:enemy.shoot()
                if collide(enemy, player):
                    player.health -= 5
                    enemies.remove(enemy)
                elif enemy.y + enemy.get_height() > HEIGHT:
                    lives -= 1
                    enemies.remove(enemy)
            player.move_lasers(-laser_vel, enemies)
            
    def main_menu():
        title_font = pygame.font.SysFont("comicsans", 30)
        run = True
        while run:
            WIN.blit(BG2, (0,0))
            title_label = title_font.render("Space Invanders ", 1, (255,192,255))
            # draw buttons
            single_button = pygame.draw.rect(WIN, (255,69,0), (150, 400, 150, 100))
            multiplayer_button = pygame.draw.rect(WIN, (255,69,0), (450, 400, 150, 100))
            W_button = pygame.draw.rect(WIN, (255,255,255), (200, 520, 40, 40))
            S_button = pygame.draw.rect(WIN, (255,255,255), (200, 565, 40, 40))
            A_button = pygame.draw.rect(WIN, (255,255,255), (150, 565, 40, 40))
            D_button = pygame.draw.rect(WIN, (255,255,255), (250, 565, 40, 40))
            space_button = pygame.draw.rect(WIN, (255,255,255), (150, 655, 140, 40))
            up_button = pygame.draw.rect(WIN, (255,255,255), (500, 520, 60, 40))
            down_button = pygame.draw.rect(WIN, (255,255,255), (500, 565, 60, 40))
            left_button = pygame.draw.rect(WIN, (255,255,255), (430, 565, 60, 40))
            right_button = pygame.draw.rect(WIN, (255,255,255), (570, 565, 60, 40))
            ctrl_button = pygame.draw.rect(WIN, (255,255,255), (430, 655, 200, 40))
            # draw text on buttons
            font = pygame.font.SysFont("comicsans", 30)
            single_text = font.render("1 PLAYER", 1, (255,192,255))
            multiplayer_text = font.render("2 PLAYER", 1, (255,192,255))
            font2 = pygame.font.SysFont("comicsans", 25)
            W_text = font.render("W",1,(0,0,0))
            S_text = font.render("S",1,(0,0,0))
            A_text = font.render("A",1,(0,0,0))
            D_text = font.render("D",1,(0,0,0))
            space_text = font.render("Space",1,(0,0,0))

            up_text = font2.render("up",1,(0,0,0))
            down_text = font2.render("down",1,(0,0,0))
            left_text = font2.render("left",1,(0,0,0))
            right_text = font2.render("right",1,(0,0,0))
            ctrl_text = font2.render("right ctrl",1,(0,0,0))
            WIN.blit(single_text, (single_button.center[0]-single_text.get_width()//2, single_button.center[1]-single_text.get_height()//2))
            WIN.blit(multiplayer_text, (multiplayer_button.center[0]-multiplayer_text.get_width()//2, multiplayer_button.center[1]-multiplayer_text.get_height()//2))
            WIN.blit(W_text, (205,520))
            WIN.blit(S_text, (205,565))
            WIN.blit(A_text, (155,565))
            WIN.blit(D_text, (255,565))
            WIN.blit(space_text, (180,655))
            WIN.blit(up_text, (515,520))
            WIN.blit(down_text, (500,565))
            WIN.blit(left_text, (440,565))
            WIN.blit(right_text, (575,565))
            WIN.blit(ctrl_text, (480,655))
            WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 50))
            pygame.display.update()
            # event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if single_button.collidepoint(pos):single_player_game()
                    elif multiplayer_button.collidepoint(pos):main()
        pygame.quit()

    main_menu()
except Exception as bug:
    print(bug) 