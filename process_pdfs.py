import os
import json
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar
import numpy as np

def is_heading(text):
    text = text.strip()
    if len(text) < 2 or len(text) > 120:
        return False
    if text.replace(' ', '').isnumeric():
        return False
    # Allow headings ending with colon
    if text.endswith('.') or text.endswith('?'):
        return False
    return True

def extract_title_and_headings(pdf_path):
    lines = []
    # 1. Gather all lines with font sizes and pages
    for page_num, page_layout in enumerate(extract_pages(pdf_path), 1):
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                text = element.get_text().strip()
                if not text:
                    continue
                font_sizes = [char.size for line in element for char in line if isinstance(char, LTChar)]
                if not font_sizes:
                    continue
                max_size = max(font_sizes)
                lines.append({'text': text, 'size': max_size, 'page': page_num})

    # 2. Use font size histogram to determine heading levels
    all_sizes = np.array([l['size'] for l in lines])
    # The body text size is often the mode or median of all font sizes
    body_size = float(np.median(all_sizes))
    # Any line with a font size greater than body_size + threshold is a heading
    # Threshold can be 1.5pt, but can be tuned
    threshold = 1.5
    candidate_headings = [l for l in lines if l['size'] >= body_size + threshold and is_heading(l['text'])]

    # 3. Group heading sizes (H1, H2, H3) by unique sizes, largest is H1, etc
    unique_sizes = sorted({l['size'] for l in candidate_headings}, reverse=True)
    outline = []
    for h in candidate_headings:
        if h['size'] == unique_sizes[0]:
            lvl = "H1"
        elif len(unique_sizes) > 1 and h['size'] == unique_sizes[1]:
            lvl = "H2"
        elif len(unique_sizes) > 2 and h['size'] == unique_sizes[2]:
            lvl = "H3"
        else:
            lvl = "H3"  # fallback: treat smaller headings as H3
        outline.append({'level': lvl, 'text': h['text'], 'page': h['page']})

    # 4. Title: largest heading on page 1
    title = ""
    page1_headings = [h for h in outline if h['level'] == "H1" and h['page'] == 1]
    if page1_headings:
        title = page1_headings[0]['text']
    elif outline:
        # fallback: any biggest heading anywhere
        title = outline[0]['text']

    return {"title": title, "outline": outline}

def process_pdfs(input_dir, output_dir):
    for fname in os.listdir(input_dir):
        if fname.lower().endswith('.pdf'):
            pdf_path = os.path.join(input_dir, fname)
            outname = fname[:-4] + ".json"
            outpath = os.path.join(output_dir, outname)
            result = extract_title_and_headings(pdf_path)
            with open(outpath, "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    input_dir = "/app/input"
    output_dir = "/app/output"
    os.makedirs(output_dir, exist_ok=True)
    process_pdfs(input_dir, output_dir)