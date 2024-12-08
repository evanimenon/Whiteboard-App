import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
from PIL import Image, ImageDraw

class PaintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Paint with Tkinter")
        self.root.geometry("1000x600")

        self.canvas = tk.Canvas(root, bg="white", width=800, height=600)
        self.canvas.pack(side=tk.LEFT, fill="both", expand=True)

        self.image = Image.new("RGB", (800, 600), "white")
        self.draw = ImageDraw.Draw(self.image)

        self.drawing = False
        self.last_x, self.last_y = None, None
        self.brush_size = 2
        self.brush_color = "black"
        self.last_brush_color = "black" 
        self.mode = "brush" 

        self.history = []
        self.redo_history = []
        self.current_stroke = []

        self.canvas.bind("<ButtonPress-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw_line)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)

        self.create_side_menu()
        self.create_menu()

    def create_side_menu(self):
        side_menu = tk.Frame(self.root, width=200, bg="#1E1E1E")
        side_menu.pack(side=tk.RIGHT, fill="y")

        color_picker_button = tk.Button(side_menu, text="Choose Color", command=self.choose_color)
        color_picker_button.pack(pady=0)

        brush_size_label = tk.Label(side_menu, text="Brush Size")
        brush_size_label.pack(pady=5)
        self.brush_size_slider = tk.Scale(side_menu, from_=1, to=100, orient=tk.HORIZONTAL, command=self.update_brush_size)
        self.brush_size_slider.set(self.brush_size)
        self.brush_size_slider.pack(pady=10)

        self.mode_label = tk.Label(side_menu, text="Mode: Brush")
        self.mode_label.pack(pady=5)
        brush_button = tk.Button(side_menu, text="Brush", command=lambda: self.set_mode("brush"))
        brush_button.pack(pady=5)
        erase_button = tk.Button(side_menu, text="Erase", command=lambda: self.set_mode("erase"))
        erase_button.pack(pady=5)

        save_button = tk.Button(side_menu, text="Save", command=self.save_image)
        save_button.pack(pady=5)
        clear_button = tk.Button(side_menu, text="Clear", command=self.clear_canvas)
        clear_button.pack(pady=5)
        undo_button = tk.Button(side_menu, text="Undo", command=self.undo)
        undo_button.pack(pady=5)
        redo_button = tk.Button(side_menu, text="Redo", command=self.redo)
        redo_button.pack(pady=5)

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Save", command=self.save_image, accelerator="Ctrl+S")
        file_menu.add_command(label="Clear", command=self.clear_canvas, accelerator="Ctrl+C")
        file_menu.add_command(label="Undo", command=self.undo, accelerator="Ctrl+Z")
        file_menu.add_command(label="Redo", command=self.redo, accelerator="Ctrl+Y")

        self.root.bind("<Control-s>", lambda event: self.save_image())
        self.root.bind("<Control-c>", lambda event: self.clear_canvas())
        self.root.bind("<Control-z>", lambda event: self.undo())
        self.root.bind("<Control-y>", lambda event: self.redo())
        self.root.bind("<b>", lambda event: self.set_mode("brush"))
        self.root.bind("<e>", lambda event: self.set_mode("erase"))

    def set_mode(self, mode):
        self.mode = mode
        if mode == "erase":
            self.last_brush_color = self.brush_color 
            self.brush_color = "white"
            self.mode_label.config(text="Mode: Erase")
        else:
            self.brush_color = self.last_brush_color 
            self.mode_label.config(text="Mode: Brush")

    def start_drawing(self, event):
        self.drawing = True
        self.last_x, self.last_y = event.x, event.y
        self.current_stroke = [(self.last_x, self.last_y, self.brush_color, self.brush_size)]

    def draw_line(self, event):
        if self.drawing:
            x, y = event.x, event.y
            self.canvas.create_line(self.last_x, self.last_y, x, y, fill=self.brush_color, width=self.brush_size, capstyle=tk.ROUND, smooth=tk.TRUE, splinesteps=36)
            self.draw.line([self.last_x, self.last_y, x, y], fill=self.brush_color, width=self.brush_size)
            self.last_x, self.last_y = x, y
            self.current_stroke.append((x, y, self.brush_color, self.brush_size))

    def stop_drawing(self, event):
        self.drawing = False
        self.history.append(self.current_stroke)
        self.current_stroke = []
        self.redo_history = []

    def save_image(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")])
        if file_path:
            self.image.save(file_path)

    def clear_canvas(self):
        self.canvas.delete("all")
        self.image = Image.new("RGB", (800, 600), "white")
        self.draw = ImageDraw.Draw(self.image)
        self.history = []
        self.redo_history = []

    def update_brush_size(self, value):
        self.brush_size = int(value)

    def choose_color(self):
        color = colorchooser.askcolor(title="Choose color")[1]
        if color:
            self.brush_color = color
            self.last_brush_color = color 
            if self.mode == "erase":
                self.set_mode("brush")

    def undo(self):
        if self.history:
            last_stroke = self.history.pop()
            self.redo_history.append(last_stroke)
            self.redraw_canvas()

    def redo(self):
        if self.redo_history:
            next_stroke = self.redo_history.pop()
            self.history.append(next_stroke)
            self.redraw_canvas()

    def redraw_canvas(self):
        self.canvas.delete("all")
        self.image = Image.new("RGB", (800, 600), "white")
        self.draw = ImageDraw.Draw(self.image)
        for stroke in self.history:
            for i in range(1, len(stroke)):
                x1, y1, color, size = stroke[i-1]
                x2, y2, _, _ = stroke[i]
                self.canvas.create_line(x1, y1, x2, y2, fill=color, width=size, capstyle=tk.ROUND, smooth=tk.TRUE, splinesteps=36)
                self.draw.line([x1, y1, x2, y2], fill=color, width=size)

if __name__ == "__main__":
    root = tk.Tk()
    app = PaintApp(root)
    root.mainloop()
