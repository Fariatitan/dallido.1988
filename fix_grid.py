import re
import os

html_path = r"H:\Meu Drive\(009) PROJETO O ESTRANGEIRO - TCC\07_WEBSITE\Repositorios_GitHub_Pages\dallido.1988_CLONE\index.html"
with open(html_path, 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

# We need to extract the artworks array from the HTML
# Let's write a small parser or just read the `new_array.js` we generated earlier
js_path = r"H:\Meu Drive\(009) PROJETO O ESTRANGEIRO - TCC\07_WEBSITE\Repositorios_GitHub_Pages\dallido.1988_CLONE\new_array.js"
with open(js_path, 'r', encoding='utf-8') as f:
    js_content = f.read()

# Parse the JS array manually
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

# Now generate the HTML grid content
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

# Replace the innerHTML of <div class="gallery-grid">
grid_pattern = re.compile(r'(<div class="gallery-grid">)(.*?)(</section>)', re.DOTALL)
html = grid_pattern.sub(r'\1\n' + grid_html + r'      </div>\n    \3', html)

# Add an id to the modal so openModal logic can be fixed if needed
# Actually, the existing openModal(index) function should just work if the artworks array is correct.

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Injected {len(artworks)} artworks into the HTML grid.")
