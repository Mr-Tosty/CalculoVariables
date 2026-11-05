"""Módulo de interfaz POO para la sección de Gráficas y Límites.

Basado en el análisis de trayectorias y aproximación de los apuntes.
"""

import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class GraphTab(ctk.CTkFrame):
    """Componente visual para aproximación numérica de límites y gráficos."""

    def __init__(self, parent, engine):
        super().__init__(parent, fg_color="transparent")
        self.engine = engine
        self._build_ui()

    def _build_ui(self):
        title = ctk.CTkLabel(
            self,
            text="Aproximación de Límites y Gráfica (Apuntes)",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#38bdf8",
        )
        title.pack(anchor="w", padx=10, pady=5)

        f = ctk.CTkFrame(self, fg_color="#1e293b")
        f.pack(fill="x", padx=10, pady=5)

        self.entry_expr = ctk.CTkEntry(
            f, placeholder_text="Ej: (x^4 + y^2 + z^2)/(1 + x^2 + y^2 + z^2)"
        )
        self.entry_expr.pack(
            side="left", fill="x", expand=True, padx=10, pady=10
        )

        ctk.CTkButton(
            f, text="Generar Tabla y Gráfica", command=self._execute
        ).pack(side="right", padx=10, pady=10)

        self.output = ctk.CTkTextbox(
            self, height=160, font=ctk.CTkFont(family="Consolas", size=13),
            text_color="#4ade80"
        )
        self.output.pack(fill="x", padx=10, pady=5)

        self.plot_box = ctk.CTkFrame(self)
        self.plot_box.pack(fill="both", expand=True, padx=10, pady=5)

    def _execute(self):
        expr = self.entry_expr.get()
        try:
            steps = self.engine.generate_limit_table(expr)
            self.output.delete("1.0", "end")
            self.output.insert("1.0", steps)
            self._render_graph(expr)
        except Exception as e:
            self.output.delete("1.0", "end")
            self.output.insert("1.0", f"❌ ERROR: {str(e)}")

    def _render_graph(self, expr_str):
        for w in self.plot_box.winfo_children():
            w.destroy()
        try:
            fig, ax = plt.subplots(figsize=(5, 3), dpi=100)
            pts = [1.0, 0.5, 0.1, 0.05, 0.01]
            sym_e = self.engine.parse_expression(expr_str)

            y_vals = []
            for p in pts:
                v = float(
                    sym_e.subs(
                        {self.engine.x: p, self.engine.y: p, self.engine.z: p}
                    ).evalf()
                )
                y_vals.append(v)

            ax.plot(pts, y_vals, marker="o", color="#38bdf8", linestyle="-")
            ax.set_title("Secuencia de Aproximación a (0,0,0)")
            ax.set_xlabel("x = y = z")
            ax.set_ylabel("f(x,y,z)")
            ax.grid(True, alpha=0.3)
            fig.tight_layout()

            canvas = FigureCanvasTkAgg(fig, master=self.plot_box)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
        except Exception:
            pass