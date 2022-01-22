import pygame
import os
import sys
import random

pygame.init()
size = width, height = 1150, 700
screen = pygame.display.set_mode(size)
all_sprites = pygame.sprite.LayeredUpdates()
buttons_group = pygame.sprite.Group()


def monitor_text(text, y, scale=40):
    return [pygame.font.Font(None, scale).render(f'{text}', True, (1, 1, 1)), (70, y)]


def load_image(name, colorkey=None):
    fullname = os.path.join('img', name)
    if not os.path.isfile(fullname):
        print(f'Файл {name} не существует')
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


# Background
balka = pygame.transform.scale(load_image('bg_balka.png'), (194, 702))
floor = pygame.transform.scale(load_image('bg_door.png'), (1000, 712))


class Button(pygame.sprite.Sprite):
    def __init__(self, img, x, y, width, height):
        super(Button, self).__init__(all_sprites, buttons_group)
        self.img = pygame.transform.scale(load_image(img), (width, height))
        self.image = self.img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.float_y = self.rect.y

    def rotate_180_vertical(self):
        self.image = pygame.transform.rotate(self.img, 180)

    def clicked(self, pos):
        return self.rect.collidepoint(pos)


class Conveyor(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y + 130)
        self.level = 1
        self.conv_speed = {'1': 5, '2': 10, '3': 15}

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self, *args, **kwargs):
        self.cur_frame = (self.cur_frame + self.conv_speed[str(self.level)] / FPS)
        self.image = self.frames[round(self.cur_frame) % len(self.frames)]


class Monitor(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('sprite_monitor.png'), (1150, 700))

    def __init__(self, *groups):
        super(Monitor, self).__init__(*groups)
        self.image = Monitor.image.copy()
        self.kilograms = 0
        self.max_kilograms = 100
        self.money_business = 1000
        self.price_of_kilogram = 20
        self.sale_price = 22
        proc = self.kilograms / (self.max_kilograms / 255)
        self.color_metal = (255, 255 - proc, 255 - proc)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = -405
        self.float_y = self.rect.y
        self.is_open = [0, False]
        self.btn_arrow = Button('btn_arrow.png', 175, 0, 100, 100)
        self.btn_send_metal = None
        self.update_values()

    def add_counter(self):
        if self.money_business >= self.price_of_kilogram:
            self.kilograms += 1
            self.money_business -= self.price_of_kilogram
            self.update_values()
        if not self.btn_send_metal and\
                self.money_business < self.price_of_kilogram or monitor.kilograms == monitor.max_kilograms:
            self.btn_send_metal = Button('btn_send.png', 428, 150, 100, 100)
            all_sprites.move_to_front(self.btn_send_metal)

    def connect(self, pos):
        if self.btn_arrow.clicked(pos):
            self.lowering()
        if self.money_business < self.price_of_kilogram or self.kilograms == self.max_kilograms:
            if self.btn_send_metal.clicked(pos):
                self.money_business += self.kilograms * self.sale_price
                self.kilograms = 0
                self.update_values()
                self.btn_send_metal.kill()
                self.btn_send_metal = None

    def lowering(self):
        if not self.is_open[1]:
            self.btn_arrow.rotate_180_vertical()
            self.is_open[0] = FPS * 0.5
        else:
            self.btn_arrow.image = monitor.btn_arrow.img
            self.is_open[0] = FPS * -0.5
        self.is_open[1] = not self.is_open[1]

    def update(self, *args, **kwargs):
        if self.is_open[0] > 0:
            self.btn_arrow.float_y += 402 / FPS * 2
            self.float_y += 405 / FPS * 2
            if self.btn_arrow.float_y > 402:
                self.btn_arrow.float_y = 402
                self.float_y = 0
                self.is_open[0] = 0
            self.is_open[0] -= 1
        elif self.is_open[0] < 0:
            self.is_open[0] += 1
            self.btn_arrow.float_y -= 402 / FPS * 2
            self.float_y -= 405 / FPS * 2
            if self.btn_arrow.float_y < 0:
                self.btn_arrow.float_y = 0
                self.float_y = -405
                self.is_open[0] = 0
        self.btn_arrow.rect.y = round(self.btn_arrow.float_y)
        self.rect.y = round(self.float_y)

    def update_values(self):
        proc = self.kilograms / (self.max_kilograms / 255)
        self.color_metal = (255, 255 - proc, 255 - proc)
        self.image = pygame.surface.Surface((1150, 700), pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, self.color_metal, (53, 30, 358, 188))
        pygame.draw.rect(self.image, (124, 252, 0), (53, 192, 358, 70))
        pygame.draw.rect(self.image, (135, 206, 250), (53, 262, 358, 130))
        self.image.blit(Monitor.image, (0, 0))
        texts = [monitor_text('Накоплено металла:', 60),
                 monitor_text(self.kilograms, 90),
                 monitor_text('Максимальное кол-во металла:', 130, 30),
                 monitor_text(self.max_kilograms, 160, 30),
                 monitor_text('Деньги бизнеса:', 200),
                 monitor_text(self.money_business, 230),
                 monitor_text(f'Цена за килограмм: {self.price_of_kilogram}', 280, 30),
                 monitor_text(f'Цена за продажу металла: {self.sale_price}', 340, 30)]
        for text in texts:
            self.image.blit(*text)


