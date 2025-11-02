from PIL import Image, ImageDraw, ImageFont

# === CONFIGURATION ===
text = "S12 G4 Results: 2nd Beth W, 1st Tammy E"
font_path = "HairyBeard-8M8an.ttf"    # font file in same directory
background_path = "techhoneycomb.jpg"
output_path = "WeeklyResultsscroll.gif"

width, height = 800, 70               # slimmer banner
text_color = (255, 255, 0)    # bright yellow
scroll_speed = 3                      # px per frame (lower = slower)
frame_duration = 50                   # ms per frame (~20 fps)
italic_shear = 0.1763                 # tan(10°) = moderate italic slant

# === PREPARE BACKGROUND ===
bg_src = Image.open(background_path).convert("RGB")
bg_ratio = bg_src.width / bg_src.height
target_ratio = width / height

# Crop to match banner ratio
if bg_ratio > target_ratio:
    new_width = int(bg_src.height * target_ratio)
    left = (bg_src.width - new_width) // 2
    bg_src = bg_src.crop((left, 0, left + new_width, bg_src.height))
else:
    new_height = int(bg_src.width / target_ratio)
    top = (bg_src.height - new_height) // 2
    bg_src = bg_src.crop((0, top, bg_src.width, top + new_height))

bg_frame = bg_src.resize((width, height), resample=Image.LANCZOS)

# Duplicate for seamless scroll
bg_strip = Image.new("RGB", (width * 2, height))
bg_strip.paste(bg_frame, (0, 0))
bg_strip.paste(bg_frame, (width, 0))

# === LOAD FONT FROM LOCAL FILE ===
try:
    font = ImageFont.truetype(font_path, 56)
except OSError as e:
    print("⚠️  Could not load Hairy Beard font:", e)
    font = ImageFont.load_default()

# === DRAW TEXT STRIP ===
draw_img = bg_strip.copy()
draw = ImageDraw.Draw(draw_img)

# Pillow ≥10 uses textbbox()
bbox = draw.textbbox((0, 0), text, font=font)
text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]

spacing = 120
x, y = 0, (height - text_h) // 2

while x < draw_img.width + text_w:
    # Render text to its own layer
    temp = Image.new("RGBA", (text_w, text_h * 2), (255, 255, 255, 0))
    temp_draw = ImageDraw.Draw(temp)
    temp_draw.text((0, 0), text, font=font, fill=text_color)

    # Shear for italic effect (~10°)
    italic_w = int(temp.width + temp.height * italic_shear)
    italic = temp.transform(
        (italic_w, temp.height),
        Image.AFFINE,
        (1, italic_shear, -temp.height * italic_shear / 2, 0, 1, 0),
        resample=Image.BICUBIC,
    )

    # Slight upward nudge to center text visually
    draw_img.paste(italic, (x, y - text_h // 5), italic)
    x += text_w + spacing

# === CREATE FRAMES ===
frames = []
for offset in range(0, width, scroll_speed):
    frame = draw_img.crop((offset, 0, offset + width, height))
    frames.append(frame)

# === SAVE AS GIF ===
frames[0].save(
    output_path,
    save_all=True,
    append_images=frames[1:],
    duration=frame_duration,
    loop=0,
    optimize=True,
)

print(f"✅ GIF saved as: {output_path}")


