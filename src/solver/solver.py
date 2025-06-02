# -*- coding: utf-8 -*-
# Sudoku Solver
# This module provides functions to solve a Sudoku puzzle using a backtracking algorithm.

# Playing with types, so make some type aliases
type SudokuPuzzleT = dict[str, str]
type SquareT = str
type VectorStringT = list[str]
type NeighborT = tuple[dict[str, list[str]]]
type FamiliesT = tuple[list[VectorStringT]]

rowNames: tuple[str] = "ABCDEFGHI"
columnNames: tuple[str] = "123456789"
squares: tuple[VectorStringT] = [row + col for row in rowNames for col in columnNames]
cellRows: tuple[VectorStringT] = ["ABC", "DEF", "GHI"]
cellColumns: tuple[VectorStringT] = ["123", "456", "789"]

# Combines all combinations for two strings into a single loopable list of tuples.


def cross(first: str, second: str) -> list[tuple[str, str]]:
    return [(f, s) for f in first for s in second]


def _getRowNeighbors(sq: str) -> NeighborT:
    """Return all neighbors of a square in the same row.
    Finds all squares in the same row as the given square.

    Args:
            sq (str): The square ID (e.g., "A1")

    Returns:
            NeighborT: A list of square IDs in the same row, including the given square.
    """
    # sq is a square like "A1"
    return [sq[0] + col for col in columnNames]


def _getColumnNeighbors(sq: str) -> VectorStringT:
    """Return all neighbors of a square in the same column.
    Finds all squares in the same column as the given square.

    Args:
            sq (str): The square ID (e.g., "A1")

    Returns:
            VectorStringT: A list of square IDs in the same column, including the given square.
    """
    # sq is a square like "A1"
    return [row + sq[1] for row in rowNames]


def _getCellNeighbors(sq: str) -> VectorStringT:
    """Return all neighbors of a square in the same cell.
    Finds all squares in the same cell as the given square.

    Args:
            sq (str): The square ID (e.g., "A1")

    Returns:
            VectorStringT: A list of square IDs in the same cell, including the given square.
    """
    _rows: str = cellRows[[idx for idx, s in enumerate(cellRows) if sq[0] in s][0]]
    _cols: str = cellColumns[
        [idx for idx, s in enumerate(cellColumns) if sq[1] in s][0]
    ]
    return [r + c for r in _rows for c in _cols]


def _neighborsOf(sq: str) -> VectorStringT:
    """Return all neighbors of a square.
    Finds all squares that cannot share the same value as the given square.
    Args:
            sq (str): The square ID (e.g., "A1")
    Returns:
            VectorStringT: A sorted list of square IDs that cannot share the same value as the given square.
    """
    return sorted(
        list(
            (
                set(_getRowNeighbors(sq))
                | set(_getColumnNeighbors(sq))
                | set(_getCellNeighbors(sq))
            )
            - set([sq])
        )
    )


def _defineFamilies() -> FamiliesT:
    """Define all families of squares in the Sudoku puzzle.

    FamiliesT are defined as rows, columns, and cells that contain squares that cannot share the same value.
    Args:
            rowNames (str): The names of the rows (e.g., "ABCDEFGHI").
            columnNames (str): The names of the columns (e.g., "123456789").
            cellRows (list[str]): The names of the cell rows (e.g., ["ABC", "DEF", "GHI"]).
            cellColumns (list[str]): The names of the cell columns (e.g., ["123", "456", "789"]).

    Returns:
            FamiliesT: A list of families, where each family is a list of square IDs that cannot share the same value.
    """
    families: FamiliesT = []

    for rowName, colName in zip(rowNames, columnNames):
        families.append(_getRowNeighbors(rowName + columnNames[1]))
        families.append(_getColumnNeighbors(rowNames[1] + colName))

    # Cells
    for cellCol, cellRow in cross(cellColumns, cellRows):
        families.append(_getCellNeighbors(cellRow[1] + cellCol[1]))

    return families


families: FamiliesT = _defineFamilies()
# Create a dictionary of neighbors for each square
neighbors: NeighborT = {sq: _neighborsOf(sq) for sq in squares}
puzzle0: SudokuPuzzleT = {sq: "123456789" for sq in squares}


def isPuzzleComplete(pzl: SudokuPuzzleT) -> bool:
    """Check if the puzzle is complete.
    Checks if all squares in the puzzle have exactly one possible value.
    Args:
            pzl (SudokuPuzzleT): The Sudoku puzzle represented as a dictionary.
    Returns:
            bool: True if the puzzle is complete, False otherwise.
    """
    # Check if all squares have exactly one possible value
    return all([len(v) == 1 for v in pzl.values()])


def isFamilyCorrect(pzl: SudokuPuzzleT, familySquares: VectorStringT) -> bool:
    """Check if a family of squares is correct.
    Checks if the values in a family of squares contain all digits from 1 to 9 exactly once.
    Args:
            pzl (SudokuPuzzleT): The Sudoku puzzle represented as a dictionary.
            familySquares (VectorStringT): A list of square IDs that form a family.
    Returns:
            bool: True if the family is correct, False otherwise.
    """
    # Check if the values in the family squares contain all digits from 1 to 9 exactly once
    return set([pzl[familySq] for familySq in familySquares]) == set("123456789")


