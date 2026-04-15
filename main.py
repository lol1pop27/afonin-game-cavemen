import pygame  # Импорт библиотеки Pygame для создания игр
import random  # Импорт модуля random для генерации случайных чисел
import math  # Импорт модуля math для математических операций

pygame.init()  # Инициализация всех модулей
win = pygame.display.set_mode((800, 600))  # Создание игрового окна 

pygame.display.set_caption("Afonin_game")  # Установка заголовка окна игры

# Загрузка изображений для анимации движения вправо
walk_right = [
    pygame.image.load("img_right/run-cycle-inked2_xcf-Frame_01__100ms___replace_.png"),
    pygame.image.load("img_right/run-cycle-inked2_xcf-Frame_02__100ms___replace_.png"),
    pygame.image.load("img_right/run-cycle-inked2_xcf-Frame_03__100ms___replace_.png"),
    pygame.image.load("img_right/run-cycle-inked2_xcf-Frame_04__100ms___replace_.png"),
    pygame.image.load("img_right/run-cycle-inked2_xcf-Frame_05__100ms___replace_.png"),
    pygame.image.load("img_right/run-cycle-inked2_xcf-Frame_06__100ms___replace_.png"),
    pygame.image.load("img_right/run-cycle-inked2_xcf-Frame_07__100ms___replace_.png"),
    pygame.image.load("img_right/run-cycle-inked2_xcf-Frame_08__100ms___replace_.png"),
    pygame.image.load("img_right/run-cycle-inked2_xcf-Frame_09__100ms___replace_.png"),
    pygame.image.load("img_right/run-cycle-inked2_xcf-Frame_10__100ms___replace_.png"),
    pygame.image.load("img_right/run-cycle-inked2_xcf-Frame_11__100ms___replace_.png"),
    pygame.image.load("img_right/run-cycle-inked2_xcf-Frame_12__100ms___replace_.png"),
]

# Загрузка изображений для анимации движения влево
walk_left = [
    pygame.image.load("img_left/run-cycle-inked2_xcf-Frame_01__1.png"),
    pygame.image.load("img_left/run-cycle-inked2_xcf-Frame_02__1.png"),
    pygame.image.load("img_left/run-cycle-inked2_xcf-Frame_03__1.png"),
    pygame.image.load("img_left/run-cycle-inked2_xcf-Frame_04__1.png"),
    pygame.image.load("img_left/run-cycle-inked2_xcf-Frame_05__1.png"),
    pygame.image.load("img_left/run-cycle-inked2_xcf-Frame_06__1.png"),
    pygame.image.load("img_left/run-cycle-inked2_xcf-Frame_07__1.png"),
    pygame.image.load("img_left/run-cycle-inked2_xcf-Frame_08__1.png"),
    pygame.image.load("img_left/run-cycle-inked2_xcf-Frame_09__1.png"),
    pygame.image.load("img_left/run-cycle-inked2_xcf-Frame_10__1.png"),
    pygame.image.load("img_left/run-cycle-inked2_xcf-Frame_11__1.png"),
    pygame.image.load("img_left/run-cycle-inked2_xcf-Frame_12__1.png"),
]

fon = pygame.image.load("fon.jpg")  # Загрузка фонового изображения
stay = pygame.image.load("stay.png")  # Загрузка изображения персонажа в состоянии покоя

# Загрузка изображения врага 
try:
    enemy_img_right = pygame.image.load("enemy.png")
    enemy_img_left = pygame.transform.flip(enemy_img_right, True, False)
except:
    # Если нет изображения врага, создадим простой красный квадрат
    enemy_img_right = pygame.Surface((40, 40))
    enemy_img_right.fill((255, 0, 0))
    enemy_img_left = pygame.Surface((40, 40))
    enemy_img_left.fill((255, 100, 100))  # Немного другой оттенок для левого врага

# Загрузка изображения снаряда 
try:
    bullet_img = pygame.image.load("bullet.png")
    bullet_img = pygame.transform.scale(bullet_img, (20, 10))
except:
    # Если нет изображения снаряда, создадим простой желтый прямоугольник
    bullet_img = pygame.Surface((20, 10))
    bullet_img.fill((255, 255, 0))

clock = pygame.time.Clock()  # Создание объекта для контроля частоты кадров

# Начальные координаты персонажа
x = 5
y = 400

# Размеры персонажа
widht = 40  # Ширина персонажа 
height = 60  # Высота персонажа
speed = 10  # Скорость перемещения персонажа

isJump = False  # Флаг, указывающий, находится ли персонаж в прыжке
jump_count = 10  # Счетчик для управления высотой прыжка

left = False  # Флаг движения влево
right = False  # Флаг движения вправо
anim_count = 0  # Счетчик кадров анимации
last_move = ("right") # Последнее направление движения 

# Счетчик убийств
kill_count = 0
# Шрифт для отображения счета
font = pygame.font.SysFont('Arial', 30, True)

# Флаг для определения, закончилась ли игра
game_over = False

# Таймер для задержки выстрелов
shoot_cooldown = 0
shoot_delay = 20  # Задержка между выстрелами 

