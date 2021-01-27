import pygame
import game_init
import time
from constants import TILE_SIZE
from global_functions import terminate, load_image

from background import Background
from scene import Scene
from camera import Camera
from game_map import GameMap
from objects import *
from player import Player
from text import Text
from shadows import Shadow
from enemy import Enemy
from shield import Shield
from pause import Pause
from score import Score
from lost_game_screen import LostGameScreen


def start_screen():
    pass


def restart_game():
    global development_mode, mouse_rb_click_position, background, score, camera, \
        game_map, player, fps_text, pause, full_time, lost_game_screen, scene, first_touch
    development_mode = False
    mouse_rb_click_position = None

    background = Background()
    scene = Scene()
    camera = Camera((0, 0))
    game_map = GameMap(scene)
    player = Player(scene, game_map)
    player.set_ability(Shield(scene, player))
    fps_text = Text(25)
    pause = Pause()
    score = Score(75)
    lost_game_screen = LostGameScreen()

    player.set_coord(game_map.get_start_player_pos())
    camera.look_at(player)
    camera.set_target(player)

    full_time = time.time()
    first_touch = False


screen = game_init.get_screen()

development_mode = False
mouse_rb_click_position = None

background = Background()
scene = Scene()
camera = Camera((0, 0))
game_map = GameMap(scene)
player = Player(scene, game_map)
player.set_ability(Shield(scene, player))
fps_text = Text(25)
pause = Pause()
score = Score(75)
lost_game_screen = LostGameScreen()

first_touch_text = Text(20)
first_touch_text.create("press any key to start...", (WIDTH // 2, HEIGHT // 2 + 200), "white",
                        center=True)

player.set_coord(game_map.get_start_player_pos())
camera.look_at(player)
camera.set_target(player)

FPS = 1000
first_touch = False
full_time = time.time()
while True:
    for obj in scene.get_objects():
        obj.dx = obj.dy = 0
        if isinstance(obj, ObjectWithMove):
            obj.corners = [False for c in obj.corners]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not pause.get_active():
                if event.button == pygame.BUTTON_RIGHT:
                    mouse_rb_click_position = pygame.mouse.get_pos()
                    if not development_mode:
                        player.use_ability()
                if event.button == pygame.BUTTON_LEFT:
                    player.gun.punch()
            first_touch = True
        if event.type == pygame.KEYDOWN:
            if not pause.get_active():
                if event.key == pygame.K_F1 and not pause.get_active():
                    development_mode = not development_mode
                    if not development_mode:
                        camera.look_at(camera.get_target())
                if event.key == pygame.K_SPACE:
                    player.jump()
                if event.key == pygame.K_e:
                    player.use_ability()
                if event.key == pygame.K_q:
                    player.gun.punch()
            if event.key == pygame.K_f and player.is_alive() and first_touch:
                pause.switch()
            first_touch = True

    if not pause.get_active():
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            player.move_aside(-1, FPS)
        if keys[pygame.K_d]:
            player.move_aside(1, FPS)

    if not pause.get_active():
        for obj in scene.get_objects():
            if not isinstance(obj, Enemy) and not isinstance(obj, Shadow):
                obj.update(FPS)
        for obj in scene.get_objects():
            if isinstance(obj, Enemy):
                obj.update(FPS)
                if first_touch:
                    obj.update_target(player)
        for obj in scene.get_objects():
            if isinstance(obj, Shadow):
                obj.update(FPS)

    game_map.update(player)

    buttons = pygame.mouse.get_pressed(num_buttons=3)
    if development_mode and buttons[2]:
        new_mouse_position = pygame.mouse.get_pos()
        dx, dy = new_mouse_position[0] - mouse_rb_click_position[0], new_mouse_position[1] - \
                 mouse_rb_click_position[1]
        mouse_rb_click_position = new_mouse_position
        camera.move((-dx / TILE_SIZE, -dy / TILE_SIZE))
    elif not development_mode:
        camera.follow_up()
    for obj in scene.get_objects():
        try:
            camera.apply(obj)
        except TypeError:
            pass

    if not development_mode:
        k = 0.8
        background.move((-player.dx * TILE_SIZE * k, -player.dy * TILE_SIZE * k))
    background.update()

    screen.fill((30, 30, 30))
    background.draw(screen)

    for obj in scene.get_objects_with_sprites():
        if obj.active:
            obj.draw(screen)

    if development_mode and not pause.get_active():
        fps_text.create(str(int(FPS)), (10, 10), (0, 0, 0), center=False)
        pygame.draw.rect(screen, "white", fps_text.rect_image)
        fps_text.draw(screen)

    if not first_touch:
        first_touch_text.draw(screen)

    if pause.get_active():
        pause.draw(screen)
    else:
        score.set_score(player.get_kills())
        score.draw(screen)

    if not player.is_alive():
        if lost_game_screen.time < lost_game_screen.cd:
            lost_game_screen.update(FPS)
        else:
            restart_game()

    pygame.display.flip()

    try:
        FPS = 1 / (time.time() - full_time)
    except ZeroDivisionError:
        FPS = 1000
    full_time = time.time()
