import re

html_path = r"H:\Meu Drive\(009) PROJETO O ESTRANGEIRO - TCC\07_WEBSITE\Repositorios_GitHub_Pages\dallido.1988_CLONE\index.html"
with open(html_path, 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

grid_pattern = re.compile(r'(<div class="artwork-frame">\s*<img src=")(data:image/[^>]+)(" alt="[^"]+" loading="lazy" />)')

grid_count = 0
def grid_replacer(match):
    global grid_count
    repl = match.group(1) + f'assets/mockup_{grid_count}.jpg' + match.group(3)
    grid_count += 1
    return repl

html = grid_pattern.sub(grid_replacer, html)

js_pattern = re.compile(r'(image:\s*\')(data:image/[^\']+)((?:\'|"))')

js_count = 0
def js_replacer(match):
    global js_count
    repl = match.group(1) + f'assets/pura_{js_count}.jpeg' + match.group(3)
    js_count += 1
    return repl

html = js_pattern.sub(js_replacer, html)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

print('Replaced HTML grid count:', grid_count)
print('Replaced JS array count:', js_count)
