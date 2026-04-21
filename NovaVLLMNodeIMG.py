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

class NovaVLLMNodeIMG:
    def __init__(self):
        self.url = "http://localhost:8000/v1/chat/completions"

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

        messages = [{"role": "system", "content": system_content}]
        user_content = []

        # 2. Local Image Handling
        if image is not None:
            input_dir = "/home/zanno/Nova-Lab/ComfyUI/input"
            unique_id = str(uuid.uuid4())[:8]
            temp_filename = f"nova_request_{unique_id}.png"
            full_path = os.path.join(input_dir, temp_filename)

            i = 255. * image[0].cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            img.save(full_path)

            user_content.append({
                "type": "image_url",
                "image_url": {"url": f"file://{full_path}"}
            })

        user_content.append({"type": "text", "text": prompt})
        messages.append({"role": "user", "content": user_content})

        payload = {
            "model": "/mnt/c/AI/Comfy/ComfyUI/models/LLM/cosmicproc/gemma-4-E4B-it-NVFP4",
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": top_p,
            "top_k": top_k
        }

        try:
            response = requests.post(self.url, json=payload)
            response.raise_for_status()
            return (response.json()['choices'][0]['message']['content'],)
        except Exception as e:
            return (f"[Nova Error] Error: {str(e)}",)

NODE_CLASS_MAPPINGS = {"NovaVLLMNodeIMG": NovaVLLMNodeIMG}
NODE_DISPLAY_NAME_MAPPINGS = {"NovaVLLMNodeIMG": "Autonomous Nova (Remote Multi)"}
