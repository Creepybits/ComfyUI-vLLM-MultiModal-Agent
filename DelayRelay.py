# ------------------------------------------------------------------
# Created by Creepybits (2026)
# Repository: https://github.com/Creepybits/ComfyUI-vLLM-MultiModal-Agent
# Full Guide: https://zanno.se/guide-run-gemma-4-nvfp4-from-comfyui/
# ------------------------------------------------------------------

import time

class DelayRelay:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "seconds": ("FLOAT", {"default": 1.0, "min": 0.1, "step": 0.1}),
                "text": ("STRING",),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "delay"
    CATEGORY = "Nova/AI"

    def delay(self, seconds, text):
        time.sleep(seconds)
        return (text,)


NODE_CLASS_MAPPINGS = {
      "DelayRelay": DelayRelay,
}

NODE_DISPLAY_NAME_MAPPINGS = {
      "DelayRelay": "Delay Relay (Nova)",
}
