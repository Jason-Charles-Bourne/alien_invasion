# --------------------------------------------------------------
# Author: Zhao Mengfei
# Date: 2020-11-01 17:49:55
# LastEditTime: 2020-11-01 17:50:06
# LastEditors: Zhao Mengfei
# Description:
# FilePath: \python_from_introduction_to_practice\project\alien_invasion\alien_invasion.py
# --------------------------------------------------------------


import pygame
from pygame.sprite import Group

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
import game_functions as gf


def run_game():
    # 初始化pygame、设置和屏幕对象
    pygame.init()
    ai_settings = Settings()

    # 设置窗口的宽度和高度
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))

    # 设置窗口的标题
    pygame.display.set_caption("Alien Invasion          Direction: Left and right arrows       Fire: Space key        Exit: Q                   @Author: A.J.Fikry")

    # 创建Play按钮
    play_button = Button(ai_settings, screen, "Play")

    # 创建存储游戏统计信息的实例，并创建记分牌
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    # 创建一艘飞船、一个子弹编组和一个外星人编组
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group() 

    # 创建外星人人群
    gf.creat_fleet(ai_settings, screen, ship, aliens)

    # 开始游戏的主循环
    while True:
        gf.check_events(ai_settings, screen, stats, sb,
                        play_button, ship, aliens, bullets)

        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats,
                              sb, ship, aliens, bullets)
            gf.update_aliens(ai_settings, screen, stats,
                             sb, ship, aliens, bullets)

        gf.update_screen(ai_settings, screen, stats, sb,
                         ship, aliens, bullets, play_button)


run_game()
