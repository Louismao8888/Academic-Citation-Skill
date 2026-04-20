# paper-references

A [Claude Code](https://claude.ai/code) skill for managing academic paper citations — parsing, searching, inserting, and formatting references across all major citation styles, in both English and Chinese.

## What it does

**Reverse-add citations to a paper that has none.** Paste or point to your draft; the skill reads the body text, identifies claims that need citations, searches Semantic Scholar and CrossRef for relevant papers, shows you what it found, waits for your approval, then inserts numbered markers and a complete bibliography — all in one session.

It can also be used for any individual citation task:

| Task | Example prompt |
|---|---|
| Parse existing references | "Extract the citation map from this paper" |
| Find papers to cite | "Find references for the section on LSTM anomaly detection" |
| Reverse-add citations | "My draft has no references — add them" |
| Reformat bibliography | "Convert these references to APA 7th" |
| Audit citations | "Which citations in my paper have no bibliography entry?" |
| Chinese papers | "给这篇论文添加参考文献，用GB/T 7714格式" |

## Installation

1. Locate (or create) your Claude Code skills folder:
   - **macOS / Linux:** `~/.claude/skills/`
   - **Windows:** `C:\Users\<you>\.claude\skills\`

2. Clone or copy this folder there:

```bash
git clone https://github.com/<your-handle>/paper-references ~/.claude/skills/paper-references
```

3. Restart Claude Code (or open a new session). The skill is auto-discovered.

## Usage

Invoke via the `/` command in Claude Code:

```
/paper-references
```

Then describe what you want. The skill reads your request and decides which stage(s) to run.

### Examples

```
/paper-references
> @my_draft.docx Add references. Use GB/T 7714-2015.

/paper-references
> Reformat the bibliography in report.pdf to IEEE style.

/paper-references
> Find 5 papers on transformer-based time series anomaly detection and suggest where to cite them.
```

## How it works — three stages

### Stage 1 · Parse

Reads your document (`.docx`, `.pdf`, `.txt`, `.md`, or pasted text) and builds a citation map:

- Finds every citation marker in the body text: `[1]`, `(Smith, 2019)`, superscripts, footnotes
- Parses the bibliography (if one exists) into structured fields: authors, title, year, venue, DOI
- Reports orphaned markers (in-text but not in bibliography) and missing citations (claimed but uncited)

### Stage 2 · Search & Insert

Searches for papers that fit the context of your writing:

- Uses [Semantic Scholar](https://www.semanticscholar.org/) and [CrossRef](https://www.crossref.org/) (no API key required)
- Runs multiple query phrasings per topic to maximise coverage
- Presents results in a numbered checklist — **waits for your approval before modifying anything**
- On confirmation: inserts `[n]` markers at the right sentences, appends new entries to the bibliography, and shows a diff

### Stage 3 · Format

Normalises the reference list to your chosen style:

| Style | Typical field |
|---|---|
| **APA 7th** | Psychology, social sciences, education |
| **MLA 9th** | Humanities, literature |
| **Chicago 17th** | History, arts |
| **Vancouver** | Medicine, biomedical |
| **IEEE** | Engineering, computer science |
| **GB/T 7714-2015** | Chinese academic papers (国标) |
| **Custom** | Provide one example, matches it |

Always writes output to a new file — the original is never overwritten.

## Supported file types

| Format | How it's read |
|---|---|
| `.txt` / `.md` | Read tool directly |
| `.docx` | `python-docx` |
| `.pdf` | `pdfplumber` |
| Pasted text | Inline, no file needed |

## Requirements

- [Claude Code](https://claude.ai/code) (CLI or desktop app)
- Python 3 with `python-docx` and `pdfplumber` for document I/O (only needed if you process `.docx` / `.pdf` files):

```bash
pip install python-docx pdfplumber
```

## File structure

```
paper-references/
├── SKILL.md                          # Skill definition (read by Claude Code)
├── references/
│   └── citation-formats.md           # Format templates for all supported styles
└── scripts/
    ├── docx_utils.py                 # Cross-run citation insertion + reference appending
    ├── footnote_adder.py             # Native Word footnote insertion (adapted from
    │                                 #   github.com/droza123/python-docx-footnotes)
    └── insert_citations.py           # CLI: apply a JSON insertion plan to a .docx
```

### Key technical details

**Cross-run text search** — Word stores paragraph text split across many `Run` objects with different formatting. `docx_utils.py` normalises paragraphs first (merges adjacent same-format runs) before searching, an approach adapted from [sinallcom/python-docx-replace](https://github.com/sinallcom/python-docx-replace).

**Superscript markers** — citation markers are inserted as a new `Run` with `font.superscript = True` and the surrounding text's font face, preserving Chinese East-Asian font hints (`<w:rFonts w:eastAsia="宋体"/>`).

**Native footnotes** — `FootnoteAdder` directly edits `word/footnotes.xml` inside the docx ZIP after save, enabling real Word footnotes rather than inline superscript text. Adapted from [droza123/python-docx-footnotes](https://github.com/droza123/python-docx-footnotes).

## License

MIT
