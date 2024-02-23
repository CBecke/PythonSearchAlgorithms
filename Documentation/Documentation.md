The overall goal of this project is to implement search algorithms and to show how they work through a graphical user interface.
- The user should be able to draw a 2d grid map, defining an initial square, 0 or more walls, and 1 or more goal squares.
- The user should be able to chose whether to draw an initial square, a wall, or a goal.
  - If there is already an initial square, remove the previous one.
- They should be able to chose among several different search algorithms. For each search algorithm, include a short description of how it works and performs.
- When the user has drawn a grid, they can press "start search" to see a visualization of how the algorithm reaches a goal from the starting state.
  - start search should only work when a valid level has been drawn. If the level is invalid, simply print a box with "board is invalid"
- The user should be able to choose the speed at which the algorithm progress is shown.
- The user should be able to choose the size of the grid, within some limits.
- The graphical user interface should fill the whole screen.
- Potentially, the user should be able to define their own heuristic function to be used by the algorithms.
- When an algorithm has run, some metrics should be shown to the user: how long the search took and how many nodes were generated
  - furthermore, the user should be able to save the solved grid with its metrics into a window (so they can look at two algorithms side by side)
  - The user should be able to run all algorithms on a given grid and produce a table with metrics of all the algorithms. The best one should be highlighted, and its solution should be shown.


- search algorithm
  - BFS, DFS, backtracking, depth-limited, iterative deepening, (greedy) best-first, bidirectional, Beam, A* and weighted A* and iterative-deepening A* search ((if an interesting heuristic is found), recursive best-first, simplified memory-bounded A*, memory-bounded A*