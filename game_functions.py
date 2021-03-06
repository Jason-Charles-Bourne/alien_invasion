# --------------------------------------------------------------
# Author: Zhao Mengfei
# Date: 2020-11-04 13:58:13
# LastEditTime: 2020-11-04 13:58:15
# LastEditors: Zhao Mengfei
# Description:
# FilePath: \python_from_introduction_to_practice\project\alien_invasion\game_functions.py
# --------------------------------------------------------------

import sys
from time import sleep

import pygame

from bullet import Bullet
from alien import Alien

#* ----------------------------------------------------------------------------
#*         按键相关
#* ----------------------------------------------------------------------------
def check_keydown_events(stats, sb, event, ai_settings, screen, ship, bullets):
    """响应按键按下"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        write_high_score_into_file(stats, sb)
        sys.exit()


def check_keyup_events(event, ship):
    """响应按键松开"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(stats, sb, event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)


def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """在玩家单击Play按钮时开始新游戏"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active: # 只有当鼠标点击play按钮且游戏处于非活跃状态时，才重置游戏
        # 重置游戏设置
        ai_settings.initialize_dynamic_settings()

        # 隐藏光标
        pygame.mouse.set_visible(False)

        # 重置游戏统计信息
        stats.reset_stats()
        stats.game_active = True

        # 重置记分牌图像
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()
        
        # 创建一群新的外星人，并让飞船居中
        creat_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

#* ----------------------------------------------------------------------------

#* ----------------------------------------------------------------------------
#*         最高分相关
#* ----------------------------------------------------------------------------
def check_high_score(stats, sb):
    """Check to see if there's a new high score."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def write_high_score_into_file(stats, sb):
    """把最高分写入文件high_score.txt，当下一次运行游戏时加载这个最高分"""
    check_high_score(stats, sb)
    filename_high_score = 'high_score.txt'
    with open(filename_high_score, 'w') as file_object:
        file_object.write(str(stats.high_score))
    
#* ----------------------------------------------------------------------------

#* ----------------------------------------------------------------------------
#*         更新屏幕
#* ----------------------------------------------------------------------------
def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    """Update images on the screen, and flip to the new screen."""
    screen.fill(ai_settings.bg_color)  # 设置屏幕背景颜色

    # 在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()  # 绘制飞船
    aliens.draw(screen)  # 绘制外星人

    # 显示得分
    sb.show_score()

    # 如果游戏处于非活动状态，绘制Play按钮
    if not stats.game_active:
        play_button.draw_button()

    pygame.display.flip()     # 让最近绘制的屏幕可见
#* ----------------------------------------------------------------------------

#* ----------------------------------------------------------------------------
#*         子弹相关
#* ----------------------------------------------------------------------------
def fire_bullet(ai_settings, screen, ship, bullets):
    """如果还没有到达限制，就发射一颗子弹"""
    # 创建一颗子弹，并将其加入到编组bullets中
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """更新子弹的位置，并删除已消失的子弹"""
    # 更新子弹的位置
    bullets.update()

    # 删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    # print(len(bullets))  # 显示此刻有多少颗子弹

    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)
#* ----------------------------------------------------------------------------

#* ----------------------------------------------------------------------------
#*         检测子弹和外星人的碰撞
#* ----------------------------------------------------------------------------
def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """响应子弹和外星人的碰撞"""
    # 删除删除发生碰撞的子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens, False, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        # 如果整群外星人都被消灭 
        bullets.empty() # 删除现有的子弹
        ai_settings.increase_speed()
        start_new_level(stats, sb) # 提高用户的等级

        # 创建一群新的外星人
        creat_fleet(ai_settings, screen, ship, aliens)
#* ----------------------------------------------------------------------------

#* ----------------------------------------------------------------------------
#*         用户等级相关
#* ----------------------------------------------------------------------------
def start_new_level(stats, sb):
    """提高用户的等级"""
    stats.level += 1
    sb.prep_level()

#* ----------------------------------------------------------------------------

#* ----------------------------------------------------------------------------
#*         外星人相关
#* ----------------------------------------------------------------------------
def get_number_aliens_x(ai_settings, alien_width):
    """计算每行可容纳多少个外星人"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """计算屏幕可容纳多少行外星人"""
    available_space_y = (ai_settings.screen_height -
                         (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """创建一个外星人并将其放在当前行"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def creat_fleet(ai_settings, screen, ship, aliens):
    """创建外星人群"""
    # 创建一个外星人，并计算一行可容纳多少个外星人
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(
        ai_settings, ship.rect.height, alien.rect.height)

    # 创建外星人群
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def check_fleet_edges(ai_settings, aliens):
    """有外星人到达边缘时采取相应的措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """将整群外星人下移，并改变他们的方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """响应被外星人撞到的飞船"""
    if stats.ships_left > 0:
        # 将ships_left减1
        stats.ships_left -= 1

        # 更新记分牌
        sb.prep_ships()

        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        # 创建一群新的外星人，并将飞船放到屏幕底端中央
        creat_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # 暂停
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """检测是否有外星人到达了屏幕底端"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # 像飞船被撞倒一样进行处理
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break


def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """更新外星人群中所有外星人的位置"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # 检测外星人与飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)

    # 检查是否有外星人到达了屏幕底端
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)

#* ----------------------------------------------------------------------------

