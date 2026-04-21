# ComfyUI-vLLM-MultiModal-Agent

A high-performance system for integrating multimodal AI agents directly into ComfyUI. This extension utilizes a decoupled architecture, offloading heavy LLM inference to a local [vLLM](https://github.com/vllm-project/vllm) server while maintaining a lightweight interface within ComfyUI.

## Key Features
- **Decoupled Architecture:** Runs the LLM/Vision model in a separate process for maximum stability and VRAM management.
- **High-Speed Vision:** Uses a local-file protocol (`file://`) to bypass Base64 encoding bottlenecks, allowing for near-instant image processing.
- **Agentic Ready:** Designed for complex, system-prompted workflows where the AI acts as an executive engine.

## Prerequisites
This node requires a running vLLM server. To enable the high-speed image protocol, you **must** launch your server with the `--allowed-local-media-path` flag pointing to your ComfyUI input directory:

```bash
python -m vllm.entrypoints.openai.api_server \
--model [YOUR_MODEL_PATH] \
--allowed-local-media-path /path/to/comfyui/input
```
## Installation & Setup

For a detailed step-by-step walkthrough on setting up vLLM with Gemma-4 and these nodes, please refer to the full guide: [Full Setup Guide: Running Gemma-4 NVFP4 in ComfyUI](https://zanno.se/guide-run-gemma-4-nvfp4-from-comfyui/)  

## Credits
Created by [Creepybits](https://zanno.se/).
