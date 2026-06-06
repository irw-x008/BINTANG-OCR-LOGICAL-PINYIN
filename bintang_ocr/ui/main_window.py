import customtkinter as ctk
import tkinter.filedialog as fd
import threading
import asyncio
from ui.image_editor import ImageEditorFrame
from ui.history_panel import HistoryPanel
from utils.image_processor import compress_and_encode_image
from utils.file_exporter import export_to_txt
from core.fallback_manager import process_image_with_fallback
import os

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("BINTANG OCR LOGICAL PINYIN")
        self.geometry("1100x700")

        # Layout Main Frame
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ================= PANEL KIRI (Kontrol) =================
        self.left_panel = ctk.CTkFrame(self, width=280, corner_radius=0)
        self.left_panel.grid(row=0, column=0, sticky="nsew")
        self.left_panel.grid_rowconfigure(6, weight=1)

        self.logo_label = ctk.CTkLabel(self.left_panel, text="BINTANG OCR", font=ctk.CTkFont(size=22, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.btn_select = ctk.CTkButton(self.left_panel, text="Pilih Gambar (.jpg/png)", command=self.select_files)
        self.btn_select.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        # Provider Dropdown
        self.lbl_provider = ctk.CTkLabel(self.left_panel, text="Model AI:")
        self.lbl_provider.grid(row=2, column=0, padx=20, pady=(10, 0), sticky="w")
        
        self.provider_var = ctk.StringVar(value="Auto")
        self.provider_combo = ctk.CTkComboBox(self.left_panel, variable=self.provider_var, 
                                              values=["Auto", "Gemini", "OpenRouter", "Groq", "Mistral", "HuggingFace"])
        self.provider_combo.grid(row=3, column=0, padx=20, pady=(0, 10), sticky="ew")

        self.btn_process = ctk.CTkButton(self.left_panel, text="Proses OCR", command=self.start_processing_thread, fg_color="#10b981", hover_color="#059669")
        self.btn_process.grid(row=4, column=0, padx=20, pady=10, sticky="ew")

        self.status_label = ctk.CTkLabel(self.left_panel, text="Status: Menunggu File", text_color="#a1a1aa", wraplength=240)
        self.status_label.grid(row=5, column=0, padx=20, pady=5)

        self.history_panel = HistoryPanel(self.left_panel)
        self.history_panel.grid(row=6, column=0, padx=10, pady=10, sticky="nsew")

        # ================= PANEL KANAN (Editor & Hasil) =================
        self.right_panel = ctk.CTkFrame(self)
        self.right_panel.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.right_panel.grid_rowconfigure(0, weight=1)
        self.right_panel.grid_columnconfigure(0, weight=1)
        self.right_panel.grid_columnconfigure(1, weight=1)

        # Image Editor / Preview
        self.editor = ImageEditorFrame(self.right_panel)
        self.editor.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # Text Output
        self.text_output = ctk.CTkTextbox(self.right_panel, font=ctk.CTkFont(family="Consolas", size=14), wrap="word")
        self.text_output.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        self.btn_export = ctk.CTkButton(self.right_panel, text="Export ke TXT", command=self.export_result)
        self.btn_export.grid(row=1, column=1, pady=10, sticky="e", padx=5)

        self.selected_files = []

    def select_files(self):
        files = fd.askopenfilenames(title="Pilih File", filetypes=[("Images", "*.png *.jpg *.jpeg *.bmp")])
        if files:
            self.selected_files = list(files)
            if self.selected_files[0].lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                self.editor.load_image(self.selected_files[0])
            self.status_label.configure(text=f"{len(files)} file dipilih")

    def update_status(self, msg):
        self.status_label.configure(text=f"Status: {msg}")
        self.update_idletasks()

    def start_processing_thread(self):
        if not self.selected_files:
            self.update_status("Error: Tidak ada file dipilih")
            return
        
        self.btn_process.configure(state="disabled")
        threading.Thread(target=self.run_async_process, daemon=True).start()

    def run_async_process(self):
        try:
            # Compat mode Win7/asyncio
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.process_files())
        except Exception as e:
            self.update_status(f"Error: {str(e)}")
        finally:
            self.btn_process.configure(state="normal")
            loop.close()

    async def process_files(self):
        provider_choice = self.provider_var.get()
        
        for file in self.selected_files:
            filename = os.path.basename(file)
            self.update_status(f"Pre-processing {filename}...")
            
            base64_img = compress_and_encode_image(file)
            if not base64_img:
                self.history_panel.add_record(filename, "Failed (Img)")
                continue

            self.update_status("Mengirim ke AI (Tahap 1, 2, 3)...")
            try:
                result, used_provider = await process_image_with_fallback(base64_img, provider_choice, self.update_status)
                
                # Update UI safely
                self.text_output.delete("1.0", "end")
                self.text_output.insert("end", result)
                self.update_status(f"Selesai (Oleh: {used_provider})")
                self.history_panel.add_record(filename, "Success")
                
            except Exception as e:
                self.update_status(f"Gagal Total: {str(e)}")
                self.history_panel.add_record(filename, "Failed")

    def export_result(self):
        content = self.text_output.get("1.0", "end-1c")
        if content.strip():
            filepath = export_to_txt(content)
            if filepath:
                self.update_status(f"Diekspor ke {os.path.basename(filepath)}")
