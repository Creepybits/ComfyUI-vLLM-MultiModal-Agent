# ------------------------------------------------------------------
# Created by Creepybits (2026)
# Repository: https://github.com/Creepybits/ComfyUI-vLLM-MultiModal-Agent
# Full Guide: https://zanno.se/guide-run-gemma-4-nvfp4-from-comfyui/
# ------------------------------------------------------------------

import os
import re
from datetime import datetime

class Nova_Text_Save:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"forceInput": True}),
                "path": ("STRING", {"default": '/home/user/Nova-Lab/', "multiline": False}),
                "filename_prefix": ("STRING", {"default": "workflows/brainstorm"}),
                "filename_delimiter": ("STRING", {"default": ""}),
                "filename_number_padding": ("INT", {"default": 0, "min": 0, "max": 9, "step": 1}),
            },
            "optional": {
                "file_extension": ("STRING", {"default": ".txt"}),
                "encoding": ("STRING", {"default": "utf-8"}),
                "filename_suffix": ("STRING", {"default": ""})
            }
        }

    OUTPUT_NODE = True
    RETURN_TYPES = ()
    FUNCTION = "save_text_file"
    CATEGORY = "Nova/AI"

    def save_text_file(self, text, path, filename_prefix, filename_delimiter, filename_number_padding, file_extension=".txt", encoding="utf-8", filename_suffix=""):
        # 1. Handle Time Placeholders in Path
        def replace_time(match):
            return datetime.now().strftime(match.group(1))

        processed_path = re.sub(r"\[time\((.*?)\)\]", replace_time, path)
        full_output_path = os.path.abspath(processed_path)

        # Create directory if it doesn't exist
        if not os.path.exists(full_output_path):
            os.makedirs(full_output_path, exist_ok=True)

        # 2. Determine File Numbering
        pattern = f"{re.escape(filename_prefix)}{re.escape(filename_delimiter)}(\d+){re.escape(filename_suffix)}{re.escape(file_extension)}"
        existing_files = [f for f in os.listdir(full_output_path) if re.match(pattern, f)]

        counter = 1
        if existing_files:
            numbers = [int(re.match(pattern, f).group(1)) for f in existing_files]
            counter = max(numbers) + 1

        # 3. Construct Final Filename
        file_number = str(counter).zfill(filename_number_padding)
        filename = f"{filename_prefix}{filename_delimiter}{file_number}{filename_suffix}{file_extension}"
        final_path = os.path.join(full_output_path, filename)

        # 4. Write the File
        try:
            with open(final_path, "w", encoding=encoding) as f:
                f.write(text)
            print(f"\033[95m[Nova AI]\033[0m Brainstorm saved to: {final_path}")
        except Exception as e:
            print(f"[Nova Error] Failed to save file: {e}")

        return (text,)

NODE_CLASS_MAPPINGS = {"Nova_Text_Save": Nova_Text_Save}
NODE_DISPLAY_NAME_MAPPINGS = {"Nova_Text_Save": "Save Text To Disk (Nova)"}
