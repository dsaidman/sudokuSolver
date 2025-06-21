import logging
import os
from functools import cache

from .uiHelpers import getBasePath

uiLogger = logging.getLogger("uiLogger")
__all__ = ["puzzleInput"]


class PuzzleInputFile(object):
    puzzleIDs = None
    puzzleDifficulty = None
    puzzles = None
    puzzleComment = None
    basePath = getBasePath()
    puzzleFile = os.path.normpath(os.path.join(basePath, "..", "..", "resources", "puzzles.csv"))

    def __init__(self):
        uiLogger.debug("Initializing PuzzleInputFile and importing puzzles")
        self.puzzleIDs, self.puzzleDifficulty, self.puzzles, self.puzzleComment = (
            self._readPuzzleCsv()
        )
        ids = list(map(int, self.puzzleIDs))
        self.minID = min(ids)
        self.maxID = max(ids)
        self.numPuzzles = len(ids)

    @cache
    def _readPuzzleCsv(self):
        from csv import DictReader

        if not os.path.isfile(self.puzzleFile):
            uiLogger.error("Puzzle file %s not found", self.puzzleFile)
            return None

        puzzleIDs = []
        puzzleDifficulty = []
        inputPuzzle = []
        puzzleComment = []
        try:
            with open(self.puzzleFile, "r") as puzzleCsv:
                puzzleReader = DictReader(puzzleCsv)
                for row in puzzleReader:
                    puzzleIDs.append(row["ID"])
                    inputPuzzle.append(row["Puzzle"])
                    puzzleDifficulty.append(row["Score"])
                    puzzleComment.append(row["Comment"])

        except OSError:
            uiLogger.error("Failed to open %s", self.puzzleFile)
            return None

        uiLogger.info("All Puzzles imported")
        return puzzleIDs, puzzleDifficulty, inputPuzzle, puzzleComment


puzzleInput = PuzzleInputFile()
