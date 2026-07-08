import pygame
import sys
import random
import math
import json
import os

pygame.init()

# Полноэкранный режим (адаптируется под любое разрешение)
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
clock = pygame.time.Clock()
CENTER = (WIDTH // 2, HEIGHT // 2)

# Отключаем звук
pygame.mixer.quit()

# Шрифты (размеры адаптируются под экран)
font_size = max(24, int(min(WIDTH, HEIGHT) / 30))
font = pygame.font.SysFont(None, font_size)
font_big = pygame.font.SysFont(None, int(font_size * 2.2))
font_shop = pygame.font.SysFont(None, int(font_size * 0.8))
font_small = pygame.font.SysFont(None, int(font_size * 0.7))

# Константы карты
MAP_SIZE = 5000
MAP_SIZE_ARENA = 1200
MAP_SIZE_BASES = 5000
SAVE_FILE = "save.json"

# Вспомогательная функция для создания цветных квадратов
def make_square(color, size):
    surf = pygame.Surface(size, pygame.SRCALPHA)
    surf.fill(color)
    return surf

# ---- СОЗДАНИЕ ВСЕХ ТЕКСТУР КАК ПРОСТЫХ КВАДРАТОВ ----
player_surfaces = {
    "idle": make_square((0, 200, 0), (40, 40)),
    "up": make_square((0, 200, 0), (40, 40)),
    "down": make_square((0, 200, 0), (40, 40)),
    "left": make_square((0, 200, 0), (40, 40)),
    "right": make_square((0, 200, 0), (40, 40))
}
zombie_surfaces = {
    "left": make_square((200, 0, 0), (55, 55)),
    "right": make_square((200, 0, 0), (55, 55))
}
wolf_surfaces = {
    "left": make_square((150, 150, 150), (95, 55)),
    "right": make_square((150, 150, 150), (95, 55))
}
bear_surfaces = {
    "left": make_square((139, 69, 19), (130, 70)),
    "right": make_square((139, 69, 19), (130, 70))
}
boss_surfaces = {
    "left": make_square((128, 0, 128), (55, 55)),
    "right": make_square((128, 0, 128), (55, 55))
}
dog_surfaces = {
    "idle": make_square((255, 165, 0), (60, 40)),
    "left": make_square((255, 165, 0), (60, 40)),
    "right": make_square((255, 165, 0), (60, 40))
}
bot_surfaces = {
    "left": make_square((100, 100, 255), (60, 60)),
    "right": make_square((100, 100, 255), (60, 60))
}
object1 = make_square((0, 255, 255), (80, 80))
object2 = make_square((255, 255, 0), (80, 80))
object3 = make_square((255, 0, 255), (80, 80))
object4 = make_square((0, 255, 255), (80, 80))
tree = make_square((0, 128, 0), (60, 80))
bush = make_square((0, 100, 0), (40, 40))
bush_empty = make_square((100, 50, 0), (40, 40))
wall_img = make_square((50, 50, 50), (50, 50))
rust_img = make_square((139, 69, 19), (20, 20))
iron_img = make_square((192, 192, 192), (20, 20))
gold_img = make_square((255, 215, 0), (20, 20))
berry_icon = make_square((255, 0, 0), (32, 32))
svetilo_icon = make_square((0, 255, 255), (32, 32))
ldishka_icon = make_square((0, 200, 255), (32, 32))
rubin_icon = make_square((255, 0, 128), (32, 32))
svetilo_video = make_square((0, 255, 255), (75, 75))
ldishka_video = make_square((0, 200, 255), (75, 75))
rubin_video = make_square((255, 0, 128), (75, 75))
pistol_img = make_square((200, 200, 100), (40, 40))
shotgun_img = make_square((150, 100, 50), (40, 40))
rpg_img = make_square((200, 50, 50), (40, 40))
wintiwka_img = make_square((100, 100, 200), (40, 40))
farn_img = make_square((0, 200, 0), (40, 40))
kraft_img = make_square((200, 200, 0), (60, 60))
broni_img = make_square((0, 0, 200), (64, 64))
vintovka_img = make_square((200, 200, 200), (64, 64))
werstak_img = make_square((128, 128, 128), (80, 80))
safe_img = make_square((0, 255, 0), (80, 80))
sfera_img = make_square((255, 215, 0), (40, 40))
genuy_img = make_square((255, 255, 255), (60, 60))
bike_trader_img = make_square((0, 0, 255), (60, 60))
boss_npc_img = make_square((128, 0, 128), (60, 60))
bike_up = make_square((0, 255, 255), (40, 40))
bike_down = make_square((0, 255, 255), (40, 40))
bike_left = make_square((0, 255, 255), (40, 40))
bike_right = make_square((0, 255, 255), (40, 40))
arena_img = make_square((255, 0, 0), (60, 60))
background = pygame.Surface((WIDTH, HEIGHT))
background.fill((34, 139, 34))

# Маски для коллизий (упрощённо)
def create_mask_from_surface(surf):
    return pygame.mask.from_surface(surf)

object1_mask = create_mask_from_surface(object1)
object2_mask = create_mask_from_surface(object2)

# Вспомогательные функции
def save_game(data):
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)

def load_game():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            return json.load(f)
    return None

def draw_button(surface, text, rect, hover=False, small_font=False, tiny_font=False):
    if hover:
        bg_color = (76, 175, 80)
        border_color = (129, 199, 132)
    else:
        bg_color = (46, 125, 50)
        border_color = (129, 199, 132)
    text_color = (255, 255, 255)
    shadow_rect = rect.move(3, 3)
    pygame.draw.rect(surface, (0, 0, 0, 50), shadow_rect, border_radius=12)
    pygame.draw.rect(surface, bg_color, rect, border_radius=12)
    pygame.draw.rect(surface, border_color, rect, width=2, border_radius=12)
    if tiny_font:
        text_surf = font_small.render(text, True, text_color)
    elif small_font:
        text_surf = font_shop.render(text, True, text_color)
    else:
        text_surf = font.render(text, True, text_color)
    text_rect = text_surf.get_rect(center=rect.center)
    surface.blit(text_surf, text_rect)

def is_far_from_walls(x, y, margin=250, arena=False):
    size = MAP_SIZE_ARENA if arena else MAP_SIZE
    return margin <= x <= size - margin and margin <= y <= size - margin

