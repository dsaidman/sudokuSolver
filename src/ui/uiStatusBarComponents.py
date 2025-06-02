from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFrame, QLabel, QPushButton

from .uiEnums import ValidityEnum
from .uiHelpers import grabPuzzleSquares, grabWidget


class PuzzleInfoLabel(QLabel):
	def __init__(self, parent, objectName="puzzleInfoLabel"):
		super(PuzzleInfoLabel, self).__init__(parent, objectName="puzzleInfoLabel")

		self.setParent(parent)
		self.setObjectName(objectName)
		self.setText("0 OF 17 Squares Set")
		self.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
		self.setProperty("state", "NotSolvable")
		self.setStyleSheet(
			"""
            QLabel { font-family: 'Segoe UI'; font-size: 12px; font-weight: bold; }
            QLabel#puzzleInfoLabel[state="Invalid"] {
                color: rgb(255, 0, 0);
                font-style: italic;
                font-weight: regular}
            QLabel#puzzleInfoLabel[state="Solvable"] {
                color: rgb(255, 140, 0);
                font-style: regular;
                font-weight: bold}
            QLabel#puzzleInfoLabel[state="Solved"] {
                color: rgb(0, 255, 0);
                font-style: regular;
                font-weight: regular}
            QLabe#puzzleInfoLabel[state="NotSolvable"] {
                color: rgb(212,212,200);
                font-style: normal;
                font-weight: regular}
            """
		)

		# Connect the puzzle squares to update text when changed. Cant do
		# before because this class didnt exist yet
		for theSquare in grabPuzzleSquares().values():
			theSquare.textEdited.connect(self.update)

	def reset(self):
		self.setProperty("state", "NotSolvable")
		self.setText("0 OF 17 Squares Set")
		self.style().polish(self)
		self.style().unpolish(self)

	def update(self):
		puzzleFrame = grabWidget(QFrame, "puzzleFrame")

		numFilledSquares = puzzleFrame.validSquareCount
		theText = str(numFilledSquares) + " OF 17 Sqaures Set"
		puzzleIsValid = puzzleFrame.isValid

		setPuzzleBtn = grabWidget(QPushButton, "setPuzzleBtn")

		if puzzleIsValid == ValidityEnum.Invalid:
			self.setProperty("state", "Invalid")
			setPuzzleBtn._disableMe()
		elif (
			numFilledSquares >= 17 and numFilledSquares < 81 and puzzleIsValid == ValidityEnum.Valid
		):
			self.setProperty("state", "Solvable")
			theText = theText + ": READY"
			setPuzzleBtn._enableMe()
		elif numFilledSquares == 81 and puzzleIsValid == ValidityEnum.Valid:
			self.setProperty("state", "Solved")
			theText = theText + ": COMPLETE"
			setPuzzleBtn._enableMe()
		elif numFilledSquares < 17 or puzzleIsValid == ValidityEnum.Valid:
			self.setProperty("state", "NotSolvable")
			setPuzzleBtn._disableMe()
		self.setText(theText)
		self.style().polish(self)
		self.style().unpolish(self)
