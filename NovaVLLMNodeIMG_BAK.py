import requests
import json
import base64
import torch
import numpy as np
from PIL import Image
from io import BytesIO

class NovaVLLMNodeIMG:
    def __init__(self):
        self.url = "http://localhost:8000/v1/chat/completions"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True}),
                "max_tokens": ("INT", {"default": 1024}),
                "temperature": ("FLOAT", {"default": 0.7}),
            },
            "optional": {
                "image": ("IMAGE",),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "generate"
    CATEGORY = "Nova/AI"

    def generate(self, prompt, max_tokens, temperature, image=None):
        user_content = []

        # Convert ComfyUI image to Base64 for the API
        if image is not None:
            i = 255. * image[0].cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            buffered = BytesIO()
            img.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
            user_content.append({
                "type": "image_url",
                "image_url": {"url": f"data:image/png;base64,{img_str}"}
            })

        # Add the text prompt
        user_content.append({"type": "text", "text": prompt})

        payload = {
            "model": "/mnt/c/AI/Comfy/ComfyUI/models/LLM/cosmicproc/gemma-4-E4B-it-NVFP4",
            "messages": [{"role": "user", "content": user_content}],
            "max_tokens": max_tokens,
            "temperature": temperature
        }

        try:
            response = requests.post(self.url, json=payload)
            response.raise_for_status()
            return (response.json()['choices'][0]['message']['content'],)
        except Exception as e:
            return (f"[Nova Error] Is the server running? Error: {str(e)}",)

NODE_CLASS_MAPPINGS = {"NovaVLLMNodeIMG": NovaVLLMNodeIMG}
NODE_DISPLAY_NAME_MAPPINGS = {"NovaVLLMNodeIMG": "Autonomous Nova (Remote Multi)"}
