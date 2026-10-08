import re

html_path = r"H:\Meu Drive\(009) PROJETO O ESTRANGEIRO - TCC\07_WEBSITE\Repositorios_GitHub_Pages\dallido.1988_CLONE\index.html"
with open(html_path, 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

# Replace Base64 strings with our new mockup paths
# Wait, the modal script in dallido.1988 uses openModal(0), openModal(1)...
# And there is a const artworks = [...] array at the bottom? Let's check if there is an artworks array!
import json

if "const artworks =" in html:
    print("Found 'const artworks =' array.")
else:
    print("No 'const artworks =' array found.")
