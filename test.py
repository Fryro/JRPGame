#!/usr/bin/env python3
"""
Author: Nickolos Monk
Date: 
License: MIT
"""
import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

player_info = {
    "starting-pos": [screen.get_width() / 2, screen.get_height() / 2, 100, 100]
}

scenes_dict = {
    "surface": {
        "name": "surface",
        "objects": {
            "stairs-down": {
                "name": "stairs-down",
                "center": pygame.Vector2(
                    ((screen.get_width() / 2) + (screen.get_width() / 4)), 
                    ((screen.get_height() / 2) + (screen.get_width() / 4))
                ), 
                "left": screen.get_width() / 2 + screen.get_width() / 4,
                "top": screen.get_height() / 2 + screen.get_height() / 4,
                "width": 50,
                "height": 50,
                "color": "purple",
                "interactable": True,
                "destination": "cave"
            }
        },
        "background": "green",
        "timescale": 100.00/100.00 # Seconds Passed - Seconds Experienced
    },
    "cave": {
        "name": "cave",
        "objects": {
            "stairs-up": {
                "name": "stairs-up",
                "center": pygame.Vector2(
                    ((screen.get_width() / 2) - (screen.get_width() / 4)), 
                    ((screen.get_height() / 2) - (screen.get_width() / 4))
                ),
                "left": screen.get_width() / 2 - screen.get_width() / 4,
                "top": screen.get_height() / 2 + screen.get_height() / 4,
                "width": 50,
                "height": 50,
                "color": "blue",
                "interactable": True,
                "destination": "surface"
            }
        },
        "background": "gray",
        "timescale": 110.00/100.00 # Seconds Passed - Seconds Experienced
    }
}



class Interactable:
    hitbox = None
    position = None
    name = None
    color = None
    destination = None

    def __init__(self, left, top, width, height, name, color, destination):
        self.hitbox = pygame.Rect(left, top, width, height)
        self.position = pygame.Vector2(left + (width / 2), top + (height / 2))
        self.name = name
        self.color = color
        self.destination = destination



class Player:
    hitbox = None
    position = None
    speed = None
    stair_cd = None
    stair_cd_max = 2.5
    stair_cd_min = 0.0

    def __init__(self, left, top, width, height):
        self.hitbox = pygame.Rect(left, top, width, height)
        self.position = pygame.Vector2(left + (width / 2), top + (height / 2))
        self.speed = 300
        self.stair_cd = 0.0

    def update(self, dt):
        self.hitbox.update(
            self.position[0],
            self.position[1],
            self.hitbox.width,
            self.hitbox.height
        )
        
        if self.stair_cd >= self.stair_cd_min:
            self.stair_cd -= dt


def get_scene_info(scene):
    
    return_dict = {
        "interactables": [],
        "walls": [],
        "npcs": []
    }
    
    for scene_element_name in scene["objects"].keys():
        scene_element = scene["objects"][scene_element_name]
        if not scene_element["interactable"]:
            continue
        return_dict["interactables"].append(
            Interactable(
                scene_element["left"],
                scene_element["top"],
                scene_element["width"],
                scene_element["height"],
                scene_element["name"],
                scene_element["color"],
                scene_element["destination"]
            )
        )

    return(return_dict)

player = Player(player_info["starting-pos"][0], player_info["starting-pos"][1], player_info["starting-pos"][2], player_info["starting-pos"][3])

scene = scenes_dict["surface"]
scene_objects = get_scene_info(scene)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(scene["background"])
    
    for scene_element in scene_objects["interactables"]: 
        pygame.draw.rect(screen, scene_element.color, scene_element.hitbox)
        
    pygame.draw.circle(screen, "red", player.position, 40)


    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player.position.y -= player.speed * dt
    if keys[pygame.K_s]:
        player.position.y += player.speed * dt
    if keys[pygame.K_a]:
        player.position.x -= player.speed * dt
    if keys[pygame.K_d]:
        player.position.x += player.speed * dt
    player.update(dt)

    for stairs in scene_objects["interactables"]:
        if not stairs.destination:
            continue
        if ((player.hitbox.colliderect(stairs.hitbox)) and (keys[pygame.K_f]) and (player.stair_cd <= player.stair_cd_min)):
            scene = scenes_dict[stairs.destination]
            scene_objects = get_scene_info(scene)
            player.stair_cd = player.stair_cd_max
            print(f"You entered the {scene['name']}. This location has a time dilation of {scene['timescale']}.")
    #print(f"w[{keys[pygame.K_w]}] a[{keys[pygame.K_a]}] s[{keys[pygame.K_s]}] d[{keys[pygame.K_d]}] f[{keys[pygame.K_f]}]")
    #print(scene_objects["interactables"][0].hitbox)
    #print(player.hitbox)

    pygame.display.flip()

    dt = (clock.tick(60) / 1000) * scene["timescale"]

pygame.quit()
