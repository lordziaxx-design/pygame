import pygame
import numpy as np

pygame.init()
win = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Zadanie - Litera Z")

BIALY = (255, 255, 255)
CZARNY = (0, 0, 0)
CZERWONY = (255, 0, 0)


def get_z_surface(w=300, h=300):
    surf = pygame.Surface((w, h), pygame.SRCALPHA)
    surf.fill((0, 0, 0, 0))
    t = 12
    pygame.draw.line(surf, CZERWONY, (10, 10),     (w - 10, 10),      t)
    pygame.draw.line(surf, CZERWONY, (w - 10, 10), (10, h - 10),      t)
    pygame.draw.line(surf, CZERWONY, (10, h - 10), (w - 10, h - 10),  t)
    return surf


def shear_surface(surf, shear_x=0.0, shear_y=0.0):
    rgb   = pygame.surfarray.array3d(surf)         
    alpha = pygame.surfarray.array_alpha(surf)      

    w, h = rgb.shape[0], rgb.shape[1]

    pad_x = int(abs(shear_x) * h)
    pad_y = int(abs(shear_y) * w)
    new_w = w + pad_x
    new_h = h + pad_y

    new_rgb   = np.zeros((new_w, new_h, 3), dtype=np.uint8)
    new_alpha = np.zeros((new_w, new_h),    dtype=np.uint8)

    for x in range(w):
        for y in range(h):
            if shear_x >= 0:
                nx = x + int(shear_x * (h - y))
            else:
                nx = x + int(shear_x * y) + pad_x

            if shear_y >= 0:
                ny = y + int(shear_y * x)
            else:
                ny = y + int(shear_y * (w - x)) + pad_y

            if 0 <= nx < new_w and 0 <= ny < new_h:
                new_rgb[nx, ny]   = rgb[x, y]
                new_alpha[nx, ny] = alpha[x, y]

    new_surf = pygame.Surface((new_w, new_h), pygame.SRCALPHA)
    pygame.surfarray.blit_array(new_surf, new_rgb)
    alpha_surf = pygame.surfarray.pixels_alpha(new_surf)
    alpha_surf[:] = new_alpha
    del alpha_surf 

    return new_surf


TRANSFORMS = {
    1: dict(scale=(150, 150), angle=0,   pos=(300, 300), shear_x=0.0,  shear_y=0.0),
    2: dict(scale=(300, 300), angle=-45,  pos=(300, 300), shear_x=0.0,  shear_y=0.0),
    3: dict(scale=(220, 220), angle=90, pos=(300, 300), shear_x=0.0,  shear_y=0.0),
    4: dict(scale=(280, 280), angle=0,   pos=(270, 340), shear_x=0.35, shear_y=0.0), 
    5: dict(scale=(220, 75),  angle=0,   pos=(300, 160), shear_x=0.0,  shear_y=0.0),  
    6: dict(scale=(260, 260), angle=90,   pos=(340, 320), shear_x=0.0,  shear_y=0.3), 
    7: dict(scale=(160, 160), angle=90,   pos=(300, 300), shear_x=0.0,  shear_y=0.0),
    8: dict(scale=(220, 160), angle=-45, pos=(110, 450), shear_x=0.0,  shear_y=0.0),
    9: dict(scale=(280, 280), angle=10,  pos=(440, 340), shear_x=0.25, shear_y=0.15),
}
current_transform = 1

run = True
clock = pygame.time.Clock()

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            key_map = {
                pygame.K_1: 1, pygame.K_2: 2, pygame.K_3: 3,
                pygame.K_4: 4, pygame.K_5: 5, pygame.K_6: 6,
                pygame.K_7: 7, pygame.K_8: 8, pygame.K_9: 9,
            }
            if event.key in key_map:
                current_transform = key_map[event.key]

    win.fill(BIALY)

    t = TRANSFORMS[current_transform]

    surf = get_z_surface()         
    surf = pygame.transform.scale(surf, t["scale"])  

    if t["shear_x"] != 0.0 or t["shear_y"] != 0.0:
        surf = shear_surface(surf, t["shear_x"], t["shear_y"])

    if t["angle"] != 0:
        surf = pygame.transform.rotate(surf, t["angle"])

    rect = surf.get_rect(center=t["pos"])
    win.blit(surf, rect)

    font = pygame.font.SysFont("comicsans", 22)
    label = font.render(f"Transformacja: {current_transform}   (klawisze 1-9)", 1, CZARNY)
    win.blit(label, (10, 10))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
