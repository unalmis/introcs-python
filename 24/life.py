# ------------------------------------------------------------------------------
# @author Kaya Unalmis
# python3 life.py 6 32 glider
# python3 life.py 16 64 random 0.25
# ------------------------------------------------------------------------------
"""Simulates Conway's game of life.

This implementation assumes that the
board wraps-around, that is, cells can be neighbors if they lie on
opposite sides of the board.

Consider a boolean matrix corresponding to a system of cells that we refer
to as being either live or dead. The game consists of checking and perhaps
updating the value of each cell, depending on the values of its neighbors
(the adjacent cells in every direction, including diagonals). Live cells
remain live and dead cells remain dead, with the following exceptions:
• A dead cell with exactly three live neighbors becomes live.
• A live cell with exactly one live neighbor becomes dead.
• A live cell with more than three live neighbors becomes dead.

Exercise 2.4.22
Introduction to Programming in Python.
Addison-Wesley Professional, 2015, pp. 349,
by Robert Sedgewick, Kevin Wayne, Robert Dondero.

@author Kaya Unalmis
"""

import stddraw
from stdarray import create2D

import pattern


def _live_count(cells: list, i: int, j: int) -> int:
    # return the number of live neighbors of this cell

    # wrap around
    n = len(cells)
    lt = (j + n - 1) % n
    rt = (j + n + 1) % n
    up = (i + n - 1) % n
    lo = (i + n + 1) % n

    count = 0
    if cells[i][lt]:  # left
        count += 1
    if cells[i][rt]:  # right
        count += 1
    if cells[up][j]:  # up
        count += 1
    if cells[lo][j]:  # down
        count += 1
    if cells[up][lt]:  # upper left
        count += 1
    if cells[up][rt]:  # upper right
        count += 1
    if cells[lo][lt]:  # lower left
        count += 1
    if cells[lo][rt]:  # lower right
        count += 1

    return count


def _state_change(is_live: bool, count: int) -> bool:
    # should the cell state change?
    return (not is_live and count == 3) or (is_live and (count < 2 or count > 3))


def _next_state(cells: list, i: int, j: int) -> bool:
    # return this cell's next state
    is_live = cells[i][j]
    if _state_change(is_live, _live_count(cells, i, j)):
        return not is_live
    return is_live


def step(cells: list) -> list:
    """
    :param cells: pattern specifying current state
    :return:      pattern specifying next state
    """
    n = len(cells)
    cells_ = create2D(n, n)
    for i in range(n):
        for j in range(n):
            cells_[i][j] = _next_state(cells, i, j)
    return cells_


def draw_life(cells: list, t: int, pause: int = 512):
    """
    Animate t steps of simulation starting from state given in cells.

    :param cells: pattern specifying start state
    :param t:     number of steps to simulate
    :param pause: animation pause increment
    """
    pattern.draw(cells)
    stddraw.show(pause)
    for i in range(t):
        cells = step(cells)
        stddraw.clear()
        pattern.draw(cells)
        stddraw.show(pause)


def main():
    """Life module test client.

    See example executions at bottom of file. Requires arguments:
        n, pattern size
        t, number of steps to simulate
        r, either 'glider' or 'random'
            if random selected a float between 0 and 1 required.

    :raise IndexError: if there is an insufficient number of arguments
    """
    import sys

    n = int(sys.argv[1])
    t = int(sys.argv[2])
    r = sys.argv[3]
    if r == "random":
        p = float(sys.argv[4])
        cells = pattern.random(n, p)
    else:
        cells = pattern.glider(n)
    draw_life(cells, t)


if __name__ == "__main__":
    main()
