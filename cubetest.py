# made by kautzerbonito on github

import pygame
import math

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("test")

vertices = [
    [-1, -1, -1],
    [1, -1, -1],
    [1, 1, -1],
    [-1, 1, -1],
    [-1, -1, 1],
    [1, -1, 1],
    [1, 1, 1],
    [-1, 1, 1]
]

edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (0, 4), (1, 5), (2, 6), (3, 7)
]

faces = [
    (0, 1, 2, 3),
    (4, 5, 6, 7),
    (0, 1, 5, 4),
    (2, 3, 7, 6),
    (0, 3, 7, 4),
    (1, 2, 6, 5)
]

angle_x, angle_y, angle_z = 0, 0, 0
rotation_speed = 0.01
dragging = False
last_mouse_pos = None
momentum = [0, 0]

def rotate_x(point, angle):
    x, y, z = point
    y_new = y * math.cos(angle) - z * math.sin(angle)
    z_new = y * math.sin(angle) + z * math.cos(angle)
    return [x, y_new, z_new]

def rotate_y(point, angle):
    x, y, z = point
    x_new = x * math.cos(angle) + z * math.sin(angle)
    z_new = -x * math.sin(angle) + z * math.cos(angle)
    return [x_new, y, z_new]

def rotate_z(point, angle):
    x, y, z = point
    x_new = x * math.cos(angle) - y * math.sin(angle)
    y_new = x * math.sin(angle) + y * math.cos(angle)
    return [x_new, y_new, z]

font = pygame.font.SysFont(None, 24)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                dragging = True
                last_mouse_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                dx = event.pos[0] - last_mouse_pos[0]
                dy = event.pos[1] - last_mouse_pos[1]
                momentum[0] = dx * 0.01
                momentum[1] = dy * 0.01
                last_mouse_pos = event.pos

    angle_x += rotation_speed + momentum[1]
    angle_y += rotation_speed + momentum[0]

    momentum[0] *= 0.95
    momentum[1] *= 0.95

    screen.fill((0, 0, 0))

    transformed_vertices = []
    for vertex in vertices:
        rotated_vertex = rotate_x(vertex, angle_x)
        rotated_vertex = rotate_y(rotated_vertex, angle_y)
        rotated_vertex = rotate_z(rotated_vertex, angle_z)
        z = 1 / (4 - rotated_vertex[2])
        x = int(rotated_vertex[0] * z * width / 2 + width / 2)
        y = int(rotated_vertex[1] * z * height / 2 + height / 2)
        transformed_vertices.append((x, y))

    face_surface = pygame.Surface((width, height), pygame.SRCALPHA)

    for face in faces:
        pointlist = [transformed_vertices[vertex] for vertex in face]
        pygame.draw.polygon(face_surface, (255, 255, 255, 100), pointlist)

    screen.blit(face_surface, (0, 0))

    for edge in edges:
        pygame.draw.line(screen, (255, 255, 255), transformed_vertices[edge[0]], transformed_vertices[edge[1]], 1)

    total_speed = math.sqrt((rotation_speed + momentum[0])**2 + (rotation_speed + momentum[1])**2)

    speed_text = font.render(f"Speed: {total_speed:.2f}", True, (255, 255, 255))
    screen.blit(speed_text, (width - speed_text.get_width() - 10, height - speed_text.get_height() - 10))

    pygame.display.flip()
    pygame.time.wait(10)

pygame.quit()
