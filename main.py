import pygame

from settings import SettingsMonitor, SettingsWorker, SettingsConveyor
from settings import all_sprites, buttons_group, workers_group
from feature import monitor_text, load_image, Button, Hint


pygame.init()
size = width, height = 1150, 700
screen = pygame.display.set_mode(size)

# Background
balka = pygame.transform.scale(load_image('bg_balka.png'), (194, 702))
floor = pygame.transform.scale(load_image('bg_door.png'), (1000, 712))


class Conveyor(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        all_sprites.change_layer(self, 1)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y + 130)
        self.settings = SettingsConveyor()

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self, *args, **kwargs):
        if monitor.settings.is_work:
            self.cur_frame = (self.cur_frame + self.settings.conv_speed[str(self.settings.level)] / FPS)
            self.image = self.frames[round(self.cur_frame) % len(self.frames)]


class Monitor(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('sprite_monitor.png'), (1150, 700))

    def __init__(self, *groups):
        super(Monitor, self).__init__(*groups)
        all_sprites.change_layer(self, 5)
        self.image = Monitor.image.copy()
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = -405
        self.float_y = self.rect.y
        self.btn_upgrade_max = Button('btn_upgrade_arrow.png', 20, 500, 80, 80,
                                      hint_text=f'Увеличить кол-во металла за 5000')
        self.btn_arrow = Button('btn_arrow.png', 175, 0, 100, 100)
        self.btn_stop_work = Button('btn_stop_work.png', 20, 610, 80, 80, hint_text='Остановить работу')
        self.settings = SettingsMonitor()
        self.update_values()

    def add_counter(self):
        if self.settings.money_business >= self.settings.price_of_kilogram:
            self.settings.kilograms += 1
            self.settings.money_business -= self.settings.price_of_kilogram
            self.update_values()
        if not self.settings.btn_send_metal and\
                self.settings.money_business < self.settings.price_of_kilogram\
                or self.settings.kilograms == self.settings.max_kilograms:
            self.settings.btn_send_metal = Button('btn_send.png', 428, 150, 100, 100)

    def connect(self, pos):
        if self.btn_arrow.clicked(pos):
            self.lowering()
        if self.btn_upgrade_max.clicked(pos):
            if self.settings.money_business >= 5000:
                self.settings.max_kilograms += 100
                self.settings.money_business -= 5000
                self.update_values()
        if self.btn_stop_work.clicked(pos):
            if self.settings.is_work:
                self.settings.is_work = False
                self.btn_stop_work.hint_text = 'Продолжить работу'
            else:
                self.settings.is_work = True
                self.btn_stop_work.hint_text = 'Остановить работу'
            self.btn_stop_work.show_hint(pygame.mouse.get_pos())
        if self.settings.money_business < self.settings.price_of_kilogram\
                or self.settings.kilograms == self.settings.max_kilograms:
            if self.settings.btn_send_metal.clicked(pos):
                self.settings.money_business += self.settings.kilograms * self.settings.sale_price
                self.settings.kilograms = 0
                self.update_values()
                self.settings.btn_send_metal.kill()
                self.settings.btn_send_metal = None

    def lowering(self):
        if not self.settings.is_open[1]:
            self.btn_arrow.rotate_180_vertical()
            self.settings.is_open[0] = FPS * 0.5
        else:
            self.btn_arrow.image = monitor.btn_arrow.img
            self.settings.is_open[0] = FPS * -0.5
        self.settings.is_open[1] = not self.settings.is_open[1]

    def update(self, *args, **kwargs):
        # Управление в какую сторону едет монитор:
        if self.settings.is_open[0] > 0:
            self.btn_arrow.float_y += 402 / FPS * 2
            self.float_y += 405 / FPS * 2
            if self.btn_arrow.float_y > 402:
                self.btn_arrow.float_y = 402
                self.float_y = 0
                self.settings.is_open[0] = 0
            self.settings.is_open[0] -= 1
        elif self.settings.is_open[0] < 0:
            self.settings.is_open[0] += 1
            self.btn_arrow.float_y -= 402 / FPS * 2
            self.float_y -= 405 / FPS * 2
            if self.btn_arrow.float_y < 0:
                self.btn_arrow.float_y = 0
                self.float_y = -405
                self.settings.is_open[0] = 0
        self.btn_arrow.rect.y = round(self.btn_arrow.float_y)
        self.rect.y = round(self.float_y)

    def update_values(self):
        proc = self.settings.kilograms / (self.settings.max_kilograms / 255)
        self.settings.color_metal = (255, 255 - proc, 255 - proc)
        self.image = pygame.surface.Surface((1150, 700), pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, self.settings.color_metal, (53, 30, 358, 188))
        pygame.draw.rect(self.image, (124, 252, 0), (53, 192, 358, 70))
        pygame.draw.rect(self.image, (135, 206, 250), (53, 262, 358, 130))
        self.image.blit(Monitor.image, (0, 0))
        texts = [monitor_text('Накоплено металла:', 60),
                 monitor_text(self.settings.kilograms, 90),
                 monitor_text('Максимальное кол-во металла:', 130, 30),
                 monitor_text(self.settings.max_kilograms, 160, 30),
                 monitor_text('Деньги бизнеса:', 200),
                 monitor_text(self.settings.money_business, 230),
                 monitor_text(f'Цена за килограмм: {self.settings.price_of_kilogram}', 280, 30),
                 monitor_text(f'Цена за продажу металла: {self.settings.sale_price}', 340, 30)]
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
        all_sprites.change_layer(self, 1)
        self.image = Worker.image_plus.copy()
        self.rect = self.image.get_rect()
        self.rect.x = 820
        self.rect.y = y
        self.settings = SettingsWorker()

    def connect(self, pos):
        if self.settings.level:
            if self.settings.btn_upgrade.clicked(pos):
                self.upgrade()
            if self.settings.btn_conv_upgrade.clicked(pos):
                self.conveyor_work()

    def show_hint(self, pos):
        if self.settings.level >= 2:
            if self.settings.hint:
                self.settings.hint.kill()
                self.settings.hint = None
            if self.rect.collidepoint(pos):
                if self.settings.conv:
                    speed = round(1 / self.settings.speeds[str(self.settings.level
                                                               + self.settings.conv.settings.level)], 1)
                else:
                    speed = round(1 / self.settings.speeds[str(self.settings.level)], 1)
                self.settings.hint = Hint(f'Скорость: {speed} MPS',
                                          pos[0], pos[1])

    def upgrade(self):
        if self.settings.level > 3:
            return
        if int(self.settings.level_prices[str(self.settings.level)])\
                <= monitor.settings.money_business:
            monitor.settings.money_business -= int(self.settings.level_prices[
                                                       str(self.settings.level)])
            monitor.update_values()
            self.settings.level += 1
            self.image = pygame.surface.Surface((850, 500), pygame.SRCALPHA, 32)
            self.image.blit(Worker.levels[self.settings.level - 2], (-15, -3))
            self.image.blit(Worker.image_scales, (0, 20))
            if self.settings.level >= 2 and not self.settings.level > 3:
                self.settings.btn_upgrade.hint_text =\
                    f'Цена: {self.settings.level_prices[str(self.settings.level)]}'
                self.settings.btn_upgrade.show_hint(pygame.mouse.get_pos())
            if self.settings.level > 3:
                self.settings.btn_upgrade.hint.kill()
                self.settings.btn_upgrade.kill()

    def conveyor_work(self):
        if not self.settings.conv:
            if int(SettingsConveyor.level_prices['0'])\
                    <= monitor.settings.money_business:
                monitor.settings.money_business -=\
                    int(SettingsConveyor.level_prices['0'])
                monitor.update_values()
                self.settings.conv = Conveyor(load_image("sprite_conveyor_belt_animation.png"),
                                              5, 1, 0, self.rect.y)
                self.settings.btn_conv_upgrade.image = pygame.transform.scale(
                    load_image('btn_upgrade_arrow.png'), (80, 80))
                self.settings.conv.settings.level += 1
                self.settings.btn_conv_upgrade.hint_text =\
                    f'Цена: {SettingsConveyor.level_prices[str(self.settings.conv.settings.level)]}'
                self.settings.btn_conv_upgrade.show_hint(pygame.mouse.get_pos())
        else:
            if self.settings.conv.settings.level < 3:
                if int(SettingsConveyor.level_prices[str(self.settings.conv.settings.level)])\
                        <= monitor.settings.money_business:
                    monitor.settings.money_business -= int(SettingsConveyor.level_prices
                                                           [str(self.settings.conv.settings.level)])
                    monitor.update_values()
                    self.settings.conv.settings.level += 1
                    if self.settings.conv.settings.level < 3:
                        self.settings.btn_conv_upgrade.hint_text =\
                            f'Цена: {SettingsConveyor.level_prices[str(self.settings.conv.settings.level)]}'
                        self.settings.btn_conv_upgrade.show_hint(pygame.mouse.get_pos())
            if self.settings.conv.settings.level >= 3:
                self.settings.btn_conv_upgrade.hint.kill()
                self.settings.btn_conv_upgrade.kill()

    def update(self, *args, **kwargs):
        if args and self.rect.collidepoint(args[0].pos):
            if not self.settings.level:
                self.rect.y -= 20
                self.image = pygame.surface.Surface((850, 500), pygame.SRCALPHA, 32)
                self.image.blit(Worker.image_scales, (0, 20))
                self.settings.level += 1
                self.settings.btn_upgrade =\
                    Button('btn_upgrade_arrow.png', 735, self.rect.y + 55, 80, 80,
                           hint_text=f'Цена: '
                                     f'{self.settings.level_prices[str(self.settings.level)]}')
                self.settings.btn_conv_upgrade =\
                    Button('btn_upgrade_plus.png', 565, self.rect.y + 55, 80, 80,
                           hint_text=f'Цена: {SettingsConveyor.level_prices["0"]}')
                return
            if monitor.settings.kilograms < monitor.settings.max_kilograms:
                monitor.add_counter()
        if monitor.settings.is_work:
            if monitor.settings.kilograms < monitor.settings.max_kilograms:
                if self.settings.level >= 2:
                    self.settings.counter += 1
                    if self.settings.conv:
                        speed = self.settings.speeds[str(self.settings.level +
                                                         self.settings.conv.settings.level)] * FPS
                    else:
                        speed = self.settings.speeds[str(self.settings.level)] * FPS
                    if self.settings.counter >= speed:
                        self.settings.counter = 0
                        monitor.add_counter()


if __name__ == '__main__':
    FPS = 60
    clock = pygame.time.Clock()
    pygame.display.set_caption('Metal Clicker')

    worker1 = Worker(15, all_sprites, workers_group)
    worker2 = Worker(245, all_sprites, workers_group)
    worker3 = Worker(475, all_sprites, workers_group)
    monitor = Monitor(all_sprites)
    running = True
    while running:
        screen.fill((200, 195, 184))
        screen.blit(floor, (-6, -7))
        screen.blit(balka, (600, -2))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEMOTION:
                for worker in workers_group.sprites():
                    worker.show_hint(event.pos)
                for button in buttons_group:
                    button.show_hint(event.pos)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    monitor.connect(event.pos)
                    for worker in workers_group.sprites():
                        worker.connect(event.pos)
                    all_sprites.update(event)
        all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()