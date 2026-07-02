# AI Time Calibrator

用于校准 AI 辅助开发场景下的软件开发工期预估。

[English README](README.md)

## 为什么需要这个项目

很多软件开发估时仍然默认一种“前 AI 时代”的工作方式：人工写大量样板代码、人工查文档、人工补测试、人工做重复重构。可是 Codex、Claude Code、Cursor、Windsurf 等 AI 编程工具已经显著改变了开发过程。

问题是：AI 并不会等比例压缩所有工作。

- 样板代码、CRUD、测试草稿、重复框架代码通常压缩很明显。
- 需求澄清、产品判断、架构取舍、线上安全、人工验收、外部依赖等待通常压缩有限。
- Debug 和跨系统集成高度不稳定，可能很快，也可能几乎没有变快。

AI Time Calibrator 的目标不是让所有估时都变短，而是让估时更符合 AI 辅助开发的真实过程。

## 核心模型

```text
校准后工期 =
  AI 压缩后的实现时间
  + 验证时间
  + 集成时间
  + 风险缓冲
  + 人类瓶颈时间
```

这能避免一个常见误区：代码生成很快，于是误以为整个项目都会同等变快。

## 快速开始

列出支持的任务类型：

```bash
python3 scripts/estimate.py --list-task-types
```

根据传统估时和任务类型生成 AI 校准估时：

```bash
python3 scripts/estimate.py --traditional-hours 24 --task-type crud_api
```

输出 JSON：

```bash
python3 scripts/estimate.py --traditional-hours 24 --task-type crud_api --format json
```

输出 Markdown：

```bash
python3 scripts/estimate.py --traditional-hours 24 --task-type crud_api --format markdown
```

写入文件：

```bash
python3 scripts/estimate.py \
  --traditional-hours 24 \
  --task-type crud_api \
  --format markdown \
  --output report.md
```

使用团队自己的规则文件：

```bash
python3 scripts/estimate.py \
  --rules ./my-team-task-types.yaml \
  --traditional-hours 24 \
  --task-type crud_api
```

## Plugin 与 Skill 接入

统一 skill 入口是：

```text
skills/ai-time-calibrator/SKILL.md
```

这个结构更接近主流开源 skill 项目：skill 本身是主体，Codex、Claude Code、Cursor 等只是不同消费入口。

当前包含这些插件 manifest：

```text
.codex-plugin/plugin.json
.claude-plugin/plugin.json
.cursor-plugin/plugin.json
```

也保留了非 skill 规则适配：

```text
adapters/cursor/rules.md
adapters/windsurf/rules.md
```

手动安装 skill：

```bash
cp -R skills/ai-time-calibrator ~/.claude/skills/
cp -R skills/ai-time-calibrator ~/.codex/skills/
```

这些入口复用同一套校准模型，方便在不同 AI 编程工具里得到一致的估时逻辑。

## 如何贡献

欢迎贡献：

- 真实或匿名的估时案例
- 新任务类型
- 压缩系数调整建议
- 更多 AI 工具适配器
- CLI 改进

贡献前建议运行：

```bash
python3 -m py_compile scripts/estimate.py
python3 -m unittest discover -s tests
```

更多说明见 [CONTRIBUTING.md](CONTRIBUTING.md)。
