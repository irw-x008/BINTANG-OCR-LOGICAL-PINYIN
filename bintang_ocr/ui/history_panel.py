import customtkinter as ctk
import json
import os
from datetime import datetime

class HistoryPanel(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.label = ctk.CTkLabel(self, text="Riwayat Proses", font=ctk.CTkFont(size=14, weight="bold"))
        self.label.pack(pady=10)
        
        self.scrollable_frame = ctk.CTkScrollableFrame(self)
        self.scrollable_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.history_file = "history.json"
        self.load_history()
        
    def load_history(self):
        # Clear existing
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
            
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for item in reversed(data): # Terbaru di atas
                        self.add_item_to_ui(item)
            except Exception as e:
                from utils.error_logger import log_error
                log_error(f"Gagal memuat history.json: {e}")
                
    def add_item_to_ui(self, item):
        frame = ctk.CTkFrame(self.scrollable_frame)
        frame.pack(fill="x", pady=2, padx=2)
        
        lbl_time = ctk.CTkLabel(frame, text=item.get('time', ''), font=ctk.CTkFont(size=10))
        lbl_time.pack(side="top", anchor="w", padx=5)
        
        lbl_file = ctk.CTkLabel(frame, text=item.get('filename', ''), width=150, anchor="w")
        lbl_file.pack(side="left", padx=5)
        
        status_color = "#22c55e" if item.get('status') == "Success" else "#ef4444"
        lbl_status = ctk.CTkLabel(frame, text=item.get('status', ''), text_color=status_color)
        lbl_status.pack(side="right", padx=5)

    def add_record(self, filename, status):
        record = {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "filename": os.path.basename(filename),
            "status": status
        }
        data = []
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except: pass
            
        data.append(record)
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(data[-50:], f, indent=4) # Keep last 50 only
        self.load_history()
