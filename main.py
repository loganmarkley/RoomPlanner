# Room Planner!
# Author: Logan Markley
# Last Updated: 8/4/2023
# Version: Not Finished
# Latest Addition: Added wall dimensions and a show grid button!
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


def draw_grid() -> None:
    for i in range(0, 80):  # draws horizontal lines and then vertical lines with 15 pixel gaps
        pygame.draw.line(screen, (225, 225, 225), (0, i * 15), (SCREEN_WIDTH, i * 15))
        pygame.draw.line(screen, (225, 225, 225), (i * 15, 0), (i * 15, SCREEN_HEIGHT))


def draw_add_vertex_button(rect) -> None:       #makes a green button in bottom right corner
    pygame.draw.rect(screen, (100, 200, 100), rect)


def draw_minus_vertex_button(rect) -> None:     # makes a red button in bottom right corner
    pygame.draw.rect(screen, (200, 100, 100), rect)


def draw_show_grid_button(rect) -> None:     # makes a red button in bottom right corner
    pygame.draw.rect(screen, (150, 150, 150), rect)


def calculate_distance(vertex1, vertex2) -> int:    # returns the distance between two vertices in "inches" (5px = 1in)
    x_difference = vertex1.rect.x - vertex2.rect.x
    y_difference = vertex1.rect.y - vertex2.rect.y
    hypotenuse = sqrt(x_difference ** 2 + y_difference ** 2)
    return int(hypotenuse // 3)


def calculate_halfway_point(vertex1, vertex2) -> tuple:
    x_pos = (vertex1.rect.x + vertex2.rect.x) // 2
    y_pos = (vertex1.rect.y + vertex2.rect.y) // 2
    return x_pos, y_pos


class Room:
    def __init__(self):
        self.vertex1 = Vertex(400, 300)
        self.vertex2 = Vertex(800, 300)
        self.vertex3 = Vertex(800, 600)
        self.vertex4 = Vertex(400, 600)

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
        for i in range(0, len(self.wall_vertices)):
            if i == len(self.wall_vertices) - 1:
                distance = calculate_distance(self.wall_vertices[i], self.wall_vertices[0])
                halfway_pt = calculate_halfway_point(self.wall_vertices[i], self.wall_vertices[0])
            else:
                distance = calculate_distance(self.wall_vertices[i], self.wall_vertices[i+1])
                halfway_pt = calculate_halfway_point(self.wall_vertices[i], self.wall_vertices[i + 1])
            dimension = str(distance) + '"'
            text_surface = font.render(dimension, True, (100, 100, 100))
            screen.blit(text_surface, (halfway_pt[0], halfway_pt[1]))


class Vertex:
    def __init__(self, x_pos: int, y_pos: int):
        self.rect = pygame.Rect(0, 0, VERTEX_RADIUS * 2, VERTEX_RADIUS * 2)
        self.rect.center = (x_pos, y_pos)

    def draw_vertex(self) -> None:
        pygame.draw.rect(screen, (90, 90, 90), self.rect, 0, VERTEX_RADIUS)


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

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 950
SCREEN_BACKGROUND_COLOR = (240, 240, 230)
VERTEX_RADIUS = 7

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()

font = pygame.font.Font('Fonts/MilkyAgain.ttf', 18)

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

room = Room()
active_vertex_index = -1
add_vertex_rect = pygame.Rect(SCREEN_WIDTH - 75, SCREEN_HEIGHT - 75, 50, 50)
minus_vertex_rect = pygame.Rect(SCREEN_WIDTH - 150, SCREEN_HEIGHT - 75, 50, 50)
show_grid_rect = pygame.Rect(20, 20, 50, 50)
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

                if add_vertex_rect.collidepoint(event.pos):
                    room.add_vertex()
                if minus_vertex_rect.collidepoint(event.pos):
                    room.minus_vertex()
                if show_grid_rect.collidepoint(event.pos):
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

    if show_grid_bool:
        draw_grid()
    room.draw_walls()
    room.draw_vertices()
    draw_add_vertex_button(add_vertex_rect)
    draw_minus_vertex_button(minus_vertex_rect)
    draw_show_grid_button(show_grid_rect)
    room.draw_wall_dimensions()

    pygame.display.update()
    clock.tick(60)  # this while loop will never run more than 60 fps