class Worker(pygame.sprite.Sprite):
    image_plus = pygame.transform.scale(load_image('sprite_plus.png'), (200, 203))
    image_scales = pygame.transform.scale(load_image('sprite_scales.png'), (190, 217))
    image_worker2 = pygame.transform.scale(load_image('sprite_man_blue.png'), (190, 260))
    image_worker3 = pygame.transform.scale(load_image('sprite_man_green.png'), (190, 260))
    image_worker4 = pygame.transform.scale(load_image('sprite_man_red.png'), (190, 260))
    levels = [image_worker2, image_worker3, image_worker4]

    def __init__(self, y, *groups):
        super(Worker, self).__init__(*groups)
        self.image = Worker.image_plus.copy()
        self.rect = self.image.get_rect()
        self.rect.x = 820
        self.rect.y = y
        self.btn_upgrade = None
        self.btn_conv_upgrade = None
        self.conv = None
        self.counter = 0
        self.level = 0
        self.speeds = {'2': 3, '3': 2.5, '4': 2, '5': 1, '6': 0.7, '7': 0.45}

    def connect(self, pos):
        if self.level:
            if self.btn_upgrade.clicked(pos):
                self.upgrade()
            if self.btn_conv_upgrade.clicked(pos):
                self.conveyor_work()

    def upgrade(self):
        if self.level > 3:
            return
        self.level += 1
        self.image = pygame.surface.Surface((850, 500), pygame.SRCALPHA, 32)
        self.image.blit(Worker.levels[self.level - 2], (-15, -3))
        self.image.blit(Worker.image_scales, (0, 20))
        if self.level > 3:
            self.btn_upgrade.kill()

    def conveyor_work(self):
        if not self.conv:
            self.conv = Conveyor(load_image("sprite_conveyor_belt_animation.png"),
                                 5, 1, 0, self.rect.y)
            self.btn_conv_upgrade.image = pygame.transform.scale(load_image('btn_upgrade_arrow.png'),
                                                                 (80, 80))
            all_sprites.move_to_front(monitor)
            all_sprites.move_to_front(monitor.btn_arrow)
        else:
            if self.conv.level < 3:
                self.conv.level += 1
            else:
                self.btn_conv_upgrade.kill()

    def update(self, *args, **kwargs):
        if args and self.rect.collidepoint(args[0].pos):
            if not self.level:
                self.rect.y -= 20
                self.image = pygame.surface.Surface((850, 500), pygame.SRCALPHA, 32)
                self.image.blit(Worker.image_scales, (0, 20))
                self.btn_upgrade = Button('btn_upgrade_arrow.png', 735, self.rect.y + 55, 80, 80)
                self.level += 1
                self.btn_conv_upgrade = Button('btn_upgrade_plus.png', 565, self.rect.y + 55, 80, 80)
                return
            if monitor.kilograms < monitor.max_kilograms:
                monitor.add_counter()
        if monitor.kilograms < monitor.max_kilograms:
            if self.level >= 2:
                self.counter += 1
                if self.conv:
                    speed = self.speeds[str(self.level + self.conv.level)] * FPS
                else:
                    speed = self.speeds[str(self.level)] * FPS
                if self.counter >= speed:
                    self.counter = 0
                    monitor.add_counter()


if __name__ == '__main__':
    FPS = 60
    clock = pygame.time.Clock()
    pygame.display.set_caption('Metal Clicker')

    worker1 = Worker(15, all_sprites)
    worker2 = Worker(245, all_sprites)
    worker3 = Worker(475, all_sprites)
    monitor = Monitor(all_sprites)
    running = True
    while running:
        screen.fill((200, 195, 184))
        screen.blit(floor, (-6, -7))
        screen.blit(balka, (600, -2))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    monitor.connect(event.pos)
                    worker1.connect(event.pos)
                    worker2.connect(event.pos)
                    worker3.connect(event.pos)
                    all_sprites.update(event)
        all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()