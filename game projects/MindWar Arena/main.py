# main.py
from engine.utils.crash_handler import CrashHandler
from launcher import Launcher
def main():
    launcher = Launcher()
    try:
        launcher.start()
    except Exception as exception:
        CrashHandler.handle_exception(exception)
if __name__ == "__main__":
    main()