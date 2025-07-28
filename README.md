# PDF Outline Extractor

##  What It Does?
Extracts the Title and headings (H1, H2, H3) from PDF files and outputs a structured outline JSON.

## How It Works?
- Uses PyMuPDF to extract text + font size.
- Uses font-size-based clustering to detect heading hierarchy. Use Normalized font sizes to determine heading levels.
- Outputs JSON with heading level, text, and page number.

## Local Testing
- Create `input` and `output` directories in the current directory.
- Place your PDF files in the `input` directory.
- Run ```python process_pdfs.py```
- The output will be saved in the `output` directory, with each PDF generating a corresponding `.json` file (e.g., `file01.json`).

## How to Run

### Step 1: Build Docker Image
```bash
docker build --platform linux/amd64 -t image-name:tag .
```

### Step 2: Run Docker Image

```bash
docker run --rm \
  -v "$(pwd)/input:/app/input" \
  -v "$(pwd)/output:/app/output" \
  image-name:tag
```

All PDF files in the mounted `input` directory will be processed automatically, and each will generate a corresponding `.json` file in the `output` directory.