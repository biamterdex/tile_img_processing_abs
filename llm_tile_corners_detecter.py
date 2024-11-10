from transformers import BlipProcessor, BlipForConditionalGeneration
from transformers import AutoProcessor, AutoModelForCausalLM
from PIL import Image
import torch
# Use your token here
access_token = "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"

# Load model directly

processor = AutoProcessor.from_pretrained("llava-hf/llava-1.5-7b-hf")
model = AutoModelForCausalLM.from_pretrained("llava-hf/llava-1.5-7b-hf")
# # Load the LLaVA model
# model_name = "liuhaotian/llava-v1.5-7b"
# processor = BlipProcessor.from_pretrained(model_name, use_auth_token=access_token)
# model = BlipForConditionalGeneration.from_pretrained(model_name, use_auth_token=access_token)

def ask_question(image_path, question):
    image = Image.open(image_path).convert("RGB")
    inputs = processor(image, question, return_tensors="pt")

    # Generate answer
    with torch.no_grad():
        output = model.generate(**inputs, max_new_tokens=50)

    answer = processor.decode(output[0], skip_special_tokens=True)
    return answer


# Example usage
image_path = "media/Tiles/tile (1).png"
question = "How many corners are visible in the picture?"
answer = ask_question(image_path, question)
print("Answer:", answer)
