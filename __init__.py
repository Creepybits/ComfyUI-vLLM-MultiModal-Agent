# ------------------------------------------------------------------
# Created by Creepybits (2026)
# Repository: https://github.com/Creepybits/ComfyUI-vLLM-MultiModal-Agent
# Full Guide: https://zanno.se/guide-run-gemma-4-nvfp4-from-comfyui/
# ------------------------------------------------------------------

from .NovaVLLMNode import NODE_CLASS_MAPPINGS as TEXT_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as TEXT_DISPLAY
from .NovaVLLMNodeIMG import NODE_CLASS_MAPPINGS as IMG_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as IMG_DISPLAY

# Merge the two nodes together
NODE_CLASS_MAPPINGS = {**TEXT_MAPPINGS, **IMG_MAPPINGS}
NODE_DISPLAY_NAME_MAPPINGS = {**TEXT_DISPLAY, **IMG_DISPLAY}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']

print("\033[95m[Nova AI]\033[0m Dual-Node System Loaded (Text + Multimodal).")
