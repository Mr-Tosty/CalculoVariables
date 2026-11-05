"""Modulo de Interfaz de Usuario estilo Web MVC.

Replica la claridad de la version web con orden horizontal y alto contraste.
"""

import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

from core.math_engine import MathEngine

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class MainWindow(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.engine = MathEngine()

        self.title("Calculadora Multivariable MVC")
        self.geometry("1250 x 820")
        self.minsize(1050, 720)

        self._build_header()
        self._build_tabs()

    def _build_header(self):
        header = ctk.CTkFrame(self, fg_color="#101827", corner_radius=0)
        header.pack(fill="x", padx=0, pady=0)

        title = ctk.CTkLabel(
            header,
            text="Calculadora Multivariable MVC",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#38bdf8",
        )
        title.pack(anchor="w", padx=20, pady=(10, 2))

        subtitle = ctk.CTkLabel(
            header,
            text="Cálculo de derivadas parciales, mixtas, integrales y aproximación de límites.",
            font=ctk.CTkFont(size=13),
            text_color="#94a3b8",
        )
        subtitle.pack(anchor="w", padx=20, pady=(0, 10))

    def _build_tabs(self):
        self.tabview = ctk.CTkTabview(self, segmented_button_fg_color="#1e293b")
        self.tabview.pack(fill="both", expand=True, padx=15, pady=10)

        # Recreacion exacta de las pestañas de la version Web
        self.tab_graph = self.tabview.add("Función & Gráfica")
        self.tab_der = self.tabview.add("Derivadas Parciales")
        self.tab_int = self.tabview.add("Integrales Múltiples")
        self.tab_notes = self.tabview.add("Instrucciones & Formulario")

        self._setup_derivatives_tab(self.tab_der)
        self._setup_integrals_tab(self.tab_int)
        self._setup_graph_tab(self.tab_graph)
        self._setup_notes_tab(self.tab_notes)

    def _setup_derivatives_tab(self, tab):
        title = ctk.CTkLabel(
            tab,
            text="Derivadas Parciales y Mixtas",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#38bdf8",
        )
        title.pack(anchor="w", padx=10, pady=(10, 2))

        sub = ctk.CTkLabel(
            tab,
            text="Introduce la función original $f(x, y)$ y selecciona el orden o secuencia de derivación.",
            font=ctk.CTkFont(size=12),
        )
        sub.pack(anchor="w", padx=10, pady=(0, 15))

        # Fila horizontal de campos (como en la imagen Web)
        form_frame = ctk.CTkFrame(tab, fg_color="#1e293b")
        form_frame.pack(fill="x", padx=10, pady=5)

        # Columnas
        f1 = ctk.CTkFrame(form_frame, fg_color="transparent")
        f1.pack(side="left", fill="x", expand=True, padx=5, pady=5)
        ctk.CTkLabel(f1, text="Función de Entrada $f(x, y)$").pack(anchor="w")
        self.entry_der_expr = ctk.CTkEntry(
            f1, placeholder_text="3/5*x^3*y^2 + 3/2*x^3*y^2 - 9y^3"
        )
        self.entry_der_expr.pack(fill="x", pady=2)

        f2 = ctk.CTkFrame(form_frame, fg_color="transparent")
        f2.pack(side="left", padx=5, pady=5)
        ctk.CTkLabel(f2, text="Valor de $x$").pack(anchor="w")
        self.entry_der_x = ctk.CTkEntry(f2, width=80, placeholder_text="2")
        self.entry_der_x.pack(pady=2)

        f3 = ctk.CTkFrame(form_frame, fg_color="transparent")
        f3.pack(side="left", padx=5, pady=5)
        ctk.CTkLabel(f3, text="Valor de $y$").pack(anchor="w")
        self.entry_der_y = ctk.CTkEntry(f3, width=80, placeholder_text="1")
        self.entry_der_y.pack(pady=2)

        f4 = ctk.CTkFrame(form_frame, fg_color="transparent")
        f4.pack(side="left", padx=5, pady=5)
        ctk.CTkLabel(f4, text="Orden / Secuencia").pack(anchor="w")
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
            tab,
            text="Calcular Derivada",
            fg_color="#0284c7",
            hover_color="#0369a1",
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self._calc_derivative,
        )
        btn.pack(fill="x", padx=10, pady=10)

        # Output de alto contraste (Estilo consola verde web)
        self.out_der = ctk.CTkTextbox(
            tab, font=ctk.CTkFont(family="Consolas", size=13), text_color="#4ade80"
        )
        self.out_der.pack(fill="both", expand=True, padx=10, pady=10)

    def _calc_derivative(self):
        expr = self.entry_der_expr.get()
        xv = self.entry_der_x.get()
        yv = self.entry_der_y.get()
        seq = self.combo_seq.get()

        try:
            res, steps = self.engine.evaluate_derivative(expr, xv, yv, seq)
            self.out_der.delete("1.0", "end")
            self.out_der.insert("1.0", steps)
        except Exception as e:
            self.out_der.delete("1.0", "end")
            self.out_der.insert("1.0", f"❌ ERROR DE CÁLCULO: {str(e)}")

    def _setup_integrals_tab(self, tab):
        title = ctk.CTkLabel(
            tab,
            text="Integrales Múltiples (Dobles y Triples)",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#38bdf8",
        )
        title.pack(anchor="w", padx=10, pady=(10, 2))

        form = ctk.CTkFrame(tab, fg_color="#1e293b")
        form.pack(fill="x", padx=10, pady=5)

        # Fila 1
        ctk.CTkLabel(form, text="Función Integrando f(x, y, z):").pack(
            anchor="w", padx=10, pady=2
        )
        self.entry_int_expr = ctk.CTkEntry(
            form, placeholder_text="Ej: x^2 + y^2 + z^2"
        )
        self.entry_int_expr.pack(fill="x", padx=10, pady=2)

        # Limites
        lim_frame = ctk.CTkFrame(form, fg_color="transparent")
        lim_frame.pack(fill="x", padx=5, pady=5)

        self.entry_xa = ctk.CTkEntry(lim_frame, placeholder_text="X Inf (0)", width=100)
        self.entry_xa.pack(side="left", padx=5)
        self.entry_xb = ctk.CTkEntry(lim_frame, placeholder_text="X Sup (1)", width=100)
        self.entry_xb.pack(side="left", padx=5)

        self.entry_ya = ctk.CTkEntry(lim_frame, placeholder_text="Y Inf (0)", width=100)
        self.entry_ya.pack(side="left", padx=5)
        self.entry_yb = ctk.CTkEntry(lim_frame, placeholder_text="Y Sup (1)", width=100)
        self.entry_yb.pack(side="left", padx=5)

        self.entry_za = ctk.CTkEntry(lim_frame, placeholder_text="Z Inf (0)", width=100)
        self.entry_za.pack(side="left", padx=5)
        self.entry_zb = ctk.CTkEntry(lim_frame, placeholder_text="Z Sup (1)", width=100)
        self.entry_zb.pack(side="left", padx=5)

        btn_box = ctk.CTkFrame(tab, fg_color="transparent")
        btn_box.pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(
            btn_box,
            text="Calcular Integral Doble",
            command=self._calc_double_int,
            fg_color="#0284c7",
        ).pack(side="left", expand=True, fill="x", padx=5)
        ctk.CTkButton(
            btn_box,
            text="Calcular Integral Triple",
            command=self._calc_triple_int,
            fg_color="#0d9488",
        ).pack(side="left", expand=True, fill="x", padx=5)

        self.out_int = ctk.CTkTextbox(
            tab, font=ctk.CTkFont(family="Consolas", size=13), text_color="#4ade80"
        )
        self.out_int.pack(fill="both", expand=True, padx=10, pady=10)

    def _calc_double_int(self):
        try:
            res, steps = self.engine.evaluate_double_integral(
                self.entry_int_expr.get(),
                self.entry_xa.get() or "0",
                self.entry_xb.get() or "1",
                self.entry_ya.get() or "0",
                self.entry_yb.get() or "1",
            )
            self.out_int.delete("1.0", "end")
            self.out_int.insert("1.0", steps)
        except Exception as e:
            self.out_int.delete("1.0", "end")
            self.out_int.insert("1.0", f"❌ ERROR: {str(e)}")

    def _calc_triple_int(self):
        try:
            res, steps = self.engine.evaluate_triple_integral(
                self.entry_int_expr.get(),
                self.entry_xa.get() or "0",
                self.entry_xb.get() or "1",
                self.entry_ya.get() or "0",
                self.entry_yb.get() or "1",
                self.entry_za.get() or "0",
                self.entry_zb.get() or "1",
            )
            self.out_int.delete("1.0", "end")
            self.out_int.insert("1.0", steps)
        except Exception as e:
            self.out_int.delete("1.0", "end")
            self.out_int.insert("1.0", f"❌ ERROR: {str(e)}")

    def _setup_graph_tab(self, tab):
        title = ctk.CTkLabel(
            tab,
            text="Aproximación de Límites y Gráfica (Apuntes de Cuaderno)",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#38bdf8",
        )
        title.pack(anchor="w", padx=10, pady=5)

        f = ctk.CTkFrame(tab, fg_color="#1e293b")
        f.pack(fill="x", padx=10, pady=5)

        self.entry_lim_expr = ctk.CTkEntry(
            f, placeholder_text="Ej: (x^4 + y^2 + z^2)/(1 + x^2 + y^2 + z^2)"
        )
        self.entry_lim_expr.pack(
            side="left", fill="x", expand=True, padx=10, pady=10
        )

        ctk.CTkButton(
            f, text="Generar Tabla y Gráfica", command=self._calc_limit_table
        ).pack(side="right", padx=10, pady=10)

        self.out_lim = ctk.CTkTextbox(
            tab, height=180, font=ctk.CTkFont(family="Consolas", size=13), text_color="#4ade80"
        )
        self.out_lim.pack(fill="x", padx=10, pady=5)

        self.plot_box = ctk.CTkFrame(tab)
        self.plot_box.pack(fill="both", expand=True, padx=10, pady=5)

    def _calc_limit_table(self):
        expr = self.entry_lim_expr.get()
        try:
            steps = self.engine.generate_limit_table(expr)
            self.out_lim.delete("1.0", "end")
            self.out_lim.insert("1.0", steps)
            self._render_graph(expr)
        except Exception as e:
            self.out_lim.delete("1.0", "end")
            self.out_lim.insert("1.0", f"❌ ERROR: {str(e)}")

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

    def _setup_notes_tab(self, tab):
        txt = ctk.CTkTextbox(tab, font=ctk.CTkFont(size=13))
        txt.pack(fill="both", expand=True, padx=10, pady=10)

        content = (
            "FORMULARIO Y GUÍA DE APUNTES INTEGRADOS\n\n"
            "1. LÍMITES MULTIVARIABLES Y CONTINUIDAD:\n"
            "   • Se evalúa la tendencia (x,y,z) -> (0,0,0) mediante aproximación.\n"
            "   • Si no se rompe la continuidad y el límite existe, la función es continua.\n\n"
            "2. DERIVADAS PARCIALES Y MIXTAS:\n"
            "   • ∂f/∂x: Se deriva respecto a 'x' tratando 'y' como constante.\n"
            "   • ∂f/∂y: Se deriva respecto a 'y' tratando 'x' como constante.\n"
            "   • ∂²f/(∂x ∂y): Derivada mixta de segundo orden.\n\n"
            "3. INTEGRALES MÚLTIPLES:\n"
            "   • Integrales Dobles: ∬ f(x,y) dy dx\n"
            "   • Integrales Triples: ∭ f(x,y,z) dz dy dx"
        )
        txt.insert("1.0", content)