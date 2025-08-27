import threading
from services.flask import create_app, run_flask
from ui.app_ui import MainWindow

if __name__ == "__main__":
    # Crear app Flask
    app = create_app()

    # Levantar Flask en un hilo
    flask_thread = threading.Thread(target=run_flask, args=(app,), daemon=True)
    flask_thread.start()

    # Correr Tkinter en el hilo principal
    app_ui = MainWindow()
    app_ui.run()
