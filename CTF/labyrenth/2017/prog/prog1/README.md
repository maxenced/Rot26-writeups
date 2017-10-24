Here we have a "simple" maze solving problem.

I got some (recursive) algorithm from http://labix.org/snippets/labsolver to
solve the maze, then wrote the few lines of code to use it to solve the
challenge.  You're aMAZEing! (See what we did there? hehehe)

Final code : 

```python
from socket import create_connection

MAZE_SERVER = ('54.69.145.229', 16000)
RECV_SIZE = 8192

NONE, WALL, BEGN, FNSH, SEEN, GOOD = tuple(' #>X.+')

gmaze = []

def solve2(maze, posx, posy, sizex, sizey):
    global gmaze
    found = 0
    if 0 <= posx < sizex and 0 <= posy < sizey:
        if maze[posy][posx] in (NONE, BEGN):
            if maze[posy][posx] == NONE:
                maze[posy][posx] = SEEN
            if (solve2(maze, posx+1, posy, sizex, sizey) or
                solve2(maze, posx-1, posy, sizex, sizey) or
                solve2(maze, posx, posy+1, sizex, sizey) or
                solve2(maze, posx, posy-1, sizex, sizey)):
                if maze[posy][posx] == SEEN:
                    maze[posy][posx] = GOOD
                found = 1
        elif maze[posy][posx] == FNSH:
            found = 1
    gmaze = maze
    return found

def answer(posx, posy):
    global gmaze
    res = ''
    lastx = posx
    lasty = posy
    assert gmaze[posy][posx] == '>'
    while gmaze[posy][posx] != 'X':
        if gmaze[posy+1][posx] in ('+','X')  and (res == '' or res[-1] != '^'):
            res += 'V'
            lasty = posy
            posy += 1
        elif gmaze[posy-1][posx] in ('+','X') and (res == '' or res[-1] != 'V'):
            res += '^'
            lasty = posy
            posy -= 1
        elif gmaze[posy][posx+1] in ('+','X') and (res == '' or res[-1] != '<'):
            res += '>'
            lastx = posx
            posx += 1
        elif gmaze[posy][posx-1] in ('+','X') and (res == '' or res[-1] != '>'):
            res += '<'
            lastx = posx
            posx -= 1
        else:
            print("This should not happen")

    return res

def main():
    conn = create_connection(MAZE_SERVER)
    response = conn.recv(RECV_SIZE)
    global maze
    while True:
        print response
        if "Now " not in response:
            return

        response_lines = response.splitlines()
        find_delim = [x for x in response_lines if x.startswith('Now')][0]
        maze_lines = response_lines[response_lines.index(find_delim)+2:-1]
        i=0
        for l in maze_lines:
            maze_lines[i] = list(l)
            i+=1
        maze_text = '\n'.join([''.join(line) for line in maze_lines])

        # find position of start
        posx = 0
        posy = 0
        sizex = len(max(maze_lines, key=len))
        sizey = len(maze_lines)
        for line in maze_lines:
            if '>' in line:
                posx = line.index('>')
                break
            posy = posy + 1

        print("Trying to solve posx : %s, posy : %s, sizex : %s, sizey : %s" % (posx, posy, sizex, sizey))
        solve2(maze_lines, posx, posy, sizex, sizey)
        solution = answer(posx,posy)
        print("Res : %s" % solution)
        if not len(solution):
            return
        conn.send(solution)
        response = conn.recv(RECV_SIZE)


if __name__ == '__main__':
    main()
```

PAN{my_f1rst_labyM4z3.jpeg}

