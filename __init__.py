# ------------------------------------------------------------------
# Created by Creepybits (2026)
# Repository: https://github.com/Creepybits/ComfyUI-vLLM-MultiModal-Agent
# Full Guide: https://zanno.se/guide-run-gemma-4-nvfp4-from-comfyui/
# ------------------------------------------------------------------

from .NovaVLLMNode import NODE_CLASS_MAPPINGS as VLLM_TEXT_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as VLLM_TEXT_DISPLAY
from .NovaVLLMNodeIMG import NODE_CLASS_MAPPINGS as VLLM_IMG_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as VLLM_IMG_DISPLAY
from .NovaOllama import NODE_CLASS_MAPPINGS as OLLAMA_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as OLLAMA_DISPLAY
from .vLLMRelay import NODE_CLASS_MAPPINGS as vLLMRelay_NODE_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as vLLMRelay_NODE_DISPLAY
from .Nova_Text_Save import NODE_CLASS_MAPPINGS as Nova_Text_Save_NODE_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as Nova_Text_Save_NODE_DISPLAY
from .DelayRelay import NODE_CLASS_MAPPINGS as DelayRelay_NODE_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as DelayRelay_NODE_DISPLAY
from .NovaBrainstormloader import NODE_CLASS_MAPPINGS as NovaBrainstormloader_NODE_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as NovaBrainstormloader_NODE_DISPLAY

# Merge ALL THREE nodes together
NODE_CLASS_MAPPINGS = {
    **VLLM_TEXT_MAPPINGS,
    **VLLM_IMG_MAPPINGS,
    **OLLAMA_MAPPINGS,
    **vLLMRelay_NODE_MAPPINGS,
    **Nova_Text_Save_NODE_MAPPINGS,
    **DelayRelay_NODE_MAPPINGS,
    **NovaBrainstormloader_NODE_MAPPINGS
}

NODE_DISPLAY_NAME_MAPPINGS = {
    **VLLM_TEXT_DISPLAY,
    **VLLM_IMG_DISPLAY,
    **OLLAMA_DISPLAY,
    **vLLMRelay_NODE_DISPLAY,
    **Nova_Text_Save_NODE_DISPLAY,
    **DelayRelay_NODE_DISPLAY,
    **NovaBrainstormloader_NODE_DISPLAY
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']

print("\033[95m[Nova AI]\033[0m Triple-Node System Loaded (Text + Multimodal + Ollama).")
