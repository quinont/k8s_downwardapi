from flask import Flask, request
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import logging
import time
import threading
import os

app = Flask(__name__)

CONFIG_DIR = os.getenv("CONFIG_DIR", "/config/")
WATCHDOG_PATH = os.getenv("WATCHDOG_PATH", CONFIG_DIR)
CONFIG_FILE_NAME = os.getenv("CONFIG_FILE_NAME", "log_config.txt")
CONFIG_FILE = os.path.join(CONFIG_DIR, CONFIG_FILE_NAME)

print(f"Watchdog_path: {WATCHDOG_PATH}")
print(f"config_dir: {CONFIG_DIR}")
print(f"CONFIG_FILE: {CONFIG_FILE}")


def configure_logger():
    with open(CONFIG_FILE, "r") as f:
        level = f.read().strip()

    if level.lower() == "debug":
        app.logger.setLevel(logging.DEBUG)
    else:
        app.logger.setLevel(logging.INFO)


class ConfigFileEventHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith(CONFIG_FILE_NAME):
            app.logger.info(
                "Archivo de configuracion modificado, actualizando logger..."
            )
            configure_logger()


def start_watchdog():
    event_handler = ConfigFileEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path=WATCHDOG_PATH, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


configure_logger()


@app.route("/", methods=["GET"])
def hello_world():
    app.logger.info('Solicitud recibida en "/"')
    if app.logger.level == logging.DEBUG:
        app.logger.debug(f"Headers: {request.headers}")
    return "Hello, World!"


if __name__ == "__main__":
    threading.Thread(target=start_watchdog, daemon=True).start()
    app.run(host="0.0.0.0", port=8080, debug=True)
