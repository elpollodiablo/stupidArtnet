from lib.StupidArtnet import StupidArtnet
import time
import random
import sys

target_ip = '192.168.30.195'
packet_size = 384

universes = {}
UNIVERSES = 32
print("initializing")
BLACK = [0x0, 0x0, 0x0]
WHITE = [0x55, 0x55, 0x55]
HEIGHT=64
UNICOLS=2

for i in range(1, UNIVERSES+1):
    universes[i] = StupidArtnet(target_ip, i, packet_size)

CONTENT = {
    "WHITE": {
        k: WHITE * UNICOLS * HEIGHT for k in range(1, UNIVERSES+1)
    },
    "BLACK": {
        k: BLACK * UNICOLS * HEIGHT for k in range(1, UNIVERSES+1)
    },
}

def vertical_line_for(n):
    d = {}
    for i in range(0, UNIVERSES):
        idx = i + 1
        d.setdefault(idx, [])
        for cols in [0, 1]:
            if i * 2 + cols == n:
                d[idx] += BLACK * HEIGHT
            else:
                d[idx] += WHITE * HEIGHT
    return d

for i in range(0, 64):
    CONTENT[str(i)] = vertical_line_for(i)


#print(CONTENT)
print("initialized")

frames=sys.argv[1].split(",")
framecounter=0
framecount=len(frames)

while True:
    time.sleep(0.01 * int(sys.argv[2]))
    for i in range(1, UNIVERSES+1):
        universe = universes[i]
        universe.make_header()
        universe.set(CONTENT[frames[framecounter % framecount]][i])
        universe.show()
    framecounter+=1
