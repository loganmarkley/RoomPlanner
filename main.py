# Room Planner!
# Author: Logan Markley
# Last Updated: 8/4/2023
# Version: Not Finished
# Latest Addition: Added furniture panel and text to the buttons, and some other small changes
# Date Started: 8/2/2023
# Desc: Using Pygame and maybe Pickle, create a fully functioning room planner
#       where you can drag and drop items, customize dimensions, etc.

import pygame
from sys import exit
from math import sqrt


def draw_line(vertex1, vertex2) -> None:  # this static function allows for easy color changing and simpler lines
    offset = pygame.math.Vector2(VERTEX_RADIUS, VERTEX_RADIUS)
    vertex1_vector = pygame.math.Vector2(vertex1.rect.x, vertex1.rect.y) + offset
    vertex2_vector = pygame.math.Vector2(vertex2.rect.x, vertex2.rect.y) + offset
    pygame.draw.aaline(screen, (150, 150, 150), vertex1_vector, vertex2_vector)
    # draw line starts the line from the top left corner of the rect, but we want to connect it
    # to the center of our rectangle, so we need to offset the position vector by half of the radius


def calculate_distance(vertex1, vertex2) -> int:  # returns the distance between two vertices in "inches"
    x_difference = vertex1.rect.x - vertex2.rect.x
    y_difference = vertex1.rect.y - vertex2.rect.y
    hypotenuse = sqrt(x_difference ** 2 + y_difference ** 2)
    return int(hypotenuse // 4)  # (4px = 1in)


def calculate_halfway_point(vertex1, vertex2) -> tuple:
    x_pos = (vertex1.rect.centerx + vertex2.rect.centerx) // 2
    y_pos = (vertex1.rect.centery + vertex2.rect.centery) // 2
    return x_pos, y_pos


class Room:
    def __init__(self):
        self.vertex1 = Vertex(700, 300)
        self.vertex2 = Vertex(1100, 300)
        self.vertex3 = Vertex(1100, 600)
        self.vertex4 = Vertex(700, 600)

        self.wall_vertices = [self.vertex1, self.vertex2, self.vertex3, self.vertex4]

    def add_vertex(self) -> None:
        vert1 = self.wall_vertices[0]
        vert2 = self.wall_vertices[len(self.wall_vertices) - 1]
        halfway_pt = calculate_halfway_point(vert1, vert2)
        self.wall_vertices.append(Vertex(halfway_pt[0], halfway_pt[1]))

    def minus_vertex(self) -> None:
        if len(self.wall_vertices) > 2:
            self.wall_vertices.pop(len(self.wall_vertices) - 1)

    def draw_walls(self) -> None:
        all_connected = False
        current_index = 0
        while not all_connected:
            draw_line(self.wall_vertices[current_index], self.wall_vertices[current_index + 1])
            if current_index < len(self.wall_vertices) - 2:
                current_index += 1
            else:
                all_connected = True
                draw_line(self.wall_vertices[current_index + 1], self.wall_vertices[0])  # This draws the last line

    def draw_vertices(self) -> None:
        for i in range(0, len(self.wall_vertices)):
            self.wall_vertices[i].draw_vertex()

    def draw_wall_dimensions(self) -> None:
        f = pygame.font.Font('Fonts/MADEVoyager.otf', 16)
        for i in range(0, len(self.wall_vertices)):
            if i == len(self.wall_vertices) - 1:
                distance = calculate_distance(self.wall_vertices[i], self.wall_vertices[0])
                halfway_pt = calculate_halfway_point(self.wall_vertices[i], self.wall_vertices[0])
            else:
                distance = calculate_distance(self.wall_vertices[i], self.wall_vertices[i + 1])
                halfway_pt = calculate_halfway_point(self.wall_vertices[i], self.wall_vertices[i + 1])
            dimension = str(distance) + '"'
            text_surface = f.render(dimension, True, (100, 100, 100))
            screen.blit(text_surface, (halfway_pt[0] + 5, halfway_pt[1] - 20))  # arbitrary styling numbers


class Vertex:
    def __init__(self, x_pos: int, y_pos: int):
        self.rect = pygame.Rect(0, 0, VERTEX_RADIUS * 2, VERTEX_RADIUS * 2)
        self.rect.center = (x_pos, y_pos)

    def draw_vertex(self) -> None:
        pygame.draw.rect(screen, (90, 90, 90), self.rect, 0, VERTEX_RADIUS)


class UserInterface:
    def __init__(self):
        self.FURNITURE_PANEL_WIDTH = 400
        self.btn_add_vertex_rect = pygame.Rect(SCREEN_WIDTH - 75, SCREEN_HEIGHT - 75, 50, 50)
        self.btn_minus_vertex_rect = pygame.Rect(SCREEN_WIDTH - 140, SCREEN_HEIGHT - 75, 50, 50)
        self.btn_show_grid_rect = pygame.Rect(30 + self.FURNITURE_PANEL_WIDTH, SCREEN_HEIGHT - 75, 50, 50)

    def draw_user_interface(self):
        self.draw_furniture_panel()
        pygame.draw.rect(screen, (100, 200, 100), self.btn_add_vertex_rect, 0, 10)
        pygame.draw.rect(screen, (200, 100, 100), self.btn_minus_vertex_rect, 0, 10)
        pygame.draw.rect(screen, (150, 150, 150), self.btn_show_grid_rect, 0, 10)

        f = pygame.font.Font('Fonts/MADEVoyager.otf', 23)
        text_surface = f.render('Grid', True, (50, 50, 50))
        screen.blit(text_surface, (self.FURNITURE_PANEL_WIDTH + 33, SCREEN_HEIGHT - 69))
        text_surface = f.render('Corners:', True, (100, 100, 100))
        screen.blit(text_surface, (SCREEN_WIDTH - 240, SCREEN_HEIGHT - 70))

        f = pygame.font.Font('Fonts/MADEVoyager.otf', 80)
        text_surface = f.render('-', True, (80, 80, 80))
        screen.blit(text_surface, (SCREEN_WIDTH - 127, SCREEN_HEIGHT - 114))  # minus sign on button
        text_surface = f.render('+', True, (80, 80, 80))
        screen.blit(text_surface, (SCREEN_WIDTH - 66, SCREEN_HEIGHT - 110))  # plus sign on button

    def draw_grid(self, draw_grid_bool):
        if draw_grid_bool:
            for i in range(0, 76):  # draws horizontal lines and then vertical lines with 15 pixel gaps
                pygame.draw.line(screen, (225, 225, 225), (self.FURNITURE_PANEL_WIDTH, i * 15), (SCREEN_WIDTH, i * 15))
                pygame.draw.line(screen, (225, 225, 225), (self.FURNITURE_PANEL_WIDTH + i * 15, 0),
                                 (self.FURNITURE_PANEL_WIDTH + i * 15, SCREEN_HEIGHT))

    def draw_furniture_panel(self):
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

        quarter_height = (SCREEN_HEIGHT - 55) // 4  # 55px is how far the separating line is from the top
        for i in range(1, 4):  # draws 3 lines to make 8 furniture piece sections
            rect = pygame.Rect(0, 55 + quarter_height * i, self.FURNITURE_PANEL_WIDTH, 2)
            pygame.draw.rect(screen, (180, 180, 180), rect)


# class CameraGroup(pygame.sprite.Group):
#     def __init__(self):
#         super().__init__()
#         self.display_surface = pygame.display.get_surface()
#
#         #camera offset
#         self.offset = pygame.math.Vector2()
#         self.half_w = self.display_surface.get_size()[0] // 2
#         self.half_h = self.display_surface.get_size()[1] // 2
#
#
#         #camera speed
#         self.keyboard_speed = 5
#         self.mouse_speed = 0.4
#
#         #zoom
#         self.zoom_scale = 1.0
#         self.internal_surface_size = (2500, 2500)
#         self.internal_surf = pygame.Surface(self.internal_surface_size, pygame.SRCALPHA)
#         self.internal_rect = self.internal_surf.get_rect(center = (self.half_w, self.half_h))
#         self.internal_surface_size_vector = pygame.math.Vector2(self.internal_surface_size)
#
#     def zoom_keyboard_control(self):
#         keys = pygame.key.get_pressed()
#         if keys[pygame.K_PLUS]:
#             self.zoom_scale += 0.1
#         if keys[pygame.K_MINUS]:
#             self.zoom_scale -= 0.1

pygame.init()
pygame.display.set_caption('Room Planner')

# camera_group = pygame.sprite.Group()

SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 950
SCREEN_BACKGROUND_COLOR = (240, 240, 230)
VERTEX_RADIUS = 7

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

room = Room()
ui = UserInterface()
active_vertex_index = -1
show_grid_bool = True
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for num, vertex in enumerate(room.wall_vertices):
                    if vertex.rect.collidepoint(event.pos):
                        active_vertex_index = num

                if ui.btn_add_vertex_rect.collidepoint(event.pos):
                    room.add_vertex()
                if ui.btn_minus_vertex_rect.collidepoint(event.pos):
                    room.minus_vertex()
                if ui.btn_show_grid_rect.collidepoint(event.pos):
                    show_grid_bool = not show_grid_bool

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                active_vertex_index = -1

        if event.type == pygame.MOUSEMOTION:
            if active_vertex_index != -1:
                room.wall_vertices[active_vertex_index].rect.move_ip(event.rel)
        # if event.type == pygame.MOUSEWHEEL: #mouse wheel zoom
        #     camera_group.zoom_scale += event.y * 0.03

    screen.fill(SCREEN_BACKGROUND_COLOR)

    ui.draw_grid(show_grid_bool)
    room.draw_walls()
    room.draw_vertices()
    room.draw_wall_dimensions()
    ui.draw_user_interface()

    pygame.display.update()
    clock.tick(75)  # this while loop will never run more than 75 fps
