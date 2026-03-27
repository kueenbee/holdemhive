# == in Power Shell window...
# === cd C:\Users\kconheady\TD-DS\Data\saves\'K$BHEH'\'K$BHEHive-AdminFiles'\website\scrollingGIFs
# == py WeeklyResultsScrollingGIF.py

from PIL import Image, ImageDraw, ImageFont

# === CONFIGURATION ===
text = "  S14 G4 Results: 4th Amelia H, 3rd Vince A, 2nd Kay C~~, 1st Beth W*"
font_path = "HairyBeard-8M8an.ttf"    # font file in same directory
output_path = "WeeklyGameResultsScroll.gif"

width, height = 600, 33                # banner size
text_color = (255, 255, 0)             # bright yellow
scroll_speed = 2                       # px per frame
frame_duration = 50                    # ms per frame (~20 fps)
italic_shear = 0.1763                  # tan(10°) for italic
font_size = 30                         # ✅ smaller text

# === PLAIN BLACK BACKGROUND ===
bg_frame = Image.new("RGB", (width, height), (0, 0, 0))  # black

# Duplicate for seamless scrolling
bg_strip = Image.new("RGB", (width * 2, height), (0, 0, 0))
bg_strip.paste(bg_frame, (0, 0))
bg_strip.paste(bg_frame, (width, 0))

# === LOAD FONT ===
try:
    font = ImageFont.truetype(font_path, font_size)
except OSError as e:
    print("⚠️ Could not load Hairy Beard font:", e)
    font = ImageFont.load_default()

# === DRAW TEXT STRIP ===
draw_img = bg_strip.copy()
draw = ImageDraw.Draw(draw_img)

bbox = draw.textbbox((0, 0), text, font=font)
text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]

spacing = 120
x, y = 0, (height - text_h) // 2

while x < draw_img.width + text_w:
    # Render text to its own layer
    temp = Image.new("RGBA", (text_w, text_h * 2), (255, 255, 255, 0))
    temp_draw = ImageDraw.Draw(temp)
    temp_draw.text((0, 0), text, font=font, fill=text_color)

    # Apply italic shear transform
    italic_w = int(temp.width + temp.height * italic_shear)
    italic = temp.transform(
        (italic_w, temp.height),
        Image.AFFINE,
        (1, italic_shear, -temp.height * italic_shear / 2, 0, 1, 0),
        resample=Image.BICUBIC,
    )

    # Paste on background
    draw_img.paste(italic, (x, y - text_h // 5), italic)
    x += text_w + spacing

# === CREATE FRAMES ===
frames = []
for offset in range(0, width, scroll_speed):
    frame = draw_img.crop((offset, 0, offset + width, height))
    frames.append(frame)

# === SAVE GIF ===
frames[0].save(
    output_path,
    save_all=True,
    append_images=frames[1:],
    duration=frame_duration,
    loop=0,
    optimize=True,
)

print(f"✅ GIF saved as: {output_path}")
