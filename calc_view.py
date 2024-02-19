import tkinter as tk
from tkinter import ttk
from keypad import Keypad


class View(tk.Tk):
    """View class for the calculator application."""

    NUMPAD = ["CLR", "DEL", "mod", "7", "8", "9", "4", "5", "6", "1", "2", "3", "( )", "0", "."]
    OPERATORS = ["*", "/", "+", "-", "^", "="]
    FUNCTIONS = ["exp", "ln", "log10", "log2", "sqrt"]

    def __init__(self):
        super().__init__()
        self.title("Calculator")
        self.controller = None
        self.history_display = []
        self.history_label = []
        self.history_visible = False

    def set_controller(self, controller):
        """Set the controller for the view."""
        self.controller = controller
        self.init_components()

    def init_components(self):
        """Initialize the GUI components."""
        self.create_history_button()
        self.create_history_area()
        self.create_display()
        self.create_function_selector()
        self.create_keypad()

        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def create_pad(self, keys, columns):
        """Create a keypad with given keys and columns."""
        keypad = Keypad(self, keys, columns=columns)
        keypad.bind('<Button-1>', self.controller.event_handler)
        return keypad

    def create_keypad(self):
        """Create the numeric keypad and operator keypad."""
        number_pad = self.create_pad(self.NUMPAD, columns=3)
        operator_pad = self.create_pad(self.OPERATORS, columns=1)
        number_pad.grid(row=4, column=0, sticky=tk.NSEW)
        operator_pad.grid(row=4, column=1, sticky=tk.NSEW)

    def create_function_selector(self):
        """Create the function selector combobox."""
        function_label = tk.Label(self, text="Functions:", font=("Arial", 14))
        function_label.grid(row=3, column=0, sticky=tk.E)

        self.function_var = tk.StringVar()
        function_combobox = ttk.Combobox(self, textvariable=self.function_var,
                                         values=self.FUNCTIONS, width=3)
        function_combobox.grid(row=3, column=1, sticky=tk.NSEW)
        function_combobox.bind("<<ComboboxSelected>>", self.controller.function_selected)

    def create_display(self):
        """Create the display."""
        self.display_text = tk.StringVar()
        self.display = tk.Label(self, textvariable=self.display_text, height=2,
                                font=("Monospace", 32), background="black",
                                foreground="yellow", anchor=tk.E, justify=tk.RIGHT)
        self.display.grid(row=2, column=0, columnspan=2, sticky=tk.NSEW)

    def create_history_button(self):
        """Create the buttons in history frame."""
        self.history_button_frame = tk.Frame(self)
        self.history_button = tk.Button(self.history_button_frame, text="Show/Hide History",
                                        width=15, height=2, command=self.toggle_history)
        self.history_button.pack(side=tk.LEFT)
        self.clear_history_button = tk.Button(self.history_button_frame, text="Clear History",
                                              width=10, height=2,
                                              command=self.clear_history_display)
        self.clear_history_button.pack(side=tk.LEFT)
        self.history_button_frame.grid(row=0, column=0, sticky=tk.W)

    def create_history_area(self):
        """Create the area for displaying history."""
        self.history_frame = tk.Frame(self)

    def toggle_history(self):
        """Toggle the show/hide of the history area."""
        if self.history_visible:
            self.history_frame.grid_forget()
            self.grid_rowconfigure(1, weight=0)
            self.history_visible = False
        else:
            self.history_frame.grid(row=1, column=0, columnspan=2, sticky=tk.NSEW)
            self.grid_rowconfigure(1, weight=1)
            self.history_frame.grid_propagate(False)
            self.history_visible = True

    def update_history_display(self):
        """Update the history display."""
        history = self.controller.get_history()
        if history:
            for i in history:
                if i not in self.history_display:
                    self.history_text = tk.Label(self.history_frame, text=str(i),font=("Arial", 15),
                                                 background="light gray", height=2,
                                                 anchor=tk.W, justify=tk.LEFT)
                    self.history_text.bind("<Button-1>", self.recall_history)
                    self.history_text.pack(expand=True, fill='both')
                    self.history_display.append(str(i))
                    self.history_label.append(self.history_text)

    def recall_history(self, event):
        """Display recalled history in the display area."""
        text = event.widget["text"]
        input_expression = text.split("=")[0]
        self.controller.error_occurred = False
        self.display.configure(foreground="yellow")
        self.update_display(str(input_expression))

    def clear_history_display(self):
        """Clears the history display area."""
        self.controller.clear_history()
        self.history_frame.destroy()
        self.create_history_area()  # Resize the history frame back to the normal size
        self.history_visible = False
        self.grid_rowconfigure(1, weight=0)

    def update_display(self, text):
        """Update the display screen with the given text."""
        self.display_text.set(text)

    def display_error(self):
        """Change the text to red and make a sound when error occurred."""
        self.display.configure(foreground="red")
        self.bell()

    def run(self):
        """Starts the calculator application."""
        self.mainloop()
