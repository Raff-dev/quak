import ctypes
from os import system
from ctypes import c_long, c_wchar_p, c_ulong, c_void_p


gHandle = ctypes.windll.kernel32.GetStdHandle(c_long(-11))


def move_cursor(y, x):
    """Move cursor to position indicated by x and y."""
    value = x + (y << 16)
    ctypes.windll.kernel32.SetConsoleCursorPosition(gHandle, c_ulong(value))


def addstr(string):
    """Write string"""
    ctypes.windll.kernel32.WriteConsoleW(gHandle, c_wchar_p(
        string), c_ulong(len(string)), c_void_p(), None)


def draw(x: int, y: int, character: str):
    move_cursor(y, x)
    addstr(character)
