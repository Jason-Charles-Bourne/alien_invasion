# --------------------------------------------------------------
# Author: Zhao Mengfei
# Date: 2020-11-07 20:56:59
# LastEditTime: 2020-11-07 20:57:00
# LastEditors: Zhao Mengfei
# Description:
# FilePath: \python_from_introduction_to_practice\project\alien_invasion\scoreboard.py
# --------------------------------------------------------------

import pygame.font
from pygame.sprite import Group
from ship import Ship


class Scoreboard():
    """显示得分信息的类"""

    def __init__(self, ai_settings, screen, stats):
        """初始化显示得分涉及的属性"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        # 显示得分信息时使用的字体设置
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # 准备包含最高得分和当前得分的图像
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """将得分转换为一幅渲染的图像"""
        rounded_score = int(round(self.stats.score, -1))
        score_str = "{:,}".format(rounded_score)
        score_str = "Score " + score_str
        self.score_image = self.font.render(
            score_str, True, self.text_color, self.ai_settings.bg_color)

        # 将得分得在屏幕右上角
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        """在屏幕上显示飞船和得分"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)

        # 绘制飞船
        self.ships.draw(self.screen)

# * ----------------------------------------------------------------------------
# *         最高分相关
# * ----------------------------------------------------------------------------
    def prep_high_score(self):
        """Turn the high score into a rendered image."""
        # 内存中的最高分
        high_score = int(round(self.stats.high_score, -1))

        # 文件中的最高分
        with open('high_score.txt') as file_object:
            high_score_str = file_object.read()
            # print(high_score_str)
        high_score_in_file = round(int(high_score_str))

        # 决定加载哪个最高分？
        if high_score > high_score_in_file:  # 加载当前的（内存中的）最高分
            high_score_str = "{:,}".format(high_score)
            high_score_str = "Highest Record " + high_score_str
            self.high_score_image = self.font.render(high_score_str, True,
                                                     self.text_color, self.ai_settings.bg_color)

            # Center the high score at the top of the screen.
            self.high_score_rect = self.high_score_image.get_rect()
            self.high_score_rect.centerx = self.screen_rect.centerx
            self.high_score_rect.top = self.score_rect.top

        else:  # 加载在high_score.txt文件中的最高分
            high_score_str = "{:,}".format(high_score_in_file)
            high_score_str = "Highest Record " + high_score_str
            self.high_score_image = self.font.render(high_score_str, True,
                                                     self.text_color, self.ai_settings.bg_color)

            # Center the high score at the top of the screen.
            self.high_score_rect = self.high_score_image.get_rect()
            self.high_score_rect.centerx = self.screen_rect.centerx
            self.high_score_rect.top = self.score_rect.top

# * ----------------------------------------------------------------------------

    def prep_level(self):
        """Turn the level into a rendered image."""
        level_str = str(self.stats.level)
        level_str = "Level " + level_str
        self.level_image = self.font.render(level_str, True,
                                            self.text_color, self.ai_settings.bg_color)

        # Position the level below the score.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """Show how many ships are left."""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_settings, self.screen)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)
