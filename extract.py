import re
import base64
import os

html_path = r"H:\Meu Drive\(009) PROJETO O ESTRANGEIRO - TCC\07_WEBSITE\Repositorios_GitHub_Pages\dallido.1988_CLONE\index.html"
out_dir = r"H:\Meu Drive\(009) PROJETO O ESTRANGEIRO - TCC\07_WEBSITE\Repositorios_GitHub_Pages\dallido.1988_CLONE\extracted_images"

os.makedirs(out_dir, exist_ok=True)

with open(html_path, 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

images = re.findall(r'src="data:image/(.*?);base64,(.*?)"', html)
for i, (ext, data) in enumerate(images):
    img_data = base64.b64decode(data)
    with open(os.path.join(out_dir, f'image_{i}.{ext}'), 'wb') as f:
        f.write(img_data)
        
print(f"Extracted {len(images)} images.")
