# Codex 文献阅读 Skills

<details>
<summary>☕ 支持作者</summary>

如果这个项目对你有帮助，欢迎自愿赞赏，支持后续维护。感谢你的支持！

使用微信扫描下方收款码：

<img src="https://raw.githubusercontent.com/R3ze959/eis-drt-batch-analysis-skill/main/.github/assets/wechat-pay.jpg" alt="微信赞赏收款码" width="280" />

</details>

五个面向中文科研阅读的技能：全文翻译、单篇解析、多篇材料综述、专题证据比较，以及文献汇报大纲。适合材料、电池、电化学等研究，也可按论文实际领域使用。

此次更新面向 GPT-6 Astra：缩短常驻指令，把模板和排版细节放到按需读取的 references；明确子代理分工和主代理复核。精简的是指令，完整阅读所需的原文、图表、方法和证据覆盖仍然保留。技能继承当前模型设置，不切换模型、不需要额外 LLM API 密钥，也不保证特定模型的效果。

## 选择技能

| 任务 | Skill | 输出重点 |
| --- | --- | --- |
| 整篇 PDF 翻成中文 | `translate-full-pdf` | 模型翻译、离线排版、完整性和版面检查 |
| 从头读懂一篇论文 | `comprehensive-paper-analysis` | 研究问题、方法、逐图解释、结论与边界 |
| 比较同一材料体系的多篇论文 | `multi-paper-materials-review` | 合成/结构/测试条件、数据可比性、共识与分歧 |
| 只研究多篇论文中的一个主题 | `multi-paper-aspect-review` | 围绕问题比较证据，区分直接证据与推断 |
| 把阅读结果组织成文献汇报 | `literature-ppt-outline` | 逐页论点、原图定位、配文、讲稿和过渡 |

默认中文。用户指定的问题范围、语言、格式和输出位置优先。单个问题不强制生成长报告；要求全面解析时覆盖全文及关键图表。PPT 大纲技能不自动扩大为制作 `.pptx`。

## 子代理怎样参与

任务足够大且运行环境允许时，主代理可分派 1–3 个独立任务，数量不超过可用并发槽位：

- 单篇：图表、方法或关键结论复核；主代理组织全文逻辑。
- 多篇：按论文或独立文献批提取证据；主代理统一指标、判断可比性并综合。
- 全文翻译：按章节或页码翻译独立块；主代理合并术语和译文，再统一排版。
- 汇报大纲：原图定位或独立章节组织；主代理确定故事顺序和逐页信息量。

子代理返回文献 ID、页码/图表定位、相关条件、证据性质和未解决项，使用各自的临时文件。主代理回到原文核对关键结论后再整合，不能把多个代理的相同说法当成多个独立证据。短任务直接完成；无子代理工具时串行执行。

这一设计参考 [OpenAI 的 GPT-6 Astra 行为说明](https://developers.openai.com/api/docs/guides/latest-model#gpt-6-astra-behavior)：减少不必要的强制指令，明确何时委派，按任务需要进行验证。

## 安装与更新

克隆仓库后，复制所需技能文件夹到 Codex 的技能目录。例如安装全部五个：

```bash
git clone https://github.com/R3ze959/codex-literature-reading-skills.git
cd codex-literature-reading-skills
mkdir -p "$HOME/.codex/skills"
cp -R skills/. "$HOME/.codex/skills/"
```

已有同名技能时，先备份自定义内容，再覆盖对应文件。保留已有输出目录偏好。重新加载技能或开启新任务以使用更新后的指令。五个技能可分别安装，不依赖全部同时存在；导出具体文件时可使用环境中已有的 PDF、Word 或幻灯片工具。

使用示例：

```text
用 $comprehensive-paper-analysis 全面解析这篇论文，尤其讲清楚每张图。
用 $multi-paper-materials-review 比较这几篇论文的测试条件和性能，适合时使用子代理。
用 $multi-paper-aspect-review 只分析这些论文是否证明了体相扩散加快。
用 $literature-ppt-outline 把这些论文整理成 15 分钟组会汇报大纲。
用 $translate-full-pdf 把整篇 PDF 翻译为中文，保留图片并检查漏译。
```

## 全文翻译：模型翻译，脚本排版

默认流程不向翻译服务发送正文，也不额外调用 LLM API。当前模型填写译文，Python 脚本负责提取和排版。Python 环境需要 PyMuPDF，排版需可用的中日韩字体（可用 `--font` 指定）；只有使用这个脚本才需要这些依赖。

```bash
python3 -m venv .venv
.venv/bin/python -m pip install pymupdf
.venv/bin/python skills/translate-full-pdf/scripts/translate_full_pdf.py source.pdf \
  --extract-only --manifest /path/to/work/blocks.json
```

让模型依据原文填写 manifest 中标记为 `translate` 的块，保留块 ID 和来源信息。多个子代理使用独立文件，主代理按 ID 合并。随后排版：

```bash
.venv/bin/python skills/translate-full-pdf/scripts/translate_full_pdf.py source.pdf \
  --translations /path/to/work/completed.json \
  --output /path/to/results/source_中文翻译版.pdf
```

脚本校验来源哈希、语言与翻译块，缺失或不匹配时停止，不自动回退到远端。扫描件需先 OCR，复杂表格、公式或特殊布局可能需要人工式排版修复。脚本运行成功不等于译文正确或所有页面已通过视觉检查；详情见 [离线翻译流程](skills/translate-full-pdf/references/offline-workflow.md)。

原有 Google 接口保留为显式 `--backend google` 选项；选用该服务会发送源文。原先仅传入 PDF 就联网翻译的行为已改变。

## 归档与来源

用户指定或既有的归档位置优先。公共默认可用环境变量调整：

```bash
export CODEX_LITERATURE_ARCHIVE_ROOT="$HOME/CodexLiteratureArchive/Skill生成结果_含原始文献PDF归档"
```

未配置时使用上面的路径。需要 PDF 归档时沿用分类 `01_翻译全文_skill`、`02_全文解析_skill`、`03_多论文联合与同一方面深度分析_skill`，在主题目录下分别存放 `生成结果PDF/` 和 `原始文献PDF/`。用户指定的其他格式按其要求交付；原始文件保留，已有的不同结果不覆盖，预览、缓存和译文清单留在工作目录。

仓库只包含技能、辅助脚本和合成测试，不包含私人论文、真实研究数据或生成报告。[版式示例](examples/literature-skill-preview-template.pdf) 使用模拟内容，仅供参考，不是强制报告模板。

## 验证

翻译脚本的测试使用合成 PDF，可在安装了 PyMuPDF 且有脚本可发现的中日韩字体的 Python 环境运行，不需要网络：

```bash
python3 -m unittest discover -s tests -v
```

技能结构另可用 Codex `skill-creator` 的 `scripts/quick_validate.py` 逐个检查；结构检查不能替代真实任务中的来源核查、科学判断和版面检查。
