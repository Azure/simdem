# pylint: disable=R0903,E0401,W0612
""" Get Character Class """

# https://stackoverflow.com/a/510404/8475874
class Getch:
    """Gets a single character from standard input.  Does not echo to the screen."""
    def __init__(self):
        try:
            self.impl = GetchWindows()
        except ImportError:
            self.impl = GetchUnix()

    def __call__(self):
        return self.impl()


class GetchUnix:
    """ Get character impl for *nix """
    def __call__(self):
        import sys
        import tty
        import termios
        filedesc = sys.stdin.fileno()
        old_settings = termios.tcgetattr(filedesc)
        try:
            tty.setraw(sys.stdin.fileno())
            char = sys.stdin.read(1)
        finally:
            termios.tcsetattr(filedesc, termios.TCSADRAIN, old_settings)
        return char


class GetchWindows:
    """ Get character impl for *nix """
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()
