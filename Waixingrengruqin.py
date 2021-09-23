# elif event.type == pygame.KEYDOWN:
#    if event.key == pygame.K_RIGHT:
#        ship.rect.centerx += 1

import sys
import pygame
from pygame.sprite import Group
import Waixingrengruqin_settings as settings
from Waixingrengruqin_bullet import Bullet
from alien import Alien
from time import sleep
from pleay import Button


class Ship():
    def __init__(self, ai_settings, screen):
        self.screen = screen
        #路径\图片名称.bmp
        self.image = pygame.image.load(('images\白底-飞船-最小版.bmp'))
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        self.ai_settings = ai_settings
        self.center = float(self.rect.centerx)

        self.moving_right = False
        self.moving_left = False

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            #self.center += self.ai_settings.ship_speed_factor
            self.rect.centerx += self.ai_settings.ship_speed_factor
            #self.rect.centerx += 1
        if self.moving_left and self.rect.left > 0:
            #self.center -= self.ai_settings.ship_speed_factor
            self.rect.centerx -= self.ai_settings.ship_speed_factor
            #self.rect.centerx -= 1

    #飞船被撞毁后生成居中位置参数
    def center_ship(self):
        #值存储使用 self.rect.centerx
        #self.center 无法调用
        self.rect.centerx = self.screen_rect.centerx

    def blitme(self):
        self.screen.blit(self.image, self.rect)

#------
#判断子弹数量决定是否创建
def fire_bullet(ai_settings, screen, ship, bullects):
    if len(bullects) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullects.add(new_bullet)

def check_keydown_events(event, ai_settings, screen, ship, bullects):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    #将创建的子弹加入到编组bullects中
    elif event.key == pygame.K_SPACE:
        #控制子弹数量
        fire_bullet(ai_settings, screen, ship, bullects)

def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(ai_settings, screen, stats, play_button, ship, aliens, bullets):
    for event in pygame.event.get():
        #通过右上角关闭窗口退出
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            # 通过Q快捷键退出窗口
            if event.key == pygame.K_q:
                sys.exit()
            else:
                check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        #play的判断点击,单次重置
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, play_button, ship, aliens, bullets, mouse_x, mouse_y)

#点击则开始游戏
def check_play_button(ai_settings, screen, stats, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    if play_button.rect.collidepoint(mouse_x, mouse_y):
        #重置游戏统计信息
        stats.rest_stats()
        stats.game_active =True
        #清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()
        #创建一群新的外星人,并让飞船居中
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship
#------
#计算每行可以容纳多少个外星人
def get_number_aliens_x(ai_settings, alien_width):
    available_space_x = ai_settings.screen_width - 2 * alien_width
    #Alien间距为Alien宽度
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

#计算屏幕可以容纳多少行外星人
def get_number_rows(ai_settings, ship_height, alien_height):
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    #最优生成Aliens行数
    #number_rows = int(available_space_y / (2 * alien_height))
    #自定义生成Aliens行数
    number_rows = 3
    return number_rows

# 创建一个Alien将其加入当前行
def create_alien(ai_settings, screen, aliens, alien_width, alien_number,  row_number):
    alien = Alien(ai_settings, screen)
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

#创建一行Alien群
def create_fleet(ai_settings, screen, ship, aliens):
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    #调用计算容纳数量
    number_aliens_x = get_number_aliens_x(ai_settings, alien_width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    # 创建Alien群
    for row_number in range(number_rows):
        #最优创建Alien数量
        #for alien_number in range(number_aliens_x):
        #自定义创建Alien数量
        for alien_number in range(1):
            create_alien(ai_settings, screen, aliens, alien_width, alien_number, row_number)

#------
def check_fleet_edges(ai_settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

#------
#跟踪统计游戏的统计信息
class GameStats():
    def __init__(self, ai_settings):
        #初始化统计信息
        self.ai_settings = ai_settings
        self.rest_stats()
        # True表示程序继续运行,False表示程序停止
        self.game_active = False
        #默认游戏不激活
        #self.game_active = False

    def rest_stats(self):
        #初始化在游戏运行期间可能变化的统计信息
        self.ships_left = self.ai_settings.ship_limit

#飞船被撞走此流程,惩罚生命并初始化操作
def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
    #飞船被撞生命-1
    if stats.ships_left > 0:
        stats.ships_left -= 1
        #清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()
        #从新创建新的Aliens,并将飞船放到屏幕低端中央
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        #时间暂停
        sleep(0.5)
    else:
        stats.game_active = False
#------

#------
#检查Alien是否到达了屏幕低端
def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
            break

#调用Aliens移动方法
def update_aliens(ai_settings, stats, screen, ship, aliens, bullets):
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    #检测外星人和飞船碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
    #检查Alien底端碰撞
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)
#------

def update_screen(ai_settings, screen, ship, aliens, bullets, play_button, stats):
    screen.fill(ai_settings.bg_color)
    #初始化子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    #调用数据让飞船显示
    ship.blitme()
    #调用数据让外星人显示
    #alien.blitme()
    #调用创建多个Alien
    aliens.draw(screen)
    #如果游戏处于非活动状态,就绘制Play按钮
    if not stats.game_active:
        play_button.draw_button()
    #
    pygame.display.flip()

#------
#通过sprite.groupcollide()检查碰撞,删除对应Alien
def check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets):
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if len(aliens) == 0:
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)

#控制子弹数量
def update_bulletc(ai_settings, screen, ship, aliens, bullets):
    # 子弹位置不断减少
    bullets.update()
    # 子弹位置不断减少但不会消失,通过子弹位置值的判断来删除子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    #删除Alien
    check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets)
#------

#执行模块
def run_game():
    pygame.init()
    #属性设置
    ai_settings = settings.Settings()
    #窗口宽高
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    #窗口名称
    pygame.display.set_caption("Alien Invasion")
    #创建play按钮
    play_button = Button(ai_settings, screen, "Play")
    #调用Ship类内属性方法
    ship = Ship(ai_settings, screen)
    #调用Alienn类属性方法
    alien = Alien(ai_settings, screen)
    # 调用子弹类属性方法
    bullets = Group()
    #
    aliens = Group()
    # 创建Alien群
    create_fleet(ai_settings, screen, ship, aliens)
    #创建允许存储游戏统计信息的实例
    stats = GameStats(ai_settings)
    while True:
        #负责对键鼠操作进行判断，关闭窗口
        check_events(ai_settings, screen, stats, play_button, ship, aliens, bullets)
        if stats.game_active:
            #飞船左右移动检测
            ship.update()
            #生成子弹,子弹阈值;
            #检测Aliens是否被消灭,无Alien后重新生成Aliens
            update_bulletc(ai_settings, screen, ship, aliens, bullets)
            #外星人移动轨迹，速度
            update_aliens(ai_settings, stats, screen, ship, aliens, bullets)
        #创建窗口初始化
        update_screen(ai_settings, screen, ship, aliens, bullets, play_button, stats)
run_game()










