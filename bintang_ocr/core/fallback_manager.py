import asyncio
from core.ai_handler import call_gemini, call_openrouter, call_groq, call_mistral, call_github, call_huggingface
from utils.error_logger import log_error, log_info

PROVIDERS = [
    {"name": "Gemini (gemini-2.0-flash)", "func": call_gemini},
    {"name": "OpenRouter (qwen-2.5-vl-7b)", "func": call_openrouter},
    {"name": "Groq (llama-3.2-11b-vision)", "func": call_groq},
    {"name": "Mistral (pixtral-12b)", "func": call_mistral},
    {"name": "GitHub (gpt-4o)", "func": call_github},
    {"name": "HuggingFace (qwen-2.5-vl)", "func": call_huggingface}
]

async def process_image_with_fallback(base64_img, manual_provider=None, ui_callback=None):
    providers_to_try = PROVIDERS
    
    if manual_provider and manual_provider != "Auto":
        # Override jika user pilih spesifik provider manual
        selected = next((p for p in PROVIDERS if p["name"].lower().startswith(manual_provider.lower())), None)
        if selected:
            providers_to_try = [selected]

    for index, provider in enumerate(providers_to_try):
        retries = 2
        for attempt in range(retries):
            try:
                if ui_callback:
                    ui_callback(f"Mencoba {provider['name']} (Attempt {attempt+1}/{retries})")
                log_info(f"Menggunakan provider AI: {provider['name']}")
                
                result = await provider["func"](base64_img)
                return result, provider['name']
            
            except Exception as e:
                log_error(f"Provider {provider['name']} gagal: {e}")
                if attempt == retries - 1:
                    log_info(f"Pindah ke fallback selanjutnya.")
                await asyncio.sleep(2) # delay sebelum retry
                
    raise Exception("Semua provider AI Gagal. Periksa Koneksi Internet atau API Key Anda.")
