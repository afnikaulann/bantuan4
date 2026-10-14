import urllib.request
from PIL import Image, ImageDraw, ImageFont
import os

assets_dir = r"c:\Users\ACER\info bantuan malaysia\assets"

# 1. Create testimoni_3.jpg (Siti Aisha - Young Malaysian Female Student holding MYR banknotes)
t3_path = os.path.join(assets_dir, "testimoni_3.jpg")
t3_url = "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=600&q=80"
t3_temp = os.path.join(assets_dir, "temp_t3.jpg")

# 2. Create testimoni_4.jpg (Encik Rosli - Malaysian Father holding MYR banknotes)
t4_path = os.path.join(assets_dir, "testimoni_4.jpg")
t4_url = "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=600&q=80"
t4_temp = os.path.join(assets_dir, "temp_t4.jpg")

def generate_cash_overlay(width=600, height=600):
    cash_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    
    # MYR Banknote colors: RM50 (blue), RM100 (violet/pink), RM20 (orange), RM10 (red)
    notes_info = [
        (10, (-15, (160, 410)), (2, 132, 199, 235), "RM50"),
        (20, (0, (220, 400)), (225, 29, 72, 235), "RM100"),
        (30, (15, (280, 410)), (234, 179, 8, 235), "RM20"),
        (40, (30, (340, 420)), (16, 185, 129, 235), "RM50")
    ]
    
    for _, (angle, pos), color, label in notes_info:
        note_img = Image.new("RGBA", (145, 75), color)
        ndraw = ImageDraw.Draw(note_img)
        ndraw.rectangle([4, 4, 141, 71], outline=(255, 255, 255, 240), width=2)
        ndraw.text((10, 8), "BANK NEGARA", fill=(255, 255, 255, 255))
        ndraw.text((10, 28), "MALAYSIA", fill=(255, 255, 255, 255))
        ndraw.text((95, 38), label, fill=(255, 255, 255, 255))
        
        rotated = note_img.rotate(angle, expand=True)
        cash_layer.paste(rotated, pos, rotated)
        
    return cash_layer

headers = {'User-Agent': 'Mozilla/5.0'}

# Generate Testimoni 3
try:
    req = urllib.request.Request(t3_url, headers=headers)
    with urllib.request.urlopen(req) as response, open(t3_temp, 'wb') as out_file:
        out_file.write(response.read())
    
    img3 = Image.open(t3_temp).convert("RGBA").resize((600, 600))
    cash3 = generate_cash_overlay()
    img3_final = Image.alpha_composite(img3, cash3)
    img3_final.convert("RGB").save(t3_path, "JPEG", quality=95)
    print("Successfully generated testimoni_3.jpg")
except Exception as e:
    print("Error T3:", e)

# Generate Testimoni 4
try:
    req = urllib.request.Request(t4_url, headers=headers)
    with urllib.request.urlopen(req) as response, open(t4_temp, 'wb') as out_file:
        out_file.write(response.read())
    
    img4 = Image.open(t4_temp).convert("RGBA").resize((600, 600))
    cash4 = generate_cash_overlay()
    img4_final = Image.alpha_composite(img4, cash4)
    img4_final.convert("RGB").save(t4_path, "JPEG", quality=95)
    print("Successfully generated testimoni_4.jpg")
except Exception as e:
    print("Error T4:", e)
