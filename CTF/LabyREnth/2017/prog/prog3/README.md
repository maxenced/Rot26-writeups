# WTF

Like many others, this prog3 was the hardest for me (in prog track).

Connecting to the socket, you get a 3D like view, with walls either on your left, right, front etc ...

You can press either q,s,d or w to go one step front or back, or turn left or right.
So, basically, what you see is a maze where you only see your next 2/3 moves.

Playing a bit, we see that at some point we hit a wall (with some meme) that wasn't expected.

# Disclaimer

Though I finally flagged it, the code is far from perfect. Especially, it
didn't work in all cases, but often enough (~ 30% of the time) to get the flag.

I spent so much time understanding how the game was cheating that I just went ahead and didn't try to fix the script.

# And then ... nightmare begins

First,I wrote some class which "map" the maze. With this, I was able to draw it
in 2D version. The class basically uses a x*y matrix to remember the maze
state.

Every time a move is done, the class update the direction to have a correct view of the path / walls, etc ...

```python
maze = None

DEBUG = True
# directions
DOWN=0
LEFT=1
UP=2
RIGHT=3

LETTERS=""
MOVES=0

class Maze():
    def __init__( self, n_rows, n_cols ):
        """Create a maze with given number of rows and cols.
        """
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.maze = [None]*n_rows
        self.curr_x = n_cols // 2
        self.curr_y = n_rows // 2
        self.direction = UP

        for i in range(n_rows):
            self.maze[i] = ['   ']*n_cols
        # So here we have an array of arrays. first array position is defined by curr_x
        # then curr_y is the position in the 2nd array, from top to bottom (curr_y =0 is the top)

        self.maze[self.curr_x][self.curr_y] = "|S|" #Start

    def add_wall(self, left = True, right = True, front = True):
        """ For each param, True means there is a wall, False there is a path
        This method takes care of current direction
        """
        debug("Direction : %s" % self.direction)
        if self.direction == UP:
            if left:
                self.maze[self.curr_x][self.curr_y-1] = '|' + self.maze[self.curr_x][self.curr_y-1][1:]
            if right:
                self.maze[self.curr_x][self.curr_y-1] = self.maze[self.curr_x][self.curr_y-1][:-1] + '|'
            if front:
                assert(self.curr_y > 0)
                #self.maze[self.curr_x][self.curr_y-2] = self.maze[self.curr_x][self.curr_y-2][0] + '_' + self.maze[self.curr_x][self.curr_y-2][-1]
                self.maze[self.curr_x][self.curr_y-2] = '._.'
        elif self.direction == DOWN:
            if right:
                self.maze[self.curr_x][self.curr_y+1] = '|' + self.maze[self.curr_x][self.curr_y+1][1:]
            if left:
                self.maze[self.curr_x][self.curr_y+1] = self.maze[self.curr_x][self.curr_y+1][:-1] + '|'
            if front:
                self.maze[self.curr_x][self.curr_y+1] = self.maze[self.curr_x][self.curr_y+2][0] + '_' + self.maze[self.curr_x][self.curr_y+2][-1]
        elif self.direction == LEFT:
            if right:
                assert(self.curr_x > 0)
                #self.maze[self.curr_x][self.curr_y-1] = self.maze[self.curr_x][self.curr_y-1][0] + '_' + self.maze[self.curr_x][self.curr_y-1][-1]
                self.maze[self.curr_x-1][self.curr_y-1] = '._.'
            if left:
                #self.maze[self.curr_x][self.curr_y] = self.maze[self.curr_x][self.curr_y][0] + '_' + self.maze[self.curr_x][self.curr_y][-1]
                self.maze[self.curr_x-1][self.curr_y] = '._.'
            if front:
                self.maze[self.curr_x-1][self.curr_y] = '|' + self.maze[self.curr_x-1][self.curr_y][1:]
        elif self.direction == RIGHT:
            if left:
                assert(self.curr_x > 0)
                #self.maze[self.curr_x+1][self.curr_y-1] = self.maze[self.curr_x+1][self.curr_y-1][0] + '_' + self.maze[self.curr_x][self.curr_y-1][-1]
                self.maze[self.curr_x+1][self.curr_y-1] = '._.'
            if right:
                #self.maze[self.curr_x+1][self.curr_y] = self.maze[self.curr_x+1][self.curr_y][0] + '_' + self.maze[self.curr_x][self.curr_y][-1]
                self.maze[self.curr_x+1][self.curr_y] = '._.'
            if front:
                self.maze[self.curr_x+1][self.curr_y] = self.maze[self.curr_x+1][self.curr_y][:-1] + '|'

    def left(self):
        """ Simply rotate to left
        """
        # Could use a modulo here, but let's keep things clear
        next_direction = {
            LEFT: DOWN,
            DOWN: RIGHT,
            RIGHT: UP,
            UP: LEFT,
        }
        self.direction = next_direction[self.direction]

    def right(self):
        """ Simply rotate to right
        """
        # Could use a modulo here, but let's keep things clear
        next_direction = {
            LEFT: UP,
            UP: RIGHT,
            RIGHT: DOWN,
            DOWN: LEFT
        }
        self.direction = next_direction[self.direction]

    def step(self):
        """ Move one step further
        """
        # Format: change[DIRECTION] = (x_delta, y_delta)
        change = {
            LEFT: (-1,0),
            RIGHT: (1,0),
            DOWN: (0,1),
            UP: (0,-1),
        }
        self.curr_x = self.curr_x + change[self.direction][0]
        self.curr_y = self.curr_y + change[self.direction][1]
        assert(self.curr_x >=0 and self.curr_x < self.n_cols)
        assert(self.curr_y >=0 and self.curr_y < self.n_rows)

    def stepback(self):
        """ Move one step back
        """
        # Format: change[DIRECTION] = (x_delta, y_delta)
        change = {
            LEFT: (1,0),
            RIGHT: (-1,0),
            DOWN: (0,-1),
            UP: (0,1),
        }
        self.curr_x = self.curr_x + change[self.direction][0]
        self.curr_y = self.curr_y + change[self.direction][1]
        assert(self.curr_x >=0 and self.curr_x < self.n_cols)
        assert(self.curr_y >=0 and self.curr_y < self.n_rows)

    def __str__(self):
        res = ''
        # set a 'x' to mark current position
        keep = self.maze[self.curr_x][self.curr_y]
        self.maze[self.curr_x][self.curr_y] = self.maze[self.curr_x][self.curr_y][0] + 'x' + self.maze[self.curr_x][self.curr_y][-1]
        for y in range(0, self.n_rows):
            res += (''.join([ self.maze[x][y] for x in range(0, self.n_cols)])) + '\n'

        self.maze[self.curr_x][self.curr_y] = keep
        return res
```

