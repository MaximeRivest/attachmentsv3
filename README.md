# attachments – the Python funnel for LLM context

### Turn *any* file into model-ready text ＋ images, in one line

Most users will not have to learn anything more than: `att("path/to/file.pdf")`

## 🎬 Demo

![Demo](https://github.com/MaximeRivest/att/raw/main/demo_full.gif)

> **TL;DR**  
> ```bash
> pip install att
> ```
> ```python
> from attachments import att
> ctx = att("https://github.com/MaximeRivest/att/raw/main/src/att/data/sample.pdf")
> llm_ready_text   = str(ctx)       # all extracted text, already "prompt-engineered"
> llm_ready_images = ctx.images     # list[str] – base64 PNGs
> ```


Attachments aims to be **the** community funnel from *file → text + base64 images* for LLMs.  
Stop re-writing that plumbing in every project – contribute your *loader / modifier / presenter / refiner / adapter* plugin instead!

## Quick-start ⚡

```bash
pip install attachments
```

### Try it now with sample files

```python
from attachments import att
from attachments.data import get_sample_path

# Option 1: Use included sample files (works offline)
pdf_path = get_sample_path("sample.pdf")
txt_path = get_sample_path("sample.txt")
ctx = att(pdf_path, txt_path)

print(str(ctx))      # Pretty text view
print(len(ctx.images))  # Number of extracted images

# Try different file types
docx_path = get_sample_path("test_document.docx")
csv_path = get_sample_path("test.csv")
json_path = get_sample_path("sample.json")

ctx = att(docx_path, csv_path, json_path)
print(f"Processed {len(ctx)} files: Word doc, CSV data, and JSON")

# Option 2: Use URLs (same API, works with any URL)
ctx = att(
    "https://github.com/MaximeRivest/att/raw/main/src/att/data/sample.pdf",
    "https://github.com/MaximeRivest/att/raw/main/src/att/data/sample_multipage.pptx"
)

print(str(ctx))      # Pretty text view  
print(len(ctx.images))  # Number of extracted images
```

### Advanced usage with DSL

```python
from attachments import att

a = att(
    "https://github.com/MaximeRivest/att/raw/main/src/att/data/" \
    "sample_multipage.pptx[3-5]"
)
print(a)           # pretty text view
len(a.images)      # 👉 base64 PNG list
```

### Send to OpenAI

```bash
pip install openai
```

```python
from openai import OpenAI
from attachments import att

pptx = att("https://github.com/MaximeRivest/att/raw/main/src/att/data/sample_multipage.pptx[3-5]")

client = OpenAI()
resp = client.chat.completions.create(
    model="gpt-4.1-nano",
    messages=pptx.openai_chat("Analyse the following document:")
)
print(resp.choices[0].message.content)
```

or with the response API

```python
from openai import OpenAI
from attachments import att

pptx = att("https://github.com/MaximeRivest/att/raw/main/src/att/data/sample_multipage.pptx[3-5]")

client = OpenAI()
resp = client.responses.create(
    input=pptx.openai_responses("Analyse the following document:"),
    model="gpt-4.1-nano"
)
print(resp.output[0].content[0].text)
```

### Send to Anthropic / Claude

```bash
pip install anthropic
```

```python
import anthropic
from attachments import att

pptx = att("https://github.com/MaximeRivest/att/raw/main/src/att/data/sample_multipage.pptx[3-5]")

msg = anthropic.Anthropic().messages.create(
    model="claude-3-5-haiku-20241022",
    max_tokens=8_192,
    messages=pptx.claude("Analyse the slides:")
)
print(msg.content)
```

### DSPy Integration

We have a special `dspy` module that allows you to use att with DSPy.

```bash
pip install dspy
```

```python
from attachments.dspy import att  # Automatic type registration!
import dspy

# Configure DSPy
dspy.configure(lm=dspy.LM('openai/gpt-4.1-nano'))

# Both approaches work seamlessly:

# 1. Class-based signatures (recommended)
class DocumentAnalyzer(dspy.Signature):
    """Analyze document content and extract insights."""
    document: att = dspy.InputField()
    insights: str = dspy.OutputField()

# 2. String-based signatures (works automatically!)
analyzer = dspy.Signature("document: att -> insights: str")

# Use with any file type
doc = att("report.pdf")
result = dspy.ChainOfThought(DocumentAnalyzer)(document=doc)
print(result.insights)
```

**Key Features:**
- 🎯 **Automatic Type Registration**: Import from `att.dspy` and use `att` in string signatures immediately
- 🔄 **Seamless Serialization**: Handles complex multimodal content automatically  
- 🖼️ **Image Support**: Base64 images work perfectly with vision models
- 📝 **Rich Text**: Preserves formatting and structure
- 🧩 **Full Compatibility**: Works with all DSPy signatures and programs

### Optional: CSS Selector Highlighting 🎯

For advanced web scraping with visual element highlighting in screenshots:

```bash
# Install Playwright for CSS selector highlighting
pip install playwright
playwright install chromium

# Or with uv
uv add playwright
uv run playwright install chromium

# Or install with browser extras
pip install att[browser]
playwright install chromium
```

**What this enables:**
- 🎯 Visual highlighting of selected elements with animations
- 📸 High-quality screenshots with JavaScript rendering  
- 🎨 Professional styling with glowing borders and badges
- 🔍 Perfect for extracting specific page elements

```python
# CSS selector highlighting examples
title = att("https://example.com[select:h1]")  # Highlights H1 elements
content = att("https://example.com[select:.content]")  # Highlights .content class
main = att("https://example.com[select:#main]")  # Highlights #main ID

# Multiple elements with counters and different colors
multi = att("https://example.com[select:h1, .important][viewport:1920x1080]")
```

*Note: Without Playwright, CSS selectors still work for text extraction, but no visual highlighting screenshots are generated.*

### Optional: Microsoft Office Support 📄

For dedicated Microsoft Office format processing:

```bash
# Install just Office format support
pip install att[office]

# Or with uv
uv add att[office]
```

## Contributing

See `CONTRIBUTING.md` for a step‑by‑step developer setup and daily workflow (uv, Ruff, pytest, Quarto docs).

**What this enables:**
- 📊 PowerPoint (.pptx) slide extraction and processing
- 📝 Word (.docx) document text and formatting extraction  
- 📈 Excel (.xlsx) spreadsheet data analysis
- 🎯 Lightweight installation for Office-only workflows

```python
# Office format examples
presentation = att("slides.pptx[1-5]")  # Extract specific slides
document = att("report.docx")           # Word document processing
spreadsheet = att("data.xlsx[summary:true]")  # Excel with summary
```

*Note: Office formats are also included in the `common` and `all` dependency groups.*


## DSL cheatsheet 📝

| Piece                     | Example                   | Notes                                         |
| ------------------------- | ------------------------- | --------------------------------------------- |
| **Select pages / slides** | `report.pdf[1,3-5,-1]`    | Supports ranges, negative indices, `N` = last |
| **Image transforms**      | `photo.jpg[rotate:90]`    | Any token implemented by a `Transform` plugin |
| **Data-frame summary**    | `table.csv[summary:true]` | Ships with a quick `df.describe()` renderer   |
| **Web content selection** | `url[select:title]`       | CSS selectors for web scraping               |
| **Web element highlighting** | `url[select:h1][viewport:1920x1080]` | Visual highlighting in screenshots |
| **Image processing**      | `image.jpg[crop:100,100,400,300][rotate:45]` | Chain multiple transformations |
| **Content filtering**     | `doc.pdf[format:plain][images:false]` | Control text/image extraction |
| **Repository processing** | `repo[files:false][ignore:standard]` | Smart codebase analysis |
| **Content Control**       | `doc.pdf[truncate:5000]`  | *Explicit* truncation when needed (user choice) |
| **Repository Filtering**  | `repo[max_files:100]`     | Limit file processing (performance, not content) |
| **Processing Limits**     | `data.csv[limit:1000]`    | Row limits for large datasets (explicit) |

> 🔒 **Default Philosophy**: All content preserved unless you explicitly request limits

---

## Supported formats (out of the box)

* **Docs**: PDF, PowerPoint (`.pptx`), CSV, TXT, Markdown, HTML
* **Images**: PNG, JPEG, BMP, GIF, WEBP, HEIC/HEIF, …
* **Web**: URLs with BeautifulSoup parsing and CSS selection
* **Archives**: ZIP files → image collections with tiling
* **Repositories**: Git repos with smart ignore patterns
* **Data**: CSV with pandas, JSON

---

## Advanced Examples 🧩

### **Multimodal Document Processing**
```python
# PDF with image tiling and analysis
result = att("report.pdf[tile:2x3][resize_images:400]")
analysis = result.claude("Analyze both text and visual elements")

# Multiple file types in one context
ctx = att("report.pdf", "data.csv", "chart.png")
comparison = ctx.openai("Compare insights across all documents")
```

### **Repository Analysis**
```python
# Codebase structure only
structure = att("./my-project[mode:structure]")

# Full codebase analysis with smart filtering
codebase = att("./my-project[ignore:standard]")
review = codebase.claude("Review this code for best practices")

# Custom ignore patterns
filtered = att("./app[ignore:.env,*.log,node_modules]")
```

### **Web Scraping with CSS Selectors**
```python
# Extract specific content from web pages
title = att("https://example.com[select:h1]")
paragraphs = att("https://example.com[select:p]")

# Visual highlighting in screenshots with animations
highlighted = att("https://example.com[select:h1][viewport:1920x1080]")
# Creates screenshot with animated highlighting of h1 elements

# Multiple element highlighting with counters
multi_select = att("https://example.com[select:h1, .important][fullpage:true]")
```

### **Image Processing Chains**
```python
# HEIC support with transformations
processed = att("IMG_2160.HEIC[crop:100,100,400,300][rotate:90]")

# Batch image processing with tiling
collage = att("photos.zip[tile:3x2][resize_images:800]")
description = collage.claude("Describe this image collage")
```

### **Data Analysis Workflows**
```python
# Rich data presentation
data_summary = att("sales_data.csv[limit:1000][summary:true]")

```

---



Resolve  →  Fetch  →  Expand  →  Identify  →  Load  →  Split  →  Present  →  Refine  →  Aggregate
  |          |         |          |            |        |         |           |
inputs   downloads   explode   sniff type     read   per-type   text/img   headers,
(strings) & cache   dirs/zips   (MIME/magic) objects  chunking   rendering  tiling, meta
    |          |         |          |            |        |         |           |
    -------------------------------------------------------------------------------
                                        |
                                att object
                                (str, images, metadata)