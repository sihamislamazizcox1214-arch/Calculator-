%%writefile main.py
import math
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.label import Label

class ScientificCalculatorApp(App):
    def build(self):
        self.operators = ["/", "*", "+", "-"]
        self.history = []
        self.is_dark_mode = True
        
        main_layout = BoxLayout(orientation="vertical", spacing=8, padding=12)
        
        # ডিসপ্লে স্ক্রিন
        self.solution = TextInput(
            background_color=[0, 0, 0, 1], foreground_color=[1, 1, 1, 1],
            font_size=45, halign="right", readonly=True, multiline=False,
            size_hint_y=0.15
        )
        main_layout.add_widget(self.solution)
        
        # 🌟 নতুন স্পেশাল ফিচার টপ বার (লাইট মোড, হিস্ট্রি, সমীকরণ ও উৎপাদক)
        top_bar = BoxLayout(orientation="horizontal", size_hint_y=0.08, spacing=5)
        
        self.theme_btn = Button(text="☀️ Light", font_size=13, background_color=[0.3, 0.3, 0.3, 1])
        self.theme_btn.bind(on_press=self.toggle_theme)
        
        self.hist_btn = Button(text="🕒 Hist", font_size=13, background_color=[0.3, 0.3, 0.3, 1])
        self.hist_btn.bind(on_press=self.show_history)
        
        self.eq_btn = Button(text="🟰 Eq Solve", font_size=13, background_color=[0.2, 0.5, 0.6, 1])
        self.eq_btn.bind(on_press=self.solve_equation_popup)
        
        self.fac_btn = Button(text="🧬 Factor", font_size=13, background_color=[0.5, 0.3, 0.6, 1])
        self.fac_btn.bind(on_press=self.factorize_popup)
        
        top_bar.add_widget(self.theme_btn)
        top_bar.add_widget(self.hist_btn)
        top_bar.add_widget(self.eq_btn)
        top_bar.add_widget(self.fac_btn)
        main_layout.add_widget(top_bar)
        
        # 📱 আপনার সাজানো গ্রিড লেআউট (৭টি সারি, ৪টি কলাম)
        grid_layout = GridLayout(cols=4, spacing=8, size_hint_y=0.77)
        
        buttons = [
            "sin", "cos", "tan", "log",
            "ln", "√", "x²", "x³",
            "^", "(", ")", ",",
            "7", "8", "9", "/",
            "4", "5", "6", "*",
            "1", "2", "3", "-",
            "Aziz", "0", "=", "+"
        ]
        
        for label in buttons:
            if label in ["sin", "cos", "tan", "log", "ln", "√", "x²", "x³", "^", "(", ")", ","]:
                btn_color = [0.1, 0.5, 0.7, 1]
                f_size = 32
            elif label in self.operators:
                btn_color = [0.9, 0.5, 0, 1]
                f_size = 42
            elif label == "Aziz":
                btn_color = [0.8, 0.2, 0.2, 1]
                f_size = 26
            elif label == "=":
                btn_color = [1, 1, 1, 1]
                f_size = 42
            else:
                btn_color = [0.2, 0.2, 0.2, 1]
                f_size = 32
                
            if label == "=":
                button = Button(text=label, font_size=f_size, background_color=btn_color, color=[0, 0, 0, 1], background_normal='')
                button.bind(on_press=self.on_solution)
            else:
                button = Button(text=label, font_size=f_size, background_color=btn_color)
                button.bind(on_press=self.on_button_press)
                
            grid_layout.add_widget(button)
            
        main_layout.add_widget(grid_layout)
        return main_layout

    # ☀️ ১. লাইট / ডার্ক মোড লজিক
    def toggle_theme(self, instance):
        if self.is_dark_mode:
            self.solution.background_color = [0.9, 0.9, 0.9, 1]
            self.solution.foreground_color = [0, 0, 0, 1]
            self.theme_btn.text = "🌙 Dark"
            self.is_dark_mode = False
        else:
            self.solution.background_color = [0, 0, 0, 1]
            self.solution.foreground_color = [1, 1, 1, 1]
            self.theme_btn.text = "☀️ Light"
            self.is_dark_mode = True

    # 🕒 ২. ক্যালকুলেশন হিস্ট্রি পপ-আপ
    def show_history(self, instance):
        history_text = "\n".join(self.history[-10:]) if self.history else "No history yet!"
        self.show_popup("Calculation History", history_text)

    # 🟰 ৩. ৪ ঘাত পর্যন্ত সমীকরণ সমাধানের মাস্টার লজিক
    def solve_equation_popup(self, instance):
        raw = self.solution.text
        if not raw or "," not in raw:
            self.solution.text = "Enter coefficients separated by comma"
            return
        try:
            coeffs = [float(x) for x in raw.split(",")]
            order = len(coeffs) - 1
            if order < 1 or order > 4 or coeffs[0] == 0:
                self.show_popup("Error", "Invalid Coefficients (1-4 Degree Only)!")
                return
            roots = []
            if order == 1:
                roots.append(-coeffs[1] / coeffs[0])
            elif order == 2:
                a, b, c = coeffs
                d = b**2 - 4*a*c
                if d >= 0:
                    roots.append((-b + math.sqrt(d)) / (2*a))
                    roots.append((-b - math.sqrt(d)) / (2*a))
                else:
                    real = -b / (2*a)
                    imag = math.sqrt(-d) / (2*a)
                    self.show_popup("Complex Roots", f"x1 = {round(real,4)} + {round(imag,4)}i\nx2 = {round(real,4)} - {round(imag,4)}i")
                    return
            else:
                def f(x): return sum(c * (x ** (order - i)) for i, c in enumerate(coeffs))
                def df(x): return sum(c * (order - i) * (x ** (order - i - 1)) for i, c in enumerate(coeffs[:-1]))
                for start in [-100, -10, -1, 0, 1, 10, 100]:
                    x = start
                    for _ in range(100):
                        fx = f(x)
                        dfx = df(x)
                        if abs(dfx) < 1e-12: break
                        nx = x - fx / dfx
                        if abs(nx - x) < 1e-6:
                            val = round(nx, 4)
                            if val not in roots: roots.append(val)
                            break
                        x = nx
            if roots:
                res_text = "\n".join([f"x{i+1} = {r}" for i, r in enumerate(sorted(roots))])
                self.show_popup(f"Degree {order} Result", f"Real Roots:\n\n{res_text}")
            else:
                self.show_popup(f"Degree {order} Result", "No real roots found (Complex)!")
        except Exception:
            self.solution.text = "Format Error!"

    # 🧬 ৪. উৎপাদক বিশ্লেষণ লজিক
    def factorize_popup(self, instance):
        raw = self.solution.text
        if not raw:
            self.solution.text = "Enter Number (eg: 36)"
            return
        try:
            n = int(raw)
            if n <= 0: return
            factors = []
            d = 2
            temp = n
            while d * d <= temp:
                while (temp % d) == 0:
                    factors.append(str(d))
                    temp //= d
                d += 1
            if temp > 1: factors.append(str(temp))
            res = " * ".join(factors)
            self.show_popup("Prime Factors", f"{n} = {res}")
        except Exception:
            self.solution.text = "Integer Only"

    def show_popup(self, title, text):
        content = BoxLayout(orientation="vertical", padding=10)
        content.add_widget(Label(text=text, font_size=18, halign="center"))
        close_btn = Button(text="Close", size_hint_y=0.2, background_color=[0.7, 0.2, 0.2, 1])
        content.add_widget(close_btn)
        popup = Popup(title=title, content=content, size_hint=(0.9, 0.5))
        close_btn.bind(on_press=popup.dismiss)
        popup.open()

    def on_button_press(self, instance):
        current = self.solution.text
        button_text = instance.text
        
        if button_text == "Aziz":
            self.solution.text = ""
        else:
            if "Enter" in current or "ERROR" in current or "Only" in current or "Format" in current:
                current = ""
            if button_text in ["sin", "cos", "tan"]:
                self.solution.text = current + button_text + "("
            elif button_text == "log":
                self.solution.text = current + "log("
            elif button_text == "ln":
                self.solution.text = current + "ln("
            elif button_text == "√":
                self.solution.text = current + "√("
            elif button_text == "x²":
                self.solution.text = current + "²"
            elif button_text == "x³":
                self.solution.text = current + "³"
            else:
                self.solution.text = current + button_text

    def on_solution(self, instance):
        text = self.solution.text
        if not text or "," in text: return
        try:
            raw_input_save = text
            text = text.replace("²", "**2")
            text = text.replace("³", "**3")
            text = text.replace("^", "**")
            text = text.replace("sin(", "math.sin(math.radians(")
            text = text.replace("cos(", "math.cos(math.radians(")
            text = text.replace("tan(", "math.tan(math.radians(")
            text = text.replace("√(", "math.sqrt(")
            text = text.replace("ln(", "math.log(")
            
            open_b = text.count("(")
            close_b = text.count(")")
            if open_b > close_b:
                text += ")" * (open_b - close_b)
            
            if "math.tan(math.radians(90))" in text or "math.tan(math.radians(270))" in text:
                self.solution.text = "Math ERROR"
                return
            
            raw_text = self.solution.text
            if "log(" in raw_text and "," not in raw_text:
                text = text.replace("math.log(", "math.log10(")

            ans = eval(text, {"math": math})
            
            if isinstance(ans, (int, float)):
                ans = round(ans, 4)
            
            # আপনার কাস্টম ফ্র্যাকশন ভ্যালু ট্রিক
            if ans == 1.4142: final_res = "√2"
            elif ans == 1.7321: final_res = "√3"
            elif ans == 2.2361: final_res = "√5"
            elif ans == 2.8284: final_res = "2√2"
            elif ans == 3.4641: final_res = "2√3"
            elif ans == 0.5: final_res = "1/2"
            elif ans == 0.7071: final_res = "√2/2"
            elif ans == 0.866: final_res = "√3/2"
            elif ans == 0.5774: final_res = "1/√3"
            elif ans == int(ans):
                final_res = str(int(ans))
            else:
                final_res = str(ans)
                
            self.solution.text = final_res
            self.history.append(f"{raw_input_save} = {final_res}")
                
        except ZeroDivisionError:
            self.solution.text = "Math ERROR"
        except Exception:
            self.solution.text = "Syntax ERROR"

if __name__ == "__main__":
    ScientificCalculatorApp().run()