The `add_wall` function just 'draws' the next step based on current direction and what we "see".
The `left`, `right`, `stepback` and `step` functions just fix the position / direction after a move.

# Cheater

So, yeah, the game cheats. After I made some "fuzzing" of the maze until I get an unexpected wall/meme, I got these patterns :

```
wwwwdwwaww
wwdwwdwwdw
wwwwwwdwww
wwwwdwwwww
wwdwwdwwdw
wwdwwdwwdw
wwwwwwwwwwdwwawwwwdw
wwwwdwwawwawwdwwdwww
wwdwwawwwwdwwdwwawww
wwwwdwwawwawwdwwdwwawwwwawwdww
```

what you see is that it always happens after n*10 moves, and only with a 'w' as last move. 
After some guessing, I understood that, to avoid the trap, I need to do a half-turn, go back 1 step, then another half-turn.

So basically, what I had to do is to count my moves and, if my next move is a
'w' and I'm at a 10th move, just do left-left-back-left-left. 

The following code handles both the turn left/turn right and the avoid-the-trap stuff:

```python
def send_and_inc(sock,letter):
    global MOVES
    global maze
    MOVES += 1
    debug("Sending letter %s" % letter)
    update_call = {
        'a': maze.left,
        'd': maze.right,
        'w': maze.step,
        's': maze.stepback
    }
    update_call[letter]()
    sock.send(letter)
    time.sleep(0.2)
    response = sock.recv(RECV_SIZE)
    return response

def send(sock, maze, letter = None, response = None, will_turn = False):
    """ Send a move to the remote maze, and add it to our internal maze
        also parse the result to map the new environment in our internal maze
        before returning it to main process
        if response is set, only parse it and don't send a move
        response and letter are mutualy exclusive
        if will_turn is True, then we expect next move to be a turn, so won't crash if we hit a wall and get some meme
        @return a tuple of three boolean (left, right, front). True means there is a wall, False there is a path
    """
    global LETTERS
    global MOVES

    assert(not (letter is not None and response is not None))
    print("MOVES : %s" % MOVES)
    debug("1) Sending letter %s" % letter)
    if  (MOVES +1) % 10 == 0 and letter == 'w':
        # Every ten moves, we may get a meme if we go straight
        # So just turn half and go back, then turn again
        send_and_inc(sock,'a')
        send_and_inc(sock,'a')
        send_and_inc(sock,'s')
        send_and_inc(sock,'a')
        letter = 'a'
    debug("2) Sending letter %s" % letter)
    if letter:
        assert(letter in ['a','d','w','s'])
        response = send_and_inc(sock,letter)
        LETTERS = LETTERS + letter
    debug("Response : %s" % response)
    debug("len(Response) : %s" % len(response))
    if len(response) < 1000:
        response = sock.recv(RECV_SIZE)
    left, right, front = True, True, True

    if ("right turn" in response):
        right = False
    elif ("some turn" in response and " \|__|" in response):
        right = False
        front = False
    elif "left turn" in response:
        left = False
    elif("some turn" in response and " |__|/" in response):
        left = False
        front = False
    elif ("some turn" in response and " |____________________________________________|" in response):
        # left and right turns
        left = False
        right = False
    elif "some turn" in response: #There is a turn in more than 1 step
        front = False
    elif "hallway" in response:
        front = False

    if '------------------------------' in response and letter == "w" and not will_turn:
        print("Hit some meme while I was walking straight. This should *not* append, fix me!")
        exit(1)
    if 'PAN' in response:
        print("We did it !")
        exit(0)
    if '------------------------------' not in response:
        # ascii art, don't draw anything
        debug("Found walls : left=%s; right=%s, front=%s" % (left, right, front))
        maze.add_wall(left, right, front)
    return (left, right, front)
```

