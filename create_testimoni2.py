import urllib.request
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

# Create testimoni_2.jpg
# Base portrait of a friendly man wearing a black songkok (peci) and holding Malaysian Ringgit money

assets_dir = r"c:\Users\ACER\info bantuan malaysia\assets"
target_path = os.path.join(assets_dir, "testimoni_2.jpg")

# Download a high quality base photo of a man in songkok / traditional attire or generate composite
url = "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?auto=format&fit=crop&w=600&q=80"
temp_man_path = os.path.join(assets_dir, "temp_man.jpg")

try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response, open(temp_man_path, 'wb') as out_file:
        out_file.write(response.read())
    
    img = Image.open(temp_man_path).convert("RGBA")
    img = img.resize((600, 600))

    draw = ImageDraw.Draw(img)

    # Draw Songkok (Peci) on top of his head
    # Black Velvet Songkok shape: width 260, height 90, top oval shape
    songkok_box = [170, 70, 430, 175]
    draw.rectangle(songkok_box, fill=(15, 20, 30, 255))
    draw.ellipse([170, 60, 430, 100], fill=(25, 30, 45, 255))
    # Gold thread trim accent on songkok
    draw.line([(170, 170), (430, 170)], fill=(212, 175, 55, 255), width=4)

    # Draw Malaysian Ringgit Cash Notes (RM50 blue & RM100 green/violet notes) in lower hands area
    # Fan of Ringgit Notes
    notes_color = [(2, 132, 199, 230), (16, 185, 129, 230), (225, 29, 72, 230), (234, 179, 8, 230)]
    
    # Create an overlay layer for cash notes
    cash_layer = Image.new("RGBA", (600, 600), (0, 0, 0, 0))
    cash_draw = ImageDraw.Draw(cash_layer)

    # Draw 4 fan notes
    angles_and_pos = [
        (-20, (180, 420)),
        (-5, (230, 410)),
        (10, (280, 410)),
        (25, (330, 420))
    ]

    for idx, (angle, pos) in enumerate(angles_and_pos):
        note_img = Image.new("RGBA", (140, 70), notes_color[idx])
        ndraw = ImageDraw.Draw(note_img)
        ndraw.rectangle([4, 4, 136, 66], outline=(255, 255, 255, 230), width=2)
        ndraw.text((10, 10), "BANK NEGARA", fill=(255, 255, 255, 255))
        ndraw.text((10, 30), "MALAYSIA", fill=(255, 255, 255, 255))
        ndraw.text((90, 35), "RM50" if idx % 2 == 0 else "RM100", fill=(255, 255, 255, 255))
        
        # Rotate note
        rotated_note = note_img.rotate(angle, expand=True)
        cash_layer.paste(rotated_note, pos, rotated_note)

    # Combine cash layer onto image
    img = Image.alpha_composite(img, cash_layer)
    
    # Save as JPEG
    img.convert("RGB").save(target_path, "JPEG", quality=95)
    print("Successfully created testimoni_2.jpg")

except Exception as e:
    print("Error creating composite image:", e)
