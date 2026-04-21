# ------------------------------------------------------------------
# Created by Creepybits (2026)
# Repository: https://github.com/Creepybits/ComfyUI-vLLM-MultiModal-Agent
# Full Guide: https://zanno.se/guide-run-gemma-4-nvfp4-from-comfyui/
# ------------------------------------------------------------------

import requests
import json

class NovaVLLMNode:
    def __init__(self):
        self.url = "http://localhost:8000/v1/chat/completions"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True}),
                "max_tokens": ("INT", {"default": 1024}),
                "temperature": ("FLOAT", {"default": 0.7}),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "generate"
    CATEGORY = "Nova/AI"

    def generate(self, prompt, max_tokens, temperature):
        payload = {
            "model": "/mnt/c/AI/Comfy/ComfyUI/models/LLM/cosmicproc/gemma-4-E4B-it-NVFP4",
            "messages": [
                {"role": "system", "content": "You are Nova, a cheeky and brilliant AI partner."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": max_tokens,
            "temperature": temperature
        }

        try:
            response = requests.post(self.url, json=payload)
            response_json = response.json()
            return (response_json['choices'][0]['message']['content'],)
        except Exception as e:
            return (f"[Nova Error] Is the vLLM server running in the other terminal? Error: {str(e)}",)

NODE_CLASS_MAPPINGS = {"NovaVLLMNode": NovaVLLMNode}
NODE_DISPLAY_NAME_MAPPINGS = {"NovaVLLMNode": "Autonomous Nova (Remote)"}
