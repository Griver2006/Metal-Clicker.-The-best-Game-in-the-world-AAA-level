import pygame


class SettingsMonitor:
    def __init__(self):
        self.kilograms = 0
        self.max_kilograms = 100
        self.money_business = 100000
        self.price_of_kilogram = 20
        self.sale_price = 22
        proc = self.kilograms / (self.max_kilograms / 255)
        self.color_metal = (255, 255 - proc, 255 - proc)
        self.is_open = [0, False]
        self.btn_send_metal = None
        self.is_work = True


class SettingsWorker:
    def __init__(self):
        self.btn_upgrade = None
        self.btn_conv_upgrade = None
        self.conv = None
        self.hint = None
        self.counter = 0
        self.level = 0
        self.level_prices = {'1': '1020', '2': '1050', '3': '1150'}
        self.speeds = {'2': 3, '3': 2.5, '4': 2, '5': 1, '6': 0.8, '7': 0.45}


class SettingsConveyor:
    level_prices = {'0': '1100', '1': '1150', '2': '1300', '3': '1350'}

    def __init__(self):
        self.level = 0
        self.conv_speed = {'1': 5, '2': 10, '3': 15}


all_sprites = pygame.sprite.LayeredUpdates()
buttons_group = pygame.sprite.Group()
workers_group = pygame.sprite.Group()