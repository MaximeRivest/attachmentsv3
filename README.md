# Architecture: The Genius of attachments

## The Core Insight

The architecture answers one question brilliantly:

> **"How do I turn *anything* into something an LLM can consume?"**

```python
att("file.pdf")           # local file
att("data/")              # directory
att("github://org/repo")  # entire repo
att("https://...")        # URL
att("s3://bucket/key")    # extensible to anything
```

**One function. One output format. Any input.**

## The Genius: Composable Universality

### 1. The Artifact as Universal Currency

```python
{
    "text": "...",      # What LLMs read
    "images": [...],    # What multimodal LLMs see
    "audio": [],        # Future-ready
    "video": [],        # Future-ready
    "flags": {...}      # Metadata for routing/debugging
}
```

This isn't just a data structure—it's a **protocol**. Every processor speaks the same language. Every consumer expects the same shape. You can:

- Chain processors
- Merge artifacts from different sources
- Build middleware that transforms artifacts
- Route based on flags

### 2. Two Orthogonal Registries

```
┌─────────────────┐         ┌─────────────────┐
│  WHERE it comes │         │  WHAT it is     │
│  from           │         │                 │
│                 │         │                 │
│  unpack_handlers│         │  processors     │
│  - github://    │         │  - .pdf         │
│  - s3://        │         │  - .xlsx        │
│  - dropbox://   │         │  - .docx        │
└────────┬────────┘         └────────┬────────┘
         │                           │
         └──────────┬────────────────┘
                    ▼
              (filename, bytes)
                    │
                    ▼
               artifact
```

**Source and format are decoupled.** A PDF from S3 uses the same processor as a PDF from disk. This is the key insight that makes the system scale.

### 3. The "Unpack" Abstraction

The real genius is that `unpack()` flattens **any hierarchical structure** into a list:

```python
unpack("repo.zip")
# → [("repo/src/main.py", bytes), ("repo/README.md", bytes), ...]

unpack("github://org/monorepo")
# → [("src/app/index.ts", bytes), ("src/lib/utils.ts", bytes), ...]
```

Archives, repos, directories—all become flat lists. The rest of the pipeline doesn't care about hierarchy.

---

## How It Becomes Most Powerful

### 1. LLM Context Assembly

```python
def build_context(sources: list[str]) -> str:
    """Turn anything into LLM context."""
    artifacts = []
    for src in sources:
        artifacts.extend(att(src))

    # Smart assembly - fit into context window
    return assemble_for_context(artifacts, max_tokens=100_000)

# Usage
context = build_context([
    "github://company/backend",      # Entire codebase
    "https://docs.api.com/spec.pdf", # API spec
    "~/notes/requirements.txt",      # Local notes
])
```

### 2. RAG Pipeline Integration

```python
def ingest_to_vectordb(source: str, db: VectorDB):
    for artifact in att(source):
        # Text → chunks → embeddings
        if artifact["text"]:
            chunks = chunk_text(artifact["text"])
            db.add(chunks, metadata=artifact["flags"])

        # Images → vision model → descriptions → embeddings
        for img in artifact["images"]:
            description = vision_model.describe(img["bytes"])
            db.add([description], metadata={**artifact["flags"], "image": img["name"]})

# Ingest entire GitHub org
for repo in github.org_repos("my-company"):
    ingest_to_vectordb(f"github://my-company/{repo}", db)
```

### 3. Middleware Pattern

```python
def add_middleware(processor_fn):
    """Wrap any processor with cross-cutting concerns."""
    def wrapped(data: bytes, **opts) -> dict:
        artifact = processor_fn(data, **opts)

        # Add token count
        artifact["flags"]["tokens"] = count_tokens(artifact["text"])

        # Add content hash for dedup
        artifact["flags"]["hash"] = hashlib.sha256(data).hexdigest()

        # Truncate if too large
        if artifact["flags"]["tokens"] > 50_000:
            artifact["text"] = truncate_smart(artifact["text"], 50_000)
            artifact["flags"]["truncated"] = True

        return artifact
    return wrapped

# Apply to all processors
for key in processors:
    processors[key] = add_middleware(processors[key])
```

### 4. The Ultimate Vision: Universal Knowledge Ingestion

```python
# Register ALL the sources
register_unpack_handler("s3://", s3_handler)
register_unpack_handler("gdrive://", gdrive_handler)
register_unpack_handler("notion://", notion_handler)
register_unpack_handler("slack://", slack_handler)
register_unpack_handler("confluence://", confluence_handler)

# Register ALL the formats
register_processor(".docx", docx_processor)
register_processor(".pptx", pptx_processor)
register_processor(".eml", email_processor)
register_processor(".mp3", whisper_transcribe)

# Now THIS works:
knowledge = att("notion://workspace/Engineering")
knowledge += att("gdrive://shared/Product Specs")
knowledge += att("github://company/*")  # All repos
knowledge += att("slack://channel/announcements?since=2024-01-01")

# Feed to LLM
llm.chat(f"Given this context:\n{format_artifacts(knowledge)}\n\nAnswer: {question}")
```

---

## The Power Formula

```
Power = (Sources × Formats) → Unified Artifact → Any Consumer
```

| Sources (unpack) | Formats (processors) | Consumers |
|------------------|---------------------|-----------|
| Local files | PDF | LLM prompts |
| GitHub | Office docs | Vector DBs |
| S3/GCS | Code | Search indices |
| HTTP | Images | Summarizers |
| Notion | Audio/Video | Analytics |
| Slack | Email | Knowledge graphs |
| Confluence | Archives | |

**Each new source multiplies with ALL formats. Each new format works with ALL sources.**

That's the genius: **multiplicative extensibility** through two orthogonal registries connected by a universal intermediate representation.
