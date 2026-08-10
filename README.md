# AI Hardware Analyst Skill (全球 AI 硬件与半导体产业链投研分析师)

[![Skill Standard](https://img.shields.io/badge/Agent-Skill-blue.svg)](https://github.com/google/antigravity)

具备10年以上全球跨市场（美股、台股、A股）硬科技投研经验的 AI 产业链资深分析师 Skill。专为 AI 服务器硬件架构、半导体周期、三大市场闭环映射、高频数据验证、A股时间错配套利与隔夜美股开盘前瞻早报设计。

---

## 🌟 核心特性与架构设计

- **单一事实来源 (Single Source of Truth)**：
  - 核心标的全量配置文件独立存放于 [`tickers.json`](./tickers.json)。增删美/台/A三地标的只需修改一个文件，Python 脚本与 Agent 语义分析同频自动更新。
- **三地市场闭环映射与时差传导**：
  - **美股**：技术策源与需求总量（NVDA / AMD / AVGO / MRVL / ALAB / CRDO / APH / VRT / ETN / 4大 CSP）
  - **台股**：高频交货事实与工艺验证（TSMC CoWoS COUPE / 鸿海 / 广达 / 健策3653均热片 / 旺矽6223探针卡 / 信骅 BMC）
  - **A股**：全球供应链份额弹性与时间错配套利（中际旭创 / 新易盛光模块 / 胜宏科技476算力板 / 麦格米特800V电源 / 寒武纪海光国产算力）
- **实时数据防偏差铁律**：
  - 每次先确认真实日期。涉及股价、估值、AI主营占比、台股月营收**强制触发实时联网检索**，实时数据覆写静态 MD，防止因时间推移导致认知偏差。
- **隔夜美股早报与时间解耦**：
  - 支持工作日开盘前 Cron 定时任务推送或口令唤醒（`/morning-report`）。

---

## ⏰ 自定义开盘早报 Cron 定时任务

你可以根据自己的习惯，随时在 Antigravity 中灵活开启或修改定时提醒时间：

```text
# 每天早晨 08:00 自动推送早报
/schedule 0 8 * * 1-5 检索隔夜美股AI标的最新异动归因与SEC 8-K公告，按照 templates/morning_report.md 格式输出今日A股开盘前瞻早报。

# 每天早晨 08:30 自动推送早报
/schedule 30 8 * * 1-5 检索隔夜美股AI标的最新异动归因与SEC 8-K公告，按照 templates/morning_report.md 格式输出今日A股开盘前瞻早报。
```

---

## 📦 安装指南

```bash
npx skills add https://github.com/morrain/ai-hardware-analyst.git
```

---

## 📁 目录结构

```text
ai-hardware-analyst/
├── README.md                          # 本文档
├── tickers.json                       # [Single Source of Truth] 美/台/A三地全量标的配置文件
├── SKILL.md                          # Skill 核心定义、数据铁律与调度规范
├── scripts/
│   └── fetch_overnight_data.py       # [动态脚本] 自动读取 tickers.json 抓取行情与新闻
├── references/                       # 深度产业链知识库字典
│   ├── us_market_capex.md            # 美股 CSP Capex 指引与核心芯片映射
│   ├── tw_market_supplychain.md      # 台股月度营收、CoWoS/封装测试/PCB基材高频数据
│   ├── cn_market_elasticity.md       # A股光模块/液冷/组装弹性及国产替代链
│   ├── value_chain_topology.md       # 7 层物理传递拓扑与主营纯度审计框架
│   ├── data_sources.md               # 官方监管(SEC 8-K)与研报(Seeking Alpha)数据源规范
│   ├── event_calendar.md             # 高频事件时间日历与监控抓手指南
│   └── self_refinement_guide.md      # 自我完善与知识迭代标准化流程
├── templates/                        # 投研报告与输出结构标准模板
│   ├── quick_answer.md               # 简短问答响应格式
│   ├── deep_report.md                # 深度分析报告结构与 A股时差套利模板
│   ├── event_monitoring.md           # 重大变动、财报与法说会解读决策模板
│   └── morning_report.md             # 开盘前瞻早报三段式结构模板
└── examples/                         # Few-shot 典范案例库
    ├── sample_quick_query.md         # 案例一：高频数据极简短答范例
    └── sample_deep_analysis_nvl72.md # 案例二：NVL72 机柜解构四维深度推演范例
```
