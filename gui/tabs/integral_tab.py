"""Módulo de interfaz POO para la sección de Integrales Múltiples.

Basado en el formulario oficial de integrales[cite: 5].
"""

import customtkinter as ctk


class IntegralTab(ctk.CTkFrame):
    """Componente visual orientado a objetos para integrales dobles y triples."""

    def __init__(self, parent, engine):
        super().__init__(parent, fg_color="transparent")
        self.engine = engine
        self._build_ui()

    def _build_ui(self):
        title = ctk.CTkLabel(
            self,
            text="Integrales Múltiples (Dobles y Triples)",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#38bdf8",
        )
        title.pack(anchor="w", padx=10, pady=(10, 2))

        form = ctk.CTkFrame(self, fg_color="#1e293b")
        form.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(form, text="Función Integrando f(x, y, z):").pack(
            anchor="w", padx=10, pady=2
        )
        self.entry_expr = ctk.CTkEntry(
            form, placeholder_text="Ej: x^2 + y^2 + z^2"
        )
        self.entry_expr.pack(fill="x", padx=10, pady=2)

        lim_frame = ctk.CTkFrame(form, fg_color="transparent")
        lim_frame.pack(fill="x", padx=5, pady=5)

        self.e_xa = ctk.CTkEntry(lim_frame, placeholder_text="X Inf (0)", width=90)
        self.e_xa.pack(side="left", padx=4)
        self.e_xb = ctk.CTkEntry(lim_frame, placeholder_text="X Sup (1)", width=90)
        self.e_xb.pack(side="left", padx=4)

        self.e_ya = ctk.CTkEntry(lim_frame, placeholder_text="Y Inf (0)", width=90)
        self.e_ya.pack(side="left", padx=4)
        self.e_yb = ctk.CTkEntry(lim_frame, placeholder_text="Y Sup (1)", width=90)
        self.e_yb.pack(side="left", padx=4)

        self.e_za = ctk.CTkEntry(lim_frame, placeholder_text="Z Inf (0)", width=90)
        self.e_za.pack(side="left", padx=4)
        self.e_zb = ctk.CTkEntry(lim_frame, placeholder_text="Z Sup (1)", width=90)
        self.e_zb.pack(side="left", padx=4)

        btn_box = ctk.CTkFrame(self, fg_color="transparent")
        btn_box.pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(
            btn_box,
            text="Calcular Doble",
            command=self._calc_double,
            fg_color="#0284c7",
        ).pack(side="left", expand=True, fill="x", padx=5)
        ctk.CTkButton(
            btn_box,
            text="Calcular Triple",
            command=self._calc_triple,
            fg_color="#0d9488",
        ).pack(side="left", expand=True, fill="x", padx=5)

        self.output = ctk.CTkTextbox(
            self, font=ctk.CTkFont(family="Consolas", size=13), text_color="#4ade80"
        )
        self.output.pack(fill="both", expand=True, padx=10, pady=10)

    def _calc_double(self):
        try:
            _, steps = self.engine.evaluate_double_integral(
                self.entry_expr.get(),
                self.e_xa.get() or "0", self.e_xb.get() or "1",
                self.e_ya.get() or "0", self.e_yb.get() or "1"
            )
            self.output.delete("1.0", "end")
            self.output.insert("1.0", steps)
        except Exception as e:
            self.output.delete("1.0", "end")
            self.output.insert("1.0", f"❌ ERROR: {str(e)}")

    def _calc_triple(self):
        try:
            _, steps = self.engine.evaluate_triple_integral(
                self.entry_expr.get(),
                self.e_xa.get() or "0", self.e_xb.get() or "1",
                self.e_ya.get() or "0", self.e_yb.get() or "1",
                self.e_za.get() or "0", self.e_zb.get() or "1"
            )
            self.output.delete("1.0", "end")
            self.output.insert("1.0", "1.0")
            self.output.insert("1.0", steps)
        except Exception as e:
            self.output.delete("1.0", "end")
            self.output.insert("1.0", f"❌ ERROR: {str(e)}")