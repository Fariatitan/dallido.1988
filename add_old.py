from PIL import Image, ImageDraw, ImageFilter
import os
import re

extracted_dir = r"H:\Meu Drive\(009) PROJETO O ESTRANGEIRO - TCC\07_WEBSITE\Repositorios_GitHub_Pages\dallido.1988_CLONE\extracted_images"
out_assets = r"H:\Meu Drive\(009) PROJETO O ESTRANGEIRO - TCC\07_WEBSITE\Repositorios_GitHub_Pages\dallido.1988_CLONE\assets_v2"
js_path = r"H:\Meu Drive\(009) PROJETO O ESTRANGEIRO - TCC\07_WEBSITE\Repositorios_GitHub_Pages\dallido.1988_CLONE\new_array.js"
html_path = r"H:\Meu Drive\(009) PROJETO O ESTRANGEIRO - TCC\07_WEBSITE\Repositorios_GitHub_Pages\dallido.1988_CLONE\index.html"

# Titles for the original 4:
orig_info = [
    ("SEM TITULO - 01", "15 x 15 cm", "OLEO"),
    ("SEM TITULO - 02", "18 x 24 cm", "OLEO"),
    ("ORBITANTE", "10 x 15 cm", "OLEO"),
    ("SEM TITULO", "15 x 15 cm", "OLEO")
]

new_entries = []

for i in range(4):
    f_path = os.path.join(extracted_dir, f"image_{i}.jpeg")
    if not os.path.exists(f_path): continue
    
    # Generate Floating Frame
    img = Image.open(f_path).convert("RGBA")
    img.thumbnail((1000, 1000), Image.Resampling.LANCZOS)
    w, h = img.size
    
    gap = 25
    frame = 15
    framed_w = w + (gap * 2) + (frame * 2)
    framed_h = h + (gap * 2) + (frame * 2)
    
    bg_size = (framed_w + 400, framed_h + 400)
    bg = Image.new("RGBA", bg_size, (250, 250, 248, 255))
    
    frame_color = (15, 15, 15, 255)
    framed_art = Image.new("RGBA", (framed_w, framed_h), frame_color)
    draw_frame = ImageDraw.Draw(framed_art)
    draw_frame.rectangle([frame, frame, framed_w - frame, framed_h - frame], fill=(20, 20, 20, 255))
    
    framed_art.paste(img, (frame + gap, frame + gap), img)
    draw_frame.rectangle([frame + gap, frame + gap, framed_w - frame - gap, framed_h - frame - gap], outline=(255,255,255,30), width=1)
    
    shadow = Image.new("RGBA", bg_size, (0,0,0,0))
    shadow_draw = ImageDraw.Draw(shadow)
    x_offset = (bg_size[0] - framed_w) // 2
    y_offset = (bg_size[1] - framed_h) // 2
    shadow_draw.rectangle([x_offset + 10, y_offset + 20, x_offset + framed_w + 10, y_offset + framed_h + 20], fill=(0,0,0, 80))
    shadow = shadow.filter(ImageFilter.GaussianBlur(25))
    
    bg = Image.alpha_composite(bg, shadow)
    bg.paste(framed_art, (x_offset, y_offset))
    
    out_name = f"ORIGINAL_MOCKUP_{i}.jpg"
    pure_name = f"ORIGINAL_PURA_{i}.jpg"
    
    bg.convert("RGB").save(os.path.join(out_assets, out_name), quality=85)
    img.convert("RGB").save(os.path.join(out_assets, pure_name), quality=85)
    
    new_entries.append({
        'title': orig_info[i][0],
        'technique': "Pintura em Oleo / Canvas Preto",
        'dimensions': orig_info[i][1],
        'src': f"assets_v2/{pure_name}",
        'mockup': f"assets_v2/{out_name}",
        'series': orig_info[i][2]
    })
    print(f"Generated original mockup {i}")

# Now inject these into the HTML and JS array
with open(js_path, 'r', encoding='utf-8') as f:
    js_content = f.read()

# We can append these to the JS array
# First, remove the `];` at the end
js_content = js_content.strip()
if js_content.endswith("];"):
    js_content = js_content[:-2]

for e in new_entries:
    js_content += f"""  {{
    title: "{e['title']}",
    technique: "{e['technique']}",
    dimensions: "{e['dimensions']}",
    src: "{e['src']}",
    mockup: "{e['mockup']}",
    series: "{e['series']}"
  }},\n"""
js_content += "];\n"

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js_content)

# Now rebuild the HTML
# We can re-use the parser from fix_grid.py to rewrite the entire HTML grid to have 32+4 = 36 items.
import re
with open(html_path, 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

artworks = []
matches = re.finditer(r'\{\s*title:\s*"([^"]+)",\s*technique:\s*"([^"]+)",\s*dimensions:\s*"([^"]+)",\s*src:\s*"([^"]+)",\s*mockup:\s*"([^"]+)",\s*series:\s*"([^"]+)"\s*\}', js_content)

for m in matches:
    artworks.append({
        'title': m.group(1),
        'technique': m.group(2),
        'dimensions': m.group(3),
        'src': m.group(4),
        'mockup': m.group(5),
        'series': m.group(6)
    })

grid_html = ""
for i, art in enumerate(artworks):
    grid_html += f"""
        <!-- Obra {i+1:02d} -->
        <article class="artwork-card" onclick="openModal({i})">
          <div class="artwork-frame">
            <img src="{art['mockup']}" alt="{art['title']}" loading="lazy" />
          </div>
          <div class="artwork-meta">
            <h2 class="artwork-title">{art['title']}</h2>
            <span class="artwork-technique">{art['technique']}</span>
            <span class="artwork-dimensions">{art['dimensions']}</span>
          </div>
        </article>
"""

grid_pattern = re.compile(r'(<div class="gallery-grid">)(.*?)(</section>)', re.DOTALL)
html = grid_pattern.sub(r'\1\n' + grid_html + r'      </div>\n    \3', html)

# Also update the const artworks array in the HTML
js_array_pattern = re.compile(r'const artworks = \[.*?\];', re.DOTALL)
html = js_array_pattern.sub(js_content.replace('\\', '\\\\'), html)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("Added old images and rebuilt HTML. Total artworks:", len(artworks))
