import aiohttp
import asyncio
from core.prompt_injector import get_system_prompt
from utils.config_manager import get_api_key
from utils.error_logger import log_error, log_info

async def call_gemini(base64_img):
    api_key = get_api_key("gemini")
    if not api_key: raise ValueError("GEMINI_API_KEY tidak dikonfigurasi.")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{
            "parts": [
                {"text": get_system_prompt()},
                {"inline_data": {"mime_type": "image/jpeg", "data": base64_img}}
            ]
        }],
        "systemInstruction": {
            "parts": [{"text": get_system_prompt()}]
        }
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload, timeout=60) as resp:
            if resp.status == 200:
                data = await resp.json()
                return data['candidates'][0]['content']['parts'][0]['text']
            else:
                error_msg = await resp.text()
                raise Exception(f"Gemini API Error {resp.status}: {error_msg}")

async def call_openrouter(base64_img, model="qwen/qwen-2.5-vl-7b-instruct:free"):
    api_key = get_api_key("openrouter")
    if not api_key: raise ValueError("OPENROUTER_API_KEY tidak dikonfigurasi.")
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://bintangocr.id",
        "X-Title": "BintangOCR"
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": get_system_prompt()},
            {"role": "user", "content": [
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_img}"}}
            ]}
        ]
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload, timeout=60) as resp:
            if resp.status == 200:
                data = await resp.json()
                return data['choices'][0]['message']['content']
            else:
                error_msg = await resp.text()
                raise Exception(f"OpenRouter Error {resp.status}: {error_msg}")

async def call_groq(base64_img):
    api_key = get_api_key("groq")
    if not api_key: raise ValueError("GROQ_API_KEY tidak dikonfigurasi.")
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama-3.2-11b-vision-preview",
        "messages": [
            {"role": "system", "content": get_system_prompt()},
            {"role": "user", "content": [
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_img}"}}
            ]}
        ]
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload, timeout=60) as resp:
            if resp.status == 200:
                data = await resp.json()
                return data['choices'][0]['message']['content']
            else:
                error_msg = await resp.text()
                raise Exception(f"Groq Error {resp.status}: {error_msg}")

async def call_mistral(base64_img):
    return await call_openrouter(base64_img, model="mistralai/pixtral-12b")

async def call_github(base64_img):
    api_key = get_api_key("github")
    if not api_key: raise ValueError("GITHUB_API_KEY tidak dikonfigurasi.")
    url = "https://models.inference.ai.azure.com/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gpt-4o",
        "messages": [
            {"role": "system", "content": get_system_prompt()},
            {"role": "user", "content": [
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_img}"}}
            ]}
        ]
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload, timeout=60) as resp:
            if resp.status == 200:
                data = await resp.json()
                return data['choices'][0]['message']['content']
            else:
                raise Exception(f"GitHub Error {resp.status}")

async def call_huggingface(base64_img):
    return await call_openrouter(base64_img, model="qwen/qwen-2.5-vl-7b-instruct:free")
