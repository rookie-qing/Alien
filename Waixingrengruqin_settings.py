
class Settings():
    def __init__(self):
        #窗口属性
        #窗口宽
        self.screen_width = 1200
        #窗口高度
        self.screen_height = 800
        #窗口背景颜色
        #self.bg_color = (230, 230, 230)
        self.bg_color = (255, 255, 255)
        #飞船属性
        #飞船移动速度
        self.ship_speed_factor = 1.5
        #飞船允许复活次数
        self.ship_limit = 3

        #子弹属性
        #子弹射速
        self.bullet_speed_factor = 2
        #子弹宽度
        self.bullet_width = 6
        #子弹高度
        self.bullet_height = 18
        #子弹颜色
        self.bullet_color = 60,60,60
        #子弹的数量上限
        self.bullets_allowed = 5

        #Alien属性
        #Alien速度
        self.alien_speed_factor = 1
        #Aliens触碰到右方边缘向下移动时的速度
        self.fleet_drop_speed = 40
        #=1表示向右,=-1表示向左
        self.fleet_direction = 1.5
