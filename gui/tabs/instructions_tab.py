"""Módulo de interfaz POO para las instrucciones y formulario oficial."""

import customtkinter as ctk


class InstructionsTab(ctk.CTkFrame):
    """Componente visual que muestra el formulario y guía de estudio."""

    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self._build_ui()

    def _build_ui(self):
        title = ctk.CTkLabel(
            self,
            text="Formulario Oficial e Instrucciones",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#38bdf8",
        )
        title.pack(anchor="w", padx=10, pady=10)

        txt = ctk.CTkTextbox(
            self, font=ctk.CTkFont(size=13), text_color="#e2e8f0"
        )
        txt.pack(fill="both", expand=True, padx=10, pady=5)

        content = (
            "FORMULARIO DE DERIVADAS E INTEGRALES (BASE OFICIAL)\n\n"
            "1. DERIVADAS BÁSICAS Y TRIGONOMÉTRICAS:\n"
            "   • d/dx(k) = 0\n"
            "   • d/dx(x) = 1\n"
            "   • d/dx(x^n) = n * x^(n-1)\n"
            "   • d/dx(sin u) = cos u * du/dx\n"
            "   • d/dx(cos u) = -sin u * du/dx\n"
            "   • d/dx(ln u) = (1/u) * du/dx\n\n"
            "2. INTEGRALES INMEDIATAS:\n"
            "   • ∫ dx = x + C\n"
            "   • ∫ x^n dx = x^(n+1) / (n+1) + C  (para n ≠ -1)\n"
            "   • ∫ (1/x) dx = ln|x| + C\n"
            "   • ∫ sin u du = -cos u + C\n"
            "   • ∫ cos u du = sin u + C\n\n"
            "3. INSTRUCCIONES DE USO:\n"
            "   • Use asteriscos (*) para multiplicaciones explícitas.\n"
            "   • Use '^' o '**' para potencias.\n"
            "   • Las pestañas superiores replican la interfaz web probada para mayor claridad."
        )
        txt.insert("1.0", content)
        txt.configure(state="disabled")