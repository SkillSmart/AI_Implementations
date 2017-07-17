# Represent the Puzzle
rows = "ABCDEFGHI"
cols = "123456789"

# Create list of elements crossing a row
def cross(a, b):
    return [s+t for s in a for t in b]

# Create the boxes for the game
boxes = cross(rows, cols)

# for the units
row_units = [cross(r, cols) for r in rows]
col_units = [cross(rows, c) for c in cols]

# Create the individual squares
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]

# Create the final completed list of units in the game
unitlist = row_units + col_units + square_units


# PROGRAM CODE::::::
quiz = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'


def grid_values(grid):
    """Generates the Grid for a given state of the game"""
    board =  { b:n for b,n in zip(boxes, list(grid))}
    for k,v in board.items():
        if v ==".":
            board[k] = "123456789"
    return board


# Process to Eliminate solutions based on given information
def display(values):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return


def eliminate(values):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """

    # Iterate over the dict
    for k,v in values.items():
        # Check for single value
        if len(v)==1:
            # Eliminate the value v from the values of all boxes in its row
            for row in row_units:
                if k in row:
                    for box in row:
                        if len(values[box]) > 1:
                            values[box] = values[box].replace(v, '')

            # Eliminate the value v for the values of all boxes in its column
            for col in col_units:
                if k in col:
                    for box in col:
                        if len(values[box]) > 1:
                            values[box] = values[box].replace(v, '')
            # Eliminate the value for the values of all boxes in its square
            for square in square_units:
                if k in square:
                    for box in square:
                        if len(values[box]) > 1:
                            values[box] = values[box].replace(v, '')

    return values

def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces)==1:
                values[dplaces[0]] = digit
    return values

def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # Use the Eliminate Strategy
        values = eliminate(values)
        # Use the Only Choice Strategy
        values = only_choice(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    
    return values

def naked_twins(values):
    """
    Looks if within a given row  or column there are two places with an identical tuple 
    if so, these numbers are removed from all other occurrences in the field
    """
    # Get a list of all items that have a len of two
    targets = [(box,value) for box,value in values.items() if len(value)==2]
    # Check if they are duplicated items in the 
    for box,value in targets:
        # check for each row
        # [values[target] for target in row for row in row_units ]
        print([box for box in row for row in row_units])
            # print(box in row)
            
        for column in col_units:
            if box in column:
                for item in column:
                    values[item] = values[item].replace(value, '')


# If this solution so far does not work, we now need to search the tree and try out 
# Possible new subtrees to work

def search(values):
    """Using Depth First Search and propagation, we create a search tree to solve"""
    # First we reduce the existing puzzle
    values = reduce_puzzle(values)
    if values is False:
        return False #Failed earlier
    if all(len(values[s])== 1 for s in boxes):
        print('SOLVED') ##Solved
        return values
    # Choose an unfilled square with the least possibilities
    n, s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recursion to solve each one of the resulting sudokus
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt





# RUNNING THE Application
grid2 = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
board = grid_values(grid2)
# print(search(board))
reduce_puzzle(board)
naked_twins(board)