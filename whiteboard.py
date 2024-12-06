import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw

class PaintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Paint with Tkinter")
        self.root.geometry("800x600")

        self.canvas = tk.Canvas(root, bg="white")
        self.canvas.pack(fill="both", expand=True)

        self.image = Image.new("RGB", (800, 600), "white")
        self.draw = ImageDraw.Draw(self.image)

        self.drawing = False
        self.last_x, self.last_y = None, None
        self.brush_size = 2
        self.brush_color = "black"

        self.canvas.bind("<ButtonPress-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw_line)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)

        self.create_menu()

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Save", command=self.save_image, accelerator="Ctrl+S")
        file_menu.add_command(label="Clear", command=self.clear_canvas, accelerator="Ctrl+C")

        brush_size_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Brush Size", menu=brush_size_menu)
        brush_size_menu.add_command(label="4px", command=lambda: self.set_brush_size(4))
        brush_size_menu.add_command(label="7px", command=lambda: self.set_brush_size(7))
        brush_size_menu.add_command(label="9px", command=lambda: self.set_brush_size(9))
        brush_size_menu.add_command(label="12px", command=lambda: self.set_brush_size(12))

        brush_color_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Brush Color", menu=brush_color_menu)
        brush_color_menu.add_command(label="Black", command=lambda: self.set_brush_color("black"))
        brush_color_menu.add_command(label="White", command=lambda: self.set_brush_color("white"))
        brush_color_menu.add_command(label="Green", command=lambda: self.set_brush_color("green"))
        brush_color_menu.add_command(label="Yellow", command=lambda: self.set_brush_color("yellow"))
        brush_color_menu.add_command(label="Red", command=lambda: self.set_brush_color("red"))

        self.root.bind("<Control-s>", lambda event: self.save_image())
        self.root.bind("<Control-c>", lambda event: self.clear_canvas())

    def start_drawing(self, event):
        self.drawing = True
        self.last_x, self.last_y = event.x, event.y

    def draw_line(self, event):
        if self.drawing:
            x, y = event.x, event.y
            self.canvas.create_line(self.last_x, self.last_y, x, y, fill=self.brush_color, width=self.brush_size, capstyle=tk.ROUND, smooth=tk.TRUE, splinesteps=36)
            self.draw.line([self.last_x, self.last_y, x, y], fill=self.brush_color, width=self.brush_size)
            self.last_x, self.last_y = x, y

    def stop_drawing(self, event):
        self.drawing = False
        self.last_x, self.last_y = None, None

    def save_image(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")])
        if file_path:
            self.image.save(file_path)

    def clear_canvas(self):
        self.canvas.delete("all")
        self.image = Image.new("RGB", (800, 600), "white")
        self.draw = ImageDraw.Draw(self.image)

    def set_brush_size(self, size):
        self.brush_size = size

    def set_brush_color(self, color):
        self.brush_color = color

if __name__ == "__main__":
    root = tk.Tk()
    app = PaintApp(root)
    root.mainloop()