def isPuzzleSolved(pzl: SudokuPuzzleT) -> bool:
    """Check if the puzzle is solved.
    Checks if the puzzle is complete and all families are correct.
    Args:
            pzl (SudokuPuzzleT): The Sudoku puzzle represented as a dictionary.
    Returns:
            bool: True if the puzzle is solved, False otherwise.
    """
    return isPuzzleComplete(pzl) and all(
        map(lambda fam: isFamilyCorrect(pzl, fam), families)
    )


def _getNextEntryPoint(pzl: SudokuPuzzleT):
    """Get the next entry point for solving the puzzle.
    Finds the square with the most frequent unknown value and the fewest remaining possible values.
    Args:
            pzl (SudokuPuzzleT): The Sudoku puzzle represented as a dictionary.
    Returns:
            str: The key of the next square to solve.
    """
    # Of all unknowns, find the unknown value that occurs most often
    pzlStr = "".join(list(pzl.values()))
    unsolvedCount = [pzlStr.count(val) for val in "123456789"]
    mostFrequentUnsolved = str(unsolvedCount.index(max(unsolvedCount)) + 1)

    # With the value that occurs most often (mostFrequentUnsolved), find the square
    # with mostFrequentUnsolved with fewest remaining possible values.
    # The selection will eliminate the most possible paths
    nextSquareChoices = {
        k: len(v) for k, v in pzl.items() if mostFrequentUnsolved in v and len(v) > 1
    }
    if len(nextSquareChoices) == 0:
        return False
    bestValueCount = min(nextSquareChoices.values())
    nextSquareChoices = {
        k: v for k, v in nextSquareChoices.items() if v == bestValueCount
    }
    nextSquareChoiceKey = list(nextSquareChoices.keys())[0]
    nextSquareChoiceValues = "".join(
        sorted(pzl[nextSquareChoiceKey], key=pzlStr.count, reverse=True)
    )

    return nextSquareChoiceKey, nextSquareChoiceValues


def _eliminationPass(pzl: SudokuPuzzleT) -> SudokuPuzzleT:
    """Perform an elimination pass on the puzzle.
    Removes impossible values from the puzzle based on the current state.
    Args:
            pzl (SudokuPuzzleT): The Sudoku puzzle represented as a dictionary.
    Returns:
            SudokuPuzzleT: The updated puzzle after the elimination pass.
    """
    didChange = True
    while didChange and not isPuzzleComplete(pzl):
        solvedSquares = [k for k, v in pzl.items() if len(v) == 1]
        didChange = False
        for solvedSquare in solvedSquares:
            solvedValue = pzl[solvedSquare]
            solvedNeighbors = [
                nsq for nsq in neighbors[solvedSquare] if nsq is not solvedSquare
            ]
            # Remove solvedValue from all neighbors
            for nsq in solvedNeighbors:
                if len(pzl[nsq]) > 1 and solvedValue in pzl[nsq]:
                    didChange = True
                    pzl[nsq] = pzl[nsq].replace(solvedValue, "")
    # Dont return a copy in this case, change in place
    return pzl


def _solveTheThing(puzzle: SudokuPuzzleT):
    """Recursively solve the Sudoku puzzle using backtracking.
    Args:
            puzzle (SudokuPuzzleT): The Sudoku puzzle represented as a dictionary.
    Returns:
            SudokuPuzzleT | bool: The solved puzzle if successful, False if no solution exists.
    """

    if not isPuzzleSolved(puzzle):
        # Make a guess
        puzzle = _eliminationPass(puzzle)

        if puzzle is False:
            return False

        if isPuzzleSolved(puzzle):
            return puzzle

        if isPuzzleComplete(puzzle) and not isPuzzleSolved(puzzle):
            return False
        else:
            nextEntry, nextValues = _getNextEntryPoint(puzzle)
            if not nextEntry:
                return False

            for nextValue in nextValues:
                nextPuzzleGuess = puzzle.copy()
                nextPuzzleGuess[nextEntry] = nextValue
                nextPuzzleGuess = _solveTheThing(nextPuzzleGuess)

                if not nextPuzzleGuess:
                    continue  # No solution found for this guess, try the next one
                elif isPuzzleSolved(nextPuzzleGuess):
                    return nextPuzzleGuess
            return False
    else:
        return puzzle


def solve(puzzle: SudokuPuzzleT) -> SudokuPuzzleT | bool:
    """
    Solve the given sudoku puzzle using a backtracking algorithm.

    Args:
        puzzle (dict): A dictionary representing the sudoku puzzle, where keys are square IDs and values are possible values.

    Returns:
        dict: The solved puzzle or False if no solution exists.
    """
    return _solveTheThing(puzzle)
