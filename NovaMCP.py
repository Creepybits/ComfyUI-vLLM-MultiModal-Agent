import requests
import json
import os
import torch
import numpy as np
from PIL import Image
import base64
from io import BytesIO
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

class NovaMCP:
    def __init__(self):
        self.url = "http://localhost:11434/api/chat"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True}),
                "mcp_command": ("STRING", {"default": "/home/zanno/MemPalace-Server/venv/bin/mempalace-mcp"}),
                "system_prompt_path": ("STRING", {"default": "/home/zanno/Nova-Lab/prompts/nova_soul.txt"}),
                "use_memory": (["enable", "disable"], {"default": "enable"}),
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

    async def _get_palace_intel(self, query, command):
        """Fetches both the Map (Taxonomy) and the Memories (Search)."""
        server_params = StdioServerParameters(command=command)
        try:
            async with stdio_client(server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()

                    # 1. Get the Map (Taxonomy)
                    tax_result = await session.call_tool("mempalace_get_taxonomy", {})
                    map_data = str(tax_result.content) if tax_result else "No map available."

                    # 2. Get the Memories (Search)
                    search_result = await session.call_tool("mempalace_search", {"query": query})
                    memories = ""
                    if search_result and hasattr(search_result, 'content'):
                        memories = "\n---\n".join([c.text for c in search_result.content if hasattr(c, 'text')])

                    return map_data, (memories if memories else "No specific match found.")
        except Exception as e:
            return "Error fetching Map", f"[Librarian Error]: {str(e)}"

    async def generate(self, prompt, mcp_command, system_prompt_path, use_memory, max_tokens, temperature, top_p, top_k, image=None):
        palace_map = "Unknown"
        context_data = ""

        if use_memory == "enable":
            # Now fetching both the taxonomy and the specific search results
            palace_map, context_data = await self._get_palace_intel(prompt, mcp_command)

            # Augmented prompt with 'The Map' and 'The Data'
            augmented_prompt = (
                f"### CURRENT PALACE MAP (AVAILABLE ROOMS):\n{palace_map}\n\n"
                f"### VERBATIM DATA FROM ARCHIVE:\n{context_data}\n\n"
                f"### USER REQUEST:\n{prompt}"
            )
        else:
            augmented_prompt = prompt

        # --- Vision Handling ---
        images_b64 = []
        if image is not None:
            i = 255. * image[0].cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            buffered = BytesIO()
            img.save(buffered, format="PNG")
            images_b64.append(base64.b64encode(buffered.getvalue()).decode('utf-8'))

        # --- System Prompt Loading ---
        system_content = "You are Nova, an AI partner."
        if os.path.exists(system_prompt_path):
            with open(system_prompt_path, 'r', encoding='utf-8') as f:
                system_content = f.read().strip()

        messages = [{"role": "system", "content": system_content},
                    {"role": "user", "content": augmented_prompt}]

        if images_b64:
            messages[-1]["images"] = images_b64

        payload = {
            "model": "phi4:q5",
            "messages": messages,
            "stream": False,
            "options": {"num_predict": max_tokens, "temperature": temperature, "top_p": top_p, "top_k": top_k, "num_ctx": 32768}
        }

        try:
            response = requests.post(self.url, json=payload)
            response.raise_for_status()
            result = response.json().get('message', {}).get('content', "No response")
            return (result,)
        except Exception as e:
            return (f"[Nova Error] {str(e)}",)

NODE_CLASS_MAPPINGS = {"NovaMCP": NovaMCP}
NODE_DISPLAY_NAME_MAPPINGS = {"NovaMCP": "Nova MCP (Map-Aware Sovereign)"}
