from tkinter import *
from tkinter import ttk


class ThemeManager:
    """
    Manages light and dark themes for Tkinter applications.
    """

    def __init__(self):
        self.current_theme = "dark"  # Default theme

    def apply_theme(self, root, theme):
        """
        Applies the specified theme to the given root window and its child widgets.
        """
        self.current_theme = theme
        bg_color, fg_color, button_bg, button_fg = self.get_theme_colors(theme)

        # Apply theme to root window
        root.config(bg=bg_color)

        # Apply theme to child widgets recursively
        self._apply_theme_to_children(root, bg_color, fg_color, button_bg, button_fg)

        # Apply theme to ttk widgets using ttk.Style
        self._apply_ttk_theme(bg_color, fg_color, button_bg, button_fg)

    def toggle_theme(self, root):
        """
        Toggles between light and dark themes.
        """
        new_theme = "dark" if self.current_theme == "light" else "light"
        self.apply_theme(root, new_theme)

    def get_theme_colors(self, theme):
        """
        Returns color settings based on the theme.
        """
        if theme == "dark":
            return "darkblue", "Black", "darkgray", "black"
        else:
            return "white", "black", "lightgray", "black"

    def _apply_theme_to_children(self, widget, bg_color, fg_color, button_bg, button_fg):
        """
        Recursively applies the theme to all Tkinter widgets.
        """
        for child in widget.winfo_children():
            # Skip ttk widgets (handled separately)
            if isinstance(child, (ttk.Combobox, ttk.Button, ttk.Entry, ttk.Label, ttk.Frame)):
                continue

            # Apply background color universally
            if isinstance(child, (ttk.Frame, ttk.grid, ttk.Canvas, ttk.PanedWindow, ttk.LabelFrame)):
                child.config(bg=bg_color)

            # Apply text-based foreground color
            if isinstance(child, (ttk.Button, ttk.Checkbutton, ttk.Radiobutton, ttk.Message)):
                child.config(bg=bg_color, fg=fg_color)

            # Ensure input fields (Entry, Text) have correct colors
            if isinstance(child, ttk.Entry):
                child.config(bg=button_bg, fg=fg_color, insertbackground=fg_color)
            elif isinstance(child, ttk.Text):
                child.config(bg=button_bg, fg=fg_color, insertbackground=fg_color)

            # Apply styling to menu widgets
            if isinstance(child, ttk.Menu):
                child.config(bg=button_bg, fg=fg_color)

            # Apply button-specific colors
            if isinstance(child, (ttk.Label, ttk.Button)):
                child.config(bg=button_bg, fg=button_fg, activebackground=button_bg, activeforeground=button_fg)

            # Recursively apply theme to children
            self._apply_theme_to_children(child, bg_color, fg_color, button_bg, button_fg)


    def _apply_ttk_theme(self, bg_color, fg_color, button_bg, button_fg):
        """
        Applies the theme to ttk widgets using ttk.Style.
        """
        style = ttk.Style()
        style.configure("TCombobox", fieldbackground=bg_color, foreground=fg_color, background=bg_color)
        style.configure("TButton", background=button_bg, foreground=button_fg)
        style.configure("TEntry", fieldbackground=bg_color, foreground=fg_color)

