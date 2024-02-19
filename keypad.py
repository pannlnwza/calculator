import tkinter as tk


class Keypad(tk.Frame):
    """A class of keypad widget."""
    def __init__(self, parent, keynames=[], columns=1, **kwargs):
        super().__init__(parent, **kwargs)
        self.keynames = keynames
        self.parent = parent
        self.buttons = []
        self.init_components(columns)

    def init_components(self, columns) -> None:
        """Create a keypad of keys using the keynames list.
        The first keyname is at the top left of the keypad and
        fills the available columns left-to-right, adding as many
        rows as needed.
        :param columns: number of columns to use
        """
        for i in range(len(self.keynames)):
            row = i // columns
            col = i % columns
            button = tk.Button(self, text=str(self.keynames[i]),height=2, width=3)
            button.grid(row=row, column=col, sticky=tk.NSEW)
            self.grid_rowconfigure(row, weight=1)
            self.columnconfigure(col, weight=1)
            self.buttons.append(button)

    def bind(self, sequence, handler_function):
        """Bind an event handler to an event sequence."""
        for button in self.buttons:
            button.bind(sequence, handler_function)

    def __setitem__(self, key, value) -> None:
        """Overrides __setitem__ to allow configuration of all buttons
        using dictionary syntax.

        Example: keypad['foreground'] = 'red'
        sets the font color on all buttons to red.
        """
        for button in self.buttons:
            button[key] = value

    def __getitem__(self, key):
        """Overrides __getitem__ to allow reading of configuration values
        from buttons.
        Example: keypad['foreground'] would return 'red' if the button
        foreground color is 'red'.
        """
        value = ""
        for button in self.buttons:
            value = button[key]
        return value

    def configure(self, cnf=None, **kwargs):
        """Apply configuration settings to all buttons.

        To configure properties of the frame that contains the buttons,
        use `keypad.frame.configure()`.
        """
        if cnf:
            self.frame.configure(**cnf)
        elif kwargs:
            for button in self.buttons:
                button.configure(**kwargs)

    @property
    def frame(self):
        """Returns the frame object containing the buttons."""
        return super()
