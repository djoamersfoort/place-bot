from time import sleep
from PIL import Image
import numpy as np


import socketio


def place(data):
    print(data)

    henk = Image.open("Henk_het_DJO_logo.jpg")
    henk = henk.resize((20, 20))
    henk.save("Kleine_Henk.jpg")
    px = henk.load()

    palette = data["palette"]

    for x in range(0, henk.width):
        for y in range(0, henk.height):
            pixel = data["place"][y][x]
            nieuwe_pixel = px[x, y]
            kleur = find_color(palette, nieuwe_pixel)
            if int(pixel) != kleur:
                sio.emit("color", data={"x": x, "y": y, "color": kleur}, callback=emit_callback)
                sleep(10)


def find_color(colors, color) -> int:
    colors = np.array(colors)
    color = np.array(color)
    distances = np.sqrt(np.sum((colors-color)**2, axis=1))
    print(color)
    min_distance = np.where(distances == np.amin(distances))[0]
    if len(min_distance) > 1:
        min_distance = min_distance[0]
    return int(min_distance)


def error(data):
    print(data)


def emit_callback(data):
    print(data)


sio = socketio.Client()
sio.connect("https://place.sverben.nl",
            headers={"Cookie": 'connect.sid='})

sio.on("place", place)
sio.on("error", error)
