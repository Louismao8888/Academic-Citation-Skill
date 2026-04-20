# paper-references

> **中文** | [English](#english)

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet?logo=anthropic&logoColor=white)](https://claude.ai/code)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)](https://github.com/<your-handle>/paper-references)
[![Citation Styles](https://img.shields.io/badge/citation%20styles-7%20built--in-green)](#7-built-in-citation-format-templates--zero-configuration)
[![docx](https://img.shields.io/badge/docx-superscript%20%2B%20footnote-orange?logo=microsoftword&logoColor=white)](scripts/docx_utils.py)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/<your-handle>/paper-references/pulls)

一个 [Claude Code](https://claude.ai/code) Skill，专为学术论文参考文献管理而生。**内置 docx 处理引擎**，支持真正的上角标插入、多格式脚注模板，中英文论文均可，开箱即用。

---

## 为什么选择这个 Skill？· Why this skill?

市面上大多数引用工具要么是独立软件（Zotero、Mendeley），要么需要手动复制格式——而这个 Skill 直接在 Claude Code 会话里完成全部工作，还有几个同类工具没有的技术亮点：

### ✦ 内置 docx 处理引擎，无需离开对话

Skill 自带三个 Python 脚本（`scripts/`），直接操作 `.docx` 文件的底层 XML，解决了 python-docx 原生 API 的两个痛点：

**① 跨 Run 文本搜索**  
Word 在存储段落时会把同一句话拆分成多个格式不同的 `Run` 对象。例如"LSTM**能够**处理时序数据"可能是三个 Run。普通脚本直接搜 `run.text` 会找不到目标。本 Skill 先归并同格式 Run，再搜索，**任何位置的文字都能精准定位**。

**② 真正的上角标（Superscript）**  
引用标记不是拼成普通文字 `[1]`，而是写入 Word XML 的上标属性：
```xml
<w:vertAlign w:val="superscript"/>
```
在 Word / WPS 里打开效果与人工添加完全一致，字号自动缩小、位置自动上移，**不影响正文排版**。

**③ 中文字体无损保留**  
插入新 Run 时自动继承周围文字的中文字体设置（`<w:rFonts w:eastAsia="宋体"/>`），不会出现插入后部分文字字体变成默认西文字体的问题。

---

### ✦ 内置所有主流格式的脚注模板，零配置

`references/citation-formats.md` 收录了 7 种格式的完整模板，Claude 可以直接按模板输出，不需要你提供示例、也不需要额外的 token 去"学习"格式：

| 格式 | 适用场景 | 特点 |
|---|---|---|
| **GB/T 7714-2015** | 中文学术论文（国标） | 支持 [J][M][C][D][R][EB/OL] 等文献类型码 |
| **APA 7th** | 心理学、社会科学、教育学 | 作者最多 20 人规则，DOI 格式标准化 |
| **MLA 9th** | 人文、文学 | 容器（Container）嵌套结构 |
| **Chicago 17th** | 历史学、艺术 | Notes-Bibliography 与 Author-Date 双模式 |
| **Vancouver** | 医学、生物医学 | 按出现顺序编号，作者缩写无空格 |
| **IEEE** | 工程、计算机科学 | `[1] F. Last, "Title," *Journal*, vol. X` |
| **自定义** | 任意期刊投稿 | 提供一个示例自动匹配，无需额外描述 |

内置模板意味着：**格式输出一次命中，不用反复校正，节省大量 token**。

---

### ✦ 极低的 token 与 context 消耗

这个 Skill 的设计目标之一就是**减少不必要的 token 消耗**：

- **批量处理**：所有引用插入通过一个 JSON 计划文件（`plan.json`）一次性完成，不需要对每条引用分别对话
- **脚本化执行**：实际文件操作由 Python 脚本完成，Claude 只需生成计划、验证结果，不需要在 context 里传递整个文档内容
- **格式模板本地化**：引用格式模板存在 `references/citation-formats.md`，Claude 直接读取，不需要每次从头生成

---

### ✦ 推荐使用 `.docx` 格式

相比 PDF 或纯文本，`.docx` 在本 Skill 中有最完整的支持：

| 能力 | `.docx` | `.pdf` | `.txt` / `.md` |
|---|---|---|---|
| 提取正文文本 | ✅ | ✅ | ✅ |
| 插入上角标引用标记 | ✅ **原生 XML** | ❌ 只能文本覆盖 | ❌ 无格式 |
| 追加格式化参考文献列表 | ✅ 保留字体/段落样式 | ❌ | ⚠️ 纯文本 |
| 插入真正的 Word 脚注 | ✅ 页底脚注 | ❌ | ❌ |
| 保留原文排版 | ✅ | ❌ | ❌ |
| 输出新文件不覆盖原文 | ✅ | ✅ | ✅ |

如果你的论文目前是 PDF，建议先用 Word / WPS 另存为 `.docx`，再交给本 Skill 处理，效果最佳。

---

## 功能概览 · What it does

**给没有参考文献的论文反向添加引用。** 提供草稿文件，Skill 自动识别正文中需要引用的论点，搜索匹配文献，等待你确认后一次性插入全部标记和参考文献列表。

常见任务示例：

| 任务 | 示例指令 |
|---|---|
| 反向添加引用 | `@论文.docx 给这篇论文添加参考文献，用GB/T 7714-2015` |
| 格式转换 | `把参考文献转成IEEE格式` |
| 查找文献 | `找5篇关于LSTM时序异常检测的论文` |
| 解析现有引用 | `提取这篇论文的引用地图，哪些引用没有对应条目？` |
| 英文论文 | `@draft.docx Add APA 7th references to this paper` |

---

## 安装 · Installation

**1. 找到（或创建）Claude Code 的 skills 文件夹：**

| 系统 | 路径 |
|---|---|
| macOS / Linux | `~/.claude/skills/` |
| Windows | `C:\Users\<用户名>\.claude\skills\` |

**2. 克隆仓库：**

```bash
git clone https://github.com/<your-handle>/paper-references ~/.claude/skills/paper-references
```

**3. 安装依赖：**

```bash
pip install python-docx pdfplumber lxml
```

**4. 重启 Claude Code，Skill 自动加载。**

---

## 使用方法 · Usage

```
/paper-references
> @论文草稿.docx 给这篇论文添加参考文献，GB/T 7714格式
```

Skill 会依次执行三个阶段（或按需执行其中某个）：

### 阶段一 · Parse · 解析

读取文档，构建引用地图：找出所有引用标记（`[1]`、`(Smith, 2019)`、上标、脚注），解析参考文献列表，报告孤儿标记和缺失引用。

### 阶段二 · Search & Insert · 搜索与插入

通过 [Semantic Scholar](https://www.semanticscholar.org/) 和 [CrossRef](https://www.crossref.org/)（无需 API Key）搜索相关文献，展示结果清单，**等你确认后**才执行插入。

### 阶段三 · Format · 格式化

按内置模板规范化参考文献列表。输出写入新文件，**原文件不会被覆盖**。

---

## 文件结构 · File structure

```
paper-references/
├── SKILL.md                          # Skill 定义（Claude Code 读取）
├── README.md                         # 本文档
├── references/
│   └── citation-formats.md           # 7种格式的完整模板（GB/T、APA、MLA、Chicago、Vancouver、IEEE、自定义）
└── scripts/
    ├── docx_utils.py                 # 核心引擎：跨Run搜索 + 上角标插入 + 参考文献追加
    ├── footnote_adder.py             # Word原生脚注插入（直接编辑footnotes.xml）
    └── insert_citations.py           # CLI批量处理：读取plan.json，一次完成全部插入
```

---

## 开源协议 · License

Apache 2.0 — see [LICENSE](LICENSE)

---

<a name="english"></a>

## English

A [Claude Code](https://claude.ai/code) skill for academic paper reference management. **Ships with a built-in docx processing engine** that inserts real superscript markers at the XML level, includes ready-to-use templates for 7 citation formats, and is designed to minimise token and context usage. Works for both English and Chinese papers.

---

### Why this skill? · Key advantages

Most citation tools are standalone apps (Zotero, Mendeley) or require manual copy-pasting. This skill completes everything inside a Claude Code session — and has several technical advantages over similar AI-based approaches:

#### ✦ Built-in docx processing engine — no manual scripting

The skill ships three Python scripts (`scripts/`) that operate directly on `.docx` XML, solving two well-known limitations of the python-docx API:

**① Cross-run text search**  
Word stores paragraph text split across multiple `Run` objects with different formatting. For example, "LSTM **can** process sequences" might be three separate runs. A naive `run.text` search will miss any target that spans a formatting boundary. This engine normalises paragraphs first (merges adjacent same-format runs), then searches — **any substring in any paragraph is found reliably**.

**② True superscript markers**  
Citation markers are not appended as plain text `[1]`. They are written as a dedicated XML run with the superscript attribute:
```xml
<w:vertAlign w:val="superscript"/>
```
When opened in Word or WPS, the result is indistinguishable from a manually inserted citation — the font size shrinks automatically, the position rises above the baseline, and **the surrounding text layout is not disturbed**.

**③ Chinese East-Asian font preservation**  
When a run is split to insert a marker, both halves inherit every formatting attribute of the original, including the East-Asian font hint (`<w:rFonts w:eastAsia="宋体"/>`). Chinese text never reverts to a default Western font after insertion.

---

#### ✦ 7 built-in citation format templates — zero configuration

`references/citation-formats.md` contains complete, ready-to-use templates for every major style. Claude reads them directly at the start of a session — **no token cost to re-derive format rules, no repeated corrections**:

| Format | Typical field | Notable rules covered |
|---|---|---|
| **GB/T 7714-2015** | Chinese academic papers | Document type codes: [J][M][C][D][R][EB/OL]; author ALL-CAPS |
| **APA 7th** | Psychology, social sciences, education | Up-to-20-author rule; DOI as `https://doi.org/` URL |
| **MLA 9th** | Humanities, literature | Container nesting structure |
| **Chicago 17th** | History, arts | Notes-Bibliography and Author-Date modes |
| **Vancouver** | Medicine, biomedical | Appearance-order numbering; no spaces in initials |
| **IEEE** | Engineering, computer science | `[1] F. Last, "Title," *Journal*, vol. X, no. Y` |
| **Custom** | Any journal submission | Provide one example — the skill matches its exact style |

---

#### ✦ Low token & context footprint

The skill is deliberately designed to be **session-efficient**:

- **Batch execution** — all insertions are described in a single `plan.json` and executed by a Python script in one shot. No back-and-forth per citation.
- **Script-based file editing** — Claude generates a plan and verifies the result. The full document never needs to live in the context window.
- **Local format templates** — citation style rules are stored in `references/citation-formats.md` and read once per session, not regenerated from scratch each time.

---

#### ✦ Recommended: use `.docx` format

`.docx` is the only format with full feature support:

| Capability | `.docx` | `.pdf` | `.txt` / `.md` |
|---|---|---|---|
| Extract body text | ✅ | ✅ | ✅ |
| Insert true superscript markers | ✅ **native XML** | ❌ text overlay only | ❌ no formatting |
| Append formatted bibliography | ✅ preserves font & paragraph style | ❌ | ⚠️ plain text only |
| Insert native Word footnotes | ✅ page-bottom footnotes | ❌ | ❌ |
| Preserve original layout | ✅ | ❌ | ❌ |
| Output to new file (original safe) | ✅ | ✅ | ✅ |

If your paper is currently a PDF, save it as `.docx` in Word or WPS first — you'll get the full experience.

---

### What it does

**Reverse-add citations to a paper that has none.** Point the skill at your draft; it reads the body text, identifies claims that need citations, searches Semantic Scholar and CrossRef for matching papers, shows you the results, waits for your approval, then inserts all markers and the full bibliography in one pass.

Common tasks:

| Task | Example prompt |
|---|---|
| Reverse-add citations | `@draft.docx Add references. Use GB/T 7714-2015.` |
| Reformat bibliography | `Convert these references to IEEE style` |
| Find papers to cite | `Find 5 papers on transformer-based anomaly detection` |
| Parse & audit | `Which in-text citations have no bibliography entry?` |
| Chinese papers | `给这篇论文添加参考文献，用国标格式` |

---

### Three stages

#### Stage 1 · Parse

Reads your document (`.docx`, `.pdf`, `.txt`, `.md`, or pasted text) and builds a citation map:
- Locates every citation marker: `[1]`, `(Smith, 2019)`, superscripts, footnotes
- Parses the bibliography (if present) into structured fields: authors, title, year, venue, DOI
- Reports orphaned markers (in-text but missing from bibliography) and uncited claims

#### Stage 2 · Search & Insert

Searches for papers matching your writing context:
- Uses [Semantic Scholar](https://www.semanticscholar.org/) and [CrossRef](https://www.crossref.org/) — no API key required
- Runs multiple query phrasings per topic for broader coverage
- Presents a numbered checklist — **waits for your approval before touching any file**
- On confirmation: inserts `[n]` superscript markers at the right sentences and appends bibliography entries

#### Stage 3 · Format

Normalises the reference list to your chosen style using the built-in templates. Always writes to a new file — **the original is never overwritten**.

---

### Installation

**1. Locate (or create) your Claude Code skills folder:**

| OS | Path |
|---|---|
| macOS / Linux | `~/.claude/skills/` |
| Windows | `C:\Users\<you>\.claude\skills\` |

**2. Clone this repo:**

```bash
git clone https://github.com/<your-handle>/paper-references ~/.claude/skills/paper-references
```

**3. Install dependencies:**

```bash
pip install python-docx pdfplumber lxml
```

**4. Restart Claude Code** — the skill is auto-discovered.

---

### Usage

```
/paper-references
> @draft.docx Add references. Use IEEE style.
```

### File structure

```
paper-references/
├── SKILL.md                    # Skill definition (read by Claude Code)
├── references/
│   └── citation-formats.md     # Complete templates for all 7 citation styles
└── scripts/
    ├── docx_utils.py           # Core engine: cross-run search, superscript insertion, bibliography append
    ├── footnote_adder.py       # Native Word footnote insertion (edits footnotes.xml directly)
    └── insert_citations.py     # CLI: reads plan.json, applies all insertions in one shot
```

### License

Apache 2.0 — see [LICENSE](LICENSE)
