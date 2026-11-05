"""Ventana Principal actualizada que integra todas las pestañas POO."""

import customtkinter as ctk
from core.math_engine import MathEngine
from gui.tabs.derivative_tab import DerivativeTab
from gui.tabs.integral_tab import IntegralTab
from gui.tabs.graph_tab import GraphTab
from gui.tabs.instructions_tab import InstructionsTab

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.engine = MathEngine()

        self.title("Calculadora Multivariable MVC")
        self.geometry("1250 x 820")
        self.minsize(1050, 720)

        self._build_tabs()

    def _build_tabs(self):
        self.tabview = ctk.CTkTabview(self, segmented_button_fg_color="#1e293b")
        self.tabview.pack(fill="both", expand=True, padx=15, pady=10)

        # Creación de todas las pestañas mediante clases POO independientes
        tab_graph = self.tabview.add("Función & Gráfica")
        tab_der = self.tabview.add("Derivadas Parciales")
        tab_int = self.tabview.add("Integrales Múltiples")
        tab_notes = self.tabview.add("Instrucciones & Formulario")

        GraphTab(tab_graph, self.engine).pack(fill="both", expand=True)
        DerivativeTab(tab_der, self.engine).pack(fill="both", expand=True)
        IntegralTab(tab_int, self.engine).pack(fill="both", expand=True)
        InstructionsTab(tab_notes).pack(fill="both", expand=True)