import os
from datetime import datetime
from utils.error_logger import log_info, log_error

def export_to_txt(content, filename_prefix="OCR_Result"):
    try:
        output_dir = "output"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(output_dir, f"{filename_prefix}_{timestamp}.txt")
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
            
        log_info(f"Berhasil export hasil ke {filename}")
        return filename
    except Exception as e:
        log_error(f"Gagal export text: {e}")
        return None
