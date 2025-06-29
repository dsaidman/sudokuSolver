# -*- coding: utf-8 -*-
# Sudoku Solver
# This module provides functions to solve a Sudoku puzzle using a backtracking algorithm.

from copy import deepcopy
from time import process_time as ttoc

# Playing with types, so make some type aliases
type SquareT = str
type SquareValueT = list[int]
type SudokuPuzzleT = dict[SquareT, SquareValueT]

type VectorStringT = list[str]
type NeighborT = tuple[dict[SquareT, list[str]]]
type FamiliesT = tuple[list[VectorStringT]]

rowNames: tuple[str] = "ABCDEFGHI"
columnNames: tuple[str] = "123456789"
squares: tuple[VectorStringT] = [row + col for row in rowNames for col in columnNames]
cellRows: tuple[VectorStringT] = ["ABC", "DEF", "GHI"]
cellColumns: tuple[VectorStringT] = ["123", "456", "789"]

sqValues0: SquareValueT = set(range(1, 10))
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
    _cols: str = cellColumns[[idx for idx, s in enumerate(cellColumns) if sq[1] in s][0]]
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
            (set(_getRowNeighbors(sq)) | set(_getColumnNeighbors(sq)) | set(_getCellNeighbors(sq)))
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
    # Use a generator to break first time it invalid
    return not any(len(v) > 1 for v in pzl.values())


def allFamiliesValid(pzl: SudokuPuzzleT) -> bool:
    return all(isFamilyCorrect(pzl, fam) for fam in families)


def isFamilyCorrect(pzl: SudokuPuzzleT, familySquares: VectorStringT) -> bool:
    """Check if a family of squares is correct.
    Checks if the values in a family of squares contain all digits from 1 to 9 exactly once.
    Args:
            pzl (SudokuPuzzleT): The Sudoku puzzle represented as a dictionary.
            familySquares (VectorStringT): A list of square IDs that form a family.
    Returns:
            bool: True if the family is correct, False otherwise.
    """
    # Check if the values in the family squares contain all digits from 1 to 9 exactly onceamilySquares], [])))
    return set(sum([pzl[familySq] for familySq in familySquares], [])) == sqValues0


def isPuzzleSolved(pzl: SudokuPuzzleT) -> bool:
    """Check if the puzzle is solved.
    Checks if the puzzle is complete and all families are correct.
    Args:
            pzl (SudokuPuzzleT): The Sudoku puzzle represented as a dictionary.
    Returns:
            bool: True if the puzzle is solved, False otherwise.
    """
    return isPuzzleComplete(pzl) and allFamiliesValid(pzl)


def _getNextEntryPoint(pzl: SudokuPuzzleT):
    """Get the next entry point for solving the puzzle.
    Finds the square with the most frequent unknown value and the fewest remaining possible values.
    Args:
            pzl (SudokuPuzzleT): The Sudoku puzzle represented as a dictionary.
    Returns:
            str: The key of the next square to solve.
    """
    # Of all unknowns, find the unknown value that occurs most often
    pzlStr = sum(list(pzl.values()), [])
    # pzlStr = "".join(list(pzl.values()))
    unsolvedCount = [pzlStr.count(val) for val in list(sqValues0)]

    # mostFrequentUnsolved = unsolvedCount.index(max(unsolvedCount)) + 1
    mostFrequentUnsolved = unsolvedCount.index(max(unsolvedCount)) + 1
    # With the value that occurs most often (mostFrequentUnsolved), find the square
    # with mostFrequentUnsolved with fewest remaining possible values.
    # The selection will eliminate the most possible paths
    nextSquareChoices = {
        k: len(v) for k, v in pzl.items() if mostFrequentUnsolved in v and len(v) > 1
    }
    if len(nextSquareChoices) == 0:
        return (False, False)
    bestValueCount = min(nextSquareChoices.values())
    nextSquareChoiceKey = next((k for k, v in nextSquareChoices.items() if v == bestValueCount), [])
    nextSquareChoiceValues = sorted(pzl[nextSquareChoiceKey], key=pzlStr.count, reverse=True)

    return nextSquareChoiceKey, nextSquareChoiceValues


