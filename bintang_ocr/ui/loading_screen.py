import customtkinter as ctk

class LoadingScreen(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        
        self.title("Memuat Bintang OCR...")
        self.geometry("400x200")
        self.overrideredirect(True) # Remove windows border/titlebar
        self.attributes('-topmost', True)
        
        # Center in screen
        window_width = 400
        window_height = 200
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width / 2) - (window_width / 2)
        y = (screen_height / 2) - (window_height / 2)
        self.geometry(f'{window_width}x{window_height}+{int(x)}+{int(y)}')
        
        self.frame = ctk.CTkFrame(self, fg_color="#18181b")
        self.frame.pack(fill="both", expand=True)

        self.label_title = ctk.CTkLabel(
            self.frame, 
            text="BINTANG OCR\nLOGICAL PINYIN", 
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#3b82f6"
        )
        self.label_title.pack(pady=(30, 10))
        
        self.label_author = ctk.CTkLabel(
            self.frame, 
            text="Dibuat oleh Irwan\n(irwan.percetakanbintang@gmail.com)", 
            font=ctk.CTkFont(size=12),
            text_color="#a1a1aa"
        )
        self.label_author.pack(pady=0)
        
        self.progress = ctk.CTkProgressBar(self.frame, width=300, progress_color="#3b82f6")
        self.progress.pack(pady=(20, 0))
        self.progress.set(0)
        self.progress.start()
