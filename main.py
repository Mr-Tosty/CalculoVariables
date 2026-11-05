"""Lanzador principal de la aplicación Asistente de Cálculo Multivariable.

Punto de entrada único que inicializa la ventana principal y el motor POO.
"""

from gui.main_window import MainWindow


def main():
    app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    main()