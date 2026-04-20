---
name: paper-references
description: >
  Use this skill whenever the user wants to work with academic paper citations or references in any way.
  This includes: parsing a paper to extract its reference list and find where each citation appears in the text;
  searching online for missing citations and adding them to a paper; reformatting an existing reference list
  to a standard style (APA, MLA, Chicago, Vancouver, IEEE, GB/T 7714, or a user-supplied example);
  reverse-engineering citations from a paper that has inline mentions but no bibliography; auditing a paper
  for broken or missing citations; and any other reference management task on academic papers.
  Trigger even if the user just says "add references to my paper", "fix my bibliography", "format my citations",
  "find papers to cite", or uploads a paper and asks about its references. Works for both English and Chinese papers.
---

# Paper References Skill

This skill has three stages that work together or independently. Read the user's request to decide which stages are needed.

## Stage 1 — Parse: Extract citations and build a citation map

When the user provides a paper (as a file path or pasted text), parse it to understand its current citation state.

### What to extract

**From the bibliography/reference list** (usually at the end):
- All reference entries, numbered or unnumbered
- Parse each entry: authors, title, year, venue/journal, volume/pages, DOI/URL if present

**From the body text** — find every citation marker and note where it appears:
- Numbered: `[1]`, `[2,3]`, `[4-6]`, `[1, 3, 5]`
- Superscript numbers (common in medical/Chinese papers)
- Footnote markers: *, dagger, or numbers at bottom of page
- Author-year: (Smith, 2019), (Smith & Jones, 2019), (Smith et al., 2019)
- Chinese-style: [1], (1)

For footnotes, look at the bottom of each page or section for the actual footnote text.

### Output: Citation Map

Present results in a structured table:

```
## Existing References Found: N

| # | Reference Entry | Citation Count | Appears in Sections |
|---|----------------|---------------|---------------------|
| [1] | Smith, A. (2020). Title. Journal... | 3 | Introduction, Methods, Results |
| [2] | Jones, B. (2019). Title. Book. | 1 | Discussion |

## Citation Details
[1] - cited 3 times:
  - Introduction: "...previous work has shown [1] that..."
  - Methods: "We used the method from [1]..."
  - Results: "...consistent with [1]..."
```

If the paper has **no references at all**, say so clearly and ask the user what they want to do (search for relevant papers, or proceed to formatting).

If citation markers exist in the text but **no bibliography** is present, list the orphaned markers and note they need resolution.

### Tips for tricky formats

- **Footnotes**: scan for superscript numbers. The footnote text may be at page bottom (in PDFs) or end-of-document.
- **Chinese papers**: may use superscript, square bracket numbers [1], or footnotes. The reference list appears at the end under "参考文献".
- **Mixed formats**: some papers have numbered references in some sections and author-year in others — track each separately.
- **Combined citations**: `[2,3]` or `[4-6]` — resolve each component to its bibliography entry.

---

## Stage 2 — Search & Insert: Find new citations to add

Use this when the user wants to enrich the paper with additional references.

### Step 1: Understand what to search for

Ask the user (or infer from context) what kind of citations to add:
- Specific claim or passage they want to support?
- Topic-level search (e.g., "find papers on transformer attention mechanisms")?
- Fill in missing citations for specific markers that have no bibliography entry?

### Step 2: Search for papers

Use the Semantic Scholar API (free, no key required):

```
GET https://api.semanticscholar.org/graph/v1/paper/search
  ?query=<search terms>
  &fields=title,authors,year,abstract,externalIds,citationCount,venue
  &limit=10
```

Also try CrossRef for broader coverage:
```
GET https://api.crossref.org/works?query=<terms>&rows=5&sort=relevance
```

For each topic, search with 2-3 different phrasings to get diverse results.

### Step 3: Present results to the user

Show a numbered list for each search:

```
## Search results for: "attention mechanisms transformers"

Found 8 papers. Please check the ones you want to insert:

[ ] [A] Vaswani et al. (2017). Attention Is All You Need. NeurIPS.
        "We propose a new simple network architecture, the Transformer..."
        Cited by 100,000+ | DOI: 10.48550/arXiv.1706.03762

[ ] [B] Bahdanau et al. (2015). Neural Machine Translation by Jointly Learning...
        Cited by 30,000+ | DOI: 10.48550/arXiv.1409.0473
```

**Wait for the user to confirm** which papers to insert before modifying anything.

### Step 4: Insert selected papers

Once the user confirms their selection (e.g., "insert A, C, E"):

1. **Assign new reference numbers**: continue from where the existing list ends
2. **Find the right insertion points** in the body text: look for the sentence or claim each paper supports
3. **Add to the reference list**: append selected papers at the end
4. **Show a diff**: display each change so the user can verify

---

## Stage 3 — Format: Normalize the reference list

Use this when the user wants a clean, consistently formatted bibliography.

### Step 1: Choose a format

Ask the user which format they want, or infer from context:

