from PIL import ImageTk, Image

def readImage(path, size):
    return ImageTk.PhotoImage(Image.open(path).resize(size, Image.Resampling.LANCZOS))

def centerWindow(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = int((screen_width // 2) - (width // 2))
    y = int((screen_height // 2) - (height // 2))
    window.geometry(f'{width}x{height}+{x}+{y}')