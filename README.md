# Codex 文献阅读 Skills

这是一组面向科研文献阅读的 Codex skills，主要服务中文科研工作流：完整 PDF 翻译、单篇论文深度解析、多篇材料论文联合综述，以及围绕某个窄主题的跨文献证据比较。它们特别适合材料、电化学、电池和功能材料方向的论文阅读与组会/综述写作准备。

核心目标是让 Codex 不只“总结论文”，而是把论文读成可复用的科研材料：保留原始 PDF，导出结构化中文报告，逐图解释关键证据，整理实验条件和性能数据，并把最终结果与原始文献一起归档，方便以后追溯。

Four Codex skills are included:

- `translate-full-pdf`: 完整翻译 PDF，并尽量保留原始版式、图片和页面结构。
- `comprehensive-paper-analysis`: 单篇论文中文全面解析，包含研究逻辑、实验方法、逐图讲解、证据链、局限和可延伸问题。
- `multi-paper-materials-review`: 多篇材料/电池论文联合综述，比较材料体系、合成路线、测试条件、关键数据和领域发展主线。
- `multi-paper-aspect-review`: 围绕一个指定主题做跨文献深度比较，例如扩散机制、开裂失效、近零应变、包覆界面、operando 证据等。

这些 skills 默认输出中文，强调事实、推断和风险分离；最终导出的 PDF 会与原始文献 PDF 放在同一归档分支中。中间文件、缓存、图像裁剪和 QA 预览不进入最终归档。

## 输出预览

想先看效果，可以打开这个不含真实论文内容的示例模板：

[literature-skill-preview-template.pdf](examples/literature-skill-preview-template.pdf)

这个 PDF 用模拟题目、模拟图和模拟数据展示了 skills 可能生成的报告风格，包括标题页、逐图讲解、关键数据表、证据链表、多论文比较表和主题证据分析。它只用于预览版式，不代表任何真实论文。

## Install

Clone this repository, then copy the skill folders into your Codex skills directory:

```bash
mkdir -p "$HOME/.codex/skills"
cp -R skills/* "$HOME/.codex/skills/"
```

Restart Codex or reload skills after copying.

## Configure Output Archive

The skills write final PDFs into a PDF-only archive. Set this environment variable if you want a custom location:

```bash
export CODEX_LITERATURE_ARCHIVE_ROOT="$HOME/CodexLiteratureArchive/Skill生成结果_含原始文献PDF归档"
```

If the variable is not set, the public versions default to:

```text
~/CodexLiteratureArchive/Skill生成结果_含原始文献PDF归档
```

The archive layout is:

```text
Skill生成结果_含原始文献PDF归档/
├── 01_翻译全文_skill/
├── 02_全文解析_skill/
└── 03_多论文联合与同一方面深度分析_skill/
```

Each paper or topic folder should contain only:

```text
生成结果PDF/
原始文献PDF/
```

Intermediate Markdown, extracted text, JSON, rendered preview PNGs, caches, logs, and temporary figure crops should stay outside the final archive.

## Notes

- These skills do not include copyrighted papers, generated reports, caches, or user data.
- Only analyze PDFs that you are allowed to access and process.
- The translation script in `translate-full-pdf` uses PyMuPDF (`fitz`) and a public Google Translate endpoint by default. If that endpoint is unavailable or unsuitable, adapt the script or translate blocks with another available translator.
- Add a `LICENSE` file before publishing publicly if you want others to reuse or modify the skills under clear terms.
