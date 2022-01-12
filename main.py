import pygame
import os
import sys
import random

pygame.init()
size = width, height = 1150, 700
screen = pygame.display.set_mode(size)
all_sprites = pygame.sprite.Group()
go = False


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
balka = pygame.transform.scale(load_image('balka.png'), (194, 702))


class Button(pygame.sprite.Sprite):
    def __init__(self, img, x, y, width, height, *groups):
        super(Button, self).__init__(*groups)
        self.img = pygame.transform.scale(load_image(img), (width, height))
        self.image = self.img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.float_y = self.rect.y

    def rotate_180_vertical(self):
        self.image = pygame.transform.rotate(self.img, 180)


class Door(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('door.png'), (1000, 712))

    def __init__(self, *groups):
        super(Door, self).__init__(*groups)
        self.image = Door.image
        self.rect = self.image.get_rect()
        self.rect.x = -6
        self.rect.y = -7


class Monitor(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('monitor.png'), (1150, 700))

    def __init__(self, *groups):
        super(Monitor, self).__init__(*groups)
        self.image = Monitor.image.copy()
        self.kilograms = 0
        self.max_kilograms = 100
        self.money_business = 530
        self.price_of_kilogram = 20
        self.sale_price = 22
        proc = self.kilograms / (self.max_kilograms / 255)
        self.color_metal = (255, 255 - proc, 255 - proc)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.update_values()

    def add_counter(self):
        if self.money_business >= self.price_of_kilogram:
            self.kilograms += 1
            self.money_business -= self.price_of_kilogram
            self.update_values()

    def lowering(self):
        pass

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
    image_plus = pygame.transform.scale(load_image('plus.png'), (200, 203))
    image_scales = pygame.transform.scale(load_image('scales.png'), (190, 217))
    image_worker = pygame.transform.scale(load_image(random.choice(['man_blue.png', 'man_red.png',
                                                                    'man_green.png'])), (250, 270))

    def __init__(self, *groups, y=10):
        super(Worker, self).__init__(*groups)
        self.image = Worker.image_plus
        self.levels = [self.image_scales]
        self.level = 0
        self.rect = self.image.get_rect()
        self.rect.x = 820
        self.rect.y = y

    def update(self, *args, **kwargs):
        if args and self.rect.collidepoint(args[0].pos):
            if not self.level:
                self.image = self.levels[self.level]
                self.level += 1
                return
            monitor.add_counter()


if __name__ == '__main__':
    FPS = 60
    clock = pygame.time.Clock()
    pygame.display.set_caption('Metal Clicker')
    Door(all_sprites)
    y = 15
    for _ in range(3):
        Worker(all_sprites, y=y)
        y += 230
    monitor = Monitor(all_sprites)
    running = True
    while running:
        screen.fill((200, 195, 184))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                all_sprites.update(event)
        all_sprites.draw(screen)
        screen.blit(balka, (600, -2))
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()