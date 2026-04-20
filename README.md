# paper-references

> **中文** | [English](#english)

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

MIT

---

<a name="english"></a>

## English

A [Claude Code](https://claude.ai/code) skill for academic paper reference management. **Ships with a built-in docx processing engine** that inserts real superscript markers at the XML level, includes ready-to-use templates for 7 citation formats, and is designed to minimise token and context usage.

### Key advantages over other tools

**① Built-in docx engine (no manual scripting)**  
Three Python scripts handle everything: cross-run text search (Word splits paragraphs into many `Run` objects — the engine merges them before searching), true superscript XML insertion (`<w:vertAlign w:val="superscript"/>`), and Chinese East-Asian font preservation.

**② 7 built-in citation format templates**  
`references/citation-formats.md` contains complete templates for GB/T 7714-2015, APA 7th, MLA 9th, Chicago 17th, Vancouver, IEEE, and custom matching. Claude reads them directly — no token cost to re-derive the format rules each time.

**③ Low token & context footprint**  
All insertions are batched into a single `plan.json` executed by a Python script. Claude generates the plan and verifies the result — the full document never needs to live in the context window.

**④ Best results with `.docx`**  
`.docx` is the only format that supports true superscript markers, formatted bibliography appending, and native Word footnotes. If your paper is a PDF, save it as `.docx` first for best results.

### Installation

```bash
git clone https://github.com/<your-handle>/paper-references ~/.claude/skills/paper-references
pip install python-docx pdfplumber lxml
```

Restart Claude Code — the skill is auto-discovered.

### Usage

```
/paper-references
> @draft.docx Add references. Use IEEE style.
```

### License

MIT
