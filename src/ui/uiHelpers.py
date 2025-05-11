import sys
import os
from functools import lru_cache
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QMainWindow, QFrame


def grabWidget(widgetType, widgetName):
    return grabMainWindow().findChildren(widgetType, widgetName)[0]


def grabAppInstance():
    return QApplication([])


@lru_cache(typed=False)
def grabMainWindow():
    return [widget for widget in QApplication.topLevelWidgets() if isinstance(widget, QMainWindow)][0]


def grabPuzzleFrame():
    return grabWidget(QFrame, 'puzzleFrame')

def grabUiFrame():
    return grabWidget(QFrame, 'UIPanel')


def grabPuzzleSquares():
    return grabPuzzleFrame().squares

def grabCurrentSquare():
    for psquare in grabPuzzleSquares().values():
        if psquare.hasFocus()==True:
            break
    return psquare

def grabStatusBar():
    return grabMainWindow().uiStatusBar

def getAppStatus():
    return grabMainWindow().status


@lru_cache(typed=False)
def getBasePath():

    currentPath = Path(sys.argv[0]).resolve()
    if len(currentPath.parts) > 2:
        inputsPath = currentPath.parts[0:-2]
        inputsPath = os.path.join(*inputsPath, 'input')
    else:
        inputsPath = currentPath.parts[0:-1]
        inputsPath = os.path.join(*inputsPath, 'input')

    if not os.path.isdir(inputsPath):
        inputsPath = currentPath.parts[0:-1]
        inputsPath = os.path.join(*inputsPath, 'input')

    print(f'Using input location {inputsPath:s}')
    return inputsPath
