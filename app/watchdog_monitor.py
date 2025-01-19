import os
import sys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess

class RestartOnChangeHandler(FileSystemEventHandler):
    def __init__(self, script):
        self.script = script
        self.process = None
        self.start_script()

    def start_script(self):
        if self.process:
            self.process.terminate()
        self.process = subprocess.Popen([sys.executable, self.script])

    def on_modified(self, event):
        if event.src_path.endswith(self.script):
            print(f"Arquivo modificado: {event.src_path}. Reiniciando o bot...")
            self.start_script()

if __name__ == "__main__":
    script_to_watch = "app.py"  # Substitua pelo nome do arquivo do seu bot
    handler = RestartOnChangeHandler(script_to_watch)
    observer = Observer()
    observer.schedule(handler, ".", recursive=False)

    print(f"Monitorando mudanças no arquivo '{script_to_watch}'...")
    try:
        observer.start()
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
