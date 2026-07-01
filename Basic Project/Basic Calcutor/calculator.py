import customtkinter as ctk
import math

ctk.set_appearance_mode("dark")


class Calculator(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Calculator")
        self.geometry("500x660")
        self.resizable(False, False)
        self.configure(fg_color="#070D18")

        self.expression = ""

        self.create_ui()
        self.bind_keys()

    def create_ui(self):
        self.display_card = ctk.CTkFrame(
            self,
            height=170,
            corner_radius=24,
            fg_color="#101B2B",
            border_width=1,
            border_color="#344155"
        )
        self.display_card.pack(fill="x", padx=28, pady=(28, 24))
        self.display_card.pack_propagate(False)

        self.expression_label = ctk.CTkLabel(
            self.display_card,
            text="0",
            font=("Segoe UI", 24, "bold"),
            text_color="#93C5FD",
            anchor="w"
        )
        self.expression_label.pack(fill="x", padx=24, pady=(24, 0))

        self.result_label = ctk.CTkLabel(
            self.display_card,
            text="0",
            font=("Segoe UI", 58, "bold"),
            text_color="#F8FAFC",
            anchor="e"
        )
        self.result_label.pack(fill="x", padx=24, pady=(20, 0))

        self.button_frame = ctk.CTkFrame(self, fg_color="#070D18")
        self.button_frame.pack()

        buttons = [
            ["AC", "⌫", "%", "÷"],
            ["7", "8", "9", "×"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["√", "0", ".", "="],
        ]

        for r, row in enumerate(buttons):
            for c, text in enumerate(row):
                self.make_button(text).grid(row=r, column=c, padx=8, pady=8)

        footer = ctk.CTkLabel(
            self,
            text="Built with Python CustomTkinter",
            font=("Segoe UI", 13),
            text_color="#64748B"
        )
        footer.pack(pady=(14, 0))

    def make_button(self, text):
        if text == "=":
            color = "#2563EB"
            hover = "#3B82F6"
            txt = "#FFFFFF"
            border = "#60A5FA"
        elif text in ["÷", "×", "-", "+", "%", "√"]:
            color = "#103743"
            hover = "#155E75"
            txt = "#5EEAD4"
            border = "#0E7490"
        elif text in ["AC", "⌫"]:
            color = "#172437"
            hover = "#263852"
            txt = "#FB7185"
            border = "#334155"
        else:
            color = "#172437"
            hover = "#263852"
            txt = "#F8FAFC"
            border = "#334155"

        return ctk.CTkButton(
            self.button_frame,
            text=text,
            width=95,
            height=72,
            corner_radius=18,
            fg_color=color,
            hover_color=hover,
            border_width=1,
            border_color=border,
            text_color=txt,
            font=("Segoe UI", 27, "bold"),
            command=lambda: self.click(text)
        )

    def set_result(self, value):
        value = str(value)

        if len(value) <= 8:
            font_size = 58
        elif len(value) <= 11:
            font_size = 46
        else:
            font_size = 34

        self.result_label.configure(
            text=value,
            font=("Segoe UI", font_size, "bold")
        )

    def set_expression(self, value):
        value = str(value)

        if len(value) <= 16:
            font_size = 24
        elif len(value) <= 24:
            font_size = 19
        else:
            font_size = 15

        self.expression_label.configure(
            text=value if value else "0",
            font=("Segoe UI", font_size, "bold")
        )

    def click(self, value):
        if value == "AC":
            self.expression = ""
            self.set_expression("0")
            self.set_result("0")

        elif value == "⌫":
            self.expression = self.expression[:-1]
            self.set_expression(self.expression)

        elif value == "=":
            self.calculate()

        elif value == "%":
            try:
                result = float(self.expression) / 100
                self.set_expression(self.expression + "%")
                self.set_result(result)
                self.expression = str(result)
            except:
                self.set_result("Invalid")
                self.expression = ""

        elif value == "√":
            try:
                result = math.sqrt(float(self.expression))
                if result.is_integer():
                    result = int(result)

                self.set_expression("√" + self.expression)
                self.set_result(result)
                self.expression = str(result)
            except:
                self.set_result("Invalid")
                self.expression = ""

        else:
            self.expression += value
            self.set_expression(self.expression)

    def calculate(self):
        try:
            exp = self.expression.replace("×", "*").replace("÷", "/")
            result = eval(exp)

            if isinstance(result, float) and result.is_integer():
                result = int(result)

            self.set_expression(self.expression)
            self.set_result(result)
            self.expression = str(result)

        except ZeroDivisionError:
            self.set_result("Error")
            self.expression = ""
        except:
            self.set_result("Invalid")
            self.expression = ""

    def bind_keys(self):
        self.bind("<Return>", lambda e: self.calculate())
        self.bind("<BackSpace>", lambda e: self.click("⌫"))
        self.bind("<Escape>", lambda e: self.click("AC"))

        for key in "0123456789+-*/.":
            self.bind(key, lambda e, k=key: self.keyboard(k))

    def keyboard(self, key):
        if key == "*":
            key = "×"
        elif key == "/":
            key = "÷"

        self.click(key)


app = Calculator()
app.mainloop()