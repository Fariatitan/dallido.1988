from PIL import Image, ImageDraw, ImageFilter
import os

in_dir = r"H:\Meu Drive\(009) PROJETO O ESTRANGEIRO - TCC\07_WEBSITE\Repositorios_GitHub_Pages\dallido.1988_CLONE\extracted_images"
out_dir = r"H:\Meu Drive\(009) PROJETO O ESTRANGEIRO - TCC\07_WEBSITE\Repositorios_GitHub_Pages\dallido.1988_CLONE\mockups"
os.makedirs(out_dir, exist_ok=True)

for i in range(4):
    try:
        # Load the original painting
        img = Image.open(os.path.join(in_dir, f'image_{i}.jpeg')).convert("RGBA")
        
        # Calculate dimensions for the mockup
        # Let's make a standard gallery wall background: 2000x2000
        bg_size = (2000, 2000)
        bg = Image.new("RGBA", bg_size, (248, 248, 245, 255)) # off-white wall
        
        # Resize artwork to fit beautifully in the center (e.g., max 1000px)
        img.thumbnail((1000, 1000), Image.Resampling.LANCZOS)
        w, h = img.size
        
        # Passepartout (Matting) thickness
        mat_thick = 150
        
        # Frame thickness
        frame_thick = 30
        
        # Total framed size
        framed_w = w + (mat_thick * 2) + (frame_thick * 2)
        framed_h = h + (mat_thick * 2) + (frame_thick * 2)
        
        # Create the frame and matting layer
        framed_art = Image.new("RGBA", (framed_w, framed_h), (25, 25, 25, 255)) # Dark wood / black frame
        
        # Matting layer
        matting = Image.new("RGBA", (w + mat_thick*2, h + mat_thick*2), (250, 250, 250, 255))
        
        # Add a subtle inner shadow/depth to the matting where it meets the art
        # (We skip complex shadows for now and just use a thin dark line)
        draw = ImageDraw.Draw(matting)
        draw.rectangle([mat_thick-2, mat_thick-2, mat_thick+w+1, mat_thick+h+1], outline=(200, 200, 200, 255), width=2)
        
        # Paste art onto matting
        matting.paste(img, (mat_thick, mat_thick), img)
        
        # Paste matting onto frame
        framed_art.paste(matting, (frame_thick, frame_thick))
        
        # Drop shadow for the framed art on the wall
        # Create a shadow layer slightly larger
        shadow = Image.new("RGBA", bg_size, (0,0,0,0))
        shadow_draw = ImageDraw.Draw(shadow)
        
        x_offset = (bg_size[0] - framed_w) // 2
        y_offset = (bg_size[1] - framed_h) // 2
        
        # Draw shadow rectangle
        shadow_draw.rectangle([x_offset + 20, y_offset + 40, x_offset + framed_w + 20, y_offset + framed_h + 40], fill=(0,0,0, 60))
        
        # Blur the shadow
        shadow = shadow.filter(ImageFilter.GaussianBlur(30))
        
        # Composite wall + shadow
        bg = Image.alpha_composite(bg, shadow)
        
        # Composite framed art onto wall
        bg.paste(framed_art, (x_offset, y_offset))
        
        # Save mockup
        final = bg.convert("RGB")
        final.save(os.path.join(out_dir, f'mockup_{i}.jpg'), quality=85)
        print(f"Mockup {i} generated successfully.")
    except Exception as e:
        print(f"Error on {i}: {e}")
