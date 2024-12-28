import os
import threading
import time
import logging
from flask import Flask, request

CONFIG_FILE = os.getenv("CONFIG_FILE", "config.ini")
LOCK = threading.Lock()


def setup_logging(level=logging.INFO):
    """Configura el logging con formato de fecha y hora detallado"""
    log_format = "%(asctime)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=level, format=log_format)


def load_log_level():
    """Carga el nivel de log desde el archivo de configuración y lo compara con el nivel actual de logging."""
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            new_log_level = f.read().strip().lower()
            if new_log_level not in ["info", "debug"]:
                new_log_level = "info"

            if new_log_level == "debug":
                new_log_level_value = logging.DEBUG
            else:
                new_log_level_value = logging.INFO

            if new_log_level_value != logging.getLogger().level:
                logging.getLogger().setLevel(new_log_level_value)
                logging.info(f"el valor del log_level fue cambiado a {new_log_level}")

    except FileNotFoundError:
        logging.info(
            "El archivo de configuración no se encontró. Usando nivel de log por defecto."
        )
        logging.getLogger().setLevel(logging.INFO)


def monitor_config_file():
    """Monitorea el archivo de configuración y actualiza el nivel de logging en caliente."""
    while True:
        time.sleep(1)
        with LOCK:
            load_log_level()


app = Flask(__name__)


@app.route("/")
def hello():
    """Maneja la ruta principal y responde con un mensaje."""
    with LOCK:
        logging.info("Request recibida")
        logging.debug(f"Request recibida con headers: {dict(request.headers)}")
    return "Hello, World!"


if __name__ == "__main__":
    setup_logging(logging.INFO)
    config_monitor_thread = threading.Thread(target=monitor_config_file, daemon=True)
    config_monitor_thread.start()
    app.run(host="0.0.0.0", port=8080, debug=True)
