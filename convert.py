import sys
from PIL import Image
import pillow_heif

pillow_heif.register_heif_opener()

def convert_image_to_pdf(image_path):
    try:
        with Image.open(image_path) as img:
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            pdf_path = f"{image_path.rsplit('.', 1)[0]}.pdf"
            img.save(pdf_path, "PDF", resolution=100.0)
    except Exception as e:
        print(f"Failed to convert '{image_path}': {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python convert.py image1.ext image2.ext ...")
    else:
        for image_file in sys.argv[1:]:
            convert_image_to_pdf(image_file)

