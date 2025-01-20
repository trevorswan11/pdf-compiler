import os
from tkinter import Tk, filedialog
from PyPDF2 import PdfMerger
from fpdf import FPDF
from PIL import Image
from pillow_heif import register_heif_opener

register_heif_opener()

def browse_files():
    root = Tk()
    root.withdraw()
    files = filedialog.askopenfilenames(
        title="Select files to compile",
        filetypes=[
            ("All files", "*.pdf;*.txt;*.jpg;*.jpeg;*.png;*.heic"),
            ("PDF files", "*.pdf"),
            ("Text files", "*.txt"),
            ("Image files", "*.jpg;*.jpeg;*.png;*.heic"),
        ],
    )
    return root.tk.splitlist(files)

def create_pdf_from_text(text_files, output_path):
    pdf = FPDF()
    for file in text_files:
        pdf.add_page()
        with open(file, 'r', encoding='utf-8') as f:
            for line in f:
                pdf.set_font("Arial", size=12)
                pdf.multi_cell(0, 10, line)
    pdf.output(output_path)

def create_pdf_from_images(image_files, output_path):
    images = [Image.open(img).convert("RGB") for img in image_files]
    images[0].save(output_path, save_all=True, append_images=images[1:])

def merge_pdfs(pdf_files, output_path):
    merger = PdfMerger()
    for pdf in pdf_files:
        merger.append(pdf)
    merger.write(output_path)
    merger.close()

def compile_to_pdf(files, output_path):
    text_files = [f for f in files if f.endswith(".txt")]
    image_files = [f for f in files if f.lower().endswith((".jpg", ".jpeg", ".png", ".heic"))]
    pdf_files = [f for f in files if f.endswith(".pdf")]
    intermediate_pdfs = []
    if text_files:
        text_pdf = "temp_text.pdf"
        create_pdf_from_text(text_files, text_pdf)
        intermediate_pdfs.append(text_pdf)
    if image_files:
        image_pdf = "temp_images.pdf"
        create_pdf_from_images(image_files, image_pdf)
        intermediate_pdfs.append(image_pdf)
    merge_pdfs(pdf_files + intermediate_pdfs, output_path)
    for temp_file in intermediate_pdfs:
        os.remove(temp_file)

def main():
    files = browse_files()
    if files:
        output_path = filedialog.asksaveasfilename(
            title="Save compiled PDF as",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
        )
        if output_path:
            compile_to_pdf(files, output_path)
            print(f"Compiled PDF saved at: {output_path}")
        else:
            print("Save operation cancelled.")
    else:
        print("No files selected.")

if __name__ == "__main__":
    main()
