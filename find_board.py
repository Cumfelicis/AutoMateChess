from piece_detector import Camera
from piece_to_colour import piece_to_colour

camera = Camera()
frame = Camera.get_frame(camera)
first_pixel_found = False
first_pixel = []
last_pixel = []
for x, i in enumerate(frame):
    for y, j in enumerate(i):
        if piece_to_colour(tuple(j)) == "r":
            if not first_pixel_found:
                first_pixel_found = [x, y]
                first_pixel = True
            last_pixel = [x, y]
print(first_pixel, last_pixel)