# Класс для создания снарядов
class snaryad:
    def __init__(self, x, y, facing):
        self.x = x  # Координата X снаряда
        self.y = y  # Координата Y снаряда
        self.facing = facing  # Направление движения снаряда (1 - вправо, -1 - влево)
        self.vel = 12 * facing  # Скорость снаряда с учетом направления
        self.img = bullet_img
        if facing == -1:
            self.img = pygame.transform.flip(self.img, True, False)

    def draw(self, win):  # Метод для отрисовки снаряда
        win.blit(self.img, (self.x, self.y))
        
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())

# Класс для создания врагов
class Enemy:
    def __init__(self, player_x, player_y):
        # Спавн врагов только в области от игрока и выше
        min_x = max(0, player_x - 300)  # Левая граница спавна
        max_x = min(800 - 40, player_x + 300)  # Правая граница спавна
        min_y = max(0, player_y - 400)  # Верхняя граница спавна (выше игрока)
        max_y = max(0, player_y - 100)  # Нижняя граница спавна (выше игрока)
        
       
        if min_y >= max_y:
            min_y = 0
            max_y = 100
            
        self.x = random.randint(int(min_x), int(max_x))
        self.y = random.randint(int(min_y), int(max_y))
        
        # Гарантируем, что враг появится выше игрока
        if self.y >= player_y:
            self.y = max(0, player_y - random.randint(50, 200))
            
        self.width = 40  # Ширина врага
        self.height = 40  # Высота врага
        self.speed = random.randint(1, 3)  # Случайная скорость врага
        self.direction = 1  # Направление взгляда (1 - вправо, -1 - влево)
        
    def draw(self, win):
        # Выбираем изображение в зависимости от направления взгляда
        if self.direction == 1:
            win.blit(enemy_img_right, (self.x, self.y))
        else:
            win.blit(enemy_img_left, (self.x, self.y))
        
    def move(self, player_x, player_y):
        # Определяем направление взгляда в сторону игрока
        if player_x > self.x:
            self.direction = 1  # Смотрит вправо
        else:
            self.direction = -1  # Смотрит влево
            
        # Движение к игроку
        dx = player_x - self.x
        dy = player_y - self.y
        dist = max(1, math.sqrt(dx * dx + dy * dy))  # Избегаем деления на ноль
        
        # Нормализуем вектор направления
        self.x += (dx / dist) * self.speed
        self.y += (dy / dist) * self.speed
            
    def check_collision(self, player_x, player_y, player_width, player_height):
        # Проверка столкновения с игроком
        if (player_x < self.x + self.width and
            player_x + player_width > self.x and
            player_y < self.y + self.height and
            player_y + player_height > self.y):
            return True
        return False
            
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

