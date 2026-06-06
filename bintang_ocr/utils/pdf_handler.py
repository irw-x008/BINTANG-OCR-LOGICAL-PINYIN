import fitz  # PyMuPDF
import os
from utils.error_logger import log_info, log_error

def convert_pdf_to_images(pdf_path, output_dir="temp_images"):
    images = []
    try:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        pdf_document = fitz.open(pdf_path)
        for page_num in len(pdf_document):
            page = pdf_document.load_page(page_num)
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # Hi-res rendering
            
            img_path = os.path.join(output_dir, f"page_{page_num+1}.jpg")
            pix.save(img_path)
            images.append(img_path)
            
        pdf_document.close()
        log_info(f"Berhasil ekstrak {len(images)} halaman dari PDF")
        return images
    except Exception as e:
        log_error(f"Gagal memproses PDF {pdf_path}: {e}")
        return images
