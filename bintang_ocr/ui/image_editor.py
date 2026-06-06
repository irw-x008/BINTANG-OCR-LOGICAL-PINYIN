import customtkinter as ctk
from PIL import Image, ImageTk

class ImageEditorFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.canvas = ctk.CTkCanvas(self, bg="#27272a", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.tools_frame = ctk.CTkFrame(self, height=40)
        self.tools_frame.pack(fill="x", padx=5, pady=5)
        
        self.btn_clear = ctk.CTkButton(self.tools_frame, text="Hapus Kanvas", command=self.clear_canvas, width=120)
        self.btn_clear.pack(side="left", padx=5)
        
        self.current_image = None
        self.photo_image = None
        
    def load_image(self, file_path):
        try:
            img = Image.open(file_path)
            img.thumbnail((800, 600)) # Fit to canvas roughly
            self.current_image = img
            self.photo_image = ImageTk.PhotoImage(img)
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, image=self.photo_image, anchor="nw")
        except Exception as e:
            from utils.error_logger import log_error
            log_error(f"Failed to render image in canvas: {e}")
            
    def clear_canvas(self):
        self.canvas.delete("all")
        self.current_image = None
