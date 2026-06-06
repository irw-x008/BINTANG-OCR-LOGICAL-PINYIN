from PIL import Image, ImageEnhance
import base64
import io
import os

def compress_and_encode_image(image_path, max_size=(1024, 1024)):
    try:
        if not os.path.exists(image_path):
            raise FileNotFoundError("Image file not found.")
            
        with Image.open(image_path) as img:
            # Konversi ke RGB (menghindari error untuk PNG transparent)
            if img.mode != "RGB":
                img = img.convert("RGB")
            
            # Resize dengan antialiasing
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # Enhance sedikit untuk kejelasan teks OCR
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(1.2)
            
            # Simpan ke memori sebagai JPEG
            buffered = io.BytesIO()
            img.save(buffered, format="JPEG", quality=85)
            
            return base64.b64encode(buffered.getvalue()).decode("utf-8")
    except Exception as e:
        from utils.error_logger import log_error
        log_error(f"Gagal memproses gambar {image_path}: {e}")
        return None
