#engine/utils/crash_handler.py
import traceback
from pathlib import Path
from datetime import datetime
class CrashHandler:
    @staticmethod
    def handle_exception(exception):
        crash_dir = Path("logs")
        crash_dir.mkdir(exist_ok=True)
        crash_file = crash_dir / "crash.log"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        traceback_text = traceback.format_exc()
        print(traceback_text)
        print(f"[CRITICAL] Fatal Exception: {exception}")
        with open(crash_file,"a",encoding="utf-8") as file:
            file.write("\n"+ "=" * 80+ "\n")
            file.write(f"Timestamp: {timestamp}\n\n")
            file.write(f"Exception: {exception}\n\n")
            file.write(traceback_text)
            file.write("\n")
        print("[CRITICAL] Crash report written to logs/crash.log")