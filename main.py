"""Lanzador principal de la aplicacion Asistente de Calculo Multivariable.

Punto de entrada de la arquitectura modular.
"""

from gui.main_window import MainWindow


def main():
    app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    main()
