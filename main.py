# Room Planner!
# Author: Logan Markley
# Last Updated: 8/7/2023
# Version: Not Finished
# Latest Addition: Added ability to rotate, scale, and delete furniture
# Date Started: 8/2/2023
# Desc: Using Pygame, create a fully functioning room planner
#       where you can drag and drop items, customize dimensions, etc.

from sys import exit

import math
import pygame
import random


def draw_line(vertex1, vertex2) -> None:  # this static function allows for easy color changing and simpler lines
    offset = pygame.math.Vector2(VERTEX_RADIUS, VERTEX_RADIUS)
    vertex1_vector = pygame.math.Vector2(vertex1.rect.x, vertex1.rect.y) + offset
    vertex2_vector = pygame.math.Vector2(vertex2.rect.x, vertex2.rect.y) + offset
    pygame.draw.aaline(screen, (0, 0, 0), vertex1_vector, vertex2_vector)
    # draw line starts the line from the top left corner of the rect, but we want to connect it
    # to the center of our rectangle, so we need to offset the position vector by the radius


def calculate_distance(vertex1, vertex2) -> int:  # returns the distance between two vertices in "inches"
    x_difference = vertex1.rect.x - vertex2.rect.x
    y_difference = vertex1.rect.y - vertex2.rect.y
    hypotenuse = math.sqrt(x_difference ** 2 + y_difference ** 2)
    return int(hypotenuse // PIXELS_PER_INCH)


def calculate_halfway_point(vertex1, vertex2) -> tuple:
    x_pos = (vertex1.rect.centerx + vertex2.rect.centerx) // 2
    y_pos = (vertex1.rect.centery + vertex2.rect.centery) // 2
    return x_pos, y_pos


class Room:
    def __init__(self):
        self.wall_vertices = [Vertex(550, 100), Vertex(1350, 100),
                              Vertex(1350, 800), Vertex(550, 800)]
        self.furniture_pieces = []

    def add_furniture(self, furn_object) -> None:
        self.furniture_pieces.append(furn_object)

    def delete_furniture(self, index) -> None:
        self.furniture_pieces.pop(index)

    def bring_furn_to_top(self, index) -> int:  # moves the object at index to the end of the list
        self.furniture_pieces.append(self.furniture_pieces[index])
        self.furniture_pieces.pop(index)
        return len(self.furniture_pieces) - 1

    def add_vertex(self) -> None:
        vert1 = self.wall_vertices[0]
        vert2 = self.wall_vertices[len(self.wall_vertices) - 1]
        halfway_pt = calculate_halfway_point(vert1, vert2)
        self.wall_vertices.append(Vertex(halfway_pt[0], halfway_pt[1]))

    def minus_vertex(self) -> None:
        if len(self.wall_vertices) > 2:
            self.wall_vertices.pop(len(self.wall_vertices) - 1)

    def draw_walls(self) -> None:
        for index in range(len(self.wall_vertices) - 1):
            draw_line(self.wall_vertices[index], self.wall_vertices[index + 1])
        draw_line(self.wall_vertices[len(self.wall_vertices) - 1], self.wall_vertices[0])  # draws the last line

    def draw_vertices(self) -> None:
        for i in range(0, len(self.wall_vertices)):
            self.wall_vertices[i].draw_vertex()

    def draw_wall_dimensions(self) -> None:
        f = pygame.font.Font('Fonts/MADEVoyager.otf', 18)
        for i in range(0, len(self.wall_vertices)):
            if i == len(self.wall_vertices) - 1:
                distance = calculate_distance(self.wall_vertices[0], self.wall_vertices[i])
                halfway_pt = calculate_halfway_point(self.wall_vertices[0], self.wall_vertices[i])
            else:
                distance = calculate_distance(self.wall_vertices[i], self.wall_vertices[i + 1])
                halfway_pt = calculate_halfway_point(self.wall_vertices[i], self.wall_vertices[i + 1])

            dimension = str(distance) + '"'
            text_surface = f.render(dimension, True, (100, 100, 100))
            screen.blit(text_surface, (halfway_pt[0] + 4, halfway_pt[1] - 21))  # arbitrary styling numbers

    def draw_all_furniture(self, draw_overlay, overlay_index) -> None:
        for i in range(0, len(self.furniture_pieces)):
            self.furniture_pieces[i].draw_furniture()
        if draw_overlay:
            self.furniture_pieces[overlay_index].draw_furn_overlay()


class Vertex:
    def __init__(self, x_pos: int, y_pos: int):
        self.rect = pygame.Rect(0, 0, VERTEX_RADIUS * 2, VERTEX_RADIUS * 2)
        self.rect.center = (x_pos, y_pos)

    def draw_vertex(self) -> None:
        pygame.draw.rect(screen, (90, 90, 90), self.rect, 0, VERTEX_RADIUS)


class Furniture:
    def __init__(self, f_type):
        self.furn_type = f_type
        if self.furn_type == 'Bed':
            self.img = pygame.transform.scale_by(BED_IMG, .47)
        elif self.furn_type == 'Desk':
            self.img = pygame.transform.scale_by(DESK_IMG, .25)
        elif self.furn_type == 'Nightstand':
            self.img = pygame.transform.scale_by(NIGHTSTAND_IMG, .23)
        elif self.furn_type == 'Rug':
            self.img = pygame.transform.scale_by(RUG_IMG, .24)
        elif self.furn_type == 'Dresser':
            self.img = pygame.transform.scale_by(DRESSER_IMG, .33)
        elif self.furn_type == 'Chair':
            self.img = pygame.transform.scale_by(CHAIR_IMG, .32)
        elif self.furn_type == 'TV':
            self.img = pygame.transform.scale_by(TV_IMG, .32)
        elif self.furn_type == 'Lamp':
            self.img = pygame.transform.scale_by(LAMP_IMG, .32)
        elif self.furn_type == 'Door':
            self.img = pygame.transform.scale_by(DOOR_IMG, .32)
        elif self.furn_type == 'Window':
            self.img = pygame.transform.scale_by(WINDOW_IMG, .32)
        self.rect = self.img.get_rect()
        x_pos = random.randint(730, 1070)  # initially spawn the furniture randomly in the middle
        y_pos = random.randint(330, 570)
        self.rect.center = (x_pos, y_pos)

        self.rotate_btn_img = pygame.image.load('Graphics/rotate_arrow.png').convert_alpha()
        self.rotate_btn_rect = self.rotate_btn_img.get_rect()
        self.delete_btn_img = pygame.image.load('Graphics/red_x_circle.png').convert_alpha()
        self.delete_btn_rect = self.delete_btn_img.get_rect()

    def draw_furniture(self) -> None:
        screen.blit(self.img, self.rect.topleft)

    def draw_furn_overlay(self) -> None:
        self.rotate_btn_rect.topleft = self.rect.bottomright
        screen.blit(self.rotate_btn_img, self.rotate_btn_rect.topleft)
        self.delete_btn_rect.topleft = self.rect.topright
        screen.blit(self.delete_btn_img, self.delete_btn_rect.topleft)

    def rotate_furniture(self, mouse) -> None:
        old_center = self.rect.center
        x = mouse[0] - self.rect.centerx
        y = mouse[1] - self.rect.centery
        d = math.sqrt(x ** 2 + y ** 2)
        angle = math.degrees(-math.atan2(y, x))
        scale = abs(3.1 * d / SCREEN_WIDTH)
        self.img = pygame.transform.rotozoom(globals()[self.furn_type.upper() + '_IMG'], angle, scale)
        self.rect = self.img.get_rect()
        self.rect.center = old_center


class UserInterface:
    def __init__(self):
        self.FURNITURE_PANEL_WIDTH = 400
        self.btn_add_vertex_rect = pygame.Rect(SCREEN_WIDTH - 75, SCREEN_HEIGHT - 75, 50, 50)
        self.btn_minus_vertex_rect = pygame.Rect(SCREEN_WIDTH - 140, SCREEN_HEIGHT - 75, 50, 50)
        self.btn_show_grid_rect = pygame.Rect(26 + self.FURNITURE_PANEL_WIDTH, SCREEN_HEIGHT - 75, 50, 50)

        btn_width = int(self.FURNITURE_PANEL_WIDTH / 2 - 4)
        btn_height = int((SCREEN_HEIGHT - 55) // 5 - 4)
        self.btn_bed_rect = pygame.Rect(2, 58, btn_width, btn_height)
        self.btn_desk_rect = pygame.Rect(7 + btn_width, 58, btn_width, btn_height)
        self.btn_nightstand_rect = pygame.Rect(2, 58 + btn_height + 4, btn_width, btn_height)
        self.btn_rug_rect = pygame.Rect(7 + btn_width, 58 + btn_height + 4, btn_width, btn_height)
        self.btn_dresser_rect = pygame.Rect(2, 58 + 2 * (btn_height + 4), btn_width, btn_height)
        self.btn_chair_rect = pygame.Rect(7 + btn_width, 58 + 2 * (btn_height + 4), btn_width, btn_height)
        self.btn_tv_rect = pygame.Rect(2, 58 + 3 * (btn_height + 4), btn_width, btn_height)
        self.btn_lamp_rect = pygame.Rect(7 + btn_width, 58 + 3 * (btn_height + 4), btn_width, btn_height)
        self.btn_door_rect = pygame.Rect(2, 58 + 4 * (btn_height + 4), btn_width, btn_height)
        self.btn_window_rect = pygame.Rect(7 + btn_width, 58 + 4 * (btn_height + 4), btn_width, btn_height)

    def draw_user_interface(self) -> None:
        self.draw_furniture_panel()
        pygame.draw.rect(screen, (100, 200, 100), self.btn_add_vertex_rect, 0, 10)
        pygame.draw.rect(screen, (200, 100, 100), self.btn_minus_vertex_rect, 0, 10)
        pygame.draw.rect(screen, (150, 150, 150), self.btn_show_grid_rect, 0, 10)

        f = pygame.font.Font('Fonts/MADEVoyager.otf', 23)
        text_surface = f.render('Grid', True, (50, 50, 50))
        screen.blit(text_surface, (self.FURNITURE_PANEL_WIDTH + 29, SCREEN_HEIGHT - 69))
        text_surface = f.render('Corners:', True, (100, 100, 100))
        screen.blit(text_surface, (SCREEN_WIDTH - 240, SCREEN_HEIGHT - 70))

        f = pygame.font.Font('Fonts/MADEVoyager.otf', 80)
        text_surface = f.render('-', True, (80, 80, 80))
        screen.blit(text_surface, (SCREEN_WIDTH - 127, SCREEN_HEIGHT - 114))  # minus sign on button
        text_surface = f.render('+', True, (80, 80, 80))
        screen.blit(text_surface, (SCREEN_WIDTH - 66, SCREEN_HEIGHT - 110))  # plus sign on button

    def draw_grid(self) -> None:
        pixel_gap = 20
        num_horizontal_lines = SCREEN_HEIGHT // pixel_gap + 1  # an extra just in case
        num_vertical_lines = (SCREEN_WIDTH - self.FURNITURE_PANEL_WIDTH) // pixel_gap + 1
        for i in range(0, num_horizontal_lines):
            pygame.draw.line(screen, (225, 225, 225), (self.FURNITURE_PANEL_WIDTH, i * pixel_gap),
                             (SCREEN_WIDTH, i * pixel_gap))
        for i in range(0, num_vertical_lines):
            pygame.draw.line(screen, (225, 225, 225), (self.FURNITURE_PANEL_WIDTH + i * pixel_gap, 0),
                             (self.FURNITURE_PANEL_WIDTH + i * pixel_gap, SCREEN_HEIGHT))

    def draw_furniture_panel(self) -> None:
        rect = pygame.Rect(0, 0, self.FURNITURE_PANEL_WIDTH, SCREEN_HEIGHT)  # background gray of the panel
        pygame.draw.rect(screen, (230, 230, 230), rect)
        rect = pygame.Rect(self.FURNITURE_PANEL_WIDTH, 0, 2, SCREEN_HEIGHT)  # vertical line isolates panel
        pygame.draw.rect(screen, (120, 120, 120), rect)
        rect = pygame.Rect(self.FURNITURE_PANEL_WIDTH // 2, 55, 2, SCREEN_HEIGHT)  # vert line separates panel in half
        pygame.draw.rect(screen, (180, 180, 180), rect)
        rect = pygame.Rect(0, 55, self.FURNITURE_PANEL_WIDTH, 2)  # top horizontal line to separate text
        pygame.draw.rect(screen, (120, 120, 120), rect)

        f = pygame.font.Font('Fonts/MADEVoyager.otf', 35)
        text_surface = f.render('Furniture', True, (100, 100, 100))
        screen.blit(text_surface, (130, 5))  # arbitrary positioning numbers

        section_height = (SCREEN_HEIGHT - 55) // 5  # 55px is how far the separating line is from the top
        for i in range(1, 5):  # draws 4 lines to make 10 furniture piece sections
            rect = pygame.Rect(0, 55 + section_height * i, self.FURNITURE_PANEL_WIDTH, 2)
            pygame.draw.rect(screen, (180, 180, 180), rect)

        # drawing the furniture images:
        screen.blit(pygame.transform.scale_by(BED_IMG, .3), (40, 72))
        screen.blit(pygame.transform.scale_by(DESK_IMG, .16), (222, 104))
        screen.blit(pygame.transform.scale_by(NIGHTSTAND_IMG, .18), (43, 286))
        screen.blit(pygame.transform.scale_by(RUG_IMG, .15), (228, 290))
        screen.blit(pygame.transform.scale_by(DRESSER_IMG, .151), (27, 470))
        screen.blit(pygame.transform.scale_by(CHAIR_IMG, .18), (248, 470))
        screen.blit(pygame.transform.scale_by(TV_IMG, .16), (18, 652))
        screen.blit(pygame.transform.scale_by(LAMP_IMG, .212), (246, 634))
        screen.blit(pygame.transform.scale_by(DOOR_IMG, .172), (18, 854))
        screen.blit(pygame.transform.scale_by(WINDOW_IMG, .175), (228, 864))


pygame.init()
pygame.display.set_caption('Room Planner')

SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 960
SCREEN_BACKGROUND_COLOR = (250, 250, 245)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

VERTEX_RADIUS = 7
PIXELS_PER_INCH = 4  # (4px = 1in)

BED_IMG = pygame.image.load('Graphics/Bed.png').convert_alpha()
DESK_IMG = pygame.image.load('Graphics/Desk.png').convert_alpha()
NIGHTSTAND_IMG = pygame.image.load('Graphics/Nightstand.png').convert_alpha()
RUG_IMG = pygame.image.load('Graphics/Rug.png').convert_alpha()
DRESSER_IMG = pygame.image.load('Graphics/Dresser.png').convert_alpha()
CHAIR_IMG = pygame.image.load('Graphics/Chair.png').convert_alpha()
TV_IMG = pygame.image.load('Graphics/TV.png').convert_alpha()
LAMP_IMG = pygame.image.load('Graphics/Lamp.png').convert_alpha()
DOOR_IMG = pygame.image.load('Graphics/Door.png').convert_alpha()
WINDOW_IMG = pygame.image.load('Graphics/Window.png').convert_alpha()

clock = pygame.time.Clock()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

room = Room()
ui = UserInterface()
active_vertex_index = -1
active_furniture_index = -1
rotate_furn_btn_held = False
draw_furn_overlay = False
show_grid_bool = True
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if len(room.furniture_pieces) > 0:
                    if room.furniture_pieces[len(room.furniture_pieces) - 1].delete_btn_rect.collidepoint(event.pos):
                        room.delete_furniture(len(room.furniture_pieces) - 1)
                        draw_furn_overlay = False
                    elif room.furniture_pieces[len(room.furniture_pieces) - 1].rotate_btn_rect.collidepoint(event.pos):
                        rotate_furn_btn_held = True
                    else:
                        draw_furn_overlay = False  # turns off the overlay if the user clicks anywhere besides it

                for num, vertex in enumerate(room.wall_vertices):
                    if vertex.rect.collidepoint(event.pos):
                        active_vertex_index = num
                if active_vertex_index == -1 and not rotate_furn_btn_held:  # only checks furniture if nothing is held
                    for num, furniture in enumerate(room.furniture_pieces):
                        if furniture.rect.collidepoint(event.pos):
                            active_furniture_index = num
                            active_furniture_index = room.bring_furn_to_top(active_furniture_index)
                            draw_furn_overlay = True

                if ui.btn_add_vertex_rect.collidepoint(event.pos):
                    room.add_vertex()
                if ui.btn_minus_vertex_rect.collidepoint(event.pos):
                    room.minus_vertex()
                if ui.btn_show_grid_rect.collidepoint(event.pos):
                    show_grid_bool = not show_grid_bool

                if ui.btn_bed_rect.collidepoint(event.pos):
                    room.add_furniture(Furniture('Bed'))
                if ui.btn_desk_rect.collidepoint(event.pos):
                    room.add_furniture(Furniture('Desk'))
                if ui.btn_nightstand_rect.collidepoint(event.pos):
                    room.add_furniture(Furniture('Nightstand'))
                if ui.btn_rug_rect.collidepoint(event.pos):
                    room.add_furniture(Furniture('Rug'))
                if ui.btn_dresser_rect.collidepoint(event.pos):
                    room.add_furniture(Furniture('Dresser'))
                if ui.btn_chair_rect.collidepoint(event.pos):
                    room.add_furniture(Furniture('Chair'))
                if ui.btn_tv_rect.collidepoint(event.pos):
                    room.add_furniture(Furniture('TV'))
                if ui.btn_lamp_rect.collidepoint(event.pos):
                    room.add_furniture(Furniture('Lamp'))
                if ui.btn_door_rect.collidepoint(event.pos):
                    room.add_furniture(Furniture('Door'))
                if ui.btn_window_rect.collidepoint(event.pos):
                    room.add_furniture(Furniture('Window'))

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                active_vertex_index = -1
                active_furniture_index = -1
            if rotate_furn_btn_held:
                rotate_furn_btn_held = False

        if event.type == pygame.MOUSEMOTION:
            if active_vertex_index != -1:
                room.wall_vertices[active_vertex_index].rect.move_ip(event.rel)
            if active_furniture_index != -1:
                room.furniture_pieces[active_furniture_index].rect.move_ip(event.rel)
            if rotate_furn_btn_held:
                room.furniture_pieces[len(room.furniture_pieces) - 1].rotate_furniture(event.pos)

    screen.fill(SCREEN_BACKGROUND_COLOR)

    if show_grid_bool:
        ui.draw_grid()
    room.draw_walls()
    room.draw_vertices()
    room.draw_wall_dimensions()
    room.draw_all_furniture(draw_furn_overlay, active_furniture_index)
    ui.draw_user_interface()

    pygame.display.update()
    clock.tick(75)  # the program will never run more than 75 fps
