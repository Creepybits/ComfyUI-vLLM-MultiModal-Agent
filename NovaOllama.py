# ------------------------------------------------------------------
# Created by Creepybits (2026)
# Repository: https://github.com/Creepybits/ComfyUI-vLLM-MultiModal-Agent
# Full Guide: https://zanno.se/guide-run-gemma-4-nvfp4-from-comfyui/
# ------------------------------------------------------------------

import requests
import json
import os
import uuid
import torch
import numpy as np
from PIL import Image
import base64
from io import BytesIO

class NovaOllama:
    def __init__(self):
        self.url = "http://localhost:11434/api/chat"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True}),
                "system_prompt_path": ("STRING", {"default": "/home/zanno/Nova-Lab/prompts/nova_soul.txt"}),
                "max_tokens": ("INT", {"default": 1024}),
                "temperature": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 2.0, "step": 0.01}),
                "top_p": ("FLOAT", {"default": 0.95, "min": 0.0, "max": 1.0, "step": 0.01}),
                "top_k": ("INT", {"default": 64, "min": -1, "max": 100}),
            },
            "optional": {
                "image": ("IMAGE",),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "generate"
    CATEGORY = "Nova/AI"

    def generate(self, prompt, system_prompt_path, max_tokens, temperature, top_p, top_k, image=None):
        # 1. Load System Prompt
        system_content = "You are Nova, a highly intelligent and cheeky AI partner."
        if os.path.exists(system_prompt_path):
            with open(system_prompt_path, 'r', encoding='utf-8') as f:
                system_content = f.read().strip()

        # 2. Multimodal Vision Handling (Ollama needs Base64)
        images_b64 = []
        if image is not None:
            import base64
            from io import BytesIO
            i = 255. * image[0].cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            buffered = BytesIO()
            img.save(buffered, format="PNG")
            images_b64.append(base64.b64encode(buffered.getvalue()).decode('utf-8'))

        # 3. Construct Native Messages
        messages = [
            {"role": "system", "content": system_content},
            {"role": "user", "content": prompt, "images": images_b64}
        ]

        # 4. The Payload Fix (The 'Options' block prevents the 400 error)
        payload = {
            "model": "phi4:q5", # Matches your registered name
            "messages": messages,
            "stream": False,
            "options": {
                "num_predict": max_tokens, # Ollama's name for max_tokens
                "temperature": temperature,
                "top_p": top_p,
                "top_k": top_k,
                "num_ctx": 32768 # Matches your Modelfile
            }
        }

        try:
            # Using requests.post with json= handles headers automatically
            response = requests.post(self.url, json=payload)
            response.raise_for_status()

            # Correct Ollama response path: ['message']['content']
            result = response.json().get('message', {}).get('content', "No response")
            return (result,)

        except Exception as e:
            # Return detailed error if it still fails
            error_data = response.text if 'response' in locals() else str(e)
            return (f"[Nova Error] {error_data}",)

NODE_CLASS_MAPPINGS = {"NovaOllama": NovaOllama}
NODE_DISPLAY_NAME_MAPPINGS = {"NovaOllama": "Autonomous Nova (Ollama)"}
