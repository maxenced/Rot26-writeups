Again some "simple" game solver challenge.

Here we need to solve many 4 in a row games, with increasing complexity.
The most efficient algorithm for solving such challenges is [NegaMax](https://en.wikipedia.org/wiki/Negamax), so let's use it.

We found some implementation at https://github.com/duilio/c4 , thanks to him !

The only things I need to do is to parse the game in a way  that c4 engine can understand (array).
Quiet easy, just split on '|', and replace empty places with a ' 0 '.

Final code :

```python
import socket
try:
    import numpy as np
except ImportError:
    print("Sorry, this solver requires Numpy installed !")
    raise

from c4.engine import NegamaxEngine
from c4.engine.labyrinth import LabyrinthEngine
from c4.board import Board, PLAYER1, PLAYER2, DRAW

C4_SERVER = ('52.40.187.77', 16000)
RECV_SIZE = 4096
conn = socket.create_connection(C4_SERVER)

engine = NegamaxEngine()
human = LabyrinthEngine(conn)
b = Board()

def parse_grid(grid):
    """ Get the grid as ASCII, and return a list of array
    """
    res = []
    curline = 0
    for line in grid.split('\n'):
        if not line or line[0] != '|':
            continue
        res.append([])
        to_a = line.replace('   ',' 0 ').split(' ')
        for c in to_a:
            if c != '|' and c != '':
                res[curline].append(c)
        curline += 1
    return res

def play():
    global b
    move = None

    players = {
        PLAYER1: engine,
        PLAYER2: human
        }

    while b.end is None:
        player = players[b.stm]
        move = player.choose(b)
        b = b.move(move)

    if b.end == DRAW:
        winner = None
        looser = None
    else:
        winner = players[b.end]
        looser = players[PLAYER1 if b.end == PLAYER2 else PLAYER2]

    looser.choose(b, True)
    return b, winner, looser

def main():
    global b, human, engine
    response = conn.recv(RECV_SIZE)
    while True:
        print response
        if 'Skeelz' not in response:
            return

        print(parse_grid(response))
        b, winner, looser = play()
        print("Won one game ! ")
        engine = NegamaxEngine()
        human = LabyrinthEngine(conn)
        b = Board()
        print("New board is %s"% b)

if __name__ == '__main__':
    main()
```
