import os
import json
import pymupdf
from collections import Counter


ROOT_DIR = "."
INPUT_DIR = os.path.join(ROOT_DIR, "input")
OUTPUT_DIR = os.path.join(ROOT_DIR, "output")


def clean_text(text):
    return text.replace('\uf0b7', '').strip()


def normalize_font_size(font_sizes):
    """
    Determine the font size ranking (largest = Title, then H1, H2, H3)
    """
    count = Counter(font_sizes)
    common_sizes = sorted(count.items(), key=lambda x: -x[0])
    size_to_level = {}
    if len(common_sizes) >= 4:
        size_to_level[common_sizes[0][0]] = "Title"
        size_to_level[common_sizes[1][0]] = "H1"
        size_to_level[common_sizes[2][0]] = "H2"
        size_to_level[common_sizes[3][0]] = "H3"
    elif len(common_sizes) == 3:
        size_to_level[common_sizes[0][0]] = "Title"
        size_to_level[common_sizes[1][0]] = "H1"
        size_to_level[common_sizes[2][0]] = "H2"
    elif len(common_sizes) == 2:
        size_to_level[common_sizes[0][0]] = "Title"
        size_to_level[common_sizes[1][0]] = "H1"
    elif len(common_sizes) == 1:
        size_to_level[common_sizes[0][0]] = "Title"

    return size_to_level


def extract_outline(pdf_path):
    doc = pymupdf.open(pdf_path)
    text_blocks = []

    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    text = span["text"].strip()
                    text = clean_text(text)
                    if text:
                        text_blocks.append({
                            "text": text,
                            "size": span["size"],
                            "font": span["font"],
                            "page": page_num
                        })

    font_sizes = [b["size"] for b in text_blocks]
    size_to_level = normalize_font_size(font_sizes)

    outline = []
    title = ""
    for block in text_blocks:
        level = size_to_level.get(block["size"])
        if level == "Title" and not title:
            title = block["text"]
        elif level in ["H1", "H2", "H3"]:
            outline.append({
                "level": level,
                "text": block["text"],
                "page": block["page"]
            })

    return {
        "title": title,
        "outline": outline
    }


def process_all_pdfs():

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for filename in os.listdir(INPUT_DIR):
        if filename.lower().endswith(".pdf"):
            input_path = os.path.join(INPUT_DIR, filename)
            output_path = os.path.join(
                OUTPUT_DIR, filename.replace(".pdf", ".json"))

            print(f"Processing {filename}...")
            output_data = extract_outline(input_path)

            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(output_data, f, indent=2)
            print(f"Saved output to {output_path}")


if __name__ == "__main__":
    process_all_pdfs()
