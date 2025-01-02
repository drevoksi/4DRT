res = 50
rad = 4
pos = (6, 0, 0, 0)

import math

def get_unit_div():
    return [a / res * 2 - 1 for a in range(0, res + 1)]

def to_world(res_range_v):
    return res_range_v / res * 2 - 1

def cls_sph_int(sensor_c):
    o, a, b, c = sensor_c
    pa = 1 + a * a + b * b + c * c
    pb = - 2 * (pos[0] + a * pos[1] + b * pos[2] + c * pos[3])
    pc = pos[0] * pos[0] + pos[1] * pos[1] + pos[2] * pos[2] + pos[3] * pos[3] - rad * rad
    pd = pb * pb - 4 * pa * pc
    if pd < 0: return None
    x = (- pb - math.sqrt(pd)) / 2 * pa
    return x

def sd_to_int(sensor_c, intercept):
    return intercept * intercept * (1 + sensor_c[1] * sensor_c[1] + sensor_c[2] * sensor_c[2] + sensor_c[3] * sensor_c[3])


sensor = []
for y in get_unit_div():
    for z in get_unit_div():
        for w in get_unit_div():
            sensor.append((1, y, z, w))

image = [[[(0, 0, 0) for w in range(res + 1)] for z in range(res + 1)] for y in range(res + 1)]

for y in range(res + 1):
    for z in range(res + 1):
        for w in range(res + 1):
            index = (y, z, w)
            sensor_c = (1, to_world(y), to_world(z), to_world(w))
            intercept = cls_sph_int(sensor_c)
            if intercept == None:
                image[y][z][w] = (255, 255, 255, 0)
            else:
                image[y][z][w] = (0, 0, int(sd_to_int(sensor_c, intercept) * 20), 255)

from PIL import Image

for pz in range(res + 1):
    img = Image.new(mode="RGBA", size=(res + 1, res + 1))
    for px in range(res + 1):
        for py in range(res + 1):
            img.putpixel((px, py), image[pz][px][py])
    img.save(f"slices/slice{pz}.png","PNG")