def solve(puzzle: SudokuPuzzleT) -> SudokuPuzzleT | bool:
    """
    Solve the given sudoku puzzle using a backtracking algorithm.

    Args:
        puzzle (dict): A dictionary representing the sudoku puzzle, where keys are square IDs and values are possible values.

    Returns:
        dict: The solved puzzle or False if no solution exists.
    """

    # Metrics to count using nested functions
    numRecursions: int = 0
    numOperations: int = 0
    bestSinglePass: int = 0

    def _solveTheThing(puzzleNext: SudokuPuzzleT) -> SudokuPuzzleT | bool:
        """Recursively solve the Sudoku puzzle using backtracking.
        Args:
                puzzle (SudokuPuzzleT): The Sudoku puzzle represented as a dictionary.
        Returns:
                SudokuPuzzleT | bool: The solved puzzle if successful, False if no solution exists.
        """
        nonlocal numRecursions

        # Make a guess
        puzzle = _eliminationPass(puzzleNext)

        # Exit early puzzle is false to avoid extra searching
        if puzzle is False:
            return False

        # Exit early if not a valid family to avoid extra looping
        # an incomplete family can still be considered correct if no rules broken
        if not allFamiliesValid(puzzle):
            return False

        isSolved = isPuzzleSolved(puzzle)
        if isSolved:
            return puzzle

        if isPuzzleComplete(puzzle) and not isSolved:
            return False
        else:
            nextEntry, nextValues = _getNextEntryPoint(puzzle)

            if not nextEntry:
                return False

            for nextValue in nextValues:
                # Update number of recursions it takes

                nextPuzzleGuess = deepcopy(puzzle)

                nextPuzzleGuess[nextEntry] = [nextValue]
                if allFamiliesValid(nextPuzzleGuess):
                    numRecursions += 1
                    nextPuzzleGuess = _solveTheThing(nextPuzzleGuess)
                else:
                    nextPuzzleGuess = False
                    continue

                if not nextPuzzleGuess:
                    continue  # No solution found for this guess, try the next one
                elif isPuzzleSolved(nextPuzzleGuess):
                    return nextPuzzleGuess
            return False

    def _eliminationPass(pzl: SudokuPuzzleT) -> SudokuPuzzleT:
        """Perform an elimination pass on the puzzle.
        Removes impossible values from the puzzle based on the current state.
        Args:
                pzl (SudokuPuzzleT): The Sudoku puzzle represented as a dictionary.
        Returns:
                SudokuPuzzleT: The updated puzzle after the elimination pass.
        """
        nonlocal bestSinglePass
        nonlocal numOperations
        singlePassCount = 0
        didChange = True
        while didChange and not isPuzzleComplete(pzl):
            didChange = False
            for solvedSquare in (sqKey for sqKey, sqVal in pzl.items() if len(sqVal) == 1):
                solvedValue = pzl[solvedSquare][0]
                for solvedNeighbor in neighbors[solvedSquare]:
                    if len(pzl[solvedNeighbor]) > 1 and solvedValue in pzl[solvedNeighbor]:
                        didChange = True
                        singlePassCount += 1
                        numOperations += 1
                        pzl[solvedNeighbor].remove(solvedValue)

        # Update best single elimination pass

        bestSinglePass = max(bestSinglePass, singlePassCount)
        return pzl

    tStart = ttoc()
    solution = _solveTheThing(puzzle)
    # Turn lists into strings for display
    if solution:
        for k, v in solution.items():
            solution[k] = str(v[0])
    duration_ms = (ttoc() - tStart) * 1000.0
    return {
        "solution": solution,
        "bestSinglePass": bestSinglePass,
        "numOperations": numOperations,
        "numRecursions": numRecursions,
        "duration_ms": duration_ms,
    }
