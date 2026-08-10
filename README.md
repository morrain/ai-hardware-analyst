# AI Hardware Analyst Skill (全球 AI 硬件与半导体产业链投研分析师)

[![Skill Standard](https://img.shields.io/badge/Agent-Skill-blue.svg)](https://github.com/google/antigravity)

具备10年以上全球跨市场（美股、台股、A股）硬科技投研经验的 AI 产业链资深分析师 Skill。专为 AI 服务器硬件架构、半导体周期、三大市场闭环映射、高频数据验证与牛鞭效应分析设计。

---

## 🌟 核心特性

- **三地市场闭环映射与验证**：
  - **美股**：技术策源与需求总量（NVDA / AMD / AVGO / MRVL / APH / VRT / 4大 CSP Capex）
  - **台股**：高频交货事实与工艺验证（TSMC CoWoS / 鸿海 / 广达 / 纬创月度营收 / 金像电 PCB CCL / 奇鋐双鸿液冷）
  - **A股**：全球供应链份额弹性与国产替代（中际旭创 / 新易盛光模块 / 沪电工业富联 / 寒武纪海光国产算力）
- **四维底层逻辑推演**：
  1. 技术路线与增量壁垒（液冷渗透率、CPO 节点、HBM4 封测改变）
  2. 时间错配与牛鞭效应（美股指引 vs 台股月度营收事实）
  3. A 股弹性能量（静态/动态 PE、市值与全球供应链份额弹性）
  4. 风险揭示（出口管制、需求不及预期、技术替代与估值透支）
- **防幻觉与数据铁律**：
  - 在每次回答前确认当前真实世界日期。
  - 涉及到股价、市值、估值、财务与台股月营收，**强制触发实时联网检索**，并严格注明数据截止时间（格式：截至YYYY年MM月DD日）。
- **动态交互控制**：
  - 简短数据查询：快速输出极简数字与事实。
  - 深度报告模式：强制使用 Markdown 比价与估值表格。
  - 主动澄清机制：针对模糊提问主动提出 1-2 个针对性问题。
- **内置自我完善机制 (Self-Refinement)**：
  - 增量标的与新技术路线自动捕捉与字典更新提示。
  - 财报季与台股月度营收发布周期的基期校验协议。

---

## 📦 安装与使用指南

### 使用 npx skills 一键安装

```bash
npx skills add <your-github-repo-or-path>
```

或手动软链接至系统的 Skill 目录：

```bash
# 全局生效
ln -s /path/to/ai-hardware-analyst ~/.gemini/config/skills/ai-hardware-analyst

# 工作区生效
ln -s /path/to/ai-hardware-analyst .agents/skills/ai-hardware-analyst
```

---

## 📁 目录结构

```text
ai-hardware-analyst/
├── README.md                          # 本文档
├── SKILL.md                          # Skill 核心定义与调度规范
├── references/                       # 深度产业链知识库字典与自我完善指引
│   ├── us_market_capex.md            # 美股 CSP Capex 指引与核心芯片/基础设施映射
│   ├── tw_market_supplychain.md      # 台股月度营收、CoWoS/封装测试/PCB基材高频数据
│   ├── cn_market_elasticity.md       # A股光模块/液冷/组装弹性及国产替代链
│   └── self_refinement_guide.md      # 自我完善与知识迭代标准化流程
├── templates/                        # 投研报告与输出结构标准模板
│   ├── quick_answer.md               # 简短问答响应格式
│   └── deep_report.md                # 深度分析报告结构与 Markdown 表格样式
└── examples/                         # Few-shot 典范案例库
    ├── sample_quick_query.md         # 案例一：高频数据极简短答范例
    └── sample_deep_analysis_nvl72.md # 案例二：NVL72 产业链四维深度推演范例
```