# ROFL:ROFL:ROFL

And finally, just write the `main()` part which create a 50x50 maze instance, and fuzz it for up to 150 moves :

```python
def main():
    global maze
    conn = socket.create_connection(MAZE_SERVER)
    maze = Maze(50,50)
    i = 0
    response = conn.recv(RECV_SIZE)
    left, right, front = send(conn, maze, None, response)
    while i < 150:
        debug("Found walls : left=%s; right=%s, front=%s" % (left, right, front))
        if not right:
            debug("Ask for w and d and w")
            send(conn, maze, 'w', will_turn = True)
            send(conn, maze, 'd')
            left, right, front = send(conn, maze, 'w')
        elif not front:
            debug("Ask for w")
            left, right, front = send(conn, maze, 'w')
        elif not left:
            debug("Ask for w and a and w")
            send(conn, maze, 'w', will_turn = True)
            send(conn, maze, 'a')
            left, right, front = send(conn, maze, 'w')
        elif left and right and front: # Dead end
            debug("Ask for a")
            send(conn, maze, 'a')
            left, right, front = send(conn, maze, 'a')
        i += 1
        print(maze)

    print(maze)

if __name__ == '__main__':
    main()
    print(LETTERS)

```

and at some point ...

```python
                    ROFL:ROFL:LOL:ROFL:LOL:ROFL:LOL:ROFL:ROFL
                                       ||
                        _______________||_______________
                       /      ____   ___     _   __ [ 0 \
         L            /      / __ \ /   |   / | / / |_|<_\
         O           /      / /_/ // /| |  /  |/ /  |_____\
       LOLOL========       / ____// ___ | / /|  /          \
         O          |     /_/    /_/  |_|/_/ |_/            )
         L        B | O M B                                /
                    |____________,--------------__________/
                 F /      ||                       ||
                T /     }-OMGPAN{c0ntact_jugglers_R_Ballerz}ROCKET))
               W /________||_______________________||__/_/

```
