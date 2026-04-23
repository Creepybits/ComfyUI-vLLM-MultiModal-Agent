# ------------------------------------------------------------------
# Created by Creepybits (2026)
# Repository: https://github.com/Creepybits/ComfyUI-vLLM-MultiModal-Agent
# Full Guide: https://zanno.se/guide-run-gemma-4-nvfp4-from-comfyui/
# ------------------------------------------------------------------

import os
import io

class NovaBrainstormloader:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "file_path": ("STRING", {"default": '', "multiline": False}),
                "dictionary_name": ("STRING", {"default": '[filename]', "multiline": False}),
            }
        }
    
    RETURN_TYPES = ("STRING", "DICT")
    FUNCTION = "load_file"
    CATEGORY = "Nova/AI"

    def load_file(self, file_path='', dictionary_name='[filename]'):
        if not os.path.exists(file_path):
            print(f"[Nova Error] The path `{file_path}` specified cannot be found.")
            return ('', {dictionary_name: []})

        filename = ( os.path.basename(file_path).split('.', 1)[0]
            if '.' in os.path.basename(file_path) else os.path.basename(file_path) )

        if dictionary_name != '[filename]':
            filename = dictionary_name

        with open(file_path, 'r', encoding="utf-8", newline='\n') as file:
            text = file.read()

        # Simplified the parsing logic to be standard Python
        lines = []
        for line in io.StringIO(text):
            clean_line = line.strip()
            if clean_line and not clean_line.startswith('#'):
                lines.append(clean_line)

        dictionary = {filename: lines}
        return ("\n".join(lines), dictionary)

NODE_CLASS_MAPPINGS = {"NovaBrainstormloader": NovaBrainstormloader}
NODE_DISPLAY_NAME_MAPPINGS = {"NovaBrainstormloader": "Load Brainstorm (Nova)"}
