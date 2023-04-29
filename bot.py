from time import sleep
from PIL import Image, ImageColor
import numpy as np
import socketio


def rgb2hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(*rgb)


def find_color(colors, color) -> int:
    colors = np.array(colors)
    color = np.array(color)
    distances = np.sqrt(np.sum((colors - color) ** 2, axis=1))
    print(color)
    min_distance = np.where(distances == np.amin(distances))[0]
    if len(min_distance) > 1:
        min_distance = min_distance[0]
    print(min_distance)
    return colors[int(min_distance)]


def error(data):
    print(data)


def emit_callback(data):
    print(data)


class Place:
    colors = None
    board = None

    def __init__(self):
        self.sio = socketio.Client()
        self.sio.connect("https://place.djoamersfoort.nl", headers={
                        "Cookie": 'connect.sid=s%3As2u8tbsvUZEMBZPY3HZ87TjnLeMdAf-Y.lT3akNiulzc6CqZ2esqE3tfDNrB5C6gNeXVVMPB%2F%2FNQ'})
        self.sio.on("board", self.set_board)
        self.sio.on("colors", self.set_colors)
        self.sio.on("error", error)

    def set_board(self, data):
        self.board = data
        self.place()

    def set_colors(self, data):
        print(data)
        self.colors = [ImageColor.getcolor(color, "RGB") for color in data]
        self.place()

    def place(self):
        if not self.colors or not self.board:
            return
        print(self.board)
        henk = Image.open("moes.png")
        henk = henk.resize((96,32))
        henk.save("Moes-klein.png")
        px = henk.load()
        base = 0
        for x in range(0, henk.width):
            for y in range(0, henk.height):
                pixel = self.board[x+base][y]
                nieuwe_pixel = px[x, y]
                print(pixel, nieuwe_pixel)
                # kleur = rgb2hex(find_color(self.colors, nieuwe_pixel))
                # print(kleur)
                kleur = rgb2hex(nieuwe_pixel)
                if pixel != kleur:
                    self.sio.emit("color", data={"x": x+base, "y": y, "color": kleur}, callback=emit_callback)
                    sleep(10)


if __name__ == '__main__':
    Place()
