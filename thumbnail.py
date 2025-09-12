from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

def make_thumbnail_with_brand(image_bytes, brand_text="Jacpotfilm"):
    im = Image.open(BytesIO(image_bytes)).convert("RGBA")
    im.thumbnail((320, 180))
    w, h = im.size

    draw = ImageDraw.Draw(im)
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 18)
    except:
        font = ImageFont.load_default()

    tw, th = draw.textsize(brand_text, font=font)
    padding = 8
    x = w - tw - padding
    y = h - th - padding

    rect = Image.new("RGBA", (tw+6, th+6), (0, 0, 0, 120))
    im.paste(rect, (x-3, y-3), rect)

    draw.text((x, y), brand_text, font=font, fill=(255, 255, 255, 255))

    out = BytesIO()
    out.name = "thumb.png"
    im.save(out, "PNG")
    out.seek(0)
    return out