| Format | Typical use |
|--------|-------------|
| APA 7th | Psychology, social sciences, education |
| MLA 9th | Humanities, literature |
| Chicago 17th (Notes-Bibliography) | History, arts |
| Chicago 17th (Author-Date) | Social sciences |
| Vancouver | Medicine, biomedical |
| IEEE | Engineering, CS |
| GB/T 7714-2015 | Chinese academic papers |
| Custom (user example) | Match provided sample |

See `references/citation-formats.md` for detailed format templates and examples for each style.

### Step 2: Reformat all entries

Apply the chosen format to every reference. Common fixes:

- Standardize author name order and punctuation
- Fix year placement
- Normalize DOI format: always use `https://doi.org/` prefix
- Fix common artifacts (stray numbers, duplicate punctuation, etc.)
- Flag missing fields with a warning note
- Sort: alphabetically for APA/MLA/Chicago, by appearance order for Vancouver/IEEE/GB/T

### Step 3: Deliver the formatted list

Output the complete reformatted reference list with a summary of what changed. Always write modified papers to a new file — never overwrite the original.

---

## Working with files

- `.txt` / `.md`: read directly with the Read tool
- `.docx`: use the built-in scripts (see below) — do NOT use a naive one-liner
- `.pdf`: `python -c "import pdfplumber; pdf=pdfplumber.open('f.pdf'); [print(p.extract_text()) for p in pdf.pages]"`
- Pasted text: work with it inline

---

## Built-in docx tools

The skill ships two helper modules in `scripts/`. Always use these instead of
raw python-docx when modifying .docx files — they handle cross-run text search
and Chinese font preservation correctly.

### scripts/docx_utils.py

**Read text from a docx**
```python
import sys; sys.path.insert(0, r"C:\Users\Administrator\.claude\skills\paper-references")
from docx import Document
doc = Document("paper.docx")
for p in doc.paragraphs:
    if p.text.strip():
        print(p.text)
```

**Insert a citation marker ([1] as superscript) after a text substring**
```python
from scripts.docx_utils import insert_citation_in_doc
from docx import Document

doc = Document("input.docx")
# Inserts "[1]" as a superscript run immediately after the target substring.
# Handles text that is split across multiple Run objects automatically.
ok = insert_citation_in_doc(
    doc,
    target_substring="LSTM能够通过其特殊的内部结构",
    marker="[1]",
    occurrence=1,   # 1 = first match, 2 = second match, …
)
doc.save("output.docx")
```

**Append a formatted reference list**
```python
from scripts.docx_utils import append_references

append_references(
    doc,
    references=[
        "[1] HOCHREITER S, SCHMIDHUBER J. Long short-term memory[J]. Neural Computation, 1997, 9(8): 1735-1780.",
        "[2] VASWANI A, et al. Attention is all you need[C]//NeurIPS. 2017: 5998-6008.",
    ],
    font_name="Times New Roman",
    font_name_cn="宋体",      # East-Asian font for Chinese characters
    font_size_pt=10.5,
)
doc.save("output.docx")
```

### scripts/footnote_adder.py

For documents that use real Word footnotes (common in Chinese humanities papers
formatted to GB/T standards with footnotes at page bottom):

```python
from scripts.footnote_adder import FootnoteAdder
from docx import Document

doc = Document("input.docx")
adder = FootnoteAdder()

p = doc.paragraphs[5]           # paragraph where citation belongs
adder.add_footnote(
    p,
    preceding_text="",          # body text to add before the reference mark
    footnote_text="HOCHREITER S, SCHMIDHUBER J. Long short-term memory[J]. Neural Computation, 1997, 9(8): 1735-1780.",
)

doc.save("output.docx")
adder.finalize_footnotes("output.docx")   # MUST be called after save
```

> **Note:** `finalize_footnotes()` re-packs the docx ZIP to inject the
> footnote XML — it must be called **after** `doc.save()`, not before.

### scripts/insert_citations.py  (CLI)

A ready-made CLI that reads a JSON plan file and applies all insertions + references in one shot:

```bash
python scripts/insert_citations.py input.docx output.docx plan.json
```

`plan.json` format:
```json
{
  "insertions": [
    { "target": "LSTM能够通过其特殊的内部结构", "marker": "[1]", "occurrence": 1 },
    { "target": "变换器模型（Transformer）是完全基于自注意力机制", "marker": "[2]" }
  ],
  "references": [
    "[1] HOCHREITER S, SCHMIDHUBER J. Long short-term memory[J]. Neural Computation, 1997, 9(8): 1735-1780.",
    "[2] VASWANI A, et al. Attention is all you need[C]//NeurIPS. 2017."
  ],
  "options": {
    "font_name": "Times New Roman",
    "font_name_cn": "宋体",
    "font_size_pt": 10.5
  }
}
```

### When to use which tool

| Situation | Tool |
|---|---|
| Numbered citations [1][2] inline in body | `insert_citation_in_doc` + `append_references` |
| Real Word footnotes at page bottom | `FootnoteAdder` |
| Batch job from a plan file | `insert_citations.py` CLI |
| Read-only text extraction | Plain python-docx one-liner |