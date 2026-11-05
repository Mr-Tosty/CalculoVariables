"""Módulo de interfaz POO para la sección de Derivadas Parciales y Mixtas.

Basado en las reglas del formulario oficial[cite: 6].
"""

import customtkinter as ctk


class DerivativeTab(ctk.CTkFrame):
    """Componente visual orientado a objetos para derivadas."""

    def __init__(self, parent, engine):
        super().__init__(parent, fg_color="transparent")
        self.engine = engine
        self._build_ui()

    def _build_ui(self):
        title = ctk.CTkLabel(
            self,
            text="Derivadas Parciales y Mixtas",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#38bdf8",
        )
        title.pack(anchor="w", padx=10, pady=(10, 2))

        sub = ctk.CTkLabel(
            self,
            text="Introduce la función f(x, y) y selecciona el orden de derivación.",
            font=ctk.CTkFont(size=12),
        )
        sub.pack(anchor="w", padx=10, pady=(0, 15))

        form_frame = ctk.CTkFrame(self, fg_color="#1e293b")
        form_frame.pack(fill="x", padx=10, pady=5)

        # Entrada de función
        f1 = ctk.CTkFrame(form_frame, fg_color="transparent")
        f1.pack(side="left", fill="x", expand=True, padx=5, pady=5)
        ctk.CTkLabel(f1, text="Función f(x, y)").pack(anchor="w")
        self.entry_expr = ctk.CTkEntry(
            f1, placeholder_text="Ej: 3/5*x^3*y^2 - 9*y^3"
        )
        self.entry_expr.pack(fill="x", pady=2)

        # Valores x, y
        f2 = ctk.CTkFrame(form_frame, fg_color="transparent")
        f2.pack(side="left", padx=5, pady=5)
        ctk.CTkLabel(f2, text="Valor x").pack(anchor="w")
        self.entry_x = ctk.CTkEntry(f2, width=70, placeholder_text="2")
        self.entry_x.pack(pady=2)

        f3 = ctk.CTkFrame(form_frame, fg_color="transparent")
        f3.pack(side="left", padx=5, pady=5)
        ctk.CTkLabel(f3, text="Valor y").pack(anchor="w")
        self.entry_y = ctk.CTkEntry(f3, width=70, placeholder_text="1")
        self.entry_y.pack(pady=2)

        # Secuencia / Orden
        f4 = ctk.CTkFrame(form_frame, fg_color="transparent")
        f4.pack(side="left", padx=5, pady=5)
        ctk.CTkLabel(f4, text="Operación / Orden").pack(anchor="w")
        self.combo_seq = ctk.CTkOptionMenu(
            f4,
            values=[
                "∂f / ∂x",
                "∂f / ∂y",
                "∂²f / ∂x²",
                "∂²f / ∂y²",
                "∂²f / (∂x ∂y)",
            ],
        )
        self.combo_seq.pack(pady=2)

        btn = ctk.CTkButton(
            self,
            text="Calcular Derivada",
            fg_color="#0284c7",
            hover_color="#0369a1",
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self._execute,
        )
        btn.pack(fill="x", padx=10, pady=10)

        self.output = ctk.CTkTextbox(
            self, font=ctk.CTkFont(family="Consolas", size=13), text_color="#4ade80"
        )
        self.output.pack(fill="both", expand=True, padx=10, pady=10)

    def _execute(self):
        expr = self.entry_expr.get()
        xv = self.entry_x.get()
        yv = self.entry_y.get()
        seq = self.combo_seq.get()
        try:
            _, steps = self.engine.evaluate_derivative(expr, xv, yv, seq)
            self.output.delete("1.0", "end")
            self.output.insert("1.0", steps)
        except Exception as e:
            self.output.delete("1.0", "end")
            self.output.insert("1.0", f"❌ ERROR: {str(e)}")