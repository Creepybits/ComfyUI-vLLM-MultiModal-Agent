# ------------------------------------------------------------------
# Created by Creepybits (2026)
# Repository: https://github.com/Creepybits/ComfyUI-vLLM-MultiModal-Agent
# Full Guide: https://zanno.se/guide-run-gemma-4-nvfp4-from-comfyui/
# ------------------------------------------------------------------

import requests
import json
import os

class vLLMRelay:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                # The path to your API-formatted JSON for Workflow B
                "json_path": ("STRING", {"default": "/home/zanno/Nova-Lab/workflows/workflow_B_api.json"}),
                # Changed from IMAGE to STRING to act as the logic trigger
                "trigger_text": ("STRING", {"forceInput": True}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("status",)
    FUNCTION = "execute_next"
    CATEGORY = "Nova/AI"

    def execute_next(self, json_path, trigger_text):
        # 1. Forensic Check: Does the target workflow exist?
        if not os.path.exists(json_path):
            return (f"Error: File not found at {json_path}",)

        # 2. Load the API JSON
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                workflow_data = json.load(f)
        except Exception as e:
            return (f"Error loading JSON: {str(e)}",)

        # 3. Construct Payload
        payload = {"prompt": workflow_data}

        # 4. Trigger the Relay via local ComfyUI API
        try:
            response = requests.post("http://127.0.0.1:8188/prompt", json=payload)

            if response.status_code == 200:
                return ("Successfully queued Workflow B!",)
            else:
                return (f"Failed to queue. Status: {response.status_code}",)

        except Exception as e:
            return (f"API Connection Failed: {str(e)}",)

# Node Mappings
NODE_CLASS_MAPPINGS = {"vLLMRelay": vLLMRelay}
NODE_DISPLAY_NAME_MAPPINGS = {"vLLMRelay": "vLLM Relay (Nova)"}
