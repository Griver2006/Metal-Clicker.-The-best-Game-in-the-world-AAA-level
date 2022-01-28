import pygame
import os
import sys

from settings import all_sprites, buttons_group


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


class Button(pygame.sprite.Sprite):
    def __init__(self, img, x, y, width, height, hint_text=''):
        super(Button, self).__init__(all_sprites, buttons_group)
        all_sprites.change_layer(self, 2)
        self.img = pygame.transform.scale(load_image(img), (width, height))
        self.image = self.img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.float_y = self.rect.y
        self.hint_text = hint_text
        self.hint = None

    def show_hint(self, pos):
        if self.hint_text:
            if self.hint:
                self.hint.kill()
                self.hint = None
            if self.rect.collidepoint(pos):
                self.hint = Hint(self.hint_text,
                                 pos[0], pos[1])

    def rotate_180_vertical(self):
        self.image = pygame.transform.rotate(self.img, 180)

    def clicked(self, pos):
        return self.rect.collidepoint(pos)


class Hint(pygame.sprite.Sprite):
    def __init__(self, text, x, y):
        super(Hint, self).__init__(all_sprites)
        all_sprites.change_layer(self, 8)
        self.text = pygame.font.Font(None, 40).render(f'{text}', True, (200, 200, 200))
        self.image = pygame.surface.Surface(self.text.get_size(), pygame.SRCALPHA, 32)
        self.image.fill((55, 55, 55))
        self.image.blit(self.text, (0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x - 50
        self.rect.y = y - 50