# Меню (сенсорное)
def menu():
    promo_input = ""
    active = False
    bonus_gold = 0

    # Кнопки с увеличенными размерами для пальцев
    btn_w = int(WIDTH * 0.25)
    btn_h = int(HEIGHT * 0.08)
    play_rect = pygame.Rect(0, 0, btn_w, btn_h)
    load_rect = pygame.Rect(0, 0, btn_w, btn_h)
    exit_rect = pygame.Rect(0, 0, btn_w, btn_h)

    while True:
        mouse_pos = pygame.mouse.get_pos()
        screen.fill((0, 0, 0))

        title = font_big.render("Zombix OFFline", True, (255, 255, 255))
        title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        screen.blit(title, title_rect)

        play_rect.center = (WIDTH // 2, HEIGHT // 2)
        load_rect.center = (WIDTH // 2, HEIGHT // 2 + btn_h + 20)
        exit_rect.center = (WIDTH // 2, HEIGHT // 2 + 2 * (btn_h + 20))

        draw_button(screen, "Играть", play_rect, play_rect.collidepoint(mouse_pos))
        draw_button(screen, "Продолжить", load_rect, load_rect.collidepoint(mouse_pos))
        draw_button(screen, "Выйти", exit_rect, exit_rect.collidepoint(mouse_pos))

        if active:
            txt = font.render("Промокод: " + promo_input, True, (255, 255, 0))
            screen.blit(txt, (WIDTH // 2 - 150, HEIGHT // 2 + 230))
        else:
            hint = font.render("Нажми P для промокода", True, (200, 200, 200))
            screen.blit(hint, (WIDTH // 2 - 180, HEIGHT // 2 + 230))

        version_font = pygame.font.SysFont(None, int(font_size * 0.7))
        version_text = version_font.render("Версия 2.3", True, (255, 255, 255))
        dev_text = version_font.render("Разработчик: t.me/Zombixofflinenews", True, (255, 255, 255))
        screen.blit(version_text, (WIDTH - version_text.get_width() - 20, HEIGHT - 60))
        screen.blit(dev_text, (WIDTH - dev_text.get_width() - 20, HEIGHT - 30))

        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(e.pos):
                    return "new", bonus_gold
                if load_rect.collidepoint(e.pos):
                    return "load", 0
                if exit_rect.collidepoint(e.pos):
                    pygame.quit()
                    sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_p:
                    active = True
                elif active:
                    if e.key == pygame.K_RETURN:
                        if promo_input == "FREEGOLD":
                            bonus_gold = 1000
                        promo_input = ""
                        active = False
                    elif e.key == pygame.K_BACKSPACE:
                        promo_input = promo_input[:-1]
                    else:
                        promo_input += e.unicode

def location_menu():
    bases_spawn_x = 500 + 500
    bases_spawn_y = 500 + 500
    LOCATIONS = {
        "home": {"name": "Домашняя зона", "pos": (2615, 3135), "teleport_zone": False},
        "monster": {"name": "Логово монстров", "pos": (MAP_SIZE - 700, MAP_SIZE - 700), "teleport_zone": True},
        "bases": {"name": "Базы выживших", "pos": (bases_spawn_x, bases_spawn_y), "teleport_zone": "bases"},
        "base_home": {"name": "Личная база", "pos": (MAP_SIZE_ARENA//2, MAP_SIZE_ARENA//2), "teleport_zone": "base_home"},
        "hotspot": {"name": "Горячая точка", "pos": (MAP_SIZE//2, MAP_SIZE//2), "teleport_zone": "hotspot"}
    }
    selected = None
    menu_open = True
    menu_w = int(WIDTH * 0.8)
    menu_h = int(HEIGHT * 0.7)
    menu_x = WIDTH // 2 - menu_w // 2
    menu_y = HEIGHT // 2 - menu_h // 2
    btn_w = int(menu_w * 0.4)
    btn_h = int(menu_h * 0.1)
    spacing = int(btn_h * 0.5)
    btn_home = pygame.Rect(menu_x + (menu_w - btn_w)//2, menu_y + 80, btn_w, btn_h)
    btn_monster = pygame.Rect(menu_x + (menu_w - btn_w)//2, btn_home.bottom + spacing, btn_w, btn_h)
    btn_bases = pygame.Rect(menu_x + (menu_w - btn_w)//2, btn_monster.bottom + spacing, btn_w, btn_h)
    btn_base_home = pygame.Rect(menu_x + (menu_w - btn_w)//2, btn_bases.bottom + spacing, btn_w, btn_h)
    btn_hotspot = pygame.Rect(menu_x + (menu_w - btn_w)//2, btn_base_home.bottom + spacing, btn_w, btn_h)

    while menu_open:
        mouse_pos = pygame.mouse.get_pos()
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        pygame.draw.rect(screen, (50, 50, 50), (menu_x, menu_y, menu_w, menu_h), border_radius=15)
        pygame.draw.rect(screen, (100, 100, 100), (menu_x, menu_y, menu_w, menu_h), width=3, border_radius=15)
        title = font_big.render("Выберите локацию", True, (255, 255, 0))
        title_rect = title.get_rect(center=(menu_x + menu_w // 2, menu_y + 40))
        screen.blit(title, title_rect)
        draw_button(screen, "Домашняя зона", btn_home, btn_home.collidepoint(mouse_pos), tiny_font=True)
        draw_button(screen, "Логово монстров", btn_monster, btn_monster.collidepoint(mouse_pos), tiny_font=True)
        draw_button(screen, "Базы выживших", btn_bases, btn_bases.collidepoint(mouse_pos), tiny_font=True)
        draw_button(screen, "Личная база", btn_base_home, btn_base_home.collidepoint(mouse_pos), tiny_font=True)
        draw_button(screen, "Горячая точка", btn_hotspot, btn_hotspot.collidepoint(mouse_pos), tiny_font=True)
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type == pygame.MOUSEBUTTONDOWN:
                if btn_home.collidepoint(e.pos):
                    selected = LOCATIONS["home"]
                    menu_open = False
                elif btn_monster.collidepoint(e.pos):
                    selected = LOCATIONS["monster"]
                    menu_open = False
                elif btn_bases.collidepoint(e.pos):
                    selected = LOCATIONS["bases"]
                    menu_open = False
                elif btn_base_home.collidepoint(e.pos):
                    selected = LOCATIONS["base_home"]
                    menu_open = False
                elif btn_hotspot.collidepoint(e.pos):
                    selected = LOCATIONS["hotspot"]
                    menu_open = False
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                menu_open = False
                selected = None
    return selected

def quest_menu(quest_type, quest_target, reward, current_progress=0, active=False):
    if active:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        msg = font_big.render("Задание уже активно!", True, (255, 0, 0))
        msg_rect = msg.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        screen.blit(msg, msg_rect)
        btn_w = int(WIDTH * 0.2)
        btn_h = int(HEIGHT * 0.06)
        close_btn = pygame.Rect(WIDTH // 2 - btn_w//2, HEIGHT // 2 + 50, btn_w, btn_h)
        draw_button(screen, "OK", close_btn, close_btn.collidepoint(pygame.mouse.get_pos()))
        pygame.display.flip()
        waiting = True
        while waiting:
            for e in pygame.event.get():
                if e.type == pygame.MOUSEBUTTONDOWN and close_btn.collidepoint(e.pos):
                    waiting = False
                if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    waiting = False
            clock.tick(60)
        return False

    menu_open = True
    result = False
    menu_w = int(WIDTH * 0.7)
    menu_h = int(HEIGHT * 0.5)
    menu_x = WIDTH // 2 - menu_w // 2
    menu_y = HEIGHT // 2 - menu_h // 2
    btn_w = int(menu_w * 0.4)
    btn_h = int(menu_h * 0.15)
    accept_btn = pygame.Rect(menu_x + (menu_w - btn_w)//2, menu_y + menu_h - btn_h - 20, btn_w, btn_h)

    while menu_open:
        mouse_pos = pygame.mouse.get_pos()
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        pygame.draw.rect(screen, (50, 50, 50), (menu_x, menu_y, menu_w, menu_h), border_radius=15)
        pygame.draw.rect(screen, (100, 100, 100), (menu_x, menu_y, menu_w, menu_h), width=3, border_radius=15)

        title = font_big.render("Задание", True, (255, 255, 0))
        title_rect = title.get_rect(center=(menu_x + menu_w // 2, menu_y + 50))
        screen.blit(title, title_rect)

        if quest_type == "zombie":
            desc_text = f"Убейте {quest_target} зомби"
            reward_text = f"Награда: {reward} железа"
        elif quest_type == "berry":
            desc_text = f"Соберите {quest_target} ягод"
            reward_text = f"Награда: {reward} ржавчины"
        elif quest_type == "boss":
            desc_text = "Убейте босса"
            reward_text = "Награда: 5 золота"
        else:
            desc_text = "Задание"
            reward_text = "Награда: ?"

        desc_surf = font.render(desc_text, True, (255, 255, 255))
        desc_rect = desc_surf.get_rect(center=(menu_x + menu_w // 2, menu_y + 120))
        screen.blit(desc_surf, desc_rect)

        reward_surf = font.render(reward_text, True, (255, 255, 0))
        reward_rect = reward_surf.get_rect(center=(menu_x + menu_w // 2, menu_y + 170))
        screen.blit(reward_surf, reward_rect)

        draw_button(screen, "Принять", accept_btn, accept_btn.collidepoint(mouse_pos))

        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.MOUSEBUTTONDOWN:
                if accept_btn.collidepoint(e.pos):
                    result = True
                    menu_open = False
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                menu_open = False
                result = False
    return result

def arena_menu():
    menu_open = True
    result = False
    menu_w = int(WIDTH * 0.6)
    menu_h = int(HEIGHT * 0.4)
    menu_x = WIDTH // 2 - menu_w // 2
    menu_y = HEIGHT // 2 - menu_h // 2
    btn_w = int(menu_w * 0.4)
    btn_h = int(menu_h * 0.2)
    play_btn = pygame.Rect(menu_x + (menu_w - btn_w)//2, menu_y + menu_h - btn_h - 20, btn_w, btn_h)

    while menu_open:
        mouse_pos = pygame.mouse.get_pos()
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        pygame.draw.rect(screen, (50, 50, 50), (menu_x, menu_y, menu_w, menu_h), border_radius=15)
        pygame.draw.rect(screen, (100, 100, 100), (menu_x, menu_y, menu_w, menu_h), width=3, border_radius=15)

        title = font_big.render("Арена", True, (255, 255, 0))
        title_rect = title.get_rect(center=(menu_x + menu_w // 2, menu_y + 50))
        screen.blit(title, title_rect)

        reward_text = "Награда: 4 железа + 5 золота"
        reward_surf = font.render(reward_text, True, (255, 255, 255))
        reward_rect = reward_surf.get_rect(center=(menu_x + menu_w // 2, menu_y + 120))
        screen.blit(reward_surf, reward_rect)

        screen.blit(iron_img, (menu_x + menu_w // 2 - 80, menu_y + 150))
        iron_text = font.render("x4", True, (255, 255, 255))
        screen.blit(iron_text, (menu_x + menu_w // 2 - 40, menu_y + 155))
        screen.blit(gold_img, (menu_x + menu_w // 2 + 20, menu_y + 150))
        gold_text = font.render("x5", True, (255, 255, 255))
        screen.blit(gold_text, (menu_x + menu_w // 2 + 60, menu_y + 155))

        draw_button(screen, "Играть", play_btn, play_btn.collidepoint(mouse_pos))

        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.MOUSEBUTTONDOWN:
                if play_btn.collidepoint(e.pos):
                    result = True
                    menu_open = False
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                menu_open = False
                result = False
    return result

def init_hotspot():
    safe_rect = pygame.Rect(MAP_SIZE//2 - 300, MAP_SIZE//2 - 300, 600, 600)
    gens = []
    for _ in range(5):
        attempts = 0
        while attempts < 100:
            gx = random.randint(200, MAP_SIZE - 200)
            gy = random.randint(200, MAP_SIZE - 200)
            if not safe_rect.collidepoint(gx, gy):
                gens.append([gx, gy, 4, 0])
                break
            attempts += 1
    monsters = []
    for _ in range(5):
        while True:
            wx = random.randint(200, MAP_SIZE - 200)
            wy = random.randint(200, MAP_SIZE - 200)
            if not safe_rect.collidepoint(wx, wy) and is_far_from_walls(wx, wy, 250):
                monsters.append([wx, wy, 4, "wolf", "right", wx, wy])
                break
    for _ in range(3):
        while True:
            bx = random.randint(200, MAP_SIZE - 200)
            by = random.randint(200, MAP_SIZE - 200)
            if not safe_rect.collidepoint(bx, by) and is_far_from_walls(bx, by, 250):
                monsters.append([bx, by, 12, "bear", "right", bx, by])
                break
    for _ in range(10):
        while True:
            zx = random.randint(200, MAP_SIZE - 200)
            zy = random.randint(200, MAP_SIZE - 200)
            if not safe_rect.collidepoint(zx, zy) and is_far_from_walls(zx, zy, 250):
                monsters.append([zx, zy, 0, "zombie", "right", zx, zy])
                break
    while True:
        bx = random.randint(200, MAP_SIZE - 200)
        by = random.randint(200, MAP_SIZE - 200)
        if not safe_rect.collidepoint(bx, by) and is_far_from_walls(bx, by, 250):
            monsters.append([bx, by, 28, "boss", "right", bx, by])
            break
    bushes = []
    for _ in range(20):
        while True:
            bx = random.randint(200, MAP_SIZE - 200)
            by = random.randint(200, MAP_SIZE - 200)
            if not safe_rect.collidepoint(bx, by):
                bushes.append([bx, by, True, 0])
                break
    return safe_rect, gens, monsters, bushes

def init_base_home():
    werstak_pos = (MAP_SIZE_ARENA - 140, 20)
    safe_pos = (MAP_SIZE_ARENA - 140 - 100, 20)
    teleport_pos = (MAP_SIZE_ARENA//2, MAP_SIZE_ARENA - 100)
    return werstak_pos, safe_pos, teleport_pos

# ---- ГЛАВНАЯ ИГРОВАЯ ФУНКЦИЯ ----
def game(mode, bonus_gold):
    global farn_rects

    # ---- КОНСТАНТЫ ЛОКАЦИЙ ----
    SAFE_ZONE_SIZE = 1000
    SAFE_ZONE_RECT = pygame.Rect(500, 500, SAFE_ZONE_SIZE, SAFE_ZONE_SIZE)
    BASE_RECTS = [
        pygame.Rect(2000, 500, 1000, 1000),
        pygame.Rect(2000, 2000, 1000, 1000),
        pygame.Rect(500, 2000, 1000, 1000)
    ]
    BOT_SPEED = 1.5

    OBJ1 = (2215, 2845)
    OBJ2 = (2615, 2935)
    OBJ3 = (2015, 3135)
    OBJ4 = (2615, 3135)
    SPAWN_X = OBJ4[0]
    SPAWN_Y = OBJ4[1]

    save = load_game() if mode == "load" else None

    if save:
        player_x = save["player_x"]
        player_y = save["player_y"]
        hp = save["hp"]
        armor = save["armor"]
        gold = save["gold"]
        weapon = save["weapon"]
        berries = save["berries"]
        iron = save.get("iron", 0)
        rust = save.get("rust", 0)
        bike_owned = save.get("bike_owned", False)
        bike_active = False
        dog_active = save["dog_active"]
        dog_x = save["dog_x"]
        dog_y = save["dog_y"]
        quest_active = save.get("quest_active", False)
        zombies_killed = save.get("zombies_killed", 0)
        quest_target = save.get("quest_target", 5)
        teleport_zone = save.get("teleport_zone", False)
        xp = save.get("xp", 0)
        level = save.get("level", 1)
        next_level_xp = save.get("next_level_xp", 2)
        berry_quest_active = save.get("berry_quest_active", False)
        berry_quest_target = save.get("berry_quest_target", 5)
        berry_reward = save.get("berry_reward", 2)
        boss_quest_active = save.get("boss_quest_active", False)
        boss_quest_done = save.get("boss_quest_done", False)
        boss_quest_killed = save.get("boss_quest_killed", 0)
        bike_direction = "down"
        current_location = save.get("current_location", "home")
        bases_captured = save.get("bases_captured", [False, False, False])
        bases_bots = save.get("bases_bots", [])
        rust_timers = save.get("rust_timers", [0, 0, 0])
        svetilo_count = save.get("svetilo_count", 0)
        ldishka_count = save.get("ldishka_count", 0)
        rubin_count = save.get("rubin_count", 0)
        owned_weapons = save.get("owned_weapons", ["pistol"])
        if weapon not in owned_weapons:
            owned_weapons.append(weapon)
        for i, bots in enumerate(bases_bots):
            for bot in bots:
                if len(bot) < 6:
                    bot.append(random.choice(["left", "right"]))
                    bot.append(random.randint(60, 180))
        sphere_count = save.get("sphere_count", 0)
        stored_spheres = save.get("stored_spheres", 0)
        sphere_buff_timer = save.get("sphere_buff_timer", 0)
    else:
        player_x, player_y = SPAWN_X, SPAWN_Y
        hp = 100
        armor = 0
        gold = bonus_gold
        weapon = "pistol"
        berries = 0
        iron = 0
        rust = 0
        bike_owned = False
        bike_active = False
        bike_direction = "down"
        dog_active = False
        dog_x, dog_y = player_x + 50, player_y + 50
        quest_active = False
        zombies_killed = 0
        quest_target = 5
        xp = 0
        level = 1
        next_level_xp = 2
        berry_quest_active = False
        berry_quest_target = 5
        berry_reward = 2
        boss_quest_active = False
        boss_quest_done = False
        boss_quest_killed = 0
        current_location = "home"
        bases_captured = [False, False, False]
        bases_bots = []
        for i, rect in enumerate(BASE_RECTS):
            bots = []
            for _ in range(3):
                bx = rect.x + random.randint(100, 900)
                by = rect.y + random.randint(100, 900)
                bots.append([bx, by, 5, 0, random.choice(["left", "right"]), random.randint(60, 180)])
            bases_bots.append(bots)
        rust_timers = [0, 0, 0]
        svetilo_count = 0
        ldishka_count = 0
        rubin_count = 0
        owned_weapons = ["pistol"]
        sphere_count = 0
        stored_spheres = 0
        sphere_buff_timer = 0

    farn_rects = []
    for rect in BASE_RECTS:
        center_x = rect.centerx - farn_img.get_width() // 2
        center_y = rect.centery - farn_img.get_height() // 2
        farn_rects.append(pygame.Rect(center_x, center_y, farn_img.get_width(), farn_img.get_height()))

    svetilo_buff_timer = 0
    ldishka_buff_timer = 0
    rubin_buff_timer = 0
    anomalies = []
    svetilo_items = []
    ldishka_items = []
    rubin_items = []

    craft_menu_open = False

    if current_location == "bases":
        if not SAFE_ZONE_RECT.collidepoint(player_x, player_y):
            player_x = SAFE_ZONE_RECT.centerx
            player_y = SAFE_ZONE_RECT.centery

    inventory_open = False
    SAFE = 400

    boss = None
    boss_spawn_timer = 0
    boss_life_timer = 0
    BOSS_INTERVAL = 60 * 60
    BOSS_LIFETIME = 50 * 60

    objs = [OBJ1, OBJ2, OBJ3, OBJ4]

    def inside_shop_texture(x, y, radius=20):
        shop_x, shop_y = objs[1]
        return math.hypot(x - (shop_x + object2.get_width()//2), y - (shop_y + object2.get_height()//2)) < radius + 30

    def inside_object1_texture(x, y, radius=25):
        obj_x, obj_y = objs[0]
        return math.hypot(x - (obj_x + object1.get_width()//2), y - (obj_y + object1.get_height()//2)) < radius + 30

    teleport_zone = save.get("teleport_zone", False) if save else False
    teleport_return_x = objs[2][0]
    teleport_return_y = objs[2][1]

    secret_x = MAP_SIZE - 700
    secret_y = MAP_SIZE - 700
    bike_trader_x = secret_x + 250
    bike_trader_y = secret_y + 150
    boss_npc_x = secret_x + 450
    boss_npc_y = secret_y + 120

    protected_points = [
        *objs,
        (bike_trader_x, bike_trader_y),
        (boss_npc_x, boss_npc_y),
        (secret_x, secret_y)
    ]

    def is_far_from_points(x, y, points, min_dist=400, arena=False):
        if not is_far_from_walls(x, y, 250, arena):
            return False
        for px, py in points:
            if math.hypot(x - px, y - py) < min_dist:
                return False
        return True

    def is_position_free(x, y, objects, min_dist=140):
        for ox, oy in objects:
            if math.hypot(x - ox, y - oy) < min_dist:
                return False
        return True

    def generate_anomalies(count_svet=2, count_ldish=2, count_rubin=3):
        anomalies.clear()
        for _ in range(count_svet):
            attempts = 0
            while attempts < 100:
                x = random.randint(200, MAP_SIZE - 200)
                y = random.randint(200, MAP_SIZE - 200)
                if (is_far_from_points(x, y, protected_points, min_dist=300) and
                    is_far_from_walls(x, y, 200) and
                    not inside_shop_texture(x, y, 60) and
                    not inside_object1_texture(x, y, 60)):
                    anomalies.append([x, y, 0, 0])
                    break
                attempts += 1
        for _ in range(count_ldish):
            attempts = 0
            while attempts < 100:
                x = random.randint(200, MAP_SIZE - 200)
                y = random.randint(200, MAP_SIZE - 200)
                if (is_far_from_points(x, y, protected_points, min_dist=300) and
                    is_far_from_walls(x, y, 200) and
                    not inside_shop_texture(x, y, 60) and
                    not inside_object1_texture(x, y, 60)):
                    anomalies.append([x, y, 0, 1])
                    break
                attempts += 1
        for _ in range(count_rubin):
            attempts = 0
            while attempts < 100:
                x = random.randint(200, MAP_SIZE - 200)
                y = random.randint(200, MAP_SIZE - 200)
                if (is_far_from_points(x, y, protected_points, min_dist=300) and
                    is_far_from_walls(x, y, 200) and
                    not inside_shop_texture(x, y, 60) and
                    not inside_object1_texture(x, y, 60)):
                    anomalies.append([x, y, 0, 2])
                    break
                attempts += 1

    def update_anomalies_for_location(loc):
        anomalies.clear()
        if loc in ["home", "monster"]:
            generate_anomalies(2, 2, 3)

    update_anomalies_for_location(current_location)

    wall_size = wall_img.get_width()
    wall_rects = [
        pygame.Rect(0, 0, MAP_SIZE, wall_size),
        pygame.Rect(0, MAP_SIZE - wall_size, MAP_SIZE, wall_size),
        pygame.Rect(0, 0, wall_size, MAP_SIZE),
        pygame.Rect(MAP_SIZE - wall_size, 0, wall_size, MAP_SIZE)
    ]
    arena_wall_rects = [
        pygame.Rect(0, 0, MAP_SIZE_ARENA, wall_size),
        pygame.Rect(0, MAP_SIZE_ARENA - wall_size, MAP_SIZE_ARENA, wall_size),
        pygame.Rect(0, 0, wall_size, MAP_SIZE_ARENA),
        pygame.Rect(MAP_SIZE_ARENA - wall_size, 0, wall_size, MAP_SIZE_ARENA)
    ]

    trees = []
    tree_rects = []
    trees_bases = []
    tree_rects_bases = []

    if current_location == "bases":
        for _ in range(20):
            while True:
                x = random.randint(0, MAP_SIZE_BASES)
                y = random.randint(0, MAP_SIZE_BASES)
                in_base = any(rect.collidepoint(x, y) for rect in BASE_RECTS)
                in_safe = SAFE_ZONE_RECT.collidepoint(x, y)
                if not in_base and not in_safe and is_far_from_walls(x, y, 200):
                    trees_bases.append((x, y))
                    trunk_width = 22
                    trunk_height = 55
                    trunk_x = x + tree.get_width() // 2 - trunk_width // 2
                    trunk_y = y + tree.get_height() - trunk_height - 10
                    tree_rects_bases.append(pygame.Rect(trunk_x, trunk_y, trunk_width, trunk_height))
                    break
    else:
        for _ in range(80):
            while True:
                x = random.randint(0, MAP_SIZE)
                y = random.randint(0, MAP_SIZE)
                if (math.hypot(x - SPAWN_X, y - SPAWN_Y) > SAFE and
                    is_far_from_points(x, y, protected_points) and
                    is_position_free(x, y, trees, 170) and
                    not inside_shop_texture(x, y, 40) and
                    not inside_object1_texture(x, y, 40) and
                    is_far_from_walls(x, y, 200) and
                    y <= MAP_SIZE - 300):
                    trees.append((x, y))
                    trunk_width = 22
                    trunk_height = 55
                    trunk_x = x + tree.get_width() // 2 - trunk_width // 2
                    trunk_y = y + tree.get_height() - trunk_height - 10
                    tree_rects.append(pygame.Rect(trunk_x, trunk_y, trunk_width, trunk_height))
                    break
        if save:
            for tx, ty in trees:
                trunk_width = 22
                trunk_height = 55
                trunk_x = tx + tree.get_width() // 2 - trunk_width // 2
                trunk_y = ty + tree.get_height() - trunk_height - 10
                tree_rects.append(pygame.Rect(trunk_x, trunk_y, trunk_width, trunk_height))

    bushes = []
    if current_location != "bases":
        for _ in range(60):
            while True:
                x = random.randint(0, MAP_SIZE)
                y = random.randint(0, MAP_SIZE)
                bush_positions = [(b[0], b[1]) for b in bushes]
                if (math.hypot(x - SPAWN_X, y - SPAWN_Y) > SAFE and
                    is_far_from_points(x, y, protected_points) and
                    is_position_free(x, y, trees, 170) and
                    is_position_free(x, y, bush_positions, 120) and
                    not inside_shop_texture(x, y, 30) and
                    not inside_object1_texture(x, y, 30)):
                    bushes.append([x, y, True, 0])
                    break

    zombies = []
    wolves = []
    bears = []
    if current_location != "bases":
        for _ in range(20):
            while True:
                zx = random.randint(0, MAP_SIZE)
                zy = random.randint(0, MAP_SIZE)
                if (is_far_from_points(zx, zy, protected_points) and
                    not inside_shop_texture(zx, zy, 25) and
                    not inside_object1_texture(zx, zy, 25) and
                    is_far_from_walls(zx, zy, 250)):
                    zombies.append([zx, zy, 0, 4, "right"])
                    break
        for _ in range(5):
            while True:
                wx = random.randint(1000, MAP_SIZE - 1000)
                wy = random.randint(1000, MAP_SIZE - 1000)
                if math.hypot(wx - secret_x, wy - secret_y) > 1000 and is_far_from_walls(wx, wy, 250):
                    wolves.append([wx, wy, 4, "right"])
                    break
        for _ in range(2):
            while True:
                bx = random.randint(500, MAP_SIZE - 500)
                by = random.randint(500, MAP_SIZE - 500)
                if (math.hypot(bx - player_x, by - player_y) > 500 and
                    math.hypot(bx - SPAWN_X, by - SPAWN_Y) > 1200 and
                    is_far_from_walls(bx, by, 250)):
                    bears.append([bx, by, 12, "right"])
                    break

    bullets = []
    golds = []
    irons = []
    rusts = []
    explosions = []
    bot_bullets = []

    sphere_drops = []

    arena_mode = False
    arena_enemies = []
    arena_return_x = player_x
    arena_return_y = player_y
    arena_return_teleport_zone = teleport_zone
    arena_reward_given = False
    arena_dog_was_active = False

    hotspot_safe_zone_rect = None
    generators = []
    hotspot_monsters = []
    hotspot_bushes = []
    base_werstak_pos = None
    base_safe_pos = None
    base_teleport_pos = None

    if current_location == "hotspot":
        hotspot_safe_zone_rect, generators, hotspot_monsters, hotspot_bushes = init_hotspot()
        player_x, player_y = hotspot_safe_zone_rect.centerx, hotspot_safe_zone_rect.centery
    elif current_location == "base_home":
        base_werstak_pos, base_safe_pos, base_teleport_pos = init_base_home()
        player_x, player_y = MAP_SIZE_ARENA//2, MAP_SIZE_ARENA//2

    frame = 0
    player_direction = 'down'
    cooldown = 0
    ammo = 15
    reloading = False
    reload_timer = 0
    damage_cooldown = 0
    step_timer = 0
    hp_drain_timer = 0
    rust_production_timer = 0

    shoot_anim_timer = 0
    shoot_img = None

    # Фон безопасной зоны
    safe_zone_surface = pygame.Surface((SAFE_ZONE_SIZE, SAFE_ZONE_SIZE))
    safe_zone_surface.fill((0, 200, 0))

    # ---- СЕНСОРНОЕ УПРАВЛЕНИЕ ----
    joystick_center = (int(WIDTH * 0.12), int(HEIGHT * 0.85))
    joystick_radius = int(min(WIDTH, HEIGHT) * 0.09)
    joystick_knob_radius = int(joystick_radius * 0.45)
    joystick_active = False
    joystick_dx = 0.0
    joystick_dy = 0.0
    joystick_pressed = False

    # Кнопки (увеличенные)
    button_size = int(min(WIDTH, HEIGHT) * 0.075)
    spacing = int(button_size * 0.2)
    # Расположение: 3 ряда по 4, 4, 3
    rows_layout = [
        ['1','2','3','4'],
        ['E','R','G','F'],
        ['Esc','I','A']
    ]
    button_rects = {}
    start_x = WIDTH - button_size - (button_size + spacing) * 3 - 10
    start_y = HEIGHT - button_size - (button_size + spacing) * 2 - 10
    for row_idx, row in enumerate(rows_layout):
        for col_idx, key in enumerate(row):
            x = start_x + col_idx * (button_size + spacing)
            y = start_y + row_idx * (button_size + spacing)
            rect = pygame.Rect(x, y, button_size, button_size)
            button_rects[key] = {'rect': rect, 'pressed': False}

    # ---- ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ (магазин, крафт, меню базы) ----
    def show_shop_menu():
        nonlocal gold, iron, rust, weapon, armor, dog_active, cooldown, ammo, reloading, reload_timer, owned_weapons
        menu_open = True
        menu_w = int(WIDTH * 0.8)
        menu_h = int(HEIGHT * 0.7)
        menu_x = WIDTH // 2 - menu_w // 2
        menu_y = HEIGHT // 2 - menu_h // 2
        btn_w = int(menu_w * 0.35)
        btn_h = int(menu_h * 0.1)
        btn_shotgun = pygame.Rect(menu_x + 20, menu_y + 100, btn_w, btn_h)
        btn_armor   = pygame.Rect(menu_x + menu_w - btn_w - 20, menu_y + 100, btn_w, btn_h)
        btn_rpg     = pygame.Rect(menu_x + 20, menu_y + 100 + btn_h + 10, btn_w, btn_h)
        btn_dog     = pygame.Rect(menu_x + menu_w - btn_w - 20, menu_y + 100 + btn_h + 10, btn_w, btn_h)
        btn_close   = pygame.Rect(menu_x + menu_w//2 - btn_w//2, menu_y + menu_h - btn_h - 20, btn_w, btn_h)

        shotgun_cost_rust = 25
        armor_cost_iron = 50
        rpg_cost_gold = 25
        dog_cost_gold = 400

        while menu_open:
            mouse_pos = pygame.mouse.get_pos()
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(180)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))
            pygame.draw.rect(screen, (50, 50, 50), (menu_x, menu_y, menu_w, menu_h), border_radius=15)
            pygame.draw.rect(screen, (100, 100, 100), (menu_x, menu_y, menu_w, menu_h), width=3, border_radius=15)

            title = font_big.render("Магазин", True, (255, 255, 0))
            title_rect = title.get_rect(center=(menu_x + menu_w // 2, menu_y + 30))
            screen.blit(title, title_rect)

            if "shotgun" in owned_weapons:
                btn_shotgun_text = "Дробовик (выбрать)"
            else:
                btn_shotgun_text = f"Дробовик ({shotgun_cost_rust} ржавчины)"
            draw_button(screen, btn_shotgun_text, btn_shotgun, btn_shotgun.collidepoint(mouse_pos), small_font=True)

            draw_button(screen, f"Броня ({armor_cost_iron} железа)", btn_armor, btn_armor.collidepoint(mouse_pos), small_font=True)

            if "rpg" in owned_weapons:
                btn_rpg_text = "RPG (выбрать)"
            else:
                btn_rpg_text = f"RPG ({rpg_cost_gold} золота)"
            draw_button(screen, btn_rpg_text, btn_rpg, btn_rpg.collidepoint(mouse_pos), small_font=True)

            draw_button(screen, f"Собака ({dog_cost_gold} золота)", btn_dog, btn_dog.collidepoint(mouse_pos), small_font=True)
            draw_button(screen, "Закрыть", btn_close, btn_close.collidepoint(mouse_pos))

            current_weapon = f"Оружие: {weapon}"
            current_armor = f"Броня: {armor}/100"
            screen.blit(font.render(current_weapon, True, (200, 200, 200)), (menu_x + 20, menu_y + 280))
            screen.blit(font.render(current_armor, True, (200, 200, 200)), (menu_x + menu_w//2 + 20, menu_y + 280))

            pygame.display.flip()

            for e in pygame.event.get():
                if e.type == pygame.MOUSEBUTTONDOWN:
                    if btn_shotgun.collidepoint(e.pos):
                        if "shotgun" in owned_weapons:
                            weapon = "shotgun"
                            ammo = 15
                            reloading = False
                            reload_timer = 0
                        else:
                            if rust >= shotgun_cost_rust:
                                rust -= shotgun_cost_rust
                                owned_weapons.append("shotgun")
                                weapon = "shotgun"
                                ammo = 15
                                reloading = False
                                reload_timer = 0
                    elif btn_armor.collidepoint(e.pos):
                        if iron >= armor_cost_iron:
                            iron -= armor_cost_iron
                            armor = 100
                    elif btn_rpg.collidepoint(e.pos):
                        if "rpg" in owned_weapons:
                            weapon = "rpg"
                            ammo = 15
                            reloading = False
                            reload_timer = 0
                        else:
                            if gold >= rpg_cost_gold:
                                gold -= rpg_cost_gold
                                owned_weapons.append("rpg")
                                weapon = "rpg"
                    elif btn_dog.collidepoint(e.pos):
                        if gold >= dog_cost_gold and not dog_active:
                            gold -= dog_cost_gold
                            dog_active = True
                    elif btn_close.collidepoint(e.pos):
                        menu_open = False
                if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    menu_open = False

    def show_craft_menu():
        nonlocal gold, iron, armor, weapon, owned_weapons, craft_menu_open
        menu_open = True
        menu_w = int(WIDTH * 0.7)
        menu_h = int(HEIGHT * 0.55)
        menu_x = WIDTH // 2 - menu_w // 2
        menu_y = HEIGHT // 2 - menu_h // 2
        btn_w = int(menu_w * 0.35)
        btn_h = int(menu_h * 0.25)
        btn_armor_rect = pygame.Rect(menu_x + 20, menu_y + 100, btn_w, btn_h)
        btn_rifle_rect = pygame.Rect(menu_x + menu_w - btn_w - 20, menu_y + 100, btn_w, btn_h)
        btn_close_rect = pygame.Rect(menu_x + menu_w//2 - btn_w//2, menu_y + menu_h - btn_h - 20, btn_w, btn_h)

        while menu_open:
            mouse_pos = pygame.mouse.get_pos()
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(180)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))
            pygame.draw.rect(screen, (50, 50, 50), (menu_x, menu_y, menu_w, menu_h), border_radius=15)
            pygame.draw.rect(screen, (100, 100, 100), (menu_x, menu_y, menu_w, menu_h), width=3, border_radius=15)

            title = font_big.render("Крафт", True, (255, 255, 0))
            title_rect = title.get_rect(center=(menu_x + menu_w // 2, menu_y + 40))
            screen.blit(title, title_rect)

            screen.blit(broni_img, (btn_armor_rect.x + 10, btn_armor_rect.y + 10))
            armor_text = font.render("Броня", True, (255, 255, 255))
            screen.blit(armor_text, (btn_armor_rect.x + 10, btn_armor_rect.y + btn_h - 30))
            armor_cost = font.render("50 железа", True, (200, 200, 200))
            screen.blit(armor_cost, (btn_armor_rect.x + 10, btn_armor_rect.y + btn_h - 10))
            if btn_armor_rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, (76, 175, 80), btn_armor_rect, border_radius=10, width=4)
            else:
                pygame.draw.rect(screen, (100, 100, 100), btn_armor_rect, border_radius=10, width=2)

            screen.blit(vintovka_img, (btn_rifle_rect.x + 10, btn_rifle_rect.y + 10))
            rifle_text = font.render("Винтовка", True, (255, 255, 255))
            screen.blit(rifle_text, (btn_rifle_rect.x + 10, btn_rifle_rect.y + btn_h - 30))
            rifle_cost = font.render("300 золота", True, (200, 200, 200))
            screen.blit(rifle_cost, (btn_rifle_rect.x + 10, btn_rifle_rect.y + btn_h - 10))
            if btn_rifle_rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, (76, 175, 80), btn_rifle_rect, border_radius=10, width=4)
            else:
                pygame.draw.rect(screen, (100, 100, 100), btn_rifle_rect, border_radius=10, width=2)

            draw_button(screen, "Закрыть", btn_close_rect, btn_close_rect.collidepoint(mouse_pos))

            pygame.display.flip()

            for e in pygame.event.get():
                if e.type == pygame.MOUSEBUTTONDOWN:
                    if btn_armor_rect.collidepoint(e.pos):
                        if iron >= 50:
                            iron -= 50
                            armor = 100
                            overlay2 = pygame.Surface((WIDTH, HEIGHT))
                            overlay2.set_alpha(180)
                            overlay2.fill((0, 0, 0))
                            screen.blit(overlay2, (0, 0))
                            msg = font.render("Броня создана!", True, (0, 255, 0))
                            msg_rect = msg.get_rect(center=(WIDTH//2, HEIGHT//2))
                            screen.blit(msg, msg_rect)
                            pygame.display.flip()
                            pygame.time.wait(1000)
                        else:
                            overlay2 = pygame.Surface((WIDTH, HEIGHT))
                            overlay2.set_alpha(180)
                            overlay2.fill((0, 0, 0))
                            screen.blit(overlay2, (0, 0))
                            msg = font.render("Не хватает железа!", True, (255, 0, 0))
                            msg_rect = msg.get_rect(center=(WIDTH//2, HEIGHT//2))
                            screen.blit(msg, msg_rect)
                            pygame.display.flip()
                            pygame.time.wait(1000)
                    elif btn_rifle_rect.collidepoint(e.pos):
                        if gold >= 300:
                            gold -= 300
                            if "sniper" not in owned_weapons:
                                owned_weapons.append("sniper")
                            weapon = "sniper"
                            overlay2 = pygame.Surface((WIDTH, HEIGHT))
                            overlay2.set_alpha(180)
                            overlay2.fill((0, 0, 0))
                            screen.blit(overlay2, (0, 0))
                            msg = font.render("Винтовка создана!", True, (0, 255, 0))
                            msg_rect = msg.get_rect(center=(WIDTH//2, HEIGHT//2))
                            screen.blit(msg, msg_rect)
                            pygame.display.flip()
                            pygame.time.wait(1000)
                        else:
                            overlay2 = pygame.Surface((WIDTH, HEIGHT))
                            overlay2.set_alpha(180)
                            overlay2.fill((0, 0, 0))
                            screen.blit(overlay2, (0, 0))
                            msg = font.render("Не хватает золота!", True, (255, 0, 0))
                            msg_rect = msg.get_rect(center=(WIDTH//2, HEIGHT//2))
                            screen.blit(msg, msg_rect)
                            pygame.display.flip()
                            pygame.time.wait(1000)
                    elif btn_close_rect.collidepoint(e.pos):
                        menu_open = False
                        craft_menu_open = False
                if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    menu_open = False
                    craft_menu_open = False

    def show_base_menu():
        nonlocal sphere_count, stored_spheres, sphere_buff_timer
        menu_open = True
        menu_w = int(WIDTH * 0.7)
        menu_h = int(HEIGHT * 0.6)
        menu_x = WIDTH // 2 - menu_w // 2
        menu_y = HEIGHT // 2 - menu_h // 2

        btn_w = int(menu_w * 0.35)
        btn_h = int(menu_h * 0.1)
        btn_deposit = pygame.Rect(menu_x + 20, menu_y + 140, btn_w, btn_h)
        btn_withdraw = pygame.Rect(menu_x + menu_w - btn_w - 20, menu_y + 140, btn_w, btn_h)
        btn_enchant = pygame.Rect(menu_x + menu_w//2 - btn_w//2, menu_y + 140 + btn_h + 10, btn_w, btn_h)
        btn_close = pygame.Rect(menu_x + menu_w//2 - btn_w//2, menu_y + menu_h - btn_h - 20, btn_w, btn_h)

        while menu_open:
            mouse_pos = pygame.mouse.get_pos()
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(180)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))
            pygame.draw.rect(screen, (50, 50, 50), (menu_x, menu_y, menu_w, menu_h), border_radius=15)
            pygame.draw.rect(screen, (100, 100, 100), (menu_x, menu_y, menu_w, menu_h), width=3, border_radius=15)

            title = font_big.render("База", True, (255, 255, 0))
            title_rect = title.get_rect(center=(menu_x + menu_w // 2, menu_y + 30))
            screen.blit(title, title_rect)

            inv_text = font.render(f"Сферы в инвентаре: {sphere_count}", True, (255, 255, 255))
            screen.blit(inv_text, (menu_x + 20, menu_y + 80))
            stored_text = font.render(f"Сфер в хранилище: {stored_spheres}", True, (255, 255, 200))
            screen.blit(stored_text, (menu_x + 20, menu_y + 110))

            draw_button(screen, "Сложить сферы", btn_deposit, btn_deposit.collidepoint(mouse_pos), small_font=True)
            draw_button(screen, "Забрать сферы", btn_withdraw, btn_withdraw.collidepoint(mouse_pos), small_font=True)
            if sphere_buff_timer > 0:
                btn_text = f"Зачаровать (активно {sphere_buff_timer//3600} мин)"
                draw_button(screen, btn_text, btn_enchant, False, small_font=True)
            else:
                draw_button(screen, "Зачаровать (30 мин)", btn_enchant, btn_enchant.collidepoint(mouse_pos), small_font=True)

            draw_button(screen, "Закрыть", btn_close, btn_close.collidepoint(mouse_pos))

            pygame.display.flip()

            for e in pygame.event.get():
                if e.type == pygame.MOUSEBUTTONDOWN:
                    if btn_deposit.collidepoint(e.pos):
                        if sphere_count > 0:
                            stored_spheres += sphere_count
                            sphere_count = 0
                    elif btn_withdraw.collidepoint(e.pos):
                        if stored_spheres > 0:
                            sphere_count += stored_spheres
                            stored_spheres = 0
                    elif btn_enchant.collidepoint(e.pos):
                        if stored_spheres > 0 and sphere_buff_timer <= 0:
                            stored_spheres -= 1
                            sphere_buff_timer = 30 * 60 * 60
                    elif btn_close.collidepoint(e.pos):
                        menu_open = False
                if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    menu_open = False

    # ---- ФУНКЦИЯ ПОИСКА БЛИЖАЙШЕГО ВРАГА ----
    def find_nearest_enemy():
        enemies = []
        if arena_mode:
            enemies = arena_enemies
        else:
            if current_location == "bases":
                for bots in bases_bots:
                    for bot in bots:
                        enemies.append((bot[0], bot[1]))
            elif current_location == "hotspot":
                enemies = hotspot_monsters
            else:
                enemies.extend(zombies)
                enemies.extend(wolves)
                enemies.extend(bears)
                if boss:
                    enemies.append((boss[0], boss[1]))
        if not enemies:
            return None
        nearest = None
        min_dist = float('inf')
        for enemy in enemies:
            if isinstance(enemy, list):
                ex, ey = enemy[0], enemy[1]
            else:
                ex, ey = enemy[0], enemy[1]
            dist = math.hypot(player_x - ex, player_y - ey)
            if dist < min_dist:
                min_dist = dist
                nearest = (ex, ey)
        return nearest

    # ---- ФУНКЦИЯ АТАКИ ПО БЛИЖАЙШЕМУ ----
    def attack_nearest():
        nonlocal ammo, reloading, reload_timer, shoot_img, shoot_anim_timer
        if reloading or ammo <= 0 or craft_menu_open or inventory_open or bike_active:
            return
        target = find_nearest_enemy()
        if target is None:
            return
        tx, ty = target
        dx, dy = tx - player_x, ty - player_y
        d = math.hypot(dx, dy)
        if d == 0:
            return
        dx, dy = dx/d, dy/d
        damage_mult = 2 if (rubin_buff_timer > 0 or sphere_buff_timer > 0) else 1
        if weapon == "pistol":
            bullets.append([player_x, player_y, dx, dy, "pistol", damage_mult])
            shoot_img = pistol_img
            shoot_anim_timer = 8
        elif weapon == "shotgun":
            for spread in [-0.35, -0.18, 0, 0.18, 0.35]:
                angle = math.atan2(dy, dx) + spread
                sx = math.cos(angle)
                sy = math.sin(angle)
                bullets.append([player_x, player_y, sx, sy, "shotgun", damage_mult])
            shoot_img = shotgun_img
            shoot_anim_timer = 8
        elif weapon == "rpg":
            bullets.append([player_x, player_y, dx, dy, "rpg", damage_mult])
            shoot_img = rpg_img
            shoot_anim_timer = 8
        elif weapon == "sniper":
            bullets.append([player_x, player_y, dx, dy, "pistol", 10 * damage_mult])
            shoot_img = wintiwka_img
            shoot_anim_timer = 8
        ammo -= 1
        if ammo <= 0:
            reloading = True

    # ---- ОСНОВНОЙ ИГРОВОЙ ЦИКЛ ----
    while True:
        dt = clock.tick(60) / 16.67

        # ---- ОБРАБОТКА СОБЫТИЙ ----
        ui_handled = False
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_r and not reloading:
                    reloading = True
                    reload_timer = 0
                if e.key == pygame.K_g and bike_owned and not arena_mode:
                    bike_active = not bike_active
                if e.key == pygame.K_1:
                    if teleport_zone and not arena_mode and math.hypot(player_x - bike_trader_x, player_y - bike_trader_y) < 150:
                        if gold >= 100 and iron >= 50 and not bike_owned:
                            gold -= 100
                            iron -= 50
                            bike_owned = True
                if e.key == pygame.K_ESCAPE and not arena_mode:
                    save_game({
                        "player_x": player_x, "player_y": player_y, "teleport_zone": teleport_zone,
                        "hp": hp, "armor": armor, "gold": gold, "weapon": weapon, "berries": berries,
                        "iron": iron, "rust": rust, "bike_owned": bike_owned, "dog_active": dog_active,
                        "dog_x": dog_x, "dog_y": dog_y, "quest_active": quest_active,
                        "zombies_killed": zombies_killed, "quest_target": quest_target,
                        "xp": xp, "level": level, "next_level_xp": next_level_xp,
                        "berry_quest_active": berry_quest_active, "berry_quest_target": berry_quest_target,
                        "berry_reward": berry_reward, "boss_quest_active": boss_quest_active,
                        "boss_quest_done": boss_quest_done, "boss_quest_killed": boss_quest_killed,
                        "current_location": current_location, "bases_captured": bases_captured,
                        "bases_bots": bases_bots, "rust_timers": rust_timers,
                        "svetilo_count": svetilo_count, "ldishka_count": ldishka_count,
                        "rubin_count": rubin_count, "owned_weapons": owned_weapons,
                        "sphere_count": sphere_count, "stored_spheres": stored_spheres,
                        "sphere_buff_timer": sphere_buff_timer
                    })
                    return
                if e.key == pygame.K_i and not arena_mode:
                    inventory_open = not inventory_open
                if e.key == pygame.K_f and not arena_mode and current_location != "bases" and current_location != "hotspot":
                    for b in bushes:
                        if b[2] and math.hypot(player_x - b[0], player_y - b[1]) < 80:
                            berries += 1
                            b[2] = False
                            b[3] = 600
                if e.key == pygame.K_f and not arena_mode and current_location == "hotspot":
                    for b in hotspot_bushes:
                        if b[2] and math.hypot(player_x - b[0], player_y - b[1]) < 80:
                            berries += 1
                            b[2] = False
                            b[3] = 600

            # Обработка взаимодействия E
            if e.type == pygame.KEYDOWN and e.key == pygame.K_e and not arena_mode:
                if current_location == "bases":
                    obj3_x = SAFE_ZONE_RECT.centerx - object3.get_width()//2
                    obj3_y = SAFE_ZONE_RECT.centery - object3.get_height()//2
                    if math.hypot(player_x - obj3_x, player_y - obj3_y) < 120:
                        selected = location_menu()
                        if selected is not None:
                            player_x, player_y = selected["pos"]
                            if selected["teleport_zone"] == "bases":
                                current_location = "bases"
                                teleport_zone = False
                            elif selected["teleport_zone"] == "base_home":
                                current_location = "base_home"
                                teleport_zone = False
                                base_werstak_pos, base_safe_pos, base_teleport_pos = init_base_home()
                                player_x, player_y = MAP_SIZE_ARENA//2, MAP_SIZE_ARENA//2
                            elif selected["teleport_zone"] == "hotspot":
                                current_location = "hotspot"
                                teleport_zone = False
                                hotspot_safe_zone_rect, generators, hotspot_monsters, hotspot_bushes = init_hotspot()
                                player_x, player_y = hotspot_safe_zone_rect.centerx, hotspot_safe_zone_rect.centery
                            else:
                                current_location = "home" if not selected["teleport_zone"] else "monster"
                                teleport_zone = selected["teleport_zone"]
                            if dog_active:
                                dog_x, dog_y = player_x + 50, player_y + 50
                            boss = None
                            boss_spawn_timer = 0
                            boss_life_timer = 0
                            update_anomalies_for_location(current_location)
                elif current_location == "base_home":
                    if base_werstak_pos and math.hypot(player_x - base_werstak_pos[0], player_y - base_werstak_pos[1]) < 120:
                        show_base_menu()
                    if base_teleport_pos and math.hypot(player_x - base_teleport_pos[0], player_y - base_teleport_pos[1]) < 120:
                        selected = location_menu()
                        if selected is not None:
                            player_x, player_y = selected["pos"]
                            if selected["teleport_zone"] == "bases":
                                current_location = "bases"
                                teleport_zone = False
                            elif selected["teleport_zone"] == "base_home":
                                current_location = "base_home"
                                teleport_zone = False
                                base_werstak_pos, base_safe_pos, base_teleport_pos = init_base_home()
                                player_x, player_y = MAP_SIZE_ARENA//2, MAP_SIZE_ARENA//2
                            elif selected["teleport_zone"] == "hotspot":
                                current_location = "hotspot"
                                teleport_zone = False
                                hotspot_safe_zone_rect, generators, hotspot_monsters, hotspot_bushes = init_hotspot()
                                player_x, player_y = hotspot_safe_zone_rect.centerx, hotspot_safe_zone_rect.centery
                            else:
                                current_location = "home" if not selected["teleport_zone"] else "monster"
                                teleport_zone = selected["teleport_zone"]
                            if dog_active:
                                dog_x, dog_y = player_x + 50, player_y + 50
                            boss = None
                            boss_spawn_timer = 0
                            boss_life_timer = 0
                            update_anomalies_for_location(current_location)
                elif current_location == "hotspot":
                    if hotspot_safe_zone_rect is not None and hotspot_safe_zone_rect.collidepoint(player_x, player_y):
                        center_x = hotspot_safe_zone_rect.centerx
                        center_y = hotspot_safe_zone_rect.centery
                        if math.hypot(player_x - center_x, player_y - center_y) < 120:
                            selected = location_menu()
                            if selected is not None:
                                player_x, player_y = selected["pos"]
                                if selected["teleport_zone"] == "bases":
                                    current_location = "bases"
                                    teleport_zone = False
                                elif selected["teleport_zone"] == "base_home":
                                    current_location = "base_home"
                                    teleport_zone = False
                                    base_werstak_pos, base_safe_pos, base_teleport_pos = init_base_home()
                                    player_x, player_y = MAP_SIZE_ARENA//2, MAP_SIZE_ARENA//2
                                elif selected["teleport_zone"] == "hotspot":
                                    current_location = "hotspot"
                                    teleport_zone = False
                                    hotspot_safe_zone_rect, generators, hotspot_monsters, hotspot_bushes = init_hotspot()
                                    player_x, player_y = hotspot_safe_zone_rect.centerx, hotspot_safe_zone_rect.centery
                                else:
                                    current_location = "home" if not selected["teleport_zone"] else "monster"
                                    teleport_zone = selected["teleport_zone"]
                                if dog_active:
                                    dog_x, dog_y = player_x + 50, player_y + 50
                                boss = None
                                boss_spawn_timer = 0
                                boss_life_timer = 0
                                update_anomalies_for_location(current_location)
                else:
                    npc_x, npc_y = objs[0]
                    npc_rect = pygame.Rect(npc_x, npc_y, object1.get_width(), object1.get_height()).inflate(220, 220)
                    if current_location != "monster" and npc_rect.collidepoint(player_x, player_y):
                        if not quest_active:
                            if quest_menu("zombie", quest_target, quest_target * 3, active=False):
                                quest_active = True
                                zombies_killed = 0
                        else:
                            quest_menu("zombie", quest_target, quest_target * 3, active=True)
                    berry_x, berry_y = objs[3]
                    if current_location != "monster" and math.hypot(player_x - berry_x, player_y - berry_y) < 120:
                        if not berry_quest_active:
                            if quest_menu("berry", berry_quest_target, berry_reward, active=False):
                                berry_quest_active = True
                        else:
                            if berries >= berry_quest_target:
                                berries -= berry_quest_target
                                rust += berry_reward
                                overlay = pygame.Surface((WIDTH, HEIGHT))
                                overlay.set_alpha(180)
                                overlay.fill((0, 0, 0))
                                screen.blit(overlay, (0, 0))
                                msg = font.render(f"Задание выполнено! +{berry_reward} ржавчины", True, (0, 255, 0))
                                msg_rect = msg.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                                screen.blit(msg, msg_rect)
                                pygame.display.flip()
                                pygame.time.wait(1500)
                                berry_quest_target += 5
                                berry_reward += 2
                                berry_quest_active = False
                            else:
                                quest_menu("berry", berry_quest_target, berry_reward, active=True)
                    if teleport_zone and math.hypot(player_x - boss_npc_x, player_y - boss_npc_y) < 140:
                        if not boss_quest_active and not boss_quest_done:
                            if quest_menu("boss", 1, 5, active=False):
                                boss_quest_active = True
                                boss_quest_killed = 0
                        elif boss_quest_active and not boss_quest_done:
                            quest_menu("boss", 1, 5, active=True)
                    obj3_x, obj3_y = objs[2]
                    if math.hypot(player_x - obj3_x, player_y - obj3_y) < 120:
                        selected = location_menu()
                        if selected is not None:
                            player_x, player_y = selected["pos"]
                            if selected["teleport_zone"] == "bases":
                                current_location = "bases"
                                teleport_zone = False
                            elif selected["teleport_zone"] == "base_home":
                                current_location = "base_home"
                                teleport_zone = False
                                base_werstak_pos, base_safe_pos, base_teleport_pos = init_base_home()
                                player_x, player_y = MAP_SIZE_ARENA//2, MAP_SIZE_ARENA//2
                            elif selected["teleport_zone"] == "hotspot":
                                current_location = "hotspot"
                                teleport_zone = False
                                hotspot_safe_zone_rect, generators, hotspot_monsters, hotspot_bushes = init_hotspot()
                                player_x, player_y = hotspot_safe_zone_rect.centerx, hotspot_safe_zone_rect.centery
                            else:
                                current_location = "home" if not selected["teleport_zone"] else "monster"
                                teleport_zone = selected["teleport_zone"]
                            if dog_active:
                                dog_x, dog_y = player_x + 50, player_y + 50
                            boss = None
                            boss_spawn_timer = 0
                            boss_life_timer = 0
                            update_anomalies_for_location(current_location)
                    if teleport_zone and math.hypot(player_x - secret_x, player_y - secret_y) < 120:
                        selected = location_menu()
                        if selected is not None:
                            player_x, player_y = selected["pos"]
                            if selected["teleport_zone"] == "bases":
                                current_location = "bases"
                                teleport_zone = False
                            elif selected["teleport_zone"] == "base_home":
                                current_location = "base_home"
                                teleport_zone = False
                                base_werstak_pos, base_safe_pos, base_teleport_pos = init_base_home()
                                player_x, player_y = MAP_SIZE_ARENA//2, MAP_SIZE_ARENA//2
                            elif selected["teleport_zone"] == "hotspot":
                                current_location = "hotspot"
                                teleport_zone = False
                                hotspot_safe_zone_rect, generators, hotspot_monsters, hotspot_bushes = init_hotspot()
                                player_x, player_y = hotspot_safe_zone_rect.centerx, hotspot_safe_zone_rect.centery
                            else:
                                current_location = "home" if not selected["teleport_zone"] else "monster"
                                teleport_zone = selected["teleport_zone"]
                            if dog_active:
                                dog_x, dog_y = player_x + 50, player_y + 50
                            boss = None
                            boss_spawn_timer = 0
                            boss_life_timer = 0
                            update_anomalies_for_location(current_location)

            # ---- ОБРАБОТКА СЕНСОРНОГО УПРАВЛЕНИЯ ----
            if e.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = e.pos
                # Джойстик
                if math.hypot(mouse_pos[0] - joystick_center[0], mouse_pos[1] - joystick_center[1]) < joystick_radius + 20:
                    joystick_active = True
                    joystick_pressed = True
                    ui_handled = True
                    dx = mouse_pos[0] - joystick_center[0]
                    dy = mouse_pos[1] - joystick_center[1]
                    dist = math.hypot(dx, dy)
                    if dist > joystick_radius:
                        dx = dx / dist * joystick_radius
                        dy = dy / dist * joystick_radius
                    joystick_dx = dx / joystick_radius
                    joystick_dy = dy / joystick_radius
                else:
                    # Кнопки
                    for key, btn_data in button_rects.items():
                        if btn_data['rect'].collidepoint(mouse_pos):
                            btn_data['pressed'] = True
                            ui_handled = True
                            if key == 'A':
                                attack_nearest()
                            else:
                                key_map = {
                                    '1': pygame.K_1, '2': pygame.K_2, '3': pygame.K_3, '4': pygame.K_4,
                                    'E': pygame.K_e, 'R': pygame.K_r, 'G': pygame.K_g, 'F': pygame.K_f,
                                    'Esc': pygame.K_ESCAPE, 'I': pygame.K_i
                                }
                                key_code = key_map.get(key)
                                if key_code is not None:
                                    ev = pygame.event.Event(pygame.KEYDOWN, {'key': key_code, 'mod': 0, 'unicode': ''})
                                    pygame.event.post(ev)
                            break

            elif e.type == pygame.MOUSEMOTION:
                if joystick_active:
                    dx = e.pos[0] - joystick_center[0]
                    dy = e.pos[1] - joystick_center[1]
                    dist = math.hypot(dx, dy)
                    if dist > joystick_radius:
                        dx = dx / dist * joystick_radius
                        dy = dy / dist * joystick_radius
                    joystick_dx = dx / joystick_radius
                    joystick_dy = dy / joystick_radius
                    ui_handled = True

            elif e.type == pygame.MOUSEBUTTONUP:
                if joystick_active:
                    joystick_active = False
                    joystick_dx = 0.0
                    joystick_dy = 0.0
                    joystick_pressed = False
                    ui_handled = True
                for btn_data in button_rects.values():
                    btn_data['pressed'] = False

            # ---- СТАНДАРТНАЯ СТРЕЛЬБА МЫШЬЮ ----
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 and not ui_handled:
                if not craft_menu_open and not inventory_open and not bike_active and not reloading and ammo > 0 and not craft_menu_open:
                    mx, my = e.pos
                    wx = mx + (player_x - WIDTH // 2)
                    wy = my + (player_y - HEIGHT // 2)
                    dx, dy = wx - player_x, wy - player_y
                    d = math.hypot(dx, dy)
                    if d != 0:
                        dx, dy = dx / d, dy / d
                    damage_mult = 2 if (rubin_buff_timer > 0 or sphere_buff_timer > 0) else 1
                    if weapon == "pistol":
                        bullets.append([player_x, player_y, dx, dy, "pistol", damage_mult])
                        shoot_img = pistol_img
                        shoot_anim_timer = 8
                    elif weapon == "shotgun":
                        for spread in [-0.35, -0.18, 0, 0.18, 0.35]:
                            angle = math.atan2(dy, dx) + spread
                            sx = math.cos(angle)
                            sy = math.sin(angle)
                            bullets.append([player_x, player_y, sx, sy, "shotgun", damage_mult])
                        shoot_img = shotgun_img
                        shoot_anim_timer = 8
                    elif weapon == "rpg":
                        bullets.append([player_x, player_y, dx, dy, "rpg", damage_mult])
                        shoot_img = rpg_img
                        shoot_anim_timer = 8
                    elif weapon == "sniper":
                        bullets.append([player_x, player_y, dx, dy, "pistol", 10 * damage_mult])
                        shoot_img = wintiwka_img
                        shoot_anim_timer = 8
                    ammo -= 1

        # ---- ДВИЖЕНИЕ ----
        keys = pygame.key.get_pressed()
        moving = False
        base_speed = 5
        if ldishka_buff_timer > 0:
            speed = base_speed * 1.5 * dt
        else:
            speed = base_speed * dt
        if bike_active:
            speed = 10 * dt
        old_x, old_y = player_x, player_y

        new_x, new_y = player_x, player_y

        # Клавиатура
        if keys[pygame.K_w]:
            new_y -= speed
            bike_direction = "up"
            moving = True
        if keys[pygame.K_s]:
            new_y += speed
            bike_direction = "down"
            moving = True
        if keys[pygame.K_a]:
            new_x -= speed
            bike_direction = "left"
            moving = True
        if keys[pygame.K_d]:
            new_x += speed
            bike_direction = "right"
            moving = True

        # Джойстик
        if joystick_active and (abs(joystick_dx) > 0.1 or abs(joystick_dy) > 0.1):
            dx = joystick_dx
            dy = joystick_dy
            if abs(dx) > abs(dy):
                if dx > 0:
                    player_direction = "right"
                else:
                    player_direction = "left"
            else:
                if dy > 0:
                    player_direction = "down"
                else:
                    player_direction = "up"
            new_x += dx * speed
            new_y += dy * speed
            moving = True
            if bike_active:
                if abs(dx) > abs(dy):
                    if dx > 0:
                        bike_direction = "right"
                    else:
                        bike_direction = "left"
                else:
                    if dy > 0:
                        bike_direction = "down"
                    else:
                        bike_direction = "up"

        # ---- КОЛЛИЗИИ ----
        if current_location == "bases":
            player_rect = pygame.Rect(new_x - 10, new_y - 10, 20, 20)
            blocked = False
            for frect in farn_rects:
                if player_rect.colliderect(frect):
                    blocked = True
                    break
            if not blocked:
                player_x, player_y = new_x, new_y
            else:
                if keys[pygame.K_w] or keys[pygame.K_s] or (joystick_active and abs(joystick_dy) > 0.1):
                    new_x = player_x
                    player_rect = pygame.Rect(new_x - 10, new_y - 10, 20, 20)
                    blocked = False
                    for frect in farn_rects:
                        if player_rect.colliderect(frect):
                            blocked = True
                            break
                    if not blocked:
                        player_y = new_y
                if keys[pygame.K_a] or keys[pygame.K_d] or (joystick_active and abs(joystick_dx) > 0.1):
                    new_y = player_y
                    player_rect = pygame.Rect(new_x - 10, new_y - 10, 20, 20)
                    blocked = False
                    for frect in farn_rects:
                        if player_rect.colliderect(frect):
                            blocked = True
                            break
                    if not blocked:
                        player_x = new_x
        elif current_location == "base_home":
            player_x = max(wall_size, min(MAP_SIZE_ARENA - wall_size, new_x))
            player_y = max(wall_size, min(MAP_SIZE_ARENA - wall_size, new_y))
            player_rect_coll = pygame.Rect(player_x - 15, player_y - 15, 30, 30)
            for wall_rect in arena_wall_rects:
                if player_rect_coll.colliderect(wall_rect):
                    player_x, player_y = old_x, old_y
                    break
        elif current_location == "hotspot":
            player_x = max(wall_size, min(MAP_SIZE - wall_size, new_x))
            player_y = max(wall_size, min(MAP_SIZE - wall_size, new_y))
        else:
            player_x, player_y = new_x, new_y
            if current_location not in ["bases", "base_home", "hotspot"]:
                player_rect_coll = pygame.Rect(player_x - 15, player_y - 15, 30, 30)
                for wall_rect in wall_rects:
                    if player_rect_coll.colliderect(wall_rect):
                        player_x, player_y = old_x, old_y
                        break
                if not teleport_zone:
                    shop_x, shop_y = objs[1]
                    if math.hypot(player_x - (shop_x + object2.get_width()//2), player_y - (shop_y + object2.get_height()//2)) < 60:
                        player_x, player_y = old_x, old_y
                    npc_x, npc_y = objs[0]
                    if math.hypot(player_x - (npc_x + object1.get_width()//2), player_y - (npc_y + object1.get_height()//2)) < 60:
                        player_x, player_y = old_x, old_y
                player_x = max(wall_size, min(MAP_SIZE - wall_size, player_x))
                player_y = max(wall_size, min(MAP_SIZE - wall_size, player_y))

                player_hitbox = pygame.Rect(player_x - 10, player_y - 10, 20, 20)
                for trunk_rect in tree_rects:
                    if player_hitbox.colliderect(trunk_rect):
                        player_x, player_y = old_x, old_y
                        break

        if arena_mode:
            player_rect_coll = pygame.Rect(player_x - 15, player_y - 15, 30, 30)
            for wall_rect in arena_wall_rects:
                if player_rect_coll.colliderect(wall_rect):
                    player_x, player_y = old_x, old_y
                    break

        if moving and not bike_active:
            step_timer += 1
            if step_timer >= 18:
                step_timer = 0

        if cooldown > 0:
            cooldown -= 1
        if damage_cooldown > 0:
            damage_cooldown -= 1

        if ammo <= 0 and not reloading:
            reloading = True
        if reloading:
            reload_timer += 1
            if reload_timer >= 120:
                ammo = 15
                reload_timer = 0
                reloading = False

        # ---- СОБАКА ----
        if dog_active and not arena_mode:
            old_dog_x, old_dog_y = dog_x, dog_y
            dx, dy = player_x - dog_x, player_y - dog_y
            dist = math.hypot(dx, dy)
            if dist > 5:
                dog_x += dx * 0.05
                dog_y += dy * 0.05
            dog_rect = pygame.Rect(dog_x - 10, dog_y - 10, 20, 20)
            if current_location == "bases":
                dog_x = max(wall_size, min(MAP_SIZE_BASES - wall_size, dog_x))
                dog_y = max(wall_size, min(MAP_SIZE_BASES - wall_size, dog_y))
                for trunk_rect in tree_rects_bases:
                    if dog_rect.colliderect(trunk_rect):
                        dog_x, dog_y = old_dog_x, old_dog_y
                        break
            elif current_location == "base_home":
                dog_x = max(wall_size, min(MAP_SIZE_ARENA - wall_size, dog_x))
                dog_y = max(wall_size, min(MAP_SIZE_ARENA - wall_size, dog_y))
                for wall_rect in arena_wall_rects:
                    if dog_rect.colliderect(wall_rect):
                        dog_x, dog_y = old_dog_x, old_dog_y
                        break
            elif current_location == "hotspot":
                dog_x = max(wall_size, min(MAP_SIZE - wall_size, dog_x))
                dog_y = max(wall_size, min(MAP_SIZE - wall_size, dog_y))
            else:
                for wall_rect in wall_rects:
                    if dog_rect.colliderect(wall_rect):
                        dog_x, dog_y = old_dog_x, old_dog_y
                        break
                for trunk_rect in tree_rects:
                    if dog_rect.colliderect(trunk_rect):
                        dog_x, dog_y = old_dog_x, old_dog_y
                        break
            if hp < 100:
                hp += 0.03
                if hp > 100:
                    hp = 100

        # ---- АНОМАЛИИ ----
        if not arena_mode and current_location not in ["bases", "base_home", "hotspot"]:
            for anom in anomalies:
                dist = math.hypot(player_x - anom[0], player_y - anom[1])
                if dist < 40 and anom[2] == 0:
                    if armor > 0:
                        armor -= 7
                        if armor < 0:
                            hp += armor
                            armor = 0
                    else:
                        hp -= 7
                    if hp < 0:
                        hp = 0
                    offset_x = random.randint(-30, 30)
                    offset_y = random.randint(-30, 30)
                    if anom[3] == 0:
                        svetilo_items.append([anom[0] + offset_x, anom[1] + offset_y])
                    elif anom[3] == 1:
                        ldishka_items.append([anom[0] + offset_x, anom[1] + offset_y])
                    else:
                        rubin_items.append([anom[0] + offset_x, anom[1] + offset_y])
                    anom[2] = 30
                elif anom[2] > 0:
                    anom[2] -= 1

            for item in svetilo_items[:]:
                if math.hypot(player_x - item[0], player_y - item[1]) < 40:
                    svetilo_count += 1
                    svetilo_items.remove(item)
            for item in ldishka_items[:]:
                if math.hypot(player_x - item[0], player_y - item[1]) < 40:
                    ldishka_count += 1
                    ldishka_items.remove(item)
            for item in rubin_items[:]:
                if math.hypot(player_x - item[0], player_y - item[1]) < 40:
                    rubin_count += 1
                    rubin_items.remove(item)

        # ---- БОЕВАЯ ЛОГИКА ----
        if arena_mode:
            for enemy in arena_enemies[:]:
                ex, ey, ehp, etype, edir = enemy
                dx = player_x - ex
                dy = player_y - ey
                dist = math.hypot(dx, dy)
                old_ex, old_ey = ex, ey
                if dist < 600 and dist != 0:
                    if etype == "wolf":
                        ex += dx / dist * 4.5
                        ey += dy / dist * 3.5
                    elif etype == "bear":
                        ex += dx / dist * 3.5
                        ey += dy / dist * 3
                    else:
                        ex += dx / dist * 2
                        ey += dy / dist * 2
                    ex = max(wall_size, min(MAP_SIZE_ARENA - wall_size, ex))
                    ey = max(wall_size, min(MAP_SIZE_ARENA - wall_size, ey))
                    enemy[0], enemy[1] = ex, ey
                    if ex > old_ex:
                        enemy[4] = "right"
                    elif ex < old_ex:
                        enemy[4] = "left"
                if dist < 45 and damage_cooldown == 0:
                    if svetilo_buff_timer <= 0:
                        dmg = 8 if etype == "wolf" else (15 if etype == "bear" else 5)
                        if armor > 0:
                            armor -= dmg
                            if armor < 0:
                                hp += armor
                                armor = 0
                        else:
                            hp -= dmg
                    damage_cooldown = 30
                for b in bullets[:]:
                    if math.hypot(ex - b[0], ey - b[1]) < 40:
                        if b[4] == "rpg":
                            ehp -= 6 * b[5]
                        else:
                            ehp -= 1 * b[5]
                        bullets.remove(b)
                enemy[2] = ehp
                if ehp <= 0:
                    arena_enemies.remove(enemy)
                    xp += 1
                    while xp >= next_level_xp:
                        level += 1
                        next_level_xp *= 2
            if len(arena_enemies) == 0 and not arena_reward_given:
                arena_reward_given = True
                iron += 4
                gold += 5
                overlay = pygame.Surface((WIDTH, HEIGHT))
                overlay.set_alpha(180)
                overlay.fill((0, 0, 0))
                screen.blit(overlay, (0, 0))
                msg = font.render("Арена пройдена! +4 железа, +5 золота", True, (0, 255, 0))
                msg_rect = msg.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                screen.blit(msg, msg_rect)
                pygame.display.flip()
                pygame.time.wait(2000)
                arena_mode = False
                player_x, player_y = arena_return_x, arena_return_y
                teleport_zone = arena_return_teleport_zone
                if arena_dog_was_active:
                    dog_active = True
                    dog_x = player_x + 50
                    dog_y = player_y + 50
        else:
            if current_location == "bases":
                for i, rect in enumerate(BASE_RECTS):
                    captured = bases_captured[i]
                    bots = bases_bots[i]
                    for bot in bots[:]:
                        bx, by, bhp, shoot_cd, bot_dir, move_timer = bot
                        if move_timer <= 0:
                            bot[4] = random.choice(["left", "right"])
                            bot[5] = random.randint(60, 180)
                        else:
                            bot[5] -= 1
                        if bot[4] == "left":
                            bx -= BOT_SPEED
                        else:
                            bx += BOT_SPEED
                        if bx < rect.x + 20:
                            bx = rect.x + 20
                            bot[4] = "right"
                        elif bx > rect.x + rect.width - 20:
                            bx = rect.x + rect.width - 20
                            bot[4] = "left"
                        bot[0] = bx
                        bot[1] = by

                        dist_to_player = math.hypot(player_x - bx, player_y - by)
                        if not captured and dist_to_player < 300 and shoot_cd <= 0:
                            dx = player_x - bx
                            dy = player_y - by
                            d = math.hypot(dx, dy)
                            if d != 0:
                                dx, dy = dx / d, dy / d
                            bot_bullets.append([bx, by, dx, dy])
                            bot[3] = 30
                        elif shoot_cd > 0:
                            bot[3] -= 1

                        for b in bullets[:]:
                            if math.hypot(bx - b[0], by - b[1]) < 40:
                                if b[4] == "rpg":
                                    bhp -= 6 * b[5]
                                else:
                                    bhp -= 1 * b[5]
                                bullets.remove(b)
                        bot[2] = bhp
                        if bhp <= 0:
                            bots.remove(bot)
                            if len(bots) == 0 and not captured:
                                bases_captured[i] = True
                                for _ in range(3):
                                    bx2 = rect.x + random.randint(100, 900)
                                    by2 = rect.y + random.randint(100, 900)
                                    bots.append([bx2, by2, 5, 0, random.choice(["left", "right"]), random.randint(60, 180)])
                            continue

                for bb in bot_bullets[:]:
                    bb[0] += bb[2] * 8
                    bb[1] += bb[3] * 8
                    if bb[0] < 0 or bb[0] > MAP_SIZE_BASES or bb[1] < 0 or bb[1] > MAP_SIZE_BASES:
                        bot_bullets.remove(bb)
                        continue
                    if math.hypot(player_x - bb[0], player_y - bb[1]) < 30 and damage_cooldown == 0:
                        if svetilo_buff_timer <= 0:
                            dmg = 5
                            if armor > 0:
                                armor -= dmg
                                if armor < 0:
                                    hp += armor
                                    armor = 0
                            else:
                                hp -= dmg
                        damage_cooldown = 30
                        bot_bullets.remove(bb)
            elif current_location not in ["base_home", "hotspot"]:
                # ---- ВОЛКИ (двигаются только на локации monster) ----
                if teleport_zone:
                    for wolf in wolves[:]:
                        dx = player_x - wolf[0]
                        dy = player_y - wolf[1]
                        d = math.hypot(dx, dy)
                        if d < 500 and d != 0:
                            old_wx, old_wy = wolf[0], wolf[1]
                            wolf[0] += dx / d * 4.5
                            wolf[1] += dy / d * 4.5
                            wolf_rect = pygame.Rect(wolf[0] - 15, wolf[1] - 15, 30, 30)
                            for wall_rect in wall_rects:
                                if wolf_rect.colliderect(wall_rect):
                                    wolf[0], wolf[1] = old_wx, old_wy
                                    break
                            wolf[3] = "left" if player_x < wolf[0] else "right"
                        if d < 45 and damage_cooldown == 0:
                            if svetilo_buff_timer <= 0:
                                dmg = 8
                                if armor > 0:
                                    armor -= dmg
                                    if armor < 0:
                                        hp += armor
                                        armor = 0
                                else:
                                    hp -= dmg
                            damage_cooldown = 30
                        for b in bullets[:]:
                            if math.hypot(wolf[0] - b[0], wolf[1] - b[1]) < 40:
                                wolf[2] -= 1 * b[5]
                                if b in bullets:
                                    bullets.remove(b)
                        if wolf[2] <= 0:
                            xp += 1
                            while xp >= next_level_xp:
                                level += 1
                                next_level_xp *= 2
                            irons.append([wolf[0], wolf[1]])
                            wolves.remove(wolf)
                            while True:
                                wx = random.randint(1000, MAP_SIZE - 1000)
                                wy = random.randint(1000, MAP_SIZE - 1000)
                                if math.hypot(wx - secret_x, wy - secret_y) > 1000 and is_far_from_walls(wx, wy, 250):
                                    wolves.append([wx, wy, 4, "right"])
                                    break

                    # ---- МЕДВЕДИ (двигаются только на локации monster) ----
                    for bear in bears[:]:
                        dx = player_x - bear[0]
                        dy = player_y - bear[1]
                        d = math.hypot(dx, dy)
                        if d < 700 and d != 0:
                            old_bx, old_by = bear[0], bear[1]
                            bear[0] += dx / d * 3.5
                            bear[1] += dy / d * 3.5
                            bear_rect = pygame.Rect(bear[0] - 20, bear[1] - 20, 40, 40)
                            for wall_rect in wall_rects:
                                if bear_rect.colliderect(wall_rect):
                                    bear[0], bear[1] = old_bx, old_by
                                    break
                            bear[3] = "left" if player_x < bear[0] else "right"
                        if d < 55 and damage_cooldown == 0:
                            if svetilo_buff_timer <= 0:
                                dmg = 15
                                if armor > 0:
                                    armor -= dmg
                                    if armor < 0:
                                        hp += armor
                                        armor = 0
                                else:
                                    hp -= dmg
                            damage_cooldown = 30
                        for b in bullets[:]:
                            if math.hypot(bear[0] - b[0], bear[1] - b[1]) < 55:
                                if b[4] == "rpg":
                                    bear[2] -= 6 * b[5]
                                else:
                                    bear[2] -= 1 * b[5]
                                if b in bullets:
                                    bullets.remove(b)
                        if bear[2] <= 0:
                            irons.append([bear[0], bear[1]])
                            irons.append([bear[0] + 15, bear[1]])
                            bears.remove(bear)
                    while len(bears) < 2 and teleport_zone:
                        while True:
                            bx = random.randint(500, MAP_SIZE - 500)
                            by = random.randint(500, MAP_SIZE - 500)
                            if (math.hypot(bx - player_x, by - player_y) > 500 and
                                math.hypot(bx - SPAWN_X, by - SPAWN_Y) > 1200 and
                                is_far_from_walls(bx, by, 250)):
                                bears.append([bx, by, 12, "right"])
                                break

                # ---- ЗОМБИ (двигаются всегда) ----
                for z in zombies[:]:
                    dx, dy = player_x - z[0], player_y - z[1]
                    d = math.hypot(dx, dy)
                    if d < 600 and d != 0:
                        old_zx, old_zy = z[0], z[1]
                        z[0] += dx / d * 2
                        z[1] += dy / d * 2
                        z[4] = "left" if player_x < z[0] else "right"
                        zombie_rect = pygame.Rect(z[0] - 16, z[1] - 16, 32, 32)
                        if not teleport_zone:
                            shop_x, shop_y = objs[1]
                            if math.hypot(z[0] - (shop_x + object2.get_width()//2), z[1] - (shop_y + object2.get_height()//2)) < 50:
                                z[0], z[1] = old_zx, old_zy
                            npc_x, npc_y = objs[0]
                            if math.hypot(z[0] - (npc_x + object1.get_width()//2), z[1] - (npc_y + object1.get_height()//2)) < 50:
                                z[0], z[1] = old_zx, old_zy
                        for wall_rect in wall_rects:
                            if zombie_rect.colliderect(wall_rect):
                                z[0], z[1] = old_zx, old_zy
                                break
                    if d < 40 and damage_cooldown == 0:
                        if svetilo_buff_timer <= 0:
                            dmg = 5
                            if armor > 0:
                                armor -= dmg
                                if armor < 0:
                                    hp += armor
                                    armor = 0
                            else:
                                hp -= dmg
                        damage_cooldown = 30
                    for b in bullets[:]:
                        if math.hypot(z[0] - b[0], z[1] - b[1]) < 40:
                            if b[4] == "rpg":
                                explosions.append([b[0], b[1], 0])
                                for z2 in zombies[:]:
                                    if math.hypot(z2[0] - b[0], z2[1] - b[1]) < 120:
                                        zombies.remove(z2)
                                        rusts.append([z2[0], z2[1]])
                                        xp += 1
                                        while xp >= next_level_xp:
                                            level += 1
                                            next_level_xp *= 2
                                        if quest_active:
                                            zombies_killed += 1
                                        zombies.append([random.randint(0, MAP_SIZE), random.randint(0, MAP_SIZE), 0, 4, "right"])
                                bullets.remove(b)
                                break
                            else:
                                z[3] -= 1 * b[5]
                                bullets.remove(b)
                    if z in zombies and z[3] <= 0:
                        zombies.remove(z)
                        rusts.append([z[0], z[1]])
                        xp += 1
                        while xp >= next_level_xp:
                            level += 1
                            next_level_xp *= 2
                        if quest_active:
                            zombies_killed += 1
                        zombies.append([random.randint(0, MAP_SIZE), random.randint(0, MAP_SIZE), 0, 4, "right"])
                if quest_active and zombies_killed >= quest_target:
                    reward = quest_target * 3
                    iron += reward
                    quest_active = False
                    quest_target += 5
                    zombies_killed = 0

                # ---- БОСС ----
                if boss:
                    dx, dy = player_x - boss[0], player_y - boss[1]
                    d = math.hypot(dx, dy)
                    if d < 700 and d != 0:
                        old_bx, old_by = boss[0], boss[1]
                        boss[0] += dx / d * 1.5
                        boss[1] += dy / d * 1.5
                        boss_rect = pygame.Rect(boss[0] - 30, boss[1] - 30, 60, 60)
                        if not teleport_zone:
                            shop_x, shop_y = objs[1]
                            if math.hypot(boss[0] - (shop_x + object2.get_width()//2), boss[1] - (shop_y + object2.get_height()//2)) < 60:
                                boss[0], boss[1] = old_bx, old_by
                            npc_x, npc_y = objs[0]
                            if math.hypot(boss[0] - (npc_x + object1.get_width()//2), boss[1] - (npc_y + object1.get_height()//2)) < 60:
                                boss[0], boss[1] = old_bx, old_by
                        for wall_rect in wall_rects:
                            if boss_rect.colliderect(wall_rect):
                                boss[0], boss[1] = old_bx, old_by
                                break
                    if d < 50 and damage_cooldown == 0:
                        if svetilo_buff_timer <= 0:
                            hp -= 20
                        damage_cooldown = 30
                    for b in bullets[:]:
                        if math.hypot(boss[0] - b[0], boss[1] - b[1]) < 60:
                            boss[2] -= 1 * b[5]
                            bullets.remove(b)
                    if boss and boss[2] <= 0:
                        for _ in range(15):
                            golds.append([boss[0] + random.randint(-20, 20), boss[1] + random.randint(-20, 20)])
                        if boss_quest_active and not boss_quest_done:
                            boss_quest_killed = 1
                            gold += 5
                            boss_quest_done = True
                            boss_quest_active = False
                        boss = None

        # ---- ОБНОВЛЕНИЕ ПУЛЬ ----
        for b in bullets[:]:
            b[0] += b[2] * 10
            b[1] += b[3] * 10
            limit = MAP_SIZE
            if arena_mode:
                limit = MAP_SIZE_ARENA
            elif current_location == "bases":
                limit = MAP_SIZE_BASES
            elif current_location == "base_home":
                limit = MAP_SIZE_ARENA
            if b[0] < 0 or b[0] > limit or b[1] < 0 or b[1] > limit:
                bullets.remove(b)
                continue

            if current_location == "hotspot":
                for gen in generators:
                    if gen[2] > 0 and math.hypot(b[0] - gen[0], b[1] - gen[1]) < 30:
                        if b[4] == "rpg":
                            gen[2] -= 4
                        elif b[4] == "sniper" or b[4] == "pistol":
                            gen[2] -= 1 * b[5]
                        elif b[4] == "shotgun":
                            gen[2] -= 2 * b[5]
                        if gen[2] <= 0:
                            sphere_drops.append([gen[0] + random.randint(-20, 20), gen[1] + random.randint(-20, 20)])
                            gen[3] = 30 * 60
                            gen[2] = 0
                        bullets.remove(b)
                        break

        # ---- ПОДБОР ПРЕДМЕТОВ ----
        for g in golds[:]:
            if math.hypot(player_x - g[0], player_y - g[1]) < 40:
                golds.remove(g)
                gold += 1
        for ir in irons[:]:
            if math.hypot(player_x - ir[0], player_y - ir[1]) < 40:
                irons.remove(ir)
                iron += 1
        for r in rusts[:]:
            if math.hypot(player_x - r[0], player_y - r[1]) < 40:
                rusts.remove(r)
                rust += 1

        # ---- ТАЙМЕРЫ БАФФОВ ----
        if svetilo_buff_timer > 0:
            svetilo_buff_timer -= 1
        if ldishka_buff_timer > 0:
            ldishka_buff_timer -= 1
        if rubin_buff_timer > 0:
            rubin_buff_timer -= 1
        if sphere_buff_timer > 0:
            sphere_buff_timer -= 1

        # ---- АНИМАЦИЯ ВЫСТРЕЛА ----
        if shoot_anim_timer > 0:
            shoot_anim_timer -= 1
            if shoot_anim_timer == 0:
                shoot_img = None

        # ---- КАМЕРА ----
        cam_x = player_x - WIDTH // 2
        cam_y = player_y - HEIGHT // 2

        # ---- ОТРИСОВКА ----
        if arena_mode:
            screen.fill((50, 50, 50))
            for wx in range(0, MAP_SIZE_ARENA, wall_size):
                screen.blit(wall_img, (wx - cam_x, -cam_y))
                screen.blit(wall_img, (wx - cam_x, MAP_SIZE_ARENA - wall_size - cam_y))
            for wy in range(wall_size, MAP_SIZE_ARENA - wall_size, wall_size):
                screen.blit(wall_img, (-cam_x, wy - cam_y))
                screen.blit(wall_img, (MAP_SIZE_ARENA - wall_size - cam_x, wy - cam_y))
            for enemy in arena_enemies:
                ex, ey, ehp, etype, edir = enemy
                if etype == "wolf":
                    img = wolf_surfaces["left"] if edir == "left" else wolf_surfaces["right"]
                    screen.blit(img, (ex - cam_x, ey - cam_y))
                elif etype == "bear":
                    img = bear_surfaces["left"] if edir == "left" else bear_surfaces["right"]
                    screen.blit(img, (ex - cam_x, ey - cam_y))
                elif etype == "zombie":
                    img = zombie_surfaces["left"] if edir == "left" else zombie_surfaces["right"]
                    screen.blit(img, (ex - cam_x, ey - cam_y))
            screen.blit(font.render("АРЕНА", True, (255, 0, 0)), (WIDTH//2 - 50, 20))
        elif current_location == "bases":
            screen.fill((50, 50, 50))
            screen.blit(safe_zone_surface, (SAFE_ZONE_RECT.x - cam_x, SAFE_ZONE_RECT.y - cam_y))
            for rect in BASE_RECTS:
                pygame.draw.rect(screen, (0, 128, 0), (rect.x - cam_x, rect.y - cam_y, rect.width, rect.height))
                center_x = rect.centerx - farn_img.get_width() // 2
                center_y = rect.centery - farn_img.get_height() // 2
                screen.blit(farn_img, (center_x - cam_x, center_y - cam_y))
            for wx in range(0, MAP_SIZE_BASES, wall_size):
                screen.blit(wall_img, (wx - cam_x, -cam_y))
                screen.blit(wall_img, (wx - cam_x, MAP_SIZE_BASES - wall_size - cam_y))
            for wy in range(wall_size, MAP_SIZE_BASES - wall_size, wall_size):
                screen.blit(wall_img, (-cam_x, wy - cam_y))
                screen.blit(wall_img, (MAP_SIZE_BASES - wall_size - cam_x, wy - cam_y))
            if bike_active:
                bike_img = {"up": bike_up, "down": bike_down, "left": bike_left, "right": bike_right}[bike_direction]
                screen.blit(bike_img, bike_img.get_rect(center=CENTER))
            else:
                if shoot_img is not None:
                    if player_direction == "left":
                        img = pygame.transform.flip(shoot_img, True, False)
                    else:
                        img = shoot_img
                else:
                    img = player_surfaces[player_direction] if moving else player_surfaces["idle"]
                screen.blit(img, img.get_rect(center=CENTER))
            for t in trees_bases:
                screen.blit(tree, (t[0] - cam_x, t[1] - cam_y))
            obj3_x = SAFE_ZONE_RECT.centerx - object3.get_width()//2
            obj3_y = SAFE_ZONE_RECT.centery - object3.get_height()//2
            screen.blit(object3, (obj3_x - cam_x, obj3_y - cam_y))
            screen.blit(font.render("E - Телепорт", True, (0, 255, 0)), (obj3_x - cam_x - 20, obj3_y - cam_y - 40))
            for i, rect in enumerate(BASE_RECTS):
                bots = bases_bots[i]
                for bot in bots:
                    bot_img = bot_surfaces[bot[4]]
                    screen.blit(bot_img, (bot[0] - cam_x, bot[1] - cam_y))
            for bb in bot_bullets:
                pygame.draw.circle(screen, (255, 0, 0), (int(bb[0] - cam_x), int(bb[1] - cam_y)), 4)
            if dog_active:
                if abs(dog_x - player_x) < 10 and abs(dog_y - player_y) < 10:
                    dog_anim = "idle"
                else:
                    dog_anim = "left" if dog_x > player_x else "right"
                dog_img = dog_surfaces[dog_anim]
                screen.blit(dog_img, (dog_x - cam_x + 15, dog_y - cam_y))
            for i, rect in enumerate(BASE_RECTS):
                status = "Захвачена" if bases_captured[i] else "Не захвачена"
                color = (0, 255, 0) if bases_captured[i] else (255, 0, 0)
                text = font.render(f"База {i+1}: {status}", True, color)
                screen.blit(text, (rect.x - cam_x, rect.y - cam_y - 30))
                if bases_captured[i]:
                    rust_text = font.render("+1 ржавчина/сек", True, (255, 255, 0))
                    screen.blit(rust_text, (rect.x - cam_x, rect.y - cam_y + rect.height + 5))
            if not SAFE_ZONE_RECT.collidepoint(player_x, player_y):
                warning = font.render("-2 HP / сек (вне зоны)", True, (255, 0, 0))
                screen.blit(warning, (WIDTH // 2 - 100, 60))

        elif current_location == "base_home":
            screen.fill((34, 139, 34))
            for wx in range(0, MAP_SIZE_ARENA, wall_size):
                screen.blit(wall_img, (wx - cam_x, -cam_y))
                screen.blit(wall_img, (wx - cam_x, MAP_SIZE_ARENA - wall_size - cam_y))
            for wy in range(wall_size, MAP_SIZE_ARENA - wall_size, wall_size):
                screen.blit(wall_img, (-cam_x, wy - cam_y))
                screen.blit(wall_img, (MAP_SIZE_ARENA - wall_size - cam_x, wy - cam_y))
            if base_werstak_pos:
                screen.blit(werstak_img, (base_werstak_pos[0] - cam_x, base_werstak_pos[1] - cam_y))
                if math.hypot(player_x - base_werstak_pos[0], player_y - base_werstak_pos[1]) < 120:
                    screen.blit(font.render("E - Меню базы", True, (0, 255, 0)), (base_werstak_pos[0] - cam_x - 30, base_werstak_pos[1] - cam_y - 30))
            if base_safe_pos:
                screen.blit(safe_img, (base_safe_pos[0] - cam_x, base_safe_pos[1] - cam_y))
            if base_teleport_pos:
                screen.blit(object3, (base_teleport_pos[0] - cam_x - object3.get_width()//2, base_teleport_pos[1] - cam_y - object3.get_height()//2))
                screen.blit(font.render("Нажмите E", True, (0, 255, 0)), (base_teleport_pos[0] - cam_x - 40, base_teleport_pos[1] - cam_y - 50))
            if bike_active:
                bike_img = {"up": bike_up, "down": bike_down, "left": bike_left, "right": bike_right}[bike_direction]
                screen.blit(bike_img, bike_img.get_rect(center=CENTER))
            else:
                if shoot_img is not None:
                    if player_direction == "left":
                        img = pygame.transform.flip(shoot_img, True, False)
                    else:
                        img = shoot_img
                else:
                    img = player_surfaces[player_direction] if moving else player_surfaces["idle"]
                screen.blit(img, img.get_rect(center=CENTER))
            if dog_active:
                if abs(dog_x - player_x) < 10 and abs(dog_y - player_y) < 10:
                    dog_anim = "idle"
                else:
                    dog_anim = "left" if dog_x > player_x else "right"
                dog_img = dog_surfaces[dog_anim]
                screen.blit(dog_img, (dog_x - cam_x + 15, dog_y - cam_y))

        elif current_location == "hotspot":
            if hotspot_safe_zone_rect is None:
                hotspot_safe_zone_rect, generators, hotspot_monsters, hotspot_bushes = init_hotspot()
            screen.fill((50, 50, 50))
            old_clip = screen.get_clip()
            screen.set_clip(hotspot_safe_zone_rect.x - cam_x, hotspot_safe_zone_rect.y - cam_y,
                            hotspot_safe_zone_rect.width, hotspot_safe_zone_rect.height)
            screen.fill((0, 200, 0), (hotspot_safe_zone_rect.x - cam_x, hotspot_safe_zone_rect.y - cam_y,
                                      hotspot_safe_zone_rect.width, hotspot_safe_zone_rect.height))
            screen.set_clip(old_clip)
            pygame.draw.rect(screen, (0, 255, 0), (hotspot_safe_zone_rect.x - cam_x, hotspot_safe_zone_rect.y - cam_y,
                                                    hotspot_safe_zone_rect.width, hotspot_safe_zone_rect.height), 3)
            for wx in range(0, MAP_SIZE, wall_size):
                screen.blit(wall_img, (wx - cam_x, -cam_y))
                screen.blit(wall_img, (wx - cam_x, MAP_SIZE - wall_size - cam_y))
            for wy in range(wall_size, MAP_SIZE - wall_size, wall_size):
                screen.blit(wall_img, (-cam_x, wy - cam_y))
                screen.blit(wall_img, (MAP_SIZE - wall_size - cam_x, wy - cam_y))
            for gen in generators:
                if gen[2] > 0:
                    gx, gy, hp_gen, _ = gen
                    screen.blit(genuy_img, (gx - cam_x - 30, gy - cam_y - 30))
                    bar_width = 40
                    bar_height = 4
                    bar_x = gx - cam_x - 20
                    bar_y = gy - cam_y - 40
                    pygame.draw.rect(screen, (100, 0, 0), (bar_x, bar_y, bar_width, bar_height))
                    fill = int((hp_gen / 4) * bar_width)
                    pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, fill, bar_height))
            for drop in sphere_drops:
                screen.blit(sfera_img, (drop[0] - cam_x - 20, drop[1] - cam_y - 20))
            for ir in irons:
                screen.blit(iron_img, (ir[0] - cam_x - 10, ir[1] - cam_y - 10))
            for r in rusts:
                screen.blit(rust_img, (r[0] - cam_x - 10, r[1] - cam_y - 10))
            for mon in hotspot_monsters:
                mx, my, mhp, mtype, mdir, orig_x, orig_y = mon
                # Движение монстров на hotspot
                if hotspot_safe_zone_rect.collidepoint(player_x, player_y):
                    # Отходить к исходной позиции
                    dx = orig_x - mx
                    dy = orig_y - my
                    dist = math.hypot(dx, dy)
                    if dist > 1:
                        mx += dx / dist * 2
                        my += dy / dist * 2
                    if dist < 5:
                        mx, my = orig_x, orig_y
                    mon[0], mon[1] = mx, my
                    continue

                dx = player_x - mx
                dy = player_y - my
                dist = math.hypot(dx, dy)
                if dist < 500 and dist != 0:
                    speed = 2.0
                    if mtype == "wolf":
                        speed = 4.5
                    elif mtype == "bear":
                        speed = 3.5
                    elif mtype == "boss":
                        speed = 1.5
                    mx += dx / dist * speed
                    my += dy / dist * speed
                    if dx > 0:
                        mdir = "right"
                    else:
                        mdir = "left"
                    mx = max(wall_size, min(MAP_SIZE - wall_size, mx))
                    my = max(wall_size, min(MAP_SIZE - wall_size, my))
                    mon[0], mon[1] = mx, my
                    mon[4] = mdir

                if dist < 45 and damage_cooldown == 0:
                    if svetilo_buff_timer <= 0:
                        dmg = 5 if mtype == "zombie" else (8 if mtype == "wolf" else (15 if mtype == "bear" else 20))
                        if armor > 0:
                            armor -= dmg
                            if armor < 0:
                                hp += armor
                                armor = 0
                        else:
                            hp -= dmg
                    damage_cooldown = 30

                for b in bullets[:]:
                    if math.hypot(mx - b[0], my - b[1]) < 40:
                        if b[4] == "rpg":
                            mhp -= 6 * b[5]
                        else:
                            mhp -= 1 * b[5]
                        bullets.remove(b)
                mon[2] = mhp
                if mhp <= 0:
                    if mtype == "boss":
                        for _ in range(15):
                            golds.append([mx + random.randint(-20,20), my + random.randint(-20,20)])
                    else:
                        if random.random() < 0.4:
                            if random.random() < 0.5:
                                irons.append([mx + random.randint(-10,10), my + random.randint(-10,10)])
                            else:
                                rusts.append([mx + random.randint(-10,10), my + random.randint(-10,10)])
                    attempts = 0
                    while attempts < 100:
                        nx = random.randint(200, MAP_SIZE - 200)
                        ny = random.randint(200, MAP_SIZE - 200)
                        if not hotspot_safe_zone_rect.collidepoint(nx, ny) and is_far_from_walls(nx, ny, 250):
                            mon[0], mon[1] = nx, ny
                            mon[2] = 4 if mtype == "zombie" else (12 if mtype == "bear" else (28 if mtype == "boss" else 4))
                            mon[5], mon[6] = nx, ny
                            break
                        attempts += 1

            for b in hotspot_bushes:
                if not b[2]:
                    b[3] -= 1
                    if b[3] <= 0:
                        b[2] = True

            for drop in sphere_drops[:]:
                if math.hypot(player_x - drop[0], player_y - drop[1]) < 40:
                    sphere_count += 1
                    sphere_drops.remove(drop)

            # Отрисовка hotspot
            # (уже отрисовано выше, но добавим монстров, ягоды и т.д.)
            # (код отрисовки уже есть, он рисует монстров и ягоды)
            # Дополнительно отрисовываем генераторы и безопасную зону
            # (это уже сделано выше)

            # Игрок и собака отрисовываются ниже в общем блоке

        else:
            # обычные локации home/monster
            screen.fill((34, 139, 34))
            for wx in range(0, MAP_SIZE, wall_size):
                screen.blit(wall_img, (wx - cam_x, -cam_y))
                screen.blit(wall_img, (wx - cam_x, MAP_SIZE - wall_size - cam_y))
            for wy in range(wall_size, MAP_SIZE - wall_size, wall_size):
                screen.blit(wall_img, (-cam_x, wy - cam_y))
                screen.blit(wall_img, (MAP_SIZE - wall_size - cam_x, wy - cam_y))
            imgs = [object1, object2, object3, object4]
            if teleport_zone:
                screen.blit(object3, (secret_x - cam_x, secret_y - cam_y))
                screen.blit(font.render("Нажмите E", True, (0, 255, 0)), (secret_x - cam_x - 20, secret_y - cam_y - 40))
                screen.blit(bike_trader_img, (bike_trader_x - cam_x, bike_trader_y - cam_y))
                screen.blit(font.render("1-Мотоцикл (100)-(50)", True, (255, 255, 0)),
                            (bike_trader_x - cam_x - 50, bike_trader_y - cam_y - 40))
                screen.blit(boss_npc_img, (boss_npc_x - cam_x, boss_npc_y - cam_y))
                if boss_quest_done:
                    boss_text = "У меня нет заданий"
                else:
                    boss_text = "E-Задание"
                screen.blit(font.render(boss_text, True, (0, 255, 255)), (boss_npc_x - cam_x - 40, boss_npc_y - cam_y - 40))
            else:
                for i, p in enumerate(objs):
                    screen.blit(imgs[i], (p[0] - cam_x, p[1] - cam_y))
                npc_x, npc_y = objs[0]
                screen.blit(font.render("E - задание", True, (0, 255, 0)), (npc_x - cam_x + 20, npc_y - cam_y + 20))
                obj3_x, obj3_y = objs[2]
                screen.blit(font.render("Нажмите E", True, (0, 255, 0)), (obj3_x - cam_x - 20, obj3_y - cam_y - 40))
                berry_x, berry_y = objs[3]
                screen.blit(font.render("E - задание", True, (0, 255, 0)), (berry_x - cam_x, berry_y - cam_y - 40))
            screen.blit(font.render("Перезарядка-R", True, (255, 255, 0)), (20, 140))
            if quest_active:
                qt = f"Убей зомби: {zombies_killed}/{quest_target}"
            else:
                qt = "Подойди к NPC и нажми E"
            screen.blit(font.render(qt, True, (255, 255, 255)), (20, 170))
            if berry_quest_active:
                berry_text = f"Принести ягод: {berries}/{berry_quest_target}"
            else:
                berry_text = "Подойди к советчику и нажми E"
            screen.blit(font.render(berry_text, True, (255, 200, 200)), (20, 210))
            if boss_quest_active and not boss_quest_done:
                screen.blit(font.render(f"Убить босса: {boss_quest_killed}/1", True, (0, 200, 255)), (20, 250))

            if current_location in ["home", "monster"]:
                for anom in anomalies:
                    if anom[3] == 0:
                        anom_img = svetilo_video
                    elif anom[3] == 1:
                        anom_img = ldishka_video
                    else:
                        anom_img = rubin_video
                    screen.blit(anom_img, (anom[0] - cam_x, anom[1] - cam_y))

            for item in svetilo_items:
                screen.blit(svetilo_icon, (item[0] - cam_x, item[1] - cam_y))
            for item in ldishka_items:
                screen.blit(ldishka_icon, (item[0] - cam_x, item[1] - cam_y))
            for item in rubin_items:
                screen.blit(rubin_icon, (item[0] - cam_x, item[1] - cam_y))
            for g in golds:
                screen.blit(gold_img, (g[0] - cam_x, g[1] - cam_y))
            for ir in irons:
                screen.blit(iron_img, (ir[0] - cam_x, ir[1] - cam_y))
            for r in rusts:
                screen.blit(rust_img, (r[0] - cam_x, r[1] - cam_y))
            if teleport_zone:
                for wolf in wolves:
                    wolf_img = wolf_surfaces["left"] if wolf[3] == "left" else wolf_surfaces["right"]
                    screen.blit(wolf_img, (wolf[0] - cam_x, wolf[1] - cam_y))
                for bear in bears:
                    bear_img = bear_surfaces["left"] if bear[3] == "left" else bear_surfaces["right"]
                    screen.blit(bear_img, (bear[0] - cam_x, bear[1] - cam_y))
            for z in zombies:
                zombie_img = zombie_surfaces["left"] if z[4] == "left" else zombie_surfaces["right"]
                screen.blit(zombie_img, (z[0] - cam_x, z[1] - cam_y))
            if boss:
                dx_boss = player_x - boss[0]
                boss_dir = "left" if dx_boss < 0 else "right"
                boss_img = boss_surfaces[boss_dir]
                screen.blit(boss_img, (boss[0] - cam_x, boss[1] - cam_y))

            # деревья и кусты
            for t in trees:
                screen.blit(tree, (t[0] - cam_x, t[1] - cam_y))
            for b in bushes:
                img_bush = bush if b[2] else bush_empty
                screen.blit(img_bush, (b[0] - cam_x, b[1] - cam_y))
                if b[2] and math.hypot(player_x - b[0], player_y - b[1]) < 80:
                    screen.blit(font.render("F - собрать ягоды", True, (255, 255, 255)), (b[0] - cam_x, b[1] - cam_y - 30))

            # игрок, собака, байк
            if shoot_img is not None:
                if player_direction == "left":
                    img = pygame.transform.flip(shoot_img, True, False)
                else:
                    img = shoot_img
            else:
                img = player_surfaces[player_direction] if moving else player_surfaces["idle"]
            if bike_active:
                bike_img = {"up": bike_up, "down": bike_down, "left": bike_left, "right": bike_right}[bike_direction]
                screen.blit(bike_img, bike_img.get_rect(center=CENTER))
            else:
                screen.blit(img, img.get_rect(center=CENTER))
            if dog_active:
                if abs(dog_x - player_x) < 10 and abs(dog_y - player_y) < 10:
                    dog_anim = "idle"
                else:
                    dog_anim = "left" if dog_x > player_x else "right"
                dog_img = dog_surfaces[dog_anim]
                screen.blit(dog_img, (dog_x - cam_x + 15, dog_y - cam_y))

        # ---- ОБЩИЕ ЭЛЕМЕНТЫ ИНТЕРФЕЙСА (выносятся за пределы условий) ----
        if not arena_mode:
            if current_location != "hotspot":
                craft_btn_rect = pygame.Rect(WIDTH - 110, HEIGHT - 110, 90, 90)
                pygame.draw.rect(screen, (30, 30, 30, 200), craft_btn_rect, border_radius=15)
                pygame.draw.rect(screen, (100, 100, 100), craft_btn_rect, width=2, border_radius=15)
                if craft_btn_rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(screen, (76, 175, 80), craft_btn_rect, width=4, border_radius=15)
                    overlay = pygame.Surface((90, 90))
                    overlay.set_alpha(60)
                    overlay.fill((255, 255, 255))
                    screen.blit(overlay, (WIDTH - 110, HEIGHT - 110))
                screen.blit(kraft_img, (craft_btn_rect.x + 15, craft_btn_rect.y + 15))
                label = font_small.render("Крафт", True, (255, 255, 255))
                screen.blit(label, (craft_btn_rect.x + 20, craft_btn_rect.y + craft_btn_rect.height - 25))

        if svetilo_buff_timer > 0:
            seconds = svetilo_buff_timer // 60
            buff_text = font.render(f"Светило: {seconds} сек", True, (0, 255, 255))
            screen.blit(buff_text, (20, 250))
        if ldishka_buff_timer > 0:
            seconds = ldishka_buff_timer // 60
            buff_text = font.render(f"Скорость: {seconds} сек", True, (100, 200, 255))
            screen.blit(buff_text, (20, 280))
        if rubin_buff_timer > 0:
            seconds = rubin_buff_timer // 60
            buff_text = font.render(f"Урон x2: {seconds} сек", True, (255, 100, 100))
            screen.blit(buff_text, (20, 310))

        for b in bullets:
            x = int(b[0] - cam_x)
            y = int(b[1] - cam_y)
            if b[4] == "pistol":
                start = (x - int(b[2]*3), y - int(b[3]*3))
                end = (x + int(b[2]*3), y + int(b[3]*3))
                pygame.draw.line(screen, (255, 255, 100), start, end, 2)
            elif b[4] == "shotgun":
                pygame.draw.circle(screen, (255, 240, 150), (x, y), 2)
            elif b[4] == "rpg":
                pygame.draw.circle(screen, (255, 200, 50), (x, y), 8)

        for ex in explosions[:]:
            ex[2] += 4
            pygame.draw.circle(screen, (255, 150, 0), (int(ex[0] - cam_x), int(ex[1] - cam_y)), int(ex[2]))
            if ex[2] > 60:
                explosions.remove(ex)

        # Игрок на арене (повторно, если арена)
        if arena_mode:
            if bike_active:
                bike_img = {"up": bike_up, "down": bike_down, "left": bike_left, "right": bike_right}[bike_direction]
                screen.blit(bike_img, bike_img.get_rect(center=CENTER))
            else:
                if shoot_img is not None:
                    if player_direction == "left":
                        player_img = pygame.transform.flip(shoot_img, True, False)
                    else:
                        player_img = shoot_img
                else:
                    player_img = player_surfaces[player_direction] if moving else player_surfaces["idle"]
                screen.blit(player_img, player_img.get_rect(center=CENTER))

        # XP бар
        bar_width = 60
        bar_height = 3
        bar_x = WIDTH // 2 - bar_width // 2
        bar_y = HEIGHT // 2 - 60
        pygame.draw.rect(screen, (30, 30, 30), (bar_x, bar_y, bar_width, bar_height))
        fill = int((xp / next_level_xp) * bar_width)
        pygame.draw.rect(screen, (0, 255, 255), (bar_x, bar_y, fill, bar_height))
        small_font = pygame.font.SysFont(None, 18)
        lvl_text = small_font.render(f"LVL {level}", True, (255, 255, 255))
        screen.blit(lvl_text, (bar_x + 10, bar_y - 15))

        # HP и броня
        pygame.draw.rect(screen, (255, 0, 0), (20, 20, 200, 20))
        pygame.draw.rect(screen, (0, 255, 0), (20, 20, 2 * hp, 20))
        hp_text = font.render(f"{int(hp)}/100", True, (255, 255, 255))
        hp_rect = hp_text.get_rect(center=(120, 30))
        screen.blit(hp_text, hp_rect)
        if armor > 0:
            pygame.draw.rect(screen, (40, 40, 40), (20, 50, 200, 15))
            pygame.draw.rect(screen, (0, 150, 255), (20, 50, 2 * armor, 15))
            armor_text = font.render(f"{int(armor)}/100", True, (255, 255, 255))
            armor_rect = armor_text.get_rect(center=(120, 57))
            screen.blit(armor_text, armor_rect)

        screen.blit(font.render(f"Ammo: {ammo}", True, (255, 255, 255)), (20, 80))
        if not arena_mode:
            screen.blit(font.render("Инвентарь - I", True, (255, 255, 255)), (WIDTH // 2 - 100, HEIGHT - 40))

        if sphere_buff_timer > 0:
            minutes = sphere_buff_timer // 3600
            buff_text = font.render(f"Зачарование: {minutes} мин (урон x2)", True, (255, 215, 0))
            screen.blit(buff_text, (20, 340))

        if inventory_open and not arena_mode:
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(180)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))

            panel_w, panel_h = 400, 650
            panel_x = WIDTH // 2 - panel_w // 2
            panel_y = HEIGHT // 2 - panel_h // 2
            pygame.draw.rect(screen, (50, 50, 50), (panel_x, panel_y, panel_w, panel_h), border_radius=15)
            pygame.draw.rect(screen, (100, 100, 100), (panel_x, panel_y, panel_w, panel_h), width=2, border_radius=15)

            title_text = font.render("Инвентарь", True, (255, 255, 0))
            title_rect = title_text.get_rect(center=(panel_x + panel_w//2, panel_y + 25))
            screen.blit(title_text, title_rect)

            y_start = panel_y + 50
            line_h = 35
            resources = [("Золото", gold, gold_img), ("Железо", iron, iron_img), ("Ржавчина", rust, rust_img)]
            for i, (name, amount, icon) in enumerate(resources):
                y = y_start + i * line_h
                screen.blit(icon, (panel_x + 20, y))
                text_surf = font.render(f"{name}: {amount}", True, (255, 255, 255))
                screen.blit(text_surf, (panel_x + 60, y))

            sphere_y = y_start + 3 * line_h + 10
            screen.blit(sfera_img, (panel_x + 20, sphere_y))
            sphere_text = font.render(f"Сферы: {sphere_count}", True, (255, 255, 0))
            screen.blit(sphere_text, (panel_x + 60, sphere_y))

            berry_y = sphere_y + line_h + 10
            screen.blit(berry_icon, (panel_x + 20, berry_y))
            berry_text = font.render(f"Ягоды: {berries}", True, (255, 255, 255))
            screen.blit(berry_text, (panel_x + 60, berry_y))
            use_btn_rect = pygame.Rect(panel_x + 230, berry_y - 5, 120, 35)
            if berries > 0:
                pygame.draw.rect(screen, (0, 180, 0), use_btn_rect, border_radius=8)
                use_text = font.render("Применить", True, (255, 255, 255))
            else:
                pygame.draw.rect(screen, (80, 80, 80), use_btn_rect, border_radius=8)
                use_text = font.render("Нет", True, (200, 200, 200))
            use_text_rect = use_text.get_rect(center=use_btn_rect.center)
            screen.blit(use_text, use_text_rect)

            svetilo_y = berry_y + line_h + 10
            screen.blit(svetilo_icon, (panel_x + 20, svetilo_y))
            svetilo_text = font.render(f"Светило: {svetilo_count}", True, (255, 255, 255))
            screen.blit(svetilo_text, (panel_x + 60, svetilo_y))
            apply_svetilo_btn = pygame.Rect(panel_x + 230, svetilo_y - 5, 120, 35)
            if svetilo_count > 0:
                pygame.draw.rect(screen, (0, 180, 200), apply_svetilo_btn, border_radius=8)
                svetilo_btn_text = font.render("Применить", True, (255, 255, 255))
            else:
                pygame.draw.rect(screen, (80, 80, 80), apply_svetilo_btn, border_radius=8)
                svetilo_btn_text = font.render("Нет", True, (200, 200, 200))
            svetilo_btn_rect = svetilo_btn_text.get_rect(center=apply_svetilo_btn.center)
            screen.blit(svetilo_btn_text, svetilo_btn_rect)

            ldishka_y = svetilo_y + line_h + 10
            screen.blit(ldishka_icon, (panel_x + 20, ldishka_y))
            ldishka_text = font.render(f"Льдышка: {ldishka_count}", True, (255, 255, 255))
            screen.blit(ldishka_text, (panel_x + 60, ldishka_y))
            apply_ldishka_btn = pygame.Rect(panel_x + 230, ldishka_y - 5, 120, 35)
            if ldishka_count > 0:
                pygame.draw.rect(screen, (0, 180, 200), apply_ldishka_btn, border_radius=8)
                ldishka_btn_text = font.render("Применить", True, (255, 255, 255))
            else:
                pygame.draw.rect(screen, (80, 80, 80), apply_ldishka_btn, border_radius=8)
                ldishka_btn_text = font.render("Нет", True, (200, 200, 200))
            ldishka_btn_rect = ldishka_btn_text.get_rect(center=apply_ldishka_btn.center)
            screen.blit(ldishka_btn_text, ldishka_btn_rect)

            rubin_y = ldishka_y + line_h + 10
            screen.blit(rubin_icon, (panel_x + 20, rubin_y))
            rubin_text = font.render(f"Рубин: {rubin_count}", True, (255, 255, 255))
            screen.blit(rubin_text, (panel_x + 60, rubin_y))
            apply_rubin_btn = pygame.Rect(panel_x + 230, rubin_y - 5, 120, 35)
            if rubin_count > 0:
                pygame.draw.rect(screen, (180, 0, 0), apply_rubin_btn, border_radius=8)
                rubin_btn_text = font.render("Применить", True, (255, 255, 255))
            else:
                pygame.draw.rect(screen, (80, 80, 80), apply_rubin_btn, border_radius=8)
                rubin_btn_text = font.render("Нет", True, (200, 200, 200))
            rubin_btn_rect = rubin_btn_text.get_rect(center=apply_rubin_btn.center)
            screen.blit(rubin_btn_text, rubin_btn_rect)

            weapon_y = rubin_y + line_h + 15
            weapon_label = font.render("Оружие:", True, (255, 255, 255))
            screen.blit(weapon_label, (panel_x + 20, weapon_y))
            weapon_btns = []
            btn_x = panel_x + 20
            btn_y = weapon_y + 30
            for w in owned_weapons:
                btn_rect = pygame.Rect(btn_x, btn_y, 100, 30)
                weapon_btns.append((w, btn_rect))
                if w == weapon:
                    color = (0, 200, 0)
                else:
                    color = (80, 80, 80)
                pygame.draw.rect(screen, color, btn_rect, border_radius=6)
                w_name = {"pistol": "Пистолет", "shotgun": "Дробовик", "rpg": "RPG", "sniper": "Винтовка"}.get(w, w)
                w_text = font_small.render(w_name, True, (255, 255, 255))
                w_rect = w_text.get_rect(center=btn_rect.center)
                screen.blit(w_text, w_rect)
                btn_x += 110
                if btn_x + 110 > panel_x + panel_w - 20:
                    btn_x = panel_x + 20
                    btn_y += 40

            mouse_pos = pygame.mouse.get_pos()
            if pygame.mouse.get_pressed()[0]:
                if use_btn_rect.collidepoint(mouse_pos) and berries > 0:
                    berries -= 1
                    hp += 2
                    if hp > 100:
                        hp = 100
                    pygame.time.wait(100)
                elif apply_svetilo_btn.collidepoint(mouse_pos) and svetilo_count > 0:
                    svetilo_count -= 1
                    svetilo_buff_timer = 300
                    pygame.time.wait(100)
                elif apply_ldishka_btn.collidepoint(mouse_pos) and ldishka_count > 0:
                    ldishka_count -= 1
                    ldishka_buff_timer = 240
                    pygame.time.wait(100)
                elif apply_rubin_btn.collidepoint(mouse_pos) and rubin_count > 0:
                    rubin_count -= 1
                    rubin_buff_timer = 300
                    pygame.time.wait(100)
                for w, btn in weapon_btns:
                    if btn.collidepoint(mouse_pos) and w != weapon:
                        weapon = w
                        ammo = 15
                        reloading = False
                        reload_timer = 0
                        pygame.time.wait(100)

        if reloading:
            pygame.draw.rect(screen, (100, 100, 100), (20, 110, 200, 15))
            pygame.draw.rect(screen, (255, 255, 0), (20, 110, int(200 * (reload_timer / 120)), 15))

        if not arena_mode and current_location not in ["bases", "base_home", "hotspot"] and not teleport_zone:
            shop_x, shop_y = objs[1]
            shop_rect = pygame.Rect(shop_x, shop_y, object2.get_width(), object2.get_height())
            if shop_rect.inflate(200, 200).collidepoint(player_x, player_y):
                btn_shop_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 100, 200, 50)
                draw_button(screen, "Открыть магазин", btn_shop_rect, btn_shop_rect.collidepoint(pygame.mouse.get_pos()))
                if pygame.mouse.get_pressed()[0] and btn_shop_rect.collidepoint(pygame.mouse.get_pos()):
                    if not hasattr(game, 'shop_click_cooldown') or game.shop_click_cooldown == 0:
                        show_shop_menu()
                        game.shop_click_cooldown = 20
                if hasattr(game, 'shop_click_cooldown') and game.shop_click_cooldown > 0:
                    game.shop_click_cooldown -= 1

        # ---- МИНИ-КАРТА ----
        mm = 160
        m = pygame.Surface((mm, mm))
        m.fill((30, 30, 30))
        if arena_mode:
            sc = mm / MAP_SIZE_ARENA
            pygame.draw.circle(m, (0, 255, 0), (int(player_x * sc), int(player_y * sc)), 4)
            for enemy in arena_enemies:
                ex, ey, _, _, _ = enemy
                pygame.draw.circle(m, (255, 0, 0), (int(ex * sc), int(ey * sc)), 3)
        else:
            if current_location == "bases":
                sc = mm / MAP_SIZE_BASES
                safe_center = (SAFE_ZONE_RECT.centerx, SAFE_ZONE_RECT.centery)
                pygame.draw.rect(m, (0, 255, 0), (int(safe_center[0]*sc)-5, int(safe_center[1]*sc)-5, 10, 10))
                for i, rect in enumerate(BASE_RECTS):
                    center = (rect.centerx, rect.centery)
                    color = (0, 255, 0) if bases_captured[i] else (255, 0, 0)
                    pygame.draw.circle(m, color, (int(center[0]*sc), int(center[1]*sc)), 6)
                pygame.draw.circle(m, (0, 255, 0), (int(player_x * sc), int(player_y * sc)), 4)
            elif current_location == "base_home":
                sc = mm / MAP_SIZE_ARENA
                pygame.draw.circle(m, (0, 255, 0), (int(player_x * sc), int(player_y * sc)), 4)
                if base_werstak_pos:
                    pygame.draw.circle(m, (0, 200, 255), (int(base_werstak_pos[0]*sc), int(base_werstak_pos[1]*sc)), 3)
                if base_safe_pos:
                    pygame.draw.circle(m, (0, 200, 255), (int(base_safe_pos[0]*sc), int(base_safe_pos[1]*sc)), 3)
                if base_teleport_pos:
                    pygame.draw.circle(m, (255, 200, 0), (int(base_teleport_pos[0]*sc), int(base_teleport_pos[1]*sc)), 4)
            elif current_location == "hotspot":
                sc = mm / MAP_SIZE
                if hotspot_safe_zone_rect is not None:
                    pygame.draw.rect(m, (0, 255, 0), (int(hotspot_safe_zone_rect.x*sc), int(hotspot_safe_zone_rect.y*sc),
                                                       int(hotspot_safe_zone_rect.width*sc), int(hotspot_safe_zone_rect.height*sc)), 1)
                    pygame.draw.circle(m, (0, 255, 0), (int(player_x * sc), int(player_y * sc)), 4)
                    for gen in generators:
                        if gen[2] > 0:
                            pygame.draw.circle(m, (255, 200, 0), (int(gen[0]*sc), int(gen[1]*sc)), 3)
                    for mon in hotspot_monsters:
                        mx, my, _, mtype, _, _, _ = mon
                        if mtype == "boss":
                            pygame.draw.circle(m, (150, 0, 200), (int(mx*sc), int(my*sc)), 5)
                        else:
                            pygame.draw.circle(m, (255, 0, 0), (int(mx*sc), int(my*sc)), 2)
            else:
                sc = mm / MAP_SIZE
                pygame.draw.circle(m, (0, 255, 0), (int(player_x * sc), int(player_y * sc)), 4)
                if boss:
                    pygame.draw.circle(m, (150, 0, 200), (int(boss[0] * sc), int(boss[1] * sc)), 6)
                for z in zombies:
                    pygame.draw.circle(m, (255, 0, 0), (int(z[0] * sc), int(z[1] * sc)), 2)
                if teleport_zone:
                    pygame.draw.circle(m, (0, 200, 255), (int(secret_x * sc), int(secret_y * sc)), 3)
                    pygame.draw.circle(m, (0, 0, 255), (int(bike_trader_x * sc), int(bike_trader_y * sc)), 4)
                    pygame.draw.circle(m, (0, 0, 255), (int(boss_npc_x * sc), int(boss_npc_y * sc)), 4)
                    for wolf in wolves:
                        pygame.draw.circle(m, (255, 255, 0), (int(wolf[0] * sc), int(wolf[1] * sc)), 3)
                    for bear in bears:
                        pygame.draw.circle(m, (255, 255, 255), (int(bear[0] * sc), int(bear[1] * sc)), 4)
                else:
                    for p in objs:
                        pygame.draw.circle(m, (0, 200, 255), (int(p[0] * sc), int(p[1] * sc)), 3)
        pygame.draw.rect(m, (255, 255, 255), (0, 0, mm, mm), 2)
        screen.blit(m, (WIDTH - mm - 10, 10))

        if not arena_mode and current_location not in ["bases", "base_home", "hotspot"]:
            minimap_center_x = WIDTH - mm//2 - 10
            arena_btn_rect = pygame.Rect(0, 10 + mm + 5, arena_img.get_width(), arena_img.get_height())
            arena_btn_rect.centerx = minimap_center_x
            mouse_pos = pygame.mouse.get_pos()
            screen.blit(arena_img, arena_btn_rect)
            if arena_btn_rect.collidepoint(mouse_pos):
                overlay = pygame.Surface(arena_btn_rect.size)
                overlay.set_alpha(80)
                overlay.fill((255, 255, 255))
                screen.blit(overlay, arena_btn_rect)
            if pygame.mouse.get_pressed()[0] and arena_btn_rect.collidepoint(mouse_pos):
                if not hasattr(game, 'arena_click_cooldown') or game.arena_click_cooldown == 0:
                    if arena_menu():
                        arena_mode = True
                        arena_return_x = player_x
                        arena_return_y = player_y
                        arena_return_teleport_zone = teleport_zone
                        arena_reward_given = False
                        arena_enemies = []
                        for _ in range(4):
                            while True:
                                x = random.randint(200, MAP_SIZE_ARENA - 200)
                                y = random.randint(200, MAP_SIZE_ARENA - 200)
                                if math.hypot(x - MAP_SIZE_ARENA//2, y - MAP_SIZE_ARENA//2) > 100:
                                    arena_enemies.append([x, y, 4, "wolf", "right"])
                                    break
                        for _ in range(3):
                            while True:
                                x = random.randint(200, MAP_SIZE_ARENA - 200)
                                y = random.randint(200, MAP_SIZE_ARENA - 200)
                                if math.hypot(x - MAP_SIZE_ARENA//2, y - MAP_SIZE_ARENA//2) > 100:
                                    arena_enemies.append([x, y, 12, "bear", "right"])
                                    break
                        for _ in range(5):
                            while True:
                                x = random.randint(200, MAP_SIZE_ARENA - 200)
                                y = random.randint(200, MAP_SIZE_ARENA - 200)
                                if math.hypot(x - MAP_SIZE_ARENA//2, y - MAP_SIZE_ARENA//2) > 100:
                                    arena_enemies.append([x, y, 4, "zombie", "right"])
                                    break
                        player_x = MAP_SIZE_ARENA // 2
                        player_y = MAP_SIZE_ARENA // 2
                        bike_active = False
                        arena_dog_was_active = dog_active
                        dog_active = False
                        bullets = []
                        game.arena_click_cooldown = 20
            if hasattr(game, 'arena_click_cooldown') and game.arena_click_cooldown > 0:
                game.arena_click_cooldown -= 1

        bike_hint = font.render("G - призвать мотоцикл", True, (255, 255, 255))
        screen.blit(bike_hint, (20, HEIGHT - 70))
        exit_text = font.render("ESC - выйти в меню", True, (255, 255, 255))
        screen.blit(exit_text, (WIDTH - exit_text.get_width() - 20, HEIGHT - 40))

        # ---- ОТРИСОВКА СЕНСОРНОГО УПРАВЛЕНИЯ ----
        # Джойстик
        pygame.draw.circle(screen, (100, 100, 100, 180), joystick_center, joystick_radius, 2)
        pygame.draw.circle(screen, (50, 50, 50, 120), joystick_center, joystick_radius)
        if joystick_active:
            knob_x = joystick_center[0] + joystick_dx * joystick_radius
            knob_y = joystick_center[1] + joystick_dy * joystick_radius
        else:
            knob_x, knob_y = joystick_center
        pygame.draw.circle(screen, (0, 255, 0), (int(knob_x), int(knob_y)), joystick_knob_radius)
        pygame.draw.circle(screen, (200, 255, 200), (int(knob_x), int(knob_y)), joystick_knob_radius, 2)

        # Кнопки
        for key, btn_data in button_rects.items():
            rect = btn_data['rect']
            color = (80, 80, 80)
            if btn_data['pressed']:
                color = (0, 200, 0)
            elif rect.collidepoint(pygame.mouse.get_pos()):
                color = (120, 120, 120)
            pygame.draw.rect(screen, color, rect, border_radius=8)
            pygame.draw.rect(screen, (200, 200, 200), rect, width=2, border_radius=8)
            label = key if key != 'A' else '⚔'
            text_surf = font_small.render(label, True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=rect.center)
            screen.blit(text_surf, text_rect)

        pygame.display.flip()

# ---- ГЛАВНЫЙ ЦИКЛ ----
while True:
    mode, bonus = menu()
    game(mode, bonus)