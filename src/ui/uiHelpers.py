"""uiHelpers.py
This module provides helper functions to interact with the main window and its widgets in a PyQt application.
It includes functions to grab specific widgets, the main window, and the application instance.
It also provides functions to set the status bar text and retrieve puzzle-related widgets.

Functions:
    grabWidget(widgetType, widgetName: str) -> QWidget:
        Grabs a widget of the specified type and name from the main window.
    grabAppInstance() -> QApplication:
        Retrieves the QApplication instance.
    grabMainWindow() -> QMainWindow:
        Retrieves the main window of the application.
    grabPuzzleFrame() -> QFrame:
        Retrieves the puzzle frame from the main window.
    grabUiFrame() -> QFrame:
        Retrieves the UI panel frame from the main window.
    grabPuzzleInfoLabel() -> PuzzleInfoLabel:
        Retrieves the puzzle info label from the status bar.
    grabPuzzleSquares() -> dict:
        Retrieves the puzzle squares from the puzzle frame.
    grabCurrentSquare() -> dict:
        Retrieves the currently focused puzzle square.
    setAppStatusbar(statusText: str) -> None:
        Sets the status bar text in the main window.
    grabStatusBar() -> QStatusBar:
        Retrieves the status bar from the main window.
    getAppStatus() -> AppStatusEnum:
        Retrieves the current application status.
    setStatusBarText(text: str = None) -> None:
        Sets the status bar text in the main window.
    getBasePath() -> str:
        Gets the base path of the application, pointing to the 'input' directory.
"""

from functools import cache

from PyQt6.QtWidgets import QApplication, QFrame, QLabel, QMainWindow, QStatusBar


@cache
def grabWidget(widgetType, widgetName: str):
    """Grab a widget from the main window by its type and name.
    This function searches for a widget of the specified type and name in the main window.
    Args:
        widgetType (type): The type of the widget to search for (e.g., QFrame, QLabel).
        widgetName (str): The name of the widget to search for.
    Returns:
        QWidget: The first widget found that matches the specified type and name.
    """
    return grabMainWindow().findChildren(widgetType, widgetName)[0]


@cache
def grabAppInstance() -> QApplication:
    """Grab the QApplication instance.
    This function retrieves the QApplication instance, which is the main application object in a PyQt application.
    Returns:
        QApplication: The QApplication instance.
    """
    return QApplication([])


@cache
def grabMainWindow() -> QMainWindow:
    """Grab the main window of the application.
    This function retrieves the main window of the application, which is expected to be a QMainWindow instance.
    Returns:
        QMainWindow: The main window of the application.
    """
    # Iterate through all top-level widgets to find the main window
    from PyQt6.QtWidgets import QApplication, QMainWindow

    return [widget for widget in QApplication.topLevelWidgets() if isinstance(widget, QMainWindow)][
        0
    ]


@cache
def grabPuzzleFrame() -> QFrame:
    """Grab the puzzle frame from the main window.
    This function retrieves the puzzle frame, which is expected to be a QFrame instance.
    Returns:
        QFrame: The puzzle frame of the application.
    """
    # Use the grabWidget function to find the puzzle frame by its type and name
    return grabWidget(QFrame, "puzzleFrame")


@cache
def grabUiFrame() -> QFrame:
    """Grab the UI panel frame from the main window.
    This function retrieves the UI panel frame, which is expected to be a QFrame instance.
    Returns:
        QFrame: The UI panel frame of the application.
    """
    # Use the grabWidget function to find the UI panel frame by its type and name
    return grabWidget(QFrame, "UIPanel")


@cache
def grabPuzzleInfoLabel() -> QLabel:
    """Grab the puzzle info label from the status bar.
    This function retrieves the puzzle info label, which is expected to be a custom widget derived from QLabel.
    Returns:
        PuzzleInfoLabel: The puzzle info label widget.
    """
    return grabWidget(QLabel, "puzzleInfoLabel")


@cache
def grabPuzzleSquares() -> dict:
    """Grab the puzzle squares from the puzzle frame.
    This function retrieves the squares from the puzzle frame.
    Returns:
        dict: A dictionary of puzzle squares, where the keys are square identifiers
              and the values are the square widgets.
    """
    return grabPuzzleFrame().squares


def grabCurrentSquare() -> dict:
    """Grab the currently focused puzzle square.
    This function iterates through the puzzle squares and returns the one that has focus.
    Returns:
        dict: The currently focused puzzle square widget.
    """
    psquare = None
    # Iterate through the puzzle squares to find the one with focus
    for psquare in grabPuzzleSquares().values():
        if psquare.hasFocus():
            break
    return psquare


def setAppStatusbar(statusText: str) -> None:
    """Set the status bar text in the main window.
    This function updates the status bar text in the main window.
    If the main window is not found, it prints an error message to the console.
    This is useful for providing feedback to the user about the current status of the application.
    Args:
        statusText (str): The text to display in the status bar.
    Returns:
        None

    """
    mainWindow = grabMainWindow()
    if mainWindow is not None:
        mainWindow.uiStatusBar.showMessage(statusText)
    else:
        print(f"Main window not found. Status: {statusText}")


def grabStatusBar() -> QStatusBar:
    """Grab the status bar from the main window.
    This function retrieves the status bar widget from the main window.
    Returns:
        QStatusBar: The status bar of the main window.
    """
    return grabMainWindow().uiStatusBar


def getAppStatus():
    return grabMainWindow().status


def setStatusBarText(text: str = None) -> None:
    setAppStatusbar(text if text else "Ready")


@cache
def getBasePath() -> str:
    import os
    import sys
    from pathlib import Path

    """Get the base path of the application.
    This function determines the base path of the application by resolving the current script's path.
    It constructs the path to the 'input' directory, which is expected to be two levels up from the current script's location.
    If the 'input' directory does not exist at the expected location, it falls back to a default path.
    Returns:
        str: The base path of the application, pointing to the 'input' directory.
    """
    currentPath = Path(sys.argv[0]).resolve()
    if len(currentPath.parts) > 2:
        inputsPath = currentPath.parts[0:-2]
        inputsPath = os.path.join(*inputsPath, "input")
    else:
        inputsPath = currentPath.parts[0:-1]
        inputsPath = os.path.join(*inputsPath, "input")

    if not os.path.isdir(inputsPath):
        inputsPath = currentPath.parts[0:-1]
        inputsPath = os.path.join(*inputsPath, "input")

    setAppStatusbar(f"Using input location {inputsPath:s}")
    return inputsPath
