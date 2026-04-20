# paper-references

> **中文** | [English](#english)

一个 [Claude Code](https://claude.ai/code) Skill，用于管理学术论文参考文献——解析、搜索、插入、格式化，支持所有主流引用格式，中英文论文均可使用。

---

## 功能概览 · What it does

**给没有参考文献的论文反向添加引用。** 提供你的草稿文件或粘贴正文，Skill 会自动读取内容、识别需要引用的论点、搜索相关文献、展示搜索结果等待你确认，最后插入编号标记和完整参考文献列表——一次会话完成全部工作。

也可以单独完成任意引用任务：

| 任务 | 示例指令 |
|---|---|
| 解析现有引用 | "提取这篇论文的引用地图" |
| 查找可引文献 | "找5篇关于Transformer异常检测的论文" |
| 反向添加引用 | "我的草稿没有参考文献，帮我加上" |
| 重新格式化 | "把参考文献转成GB/T 7714-2015格式" |
| 引用审计 | "哪些正文引用没有对应的参考文献条目？" |
| English papers | "Add IEEE-style references to my paper" |

---

## 安装 · Installation

**1. 找到（或创建）Claude Code 的 skills 文件夹：**

| 系统 | 路径 |
|---|---|
| macOS / Linux | `~/.claude/skills/` |
| Windows | `C:\Users\<用户名>\.claude\skills\` |

**2. 克隆本仓库到该目录：**

```bash
git clone https://github.com/<your-handle>/paper-references ~/.claude/skills/paper-references
```

**3. 重启 Claude Code（或开启新会话），Skill 会被自动发现。**

---

## 使用方法 · Usage

在 Claude Code 中通过 `/` 命令调用：

```
/paper-references
```

然后用自然语言描述你的需求，Skill 会判断需要执行哪些阶段。

### 使用示例

```
/paper-references
> @论文草稿.docx 给这篇论文添加参考文献，用GB/T 7714-2015格式

/paper-references
> @report.pdf 把参考文献格式改成IEEE

/paper-references
> 找5篇关于多源时间序列异常检测的论文，并建议插入位置
```

```
/paper-references
> @my_draft.docx Add references. Use APA 7th edition.

/paper-references
> Reformat the bibliography in report.pdf to IEEE style.
```

---

## 三阶段工作原理 · How it works

### 阶段一 · Parse · 解析

读取你的文档（`.docx`、`.pdf`、`.txt`、`.md` 或粘贴文本），构建引用地图：

- 定位正文中所有引用标记：`[1]`、`(Smith, 2019)`、上标数字、脚注
- 将参考文献列表（如有）解析为结构化字段：作者、标题、年份、期刊、DOI
- 报告孤儿标记（正文有但参考文献列表无）和缺失引用（正文提到但未标注）

### 阶段二 · Search & Insert · 搜索与插入

自动搜索与你论文内容匹配的文献：

- 使用 [Semantic Scholar](https://www.semanticscholar.org/) 和 [CrossRef](https://www.crossref.org/)（无需 API Key）
- 每个主题用多种检索词提高覆盖率
- 以编号清单展示结果——**等待你确认后才修改文件**
- 确认后：在正确句子处插入 `[n]` 上标标记，在参考文献列表末尾追加条目，并展示变更对比

### 阶段三 · Format · 格式化

将参考文献列表规范化为指定格式：

| 格式 | 适用场景 |
|---|---|
| **GB/T 7714-2015** | 中文学术论文（国标） |
| **APA 7th** | 心理学、社会科学、教育学 |
| **MLA 9th** | 人文学科、文学 |
| **Chicago 17th** | 历史学、艺术 |
| **Vancouver** | 医学、生物医学 |
| **IEEE** | 工程、计算机科学 |
| **自定义** | 提供一个示例，自动匹配其格式 |

输出始终写入新文件，**原文件不会被覆盖**。

---

## 支持的文件格式 · Supported file types

| 格式 | 读取方式 |
|---|---|
| `.docx` | `python-docx`（内置跨 Run 搜索，支持中文字体） |
| `.pdf` | `pdfplumber` |
| `.txt` / `.md` | 直接读取 |
| 粘贴文本 | 无需文件，直接处理 |

---

## 环境依赖 · Requirements

- [Claude Code](https://claude.ai/code)（CLI 或桌面版）
- Python 3，以及处理文档所需的库：

```bash
pip install python-docx pdfplumber lxml
```

---

## 文件结构 · File structure

```
paper-references/
├── SKILL.md                          # Skill 定义文件（Claude Code 读取）
├── README.md                         # 本文件
├── references/
│   └── citation-formats.md           # 所有引用格式的模板与示例
└── scripts/
    ├── docx_utils.py                 # 核心库：跨 Run 引用插入 + 参考文献追加
    ├── footnote_adder.py             # 真实 Word 脚注插入
    │                                 #   （改编自 github.com/droza123/python-docx-footnotes）
    └── insert_citations.py           # CLI：从 JSON 计划文件批量处理 .docx
```

### 核心技术说明 · Key technical details

**跨 Run 文本搜索**  
Word 将段落文本拆分存储在多个格式不同的 `Run` 对象中，直接搜索 `run.text` 会遗漏跨 Run 的字符串。`docx_utils.py` 先归并相邻同格式 Run，再搜索，算法改编自 [sinallcom/python-docx-replace](https://github.com/sinallcom/python-docx-replace)。

**真正的上标标记**  
引用标记以新 `Run` 的形式插入，带有 `<w:vertAlign w:val="superscript"/>` XML 属性，并继承周围文字的字体设置，包括中文东亚字体提示（`<w:rFonts w:eastAsia="宋体"/>`）。

**原生 Word 脚注**  
`FootnoteAdder` 在 `doc.save()` 之后直接编辑 docx ZIP 内的 `word/footnotes.xml`，支持真正的页底脚注，而非行内上标文字。改编自 [droza123/python-docx-footnotes](https://github.com/droza123/python-docx-footnotes)。

---

## 开源协议 · License

MIT

---

<a name="english"></a>

## English

A [Claude Code](https://claude.ai/code) skill for managing academic paper citations — parsing, searching, inserting, and formatting references across all major citation styles, in both English and Chinese.

### Installation

1. Locate (or create) your Claude Code skills folder:
   - **macOS / Linux:** `~/.claude/skills/`
   - **Windows:** `C:\Users\<you>\.claude\skills\`

2. Clone this repo there:
   ```bash
   git clone https://github.com/<your-handle>/paper-references ~/.claude/skills/paper-references
   ```

3. Restart Claude Code. The skill is auto-discovered.

### Usage

```
/paper-references
> @my_draft.docx Add references. Use GB/T 7714-2015.
```

### Three stages

| Stage | What it does |
|---|---|
| **Parse** | Reads your document and maps every citation marker to its bibliography entry |
| **Search & Insert** | Finds relevant papers via Semantic Scholar / CrossRef, waits for approval, then inserts superscript markers and appends bibliography entries |
| **Format** | Reformats the entire reference list to APA, MLA, Chicago, Vancouver, IEEE, GB/T 7714-2015, or a custom style you provide |

### Requirements

```bash
pip install python-docx pdfplumber lxml
```

### License

MIT
