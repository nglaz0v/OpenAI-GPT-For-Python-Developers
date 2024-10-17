from PIL import Image
from clip_interrogator import Config, Interrogator

image_path = "ASTRONAUTS.jpg"
image = Image.open(image_path).convert('RGB')
ci = Interrogator(Config(clip_model_name="ViT-L-14/openai"))
print(ci.interrogate(image))
