#子弹的属性、位置存储、形状的配置
import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    def __init__(self, ai_settings, screen, ship):
        #继承父类所有属性
        #python2.7的继承方法
        #super(Bullet, self).__init__()
        #python3的继承方法
        super().__init__()
        self.screen = screen
        #在(0.0)处创建一个表示子弹的矩形,再设置正确的位置
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        #存储用小数表示子弹位置
        self.y = float(self.rect.y)
        #调用子弹颜色
        self.color = ai_settings.bullet_color
        #调用子弹速度
        self.speed_factor = ai_settings.bullet_speed_factor
    #更新并存储子弹位置
    def update(self):
            self.y -= self.speed_factor
            self.rect.y = self.y
    #在屏幕上绘制子弹
    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)


