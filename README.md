# AI Hardware Analyst Skill (全球 AI 硬件与半导体产业链投研分析师)

[![Skill Standard](https://img.shields.io/badge/Agent-Skill-blue.svg)](https://github.com/google/antigravity)

具备10年以上全球跨市场（美股、台股、A股）硬科技投研经验的专业 AI 产业链分析师 Skill。专为 AI 服务器硬件架构、半导体周期、三大市场闭环映射、高频数据验证、A股时间错配套利与隔夜美股开盘前瞻早报设计。

---

## 🌟 核心架构设计

- **单一事实来源 (Single Source of Truth)**：
  全量标的集中独立存放于 [`tickers.json`](./tickers.json)。增加或修改美/台/A三地标的只需改动此 JSON 文件，脚本与 Agent 自动感知。
- **三位一体动态防偏差架构**：
  静态知识库只提供物理层传递逻辑，标的 AI 主营占比、客户切入进展**强制触发实时联网检索**，且实时数据拥有最高覆写权，彻底杜绝硬编码死数据导致的认知偏差。
- **开盘前瞻早报与时间解耦**：
  支持自定义 Cron 定时任务推送或口令唤醒（`/morning-report`）。

---

## 🚀 常用场景与示例提示词 (Example Prompts)

你可以直接复制或参考以下提示词与 Agent 进行交互：

### 1. 隔夜美股早报与开盘前瞻 (晨报模式)
- **快捷口令**：`/morning-report` 或 `生成隔夜美股早报`
- **精准提问示例**：
  > “检索隔夜美股 NVDA、AVGO 和 Astera Labs 的异动与 SEC 8-K 公告，分析其核心归因，并给出今日 A 股光模块与高阶 HDI 板的开盘应对策略。”

### 2. A 股时间错配套利与业绩弹性推演 (A股买点模式)
- **触发关键词**：`映射`、`A股时间错配`、`传导机会`、`买点`、`弹性`
- **精准提问示例**：
  > “广达 7 月月度营收创历史新高，结合美台时间错配传导规律，分析对 A 股胜宏科技 (300476.SZ) 和中际旭创 (300308.SZ) 的买点建议，并测算 EPS 增量弹性。”
  > “ Blackwell Ultra 800V 机柜电源单柜价值量陡增，映射到 A 股麦格米特 (002851.SZ) 有多少增量弹性？当前估值匹配度如何？”

### 3. 重大事件/财报/法说会解读与去水分 (事件监控决策模式)
- **触发关键词**：`公告`、`财报`、`法说会`、`业绩预告`、`月度营收`
- **精准提问示例**：
  > “台积电 (TSMC, TSM.US) 刚召开了法说会，CoWoS 和 COUPE 硅光平台上修指引如何解读？用上游基材数据排查是否存在水份，并给出【买入/规避/观望】的明确交易结论。”
  > “对比台股月度营收事实，排查胜宏科技半年度业绩预告，判定是真实爆发还是利好兑现。”

### 4. 极速高频数据查询 (短答模式)
- **精准提问示例**：
  > “广达上个月合并营收是多少新台币？同环比表现如何？”
  > “查一下信骅 (5274.TW) 最新月度营收数据及 BMC 拉货动能。”

### 5. 硬件物理架构与代际壁垒拆解 (深度逻辑模式)
- **精准提问示例**：
  > “深度梳理 Vera Rubin (R100) 机柜物理层变革，分析 1.6T 硅光模块、背板铜线与 CPO 硅光及玻璃基板的博弈边界。”

---

## ⏰ 定时早报任务配置指南 (Schedule Configuration)

你可以随时使用 `/schedule` 指令自由开启或调整每日开盘前早报的时间：

```text
# 方案 A：每天工作日早晨 08:00 自动推送早报
/schedule 0 8 * * 1-5 检索隔夜美股AI标的最新异动归因与SEC 8-K公告，按照 templates/morning_report.md 格式输出今日A股开盘前瞻早报。

# 方案 B：每天工作日早晨 08:30 自动推送早报
/schedule 30 8 * * 1-5 检索隔夜美股AI标的最新异动归因与SEC 8-K公告，按照 templates/morning_report.md 格式输出今日A股开盘前瞻早报。
```

---

## 🛠️ 集中标的库 (`tickers.json`) 的维护与扩展

若你需要添加新的关注标的（例如美股新上市公司、台股核心零组件或 A 股新切入标的），只需直接编辑 [`tickers.json`](./tickers.json)：

```json
{
  "symbol": "NEW_TICKER",
  "full_symbol": "NEW_TICKER.US",
  "name": "Company Name",
  "name_cn": "公司中文名",
  "sector": "Sector Category",
  "sector_cn": "中文业务描述"
}
```

保存后，Python 数据抓取脚本 `scripts/fetch_overnight_data.py` 和 Agent 语义分析会自动读取新标的，**无需改动任何代码**。

---

## 📦 安装与部署指南

在 Antigravity / AGY 环境中运行：

```bash
npx skills add https://github.com/morrain/ai-hardware-analyst.git
```

---

## 📁 完整目录结构说明

```text
ai-hardware-analyst/
├── README.md                          # 本文档
├── tickers.json                       # [Single Source of Truth] 全量标的集中唯一配置文件
├── SKILL.md                          # Skill 核心调度规范与防偏差数据铁律
├── scripts/
│   └── fetch_overnight_data.py       # [Python CLI] 自动读取 tickers.json 抓取行情与新闻
├── references/                       # 深度产业链知识库字典
│   ├── us_market_capex.md            # 美股 CSP Capex 指引与核心芯片映射
│   ├── tw_market_supplychain.md      # 台股月度营收、CoWoS/封装测试/PCB基材高频数据
│   ├── cn_market_elasticity.md       # A股光模块/液冷/组装弹性及时间错配法则
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
