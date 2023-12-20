# Подключить нужные модули
from random import randint
import pygame
import pygame_menu
from pygame_menu import themes
import time

# модуль random  содержит функции, которые генерируют случайность
# его функция randint генерирует псевдослучайные целые числа

pygame.init()
win_width = 800
win_height = 600
pygame.display.set_caption("Knight & Princess")
window = pygame.display.set_mode([win_width, win_height])
fl_time = time.clock_gettime(time.CLOCK_PROCESS_CPUTIME_ID)
# во время игры пишем надписи размера 72
font = pygame.font.Font(None, 72)
#Kлассы Font находятся в модуле pygame.font, предназначены для работы со шрифтами и текстом
# #второй аргумент это размер шрифта
def start_the_game():

    """ функция, начинающая игру """

    #глобальные переменные
    global font
    global fl_time
    font_health = pygame.font.Font(None, 36)
    global window
    #во время игры пишем надписи размера 36

    #Глобальные переменные (настройки)
    win_width = 800
    win_height = 600
    left_bound = (
        win_width / 10
    )  # границы, за которые персонаж не выходит (начинает ехать фон)
    right_bound = win_width - 8 * left_bound
    shift = 0
    shift_y = 0
    x_start, y_start = 20, 10

    img_file_back = "cave.png"
    img_file_hero = "m1.png"
    img_file_enemy = "enemy.png"
    img_file_bomb = "bomb.png"
    img_file_princess = "princess.png"
    img_file_snake = "png-transparent-snake-cartoon-green-anaconda-green-snake-animals-grass-green-apple-thumbnail.png"
    img_file_fontan = "door.png"

    FPS = 240
    # ФПС - изображения в секунду, для игр должно быть от 60 и выше

    # цвета:
    C_WHITE = (255, 255, 255)
    C_GREEN = (68, 148, 74)
    C_RED = (255, 0, 0)
    C_BLACK = (0, 0, 0)
    # цвета заданные по RGBA, можно изменить, поменяв цифры
    # НУЖНО ПОМЕНЯТЬ ЦВЕТА НА БОЛЕЕ ПРИЯТНЫЕ
    player_lives = 3

    # Классы
    # Button
    class Button(pygame.sprite.Sprite):
        def __init__(
            self,
            text,
            x,
            y,
            callback,
            width=100,
            height=100,
            color=[230, 230, 230],
        ):
            """
            Класс для кнопок, наследуется от Класса`pygame.sprite.Sprite`; он вызывает кнопки по функциям

            """
            super().__init__()
            self.image = pygame.Surface([width, height])
            self.image.fill(color)
            font_size = min(30, width // len(text))
            myFont = pygame.font.SysFont("Calibri", font_size)
            myText = myFont.render(text, 1, (0, 0, 0))
            self.image.blit(
                myText, (width / 2 - width / 4, height / 2 - height / 4)
            )
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.callback = callback
            self.pressed = False

        def update(self):
            """
            Функция отслеживает состояние кнопки, в соотвествии с положением мыши выполняются соотвествующие функции
            """
            mouse = pygame.mouse.get_pos()
            if (
                self.rect.collidepoint(mouse)
                and pygame.mouse.get_pressed()[0]
                and not self.pressed
            ):
                self.callback()
                self.pressed = True
            elif self.pressed and not (
                self.rect.collidepoint(mouse) or pygame.mouse.get_pressed()[0]
            ):
                self.pressed = False

    # класс для цели (стоит и ничего не делает)
    class FinalSprite(pygame.sprite.Sprite):
        """
        Класс `FinalSprite` наследуется от класса `pygame.sprite.Sprite` и представляет собой спрайт принцессы.
        """

        def __init__(self, player_image, player_x, player_y, player_speed):
            # Вызываем конструктор класса (Sprite):
            pygame.sprite.Sprite.__init__(self)
            # каждый спрайт должен хранить свойство image - изображение
            self.image = pygame.transform.scale(
                pygame.image.load(player_image), (60, 120)
            )
            self.speed = player_speed
            # pygame.transform (модуль) содержит функции для изменения поверхностей
            # scale - изменение размера поверхности до нового расширения
            # load - загружается новое изображение из файла

            # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
            # класс Rect - его экземпляры прямоугольные области
            self.rect = self.image.get_rect()
            self.rect.x = player_x
            self.rect.y = player_y

    class DialogBox(pygame.sprite.Sprite):
        """
        Класс `DialogBox` наследуется от класса `pygame.sprite.Sprite` и представляет собой спрайт диалогового окна
        """
        def __init__(
            self,
            position_lu_corner_x: int,
            position_lu_corner_y: int,
            height: float,
            width: float,
            message: str,
            text_color=pygame.color.Color(C_BLACK),
            bg_color=pygame.color.Color(C_WHITE),
            text_size=15,
        ):
            pygame.sprite.Sprite.__init__(self)

            self.font = pygame.font.SysFont("Arial", text_size)
            self.textSurf = self.font.render(message, True, text_color)
            self.image = pygame.Surface((width, height))
            self.image.fill(bg_color)
            self.image.blit(
                self.textSurf,
                [
                    width / 2 - self.textSurf.get_width() / 2,
                    height / 2 - self.textSurf.get_height() / 2,
                ],
            )

            self.rect = self.image.get_rect()
            self.rect.x = position_lu_corner_x
            self.rect.y = position_lu_corner_y

            self.width = width
            self.height = height
            self.textColor = text_color
            self.textSize = text_size
            self.bgColor = bg_color

        def change_text(self, new_text: str):
            """
            Он принимает новый текст в качестве аргумента и обновляет
            соответствующие атрибуты объекта класса.

            :param new_text:
            :return:
            """
            self.textSurf = self.font.render(new_text, 1, self.textColor)
            self.image = pygame.Surface((self.width, self.height))
            self.image.fill(self.bgColor)
            self.image.blit(
                self.textSurf,
                [
                    self.width / 2 - self.textSurf.get_width() / 2,
                    self.height / 2 - self.textSurf.get_height() / 2,
                ],
            )

    dialogs = pygame.sprite.Group()
    snake_dialog = DialogBox(
        300, 350, 110.0, 150.0, message="Do you like apples?"
    )

    def myFunction():
        """ Удаляет ненужные обьекты, при перемещении к фонтану
        """
        robin.move_to_point(fontan.rect.x, fontan.rect.y, all_sprites, bombs)
        buttons.remove(customButton)
        buttons.remove(customButton1)
        dialogs.remove(snake_dialog)

    def myFunction1():
        """
        Функция удаляет кнопоки и диалоговое оконо из соответствующих списков.

        """
        buttons.remove(customButton)
        buttons.remove(customButton1)
        dialogs.remove(snake_dialog)

    buttons = pygame.sprite.Group()
    customButton = Button("Yes", 30, 30, myFunction, 400, 100)
    customButton1 = Button("No", 30, 140, myFunction1, 400, 100)


    class Hero(pygame.sprite.Sprite):
        """
        Kласс `Hero`, который является наследником класса `pygame.sprite.Sprite`. Класс представляет героя игры.

        """
        def __init__(
            self,
            filename,
            x_speed=0,
            y_speed=0,
            x=x_start,
            y=y_start,
            width=120,
            height=120,
            health=3,
        ):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.transform.scale(
                pygame.image.load(filename), (width, height)
            ).convert_alpha()
            self.rect = self.image.get_rect()
            # ставим персонажа в переданную точку (x, y):
            self.rect.x = x
            self.rect.y = y
            self.health = health
            # создаем свойства, запоминаем переданные значения:
            self.x_speed = x_speed
            self.y_speed = y_speed
            # добавим свойство stands_on - это та платформа, на которой стоит персонаж
            self.stands_on = (
                False  # если ни на какой не стоит, то значение - False
            )

        def gravitate(self):
            self.y_speed += 0.25

        def jump(self, y):
            if self.stands_on:
                self.y_speed = y

        def move(self, *args):
            """перемещаем на общий сдвиг все спрайты (и отдельно бомбы, они ж в другом списке

            :param args: спрайты которые будут перемещены
            :type args: list

            """
            global shift
            # shift -= robin.x_speed
            for sprite_group in args:
                for sprite in sprite_group:
                    # перемещаем на общий сдвиг все спрайты (и отдельно бомбы, они ж в другом списке):
                    sprite.rect.x -= (
                        robin.x_speed
                    )  # сам robin тоже в этом списке, поэтому его перемещение визуально отменится

        def move_to_point(self, new_x, new_y, *args):
            global shift, shift_y
            x_offset = new_x - self.rect.x
            y_offset = new_y - self.rect.y
            # shift += x_offset
            robin.rect.x += x_offset
            robin.rect.y += y_offset

        def update(self):
            """перемещает персонажа, применяя текущую горизонтальную и вертикальную скорость"""
            # сначала движение по горизонтали
            self.rect.x += self.x_speed
            # если зашли за стенку, то встанем вплотную к стене
            platforms_touched = pygame.sprite.spritecollide(
                self, barriers, False
            )

            if (
                self.x_speed > 0
            ):  # идем направо, правый край персонажа - вплотную к левому краю стены
                for p in platforms_touched:
                    self.rect.right = min(
                        self.rect.right, p.rect.left
                    )  # если коснулись сразу нескольких, то правый край - минимальный
                    # из возможных
            elif (
                self.x_speed < 0
            ):  # идем налево, ставим левый край персонажа вплотную к правому краю стены
                for p in platforms_touched:
                    self.rect.left = max(
                        self.rect.left, p.rect.right
                    )  # если коснулись нескольких стен, то левый край - максимальный

            # теперь движение по вертикали
            self.gravitate()
            self.rect.y += self.y_speed
            # если зашли за стенку, то встанем вплотную к стене
            platforms_touched = pygame.sprite.spritecollide(
                self, barriers, False
            )
            if self.y_speed > 0:  # идем вниз
                for p in platforms_touched:
                    self.y_speed = 0
                    # Проверяем, какая из платформ снизу самая высокая, выравниваемся по ней, запоминаем её как свою опору:
                    if p.rect.top < self.rect.bottom:
                        self.rect.bottom = p.rect.top
                        self.stands_on = p
            elif self.y_speed < 0:  # идем вверх
                self.stands_on = (
                    False  # пошли наверх, значит, ни на чем уже не стоим!
                )
                for p in platforms_touched:
                    self.y_speed = 0  # при столкновении со стеной вертикальная скорость гасится
                    self.rect.top = max(self.rect.top, p.rect.bottom)

            # если зашли за стенку, то встанем вплотную к стене
            platforms_touched = pygame.sprite.spritecollide(
                self, wall_play, False
            )
            if self.y_speed > 0:  # идем вниз
                for p in platforms_touched:
                    self.y_speed = 0
                    # Проверяем, какая из платформ снизу самая высокая, выравниваемся по ней, запоминаем её как свою опору:
                    if p.rect.top < self.rect.bottom:
                        self.rect.bottom = p.rect.top
                        self.stands_on = p
            elif self.y_speed < 0:  # идем вверх
                self.stands_on = (
                    False  # пошли наверх, значит, ни на чем уже не стоим!
                )
                for p in platforms_touched:
                    self.y_speed = 0  # при столкновении со стеной вертикальная скорость гасится
                    self.rect.top = max(
                        self.rect.top, p.rect.bottom
                    )  # выравниваем верхний край по нижним краям стенок, на которые наехали

    class Wall(pygame.sprite.Sprite):
        def __init__(self, x=20, y=0, width=120, height=120, color=C_GREEN):
            pygame.sprite.Sprite.__init__(self)
            # картинка - новый прямоугольник нужных размеров:
            self.image = pygame.Surface([width, height])
            self.image.fill(color)

            # создаем свойство rect
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

        def draw(self, surface):
            # calculate health ratio
            ratio = self.hp / self.max_hp
            pygame.draw.rect(surface, "red", (self.x, self.y, self.w, self.h))
            pygame.draw.rect(
                surface, "green", (self.x, self.y, self.w * ratio, self.h)
            )

    class Enemy(pygame.sprite.Sprite):  # враг
        def __init__(
            self, x=20, y=0, filename=img_file_enemy, width=100, height=100
        ):
            pygame.sprite.Sprite.__init__(self)

            self.image = pygame.transform.scale(
                pygame.image.load(filename), (width, height)
            ).convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

        def update(self):
            """перемещает персонажа, применяя текущую горизонтальную и вертикальную скорость"""
            if randint(-5, 5) >= 0:
                self.rect.x += randint(-5, 5)
            else:
                self.rect.y += randint(-1, 1)

    class Fontan(pygame.sprite.Sprite):  # фонтан
        def __init__(
            self, x=20, y=0, filename=img_file_fontan, width=100, height=100
        ):
            pygame.sprite.Sprite.__init__(self)

            self.image = pygame.transform.scale(
                pygame.image.load(filename), (width, height)
            ).convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

    class Wall_Play(pygame.sprite.Sprite):
        def __init__(self, x=20, y=0, width=120, height=120, color=C_GREEN):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface([width, height])
            self.image.fill(color)
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

        def update(self):
            """перемещает персонажа, применяя текущую горизонтальную и вертикальную скорость"""
            self.rect.x += randint(-3, 3)
            self.rect.y += randint(-0, 0)

    class Snake(pygame.sprite.Sprite):
        def __init__(
            self, x=20, y=0, filename=img_file_snake, width=100, height=100
        ):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.transform.scale(
                pygame.image.load(filename), (width, height)
            ).convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

    # Запуск игры

    # функция set caption принимае в качестве параметра строк
    window = pygame.display.set_mode([win_width, win_height])
    # функция set mode принимате в качестве параметра кортеж
    # задаем окно с параметрами
    back = pygame.transform.scale(
        pygame.image.load(img_file_back).convert(), (win_width, win_height)
    )
    # задаем задний фон

    # список всех персонажей игры:
    all_sprites = pygame.sprite.Group()
    # список препятствий:
    barriers = pygame.sprite.Group()
    wall_play = pygame.sprite.Group()
    # список врагов:
    enemies = pygame.sprite.Group()
    # список мин:
    bombs = pygame.sprite.Group()
    snake = pygame.sprite.Group()

    # список фонтанов:
    fontans = pygame.sprite.Group()

    sn = Snake(7700, 260)
    all_sprites.add(sn)
    snake.add(sn)
    # создаем персонажа, добавляем его в список всех спрайтов:
    # создаем стены, добавляем их:
    w = Wall(50, 150, 480, 20)
    barriers.add(w)
    all_sprites.add(w)
    # cамая первая палка на которой стоит герой

    w = Wall(350, 380, 640, 20)
    barriers.add(w)
    all_sprites.add(w)
    w = Wall(-200, 590, 12000, 20)
    barriers.add(w)
    all_sprites.add(w)
    w = Wall(1170, 300, 700, 20)
    barriers.add(w)
    all_sprites.add(w)
    w = Wall(2100, 250, 650, 20)
    barriers.add(w)
    all_sprites.add(w)
    w = Wall(2900, 200, 100, 20)
    barriers.add(w)
    all_sprites.add(w)
    w = Wall(3200, 150, 200, 20)
    barriers.add(w)
    all_sprites.add(w)
    w = Wall(3440, 400, 300, 20)
    barriers.add(w)
    all_sprites.add(w)
    w = Wall(4090, 550, 100, 20)
    barriers.add(w)
    all_sprites.add(w)
    w = Wall(4240, 500, 100, 20)
    barriers.add(w)
    all_sprites.add(w)
    w = Wall(4390, 450, 100, 20)
    barriers.add(w)
    all_sprites.add(w)
    w = Wall(4540, 400, 100, 20)
    barriers.add(w)
    all_sprites.add(w)
    w = Wall(4690, 350, 100, 20)
    barriers.add(w)
    all_sprites.add(w)
    w = Wall(4840, 300, 100, 20)
    barriers.add(w)
    all_sprites.add(w)
    w = Wall(4990, 250, 100, 20)
    barriers.add(w)
    all_sprites.add(w)
    w = Wall(5140, 300, 100, 20)
    barriers.add(w)
    all_sprites.add(w)
    w = Wall(5290, 200, 400, 20)
    barriers.add(w)
    all_sprites.add(w)
    w = Wall(7050, 300, 390, 20)
    barriers.add(w)
    all_sprites.add(w)
    all_sprites.add(w)
    w = Wall(7700, 350, 100, 20)
    barriers.add(w)
    all_sprites.add(w)
    all_sprites.add(w)

    # создаем движущиеся препятсвия
    w_p = Wall_Play(6000, 200, 100, 20)
    wall_play.add(w_p)
    all_sprites.add(w_p)
    w_p = Wall_Play(6150, 200, 100, 20)
    wall_play.add(w_p)
    all_sprites.add(w_p)
    w_p = Wall_Play(6300, 200, 100, 20)
    wall_play.add(w_p)
    all_sprites.add(w_p)
    w_p = Wall_Play(6450, 200, 100, 20)
    wall_play.add(w_p)
    all_sprites.add(w_p)
    w_p = Wall_Play(6600, 200, 100, 20)
    wall_play.add(w_p)
    all_sprites.add(w_p)
    w_p = Wall_Play(6750, 200, 100, 20)
    wall_play.add(w_p)
    all_sprites.add(w_p)
    w_p = Wall_Play(6900, 200, 100, 20)
    wall_play.add(w_p)
    all_sprites.add(w_p)

    # создаем врагов, добавляем их:

    en = Enemy(2010, 480)
    all_sprites.add(en)
    enemies.add(en)

    en = Enemy(2000, 480)
    all_sprites.add(en)
    enemies.add(en)

    en = Enemy(3500, 290)
    all_sprites.add(en)
    enemies.add(en)

    en = Enemy(6000, 480)
    all_sprites.add(en)
    enemies.add(en)

    en = Enemy(6350, 480)
    all_sprites.add(en)
    enemies.add(en)
    en = Enemy(7700, 480)
    all_sprites.add(en)
    enemies.add(en)
    en = Enemy(7500, 480)
    all_sprites.add(en)
    enemies.add(en)

    # создаем мины, добавляем их:
    # в список всех спрайтов бомбы не добавляем, будем рисовать их отдельной командой
    # так легко сможем подрывать бомбы, а также делаем их неподвижными, update() не вызывается

    bomb = Enemy(1100, 520, img_file_bomb, 60, 60)
    bombs.add(bomb)

    bomb = Enemy(2800, 520, img_file_bomb, 60, 60)
    bombs.add(bomb)

    bomb = Enemy(3750, 520, img_file_bomb, 60, 60)
    bombs.add(bomb)
    bomb = Enemy(3800, 520, img_file_bomb, 60, 60)
    bombs.add(bomb)
    bomb = Enemy(3850, 520, img_file_bomb, 60, 60)
    bombs.add(bomb)
    bomb = Enemy(3200, 520, img_file_bomb, 60, 60)
    bombs.add(bomb)
    bomb = Enemy(5160, 240, img_file_bomb, 60, 60)
    bombs.add(bomb)
    bomb = Enemy(8600, 520, img_file_bomb, 60, 60)
    bombs.add(bomb)

    fontan = Fontan(7300, 200)
    fontans.add(fontan)
    all_sprites.add(fontan)
    robin = Hero(img_file_hero)
    all_sprites.add(robin)
    # создаем финальный спрайт, добавляем его:
    pr = FinalSprite(img_file_princess, win_width + 8000, win_height - 150, 0)
    all_sprites.add(pr)

    # Основной цикл игры:
    run = True
    finished = False

    while run:
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    robin.x_speed = -5
                elif event.key == pygame.K_RIGHT:
                    robin.x_speed = 5
                elif event.key == pygame.K_UP:
                    robin.jump(-7)

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    robin.x_speed = 0
                elif event.key == pygame.K_RIGHT:
                    robin.x_speed = 0

        if not finished:
            # Перемещение игровых объектов
            all_sprites.update()
            events = pygame.event.get()
            buttons.update()
            # дальше проверки правил игры
            # проверяем касание с бомбами:
            # pygame.sprite.groupcollide(bombs, all_sprites, True, True)
            # если бомба коснулась спрайта, то она убирается из списка бомб, а спрайт - из all_sprites!
            if pygame.sprite.spritecollide(robin, bombs, False):
                if player_lives > 0 and (
                    abs(
                        time.clock_gettime(time.CLOCK_PROCESS_CPUTIME_ID)
                        - fl_time
                    )
                    > 1
                ):
                    player_lives -= 1
                    fl_time = time.clock_gettime(time.CLOCK_PROCESS_CPUTIME_ID)
                    pygame.sprite.groupcollide(bombs, all_sprites, True, False)

                elif player_lives == 0:
                    robin.kill()
            if pygame.sprite.spritecollide(robin, snake, False):
                dialogs.add(snake_dialog)
                buttons.add(customButton)
                buttons.add(customButton1)

            else:
                dialogs.remove(snake_dialog)
                buttons.remove(customButton)
                buttons.remove(customButton1)
            # проверяем касание героя с врагами:
            if pygame.sprite.spritecollide(robin, enemies, False):
                if player_lives > 0 and (
                    abs(
                        time.clock_gettime(time.CLOCK_PROCESS_CPUTIME_ID)
                        - fl_time
                    )
                    > 1
                ):
                    player_lives -= 1
                    fl_time = time.clock_gettime(time.CLOCK_PROCESS_CPUTIME_ID)

                elif player_lives == 0:
                    robin.kill()

                # метод kill убирает спрайт из всех групп, в которых он числится
            # проверяем границы экрана:
            if (
                robin.rect.x > right_bound
                and robin.x_speed > 0
                or robin.rect.x < left_bound
                and robin.x_speed < 0
            ):  # при выходе влево или вправо переносим изменение в сдвиг экрана
                robin.move(all_sprites, bombs)

            # Отрисовка
            # рисуем фон со сдвигом
            local_shift_x = shift % win_width
            local_shift_y = shift_y % win_height
            # print(f"{local_shift_x=}, {robin.rect.x=}, {fontan.rect.x=}, {fontan.rect.y=}")
            window.blit(back, (local_shift_x, 0))
            if local_shift_x != 0:
                window.blit(back, (local_shift_x - win_width, 0))
            # if local_shift_y != 0:
            #     window.blit(back, (0, local_shift_y - win_height))
            # Отображение количества жизней на экране
            lives_text = font_health.render(
                "Жизни: " + str(player_lives), True, C_WHITE
            )
            window.blit(lives_text, (10, 10))
            # нарисуем все спрайты на экранной поверхности до проверки на выигрыш/проигрыш
            # если в этой итерации цикла игра закончилась, то новый фон отрисуется поверх персонажей
            all_sprites.draw(window)
            # группу бомб рисуем отдельно - так бомба, которая ушла из своей группы, автоматически перестанет быть видимой
            bombs.draw(window)
            # рисуем все окошки диалогов
            dialogs.draw(window)
            buttons.draw(window)

            # проверка на выигрыш и на проигрыш:
            if pygame.sprite.collide_rect(robin, pr):
                finished = True
                window.fill(C_BLACK)
                # пишем текст на экране
                text = font.render("YOU WIN!", 1, C_GREEN)
                window.blit(text, (250, 250))

            # проверка на проигрыш:
            if robin not in all_sprites or robin.rect.top > win_height:
                finished = True
                window.fill(C_BLACK)
                # пишем текст на экране
                text = font.render("GAME OVER", 1, C_RED)
                window.blit(text, (250, 250))

        pygame.display.update()

        # Пауза
        pygame.time.delay(20)


mainmenu = pygame_menu.Menu("Welcome", 600, 400, theme=themes.THEME_SOLARIZED)
mainmenu.add.text_input("Name: ", default="username", maxchar=20)
mainmenu.add.button("Play", start_the_game)
mainmenu.add.button("Quit", pygame_menu.events.EXIT)

mainmenu.mainloop(window)