# Функция отрисовки игрового окна
def draw_window():
    global anim_count  # Используем глобальную переменную счетчика анимации
    win.blit(fon, (0, 0))  # Отрисовываем фон в начале координат (0, 0)

    if anim_count + 1 >= 60:  # Если достигнут конец анимации (12 кадров * 5)
        anim_count = 0  # Сбрасываем счетчик анимации

    if left:  # Если персонаж движется влево
        win.blit(walk_left[anim_count // 5], (x, y))  # Отрисовываем соответствующий кадр анимации
        anim_count += 1  # Увеличиваем счетчик анимации
    elif right:  # Если персонаж движется вправо
        win.blit(walk_right[anim_count // 5], (x, y))  # Отрисовываем соответствующий кадр анимации
        anim_count += 1  # Увеличиваем счетчик анимации
    else:  # Если персонаж стоит на месте
        win.blit(stay, (x, y))  # Отрисовываем статичное изображение

    for bullet in bullets:  # Для каждого снаряда в списке
        bullet.draw(win)  # Отрисовываем снаряд
        
    for enemy in enemies:  # Для каждого врага в списке
        enemy.draw(win)  # Отрисовываем врага
        
    # Отображаем счет убийств
    text = font.render(f'Убийств: {kill_count}', True, (255, 255, 255))
    win.blit(text, (10, 10))
    
    # Отображаем перезарядку
    if shoot_cooldown > 0:
        cooldown_text = font.render(f'Перезарядка: {shoot_cooldown//5}', True, (255, 0, 0))
        win.blit(cooldown_text, (10, 50))

    pygame.display.update()  # Обновляем экран (выводим все нарисованное)

# Функция отрисовки экрана Game Over
def draw_game_over():
    win.fill((0, 0, 0))  # Заливаем экран черным цветом
    game_over_text = font.render('GAME OVER', True, (255, 0, 0))
    score_text = font.render(f'Ваш счет: {kill_count}', True, (255, 255, 255))
    restart_text = font.render('Нажмите R для перезапуска', True, (255, 255, 255))
    
    win.blit(game_over_text, (800 // 2 - game_over_text.get_width() // 2, 200))
    win.blit(score_text, (800 // 2 - score_text.get_width() // 2, 250))
    win.blit(restart_text, (800 // 2 - restart_text.get_width() // 2, 300))
    
    pygame.display.update()

# Функция для перезапуска игры
def restart_game():
    global x, y, isJump, jump_count, left, right, anim_count, last_move
    global kill_count, game_over, enemies, bullets, shoot_cooldown
    
    x = 5
    y = 400
    isJump = False
    jump_count = 10
    left = False
    right = False
    anim_count = 0
    last_move = "right"
    kill_count = 0
    game_over = False
    enemies = []
    bullets = []
    shoot_cooldown = 0

run = True  # Флаг работы главного цикла игры
bullets = []  # Список для хранения активных снарядов
enemies = []  # Список для хранения врагов
enemy_spawn_timer = 0  # Таймер для спавна врагов

# Главный игровой цикл
while run:
    clock.tick(30)  # Ограничение частоты кадров до 30 FPS
    
    if game_over:
        draw_game_over()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Перезапуск игры при нажатии R
                    restart_game()
        continue

    # Уменьшаем таймер перезарядки
    if shoot_cooldown > 0:
        shoot_cooldown -= 1

    for event in pygame.event.get():  # Обработка событий
        if event.type == pygame.QUIT:  # Если событие - закрытие окна
            run = False  # Завершаем игровой цикл

    # Обработка движения снарядов и проверка столкновений с врагами
    for bullet in bullets[:]:  # Для каждого снаряда в списке 
        if 0 < bullet.x < 800:  # Если снаряд в пределах экрана по X
            bullet.x += bullet.vel  # Двигаем снаряд
        else:  # Если снаряд вышел за границы экрана
            bullets.remove(bullet)  # Удаляем снаряд из списка
            continue
            
        # Проверка столкновения снаряда с врагами
        bullet_rect = bullet.get_rect()
        for enemy in enemies[:]:
            enemy_rect = enemy.get_rect()
            if bullet_rect.colliderect(enemy_rect):
                if bullet in bullets:
                    bullets.remove(bullet)
                if enemy in enemies:
                    enemies.remove(enemy)
                kill_count += 1  # Увеличиваем счетчик убийств
                break

    # Спавн врагов
    enemy_spawn_timer += 1
    if enemy_spawn_timer >= 90:  # Спавним врага каждые 3 секунды (90 кадров)
        enemies.append(Enemy(x, y))  # Передаем позицию игрока для спавна врагов выше
        enemy_spawn_timer = 0

    # Движение врагов и проверка столкновений с игроком
    for enemy in enemies:
        enemy.move(x, y)
        if enemy.check_collision(x, y, widht, height):
            game_over = True

    keys = pygame.key.get_pressed()  # Получаем состояние всех клавиш

    if keys[pygame.K_LCTRL] and shoot_cooldown == 0:  # Если нажата левая клавиша Ctrl и нет перезарядки
        if last_move == "right":  # Если последнее движение было вправо
            facing = 1  # Направление снаряда - вправо
        else:  # Если последнее движение было влево
            facing = -1  # Направление снаряда - влево
        if len(bullets) < 6:  # Если количество снарядов меньше 6
            # Создаем новый снаряд (позиция рассчитывается от персонажа)
            bullets.append(snaryad(round(x + widht // 2), round(y + height // 2), facing,))
            shoot_cooldown = shoot_delay  # Устанавливаем перезарядку

    # Обработка движения персонажа
    if (keys[pygame.K_LEFT] and x > 0):  # Если нажата стрелка влево и персонаж не у левой границы
        x -= speed  # Двигаем персонажа влево
        left = True  # Устанавливаем флаг движения влево
        right = False  # Сбрасываем флаг движения вправо
        last_move = "left"  # Запоминаем последнее направление движения
    elif (keys[pygame.K_RIGHT] and x < 800 - widht - 40):  # Если нажата стрелка вправо и персонаж не у правой границы
        x += speed  # Двигаем персонажа вправо
        left = False  # Сбрасываем флаг движения влево
        right = True  # Устанавливаем флаг движения вправо
        last_move = "right"  # Запоминаем последнее направление движения
    else:  # Если не нажаты клавиши движения
        left = False  # Сбрасываем флаг движения влево
        right = False  # Сбрасываем флаг движения вправо
        anim_count = 0  # Сбрасываем счетчик анимации

    # Обработка прыжка
    if not (isJump):  # Если персонаж не в прыжке
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP]):  # Если нажат пробел или стрелка вверх
            isJump = True  # Устанавливаем флаг прыжка
    else:  # Если персонаж в прыжке
        if jump_count >= -10:  # Пока не завершился прыжок
            if jump_count < 0:  # Если персонаж начал опускаться
                y += (jump_count**2) / 2  # Опускаем персонажа 
            else:  # Если персонаж поднимается
                y -= (jump_count**2) / 2  # Поднимаем персонажа 

            jump_count -= 1  # Уменьшаем счетчик прыжка

        else:  # Если прыжок завершен
            isJump = False  # Сбрасываем флаг прыжка
            jump_count = 10  # Восстанавливаем счетчик прыжка

    draw_window()  # Отрисовываем новое состояние игры

pygame.quit()  # Завершаем работу Pygame при выходе из игры