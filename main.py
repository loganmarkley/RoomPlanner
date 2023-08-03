# Room Planner!
# Author: Logan Markley
# Last Updated: 8/2/2023
# Version: Not Finished
# Latest Addition: Able to move vertices by dragging and dropping and the "walls" automatically update
# Date Started: 8/2/2023
# Desc: Using Pygame and maybe Pickle, create a fully functioning room planner
#       where you can drag and drop items, customize dimensions, etc.

import pygame, sys, pickle


def draw_line(vertex1, vertex2) -> None:    # this static function allows for easy color changing and simpler lines
    offset = pygame.math.Vector2(8, 8)  # 8 comes from the radius of the vertices
    vertex1_vector = pygame.math.Vector2(vertex1.rect.x, vertex1.rect.y) + offset
    vertex2_vector = pygame.math.Vector2(vertex2.rect.x, vertex2.rect.y) + offset
    pygame.draw.aaline(screen, (150, 150, 150), vertex1_vector, vertex2_vector)
    # draw line starts the line from the top left corner of the rect, but we want to connect it
    # to the center of our rectangle, so we need to offset the position vector by half of the radius


def draw_grid() -> None:
    for i in range(0, 80):      # draws horizontal lines and then vertical lines
        pygame.draw.line(screen, (230, 230, 230), (0, i * 15), (SCREEN_WIDTH, i * 15))
        pygame.draw.line(screen, (230, 230, 230), (i * 15, 0), (i * 15, SCREEN_HEIGHT))


class Room:
    def __init__(self):
        self.vertex1 = Vertex(400, 400)
        self.vertex2 = Vertex(700, 400)
        self.vertex3 = Vertex(700, 800)
        self.vertex4 = Vertex(400, 800)

        self.wall_vertices = [self.vertex1, self.vertex2, self.vertex3, self.vertex4]

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


class Vertex:
    def __init__(self, x_pos: int, y_pos: int):
        self.rect = pygame.Rect(0, 0, 16, 16)
        self.rect.center = (x_pos, y_pos)

    def draw_vertex(self) -> None:
        pygame.draw.rect(screen, (90, 90, 90), self.rect, 0, 8)


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

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 100)

room = Room()
active_vertex_index = -1
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for num, vertex in enumerate(room.wall_vertices):
                    if vertex.rect.collidepoint(event.pos):
                        active_vertex_index = num

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                active_vertex_index = -1

        if event.type == pygame.MOUSEMOTION:
            if active_vertex_index != -1:
                room.wall_vertices[active_vertex_index].rect.move_ip(event.rel)
        # if event.type == pygame.MOUSEWHEEL: #mouse wheel zoom
        #     camera_group.zoom_scale += event.y * 0.03

    screen.fill(SCREEN_BACKGROUND_COLOR)

    draw_grid()
    room.draw_walls()
    room.draw_vertices()

    pygame.display.update()
    clock.tick(60)
