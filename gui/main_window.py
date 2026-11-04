"""Modulo de Interfaz de Usuario.

Construido con CustomTkinter para un diseno moderno y Matplotlib para plots 2D.
"""

import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

from core.math_engine import MathEngine

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class MainWindow(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.engine = MathEngine()

        self.title("Asistente de Calculo Multivariable")
        self.geometry("1100x750")
        self.minsize(900, 650)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._build_header()
        self._build_form_panel()
        self._build_results_panel()
        
        # Ejecutamos una actualizacion inicial para poblar los placeholders
        self._update_interface_fields("Derivar")

    def _build_header(self):
        header = ctk.CTkFrame(self, corner_radius=0)
        header.grid(
            row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=5
        )
        title = ctk.CTkLabel(
            header,
            text="Asistente de Calculo Multivariable",
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        title.pack(pady=5)

    def _build_form_panel(self):
        form = ctk.CTkFrame(self)
        form.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        # Campo 1: Funcion
        self.lbl_expr = ctk.CTkLabel(form, text="Funcion f(x, y, z):")
        self.lbl_expr.pack(anchor="w", padx=15, pady=(10, 2))
        self.entry_expr = ctk.CTkEntry(form)
        self.entry_expr.pack(fill="x", padx=15, pady=2)

	lbl_hint = ctk.CTkLabel(
            form,
            text="👉 Reglas: Usa '*' para multiplicar (3*x) "
            "y '**' para potencia (x**2)",
            font=ctk.CTkFont(size=11, slate="italic"),
            text_color="#AAAAAA",
        )
        lbl_hint.pack(anchor="w", padx=20, pady=(0, 10))

        # Campo 2: Operacion (Menu Desplegable)
        ctk.CTkLabel(form, text="Operacion:").pack(
            anchor="w", padx=15, pady=(10, 2)
        )
        self.op_var = ctk.StringVar(value="Derivar")
        
        # Agregamos el argumento 'command' para escuchar los cambios de opcion
        self.combo_op = ctk.CTkOptionMenu(
            form,
            values=["Derivar", "Limite", "Integrar"],
            variable=self.op_var,
            command=self._update_interface_fields
        )
        self.combo_op.pack(fill="x", padx=15, pady=2)

        # Campo 3: Variable principal
        self.lbl_var = ctk.CTkLabel(form, text="Variable principal (x, y, z):")
        self.lbl_var.pack(anchor="w", padx=15, pady=(10, 2))
        self.entry_var = ctk.CTkEntry(form)
        self.entry_var.pack(fill="x", padx=15, pady=2)

        # Campo 4: Parametro Inferior / Unico
        self.lbl_p1 = ctk.CTkLabel(form, text="Punto / Orden / Limite Inf (a):")
        self.lbl_p1.pack(anchor="w", padx=15, pady=(10, 2))
        self.entry_param1 = ctk.CTkEntry(form)
        self.entry_param1.pack(fill="x", padx=15, pady=2)

        # Campo 5: Limite Superior (Dinamico)
        self.lbl_p2 = ctk.CTkLabel(
            form, text="Limite Sup (b) [Solo Integrales]:"
        )
        self.lbl_p2.pack(anchor="w", padx=15, pady=(10, 2))
        self.entry_param2 = ctk.CTkEntry(form)
        self.entry_param2.pack(fill="x", padx=15, pady=2)

        btn_calc = ctk.CTkButton(
            form, text="Calcular", command=self._execute_calculation
        )
        btn_calc.pack(fill="x", padx=15, pady=20)

    def _update_interface_fields(self, selected_op: str):
        """Modifica de forma dinamica las etiquetas y auto-pobla los campos."""
        
        # Limpiamos los cuadros de texto antes de insertar los ejemplos automaticos
        self.entry_expr.delete(0, "end")
        self.entry_var.delete(0, "end")
        self.entry_param1.delete(0, "end")
        self.entry_param2.delete(0, "end")

        if selected_op == "Derivar":
            self.lbl_p1.configure(text="Orden de la Derivada (a):")
            self.lbl_p2.configure(text="[Opcion Inactiva para Derivadas]")
            self.entry_param2.configure(state="disabled")
            
            # Auto-poblacion automatica con un ejemplo de derivadas
            self.entry_expr.insert(0, "x**3 * y**2 + cos(x)")
            self.entry_var.insert(0, "x")
            self.entry_param1.insert(0, "2")  # Significa segunda derivada
            
        elif selected_op == "Limite":
            self.lbl_p1.configure(text="Punto de Tendencia (a):")
            self.lbl_p2.configure(text="[Opcion Inactiva para Limites]")
            self.entry_param2.configure(state="disabled")
            
            # Auto-poblacion automatica con un ejemplo de limites
            self.entry_expr.insert(0, "sin(x) / x")
            self.entry_var.insert(0, "x")
            self.entry_param1.insert(0, "0")  # x tiende a 0
            
        elif selected_op == "Integrar":
            self.lbl_p1.configure(text="Limite Inferior (a):")
            self.lbl_p2.configure(text="Limite Superior (b) [Vacio = Indefinida]:")
            self.entry_param2.configure(state="normal")
            
            # Auto-poblacion automatica con un ejemplo de integrales
            self.entry_expr.insert(0, "x**2 + 2*x")
            self.entry_var.insert(0, "x")
            self.entry_param1.insert(0, "1")  # Limite inferior a = 1
            self.entry_param2.insert(0, "3")  # Limite superior b = 3

    def _build_results_panel(self):
        self.res_frame = ctk.CTkFrame(self)
        self.res_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        ctk.CTkLabel(
            self.res_frame,
            text="Procedimiento y Resultado:",
            font=ctk.CTkFont(weight="bold"),
        ).pack(anchor="w", padx=10, pady=5)

        self.txt_output = ctk.CTkTextbox(self.res_frame, height=180)
        self.txt_output.pack(fill="x", padx=10, pady=5)

        self.plot_container = ctk.CTkFrame(self.res_frame)
        self.plot_container.pack(fill="both", expand=True, padx=10, pady=5)

    def _display_error(self, message: str):
        self.txt_output.configure(text_color="#FF5555")
        self.txt_output.delete("1.0", "end")
        self.txt_output.insert("1.0", f"[❌ BAD / ERROR]: {message}")

    def _display_success(self, text: str):
        self.txt_output.configure(text_color="#00DD66")
        self.txt_output.delete("1.0", "end")
        self.txt_output.insert("1.0", text)

    def _execute_calculation(self):
        expr = self.entry_expr.get()
        op = self.op_var.get()
        var = self.entry_var.get() or "x"
        p1 = self.entry_param1.get()
        p2 = self.entry_param2.get()

        try:
            if op == "Derivar":
                order = p1 if p1 else "1"
                res, steps = self.engine.evaluate_derivative(
                    expr, var, order
                )
            elif op == "Limite":
                point = p1 if p1 else "0"
                res, steps = self.engine.evaluate_limit(expr, var, point)
            elif op == "Integrar":
                res, steps = self.engine.evaluate_integral(
                    expr, var, p1, p2
                )
            else:
                raise ValueError("Operacion desconocida.")

            self._display_success(steps)
            self._render_plot(expr)

        except (ValueError, ArithmeticError) as e:
            self._display_error(str(e))
        except Exception as e:
            self._display_error(f"Error inesperado: {str(e)}")

    def _render_plot(self, expr_str: str):
        for widget in self.plot_container.winfo_children():
            widget.destroy()

        if "z" in expr_str.lower():
            lbl = ctk.CTkLabel(
                self.plot_container,
                text="[Grafico 2D omitido: La funcion contiene Z]",
                text_color="#FFA500",
            )
            lbl.pack(expand=True)
            return

        try:
            fig, ax = plt.subplots(figsize=(4, 3), dpi=100)
            x_vals = np.linspace(-10, 10, 200)

            sym_expr = self.engine.parse_expression(expr_str)
            
            if self.engine.y in sym_expr.free_symbols:
                sym_expr = sym_expr.subs(self.engine.y, 1)

            f_num = lambda val: float(
                sym_expr.subs(self.engine.x, val).evalf()
            )
            y_vals = [f_num(v) for v in x_vals]

            ax.plot(x_vals, y_vals, color="#1f77b4")
            ax.set_title("Corte transversal f(x)")
            ax.grid(True, linestyle="--", alpha=0.6)
            fig.tight_layout()

            canvas = FigureCanvasTkAgg(fig, master=self.plot_container)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)

        except Exception:
            lbl = ctk.CTkLabel(
                self.plot_container,
                text="[No se pudo generar la vista previa del grafico]",
                text_color="#FFA500",
            )
            lbl.pack(expand=True)
