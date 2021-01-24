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

development_mode = False
mouse_rb_click_position = None

screen = game_init.get_screen()
FPS = 1000

background = Background()
scene = Scene()
camera = Camera((0, 0))
game_map = GameMap(scene)
player = Player(scene, game_map)
player.set_ability(Shield(scene, player))
fps_text = Text(25)

player.set_coord(game_map.get_start_player_pos())
camera.look_at(player)
camera.set_target(player)

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
            if event.button == pygame.BUTTON_RIGHT:
                mouse_rb_click_position = pygame.mouse.get_pos()
                if not development_mode:
                    player.use_ability()
            if event.button == pygame.BUTTON_LEFT:
                player.gun.punch()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F1:
                development_mode = not development_mode
                if not development_mode:
                    camera.look_at(camera.get_target())
            if event.key == pygame.K_SPACE:
                player.jump()
            if event.key == pygame.K_e:
                player.use_ability()
            if event.key == pygame.K_q:
                player.gun.punch()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player.move_aside(-1, FPS)
    if keys[pygame.K_d]:
        player.move_aside(1, FPS)

    for obj in scene.get_objects():
        if not isinstance(obj, Enemy) and not isinstance(obj, Shadow):
            obj.update(FPS)
    for obj in scene.get_objects():
        if isinstance(obj, Enemy):
            obj.update(FPS)
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

    if development_mode:
        pygame.draw.rect(screen, "white", fps_text.rect_image)
        fps_text.create(str(int(FPS)), (10, 10), (0, 0, 0))
        fps_text.draw(screen)
    pygame.display.flip()

    try:
        FPS = 1 / (time.time() - full_time)
    except ZeroDivisionError:
        FPS = 1000
    full_time = time.time()
