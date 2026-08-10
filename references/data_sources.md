# 官方监管与研报数据源规范 (Data Sources Protocol - 2026 Updated)

本指南规范了 Agent 在隔夜早报生成或重大事件解读时，检索并抓取官方监管（SEC 8-K/10-Q/10-K、台湾 MOPS）及专业研报社区（Seeking Alpha、华尔街大行评级）的查询语法与解析协议。

---

## 0. 单股精细价格搜索协议 (Single-Ticker Search Protocol - 防失真防假数字)

⚠️ **防幻觉铁律**：严禁将超过 3 只股票混在一句话里检索股价（例如 `Searched: "NVDA Broadcom TSM Micron Vertiv stock price"`），此类大泛搜索无法返回确切收盘数字，会导致大模型因信息缺失而产生假数据！

### 规范检索语法表

| 目的 | 推荐语法示例 | 解析与判定抓手 |
| :--- | :--- | :--- |
| **单股隔夜精准收盘价** | `[Ticker] stock close price [Date]`<br>例：`NVDA stock close price August 7 2026` | 必须直接提取显式的收盘数字与涨跌百分比（如 `$223.96 (+2.27%)`），无确切数字时触发二次定向补搜。 |
| **指数收盘价与大盘** | `Nasdaq Composite SOX index close [Date]` | 提取纳斯达克与费城半导体指数收盘点位。 |
| **单股隔夜异动新闻** | `site:seekingalpha.com [Ticker] stock overnight movement` | 定向分析特定大涨大跌标的的深层原因。 |

---

## 1. 官方法定监管披露源 (Legal Disclosures)

### 1.1 SEC 8-K (美国证监会临时重大事项表)
- **定位**：美股公司法律强制要求在发生重大突发事件（4个工作日内）提交的法定报告。
- **检索协议与语法**：
  - 查询语法：`site:sec.gov Form 8-K [Ticker]` 或 `[Company Name] SEC Form 8-K filing`
  - 核心抓手：Item 1.01 (Entry into a Material Definitive Agreement 签署重大合同)、Item 2.02 (Results of Operations 业绩公布)、Item 5.02 (高管离职变动)。

### 1.2 台湾公开资讯观测站 (MOPS)
- **定位**：台股上市公司每月 10 日前强制披露上月合并营收的官方平台。
- **检索协议与语法**：
  - 查询语法：`[公司名称或代号] 月度合并营收 MOPS` 或 `[公司代号] 营基月报`
  - 核心抓手：当月合并营收（新台币千元）、MoM 环比增幅、YoY 同比增幅。

---

## 2. 专业投研与大行评级源 (Research & Sentiment)

### 2.1 Seeking Alpha (SA 深度研报)
- **定位**：买卖方分析师对隔夜美股财报/重大事件的深度逻辑归因与评级调整平台。
- **检索协议与语法**：
  - 查询语法：`site:seekingalpha.com [Ticker] earnings analysis` 或 `Seeking Alpha [Ticker] analysis`
  - 核心抓手：Data Center 业务增速拆解、毛利率指引变化、目标价上修/下修理由。

### 2.2 华尔街大行隔夜评级 (Street Consensus)
- **定位**：高盛、大摩、美银、瑞银等机构盘前/盘后发出的 Rating & Price Target 变动。
- **检索协议与语法**：
  - 查询语法：`[Ticker] price target raised downgraded Goldman Sachs Morgan Stanley`
  - 核心抓手：目标价调整幅度、评级变动（Overweight / Equal-weight / Underweight）。

---

## 3. 高频行情与新闻快讯源 (Quotes & Wires)

### 3.1 雅虎财经 (Yahoo Finance)
- **检索协议与语法**：`site:finance.yahoo.com/quote/[Ticker]`
- **核心抓手**：收盘价、After-hours (盘后价)、Volume (成交量倍数)。

### 3.2 华尔街见闻 / 财联社 24h 快讯
- **检索协议与语法**：`site:wallstreetcn.com [标的/芯片] 隔夜`
- **核心抓手**：美联储官员表态、美商务部出口控制政策突发事件。

---

## 4. 全量数据源权威原始出处与直达链接范例 (Authoritative Portal Patterns)

> ⚠️ **动态防幻觉溯源铁律 (Dynamic Citation Protocol)**：
> 1. 本表中的 URL 仅作为通用检索入口模版（Portal Pattern）。
> 2. **真实引用必须取自 `search_web` 实时返回的真实 URL**：Agent 在报告或早报中引用任何 SEC 公告、Seeking Alpha 研报、台股营收或大行评级时，**必须强制在文中附带该次检索动态获取到的真实原网页 URL 链接 (Citations)**。
> 3. **严禁凭空伪造/拼凑 URL**：引用的 URL 必须 100% 来自于搜索引擎真实返回的字段，严禁猜测或臆造无法访问的假 HTML 文件路径！若检索摘要未暴露完整子页面 URL，统一标注 `[来源: 官方披露/公开检索]`。

| 数据源类型 | 机构 / 平台名称 | 入口 Portal 范例 URL 链接 | 数据权威度与解析用途 |
| :--- | :--- | :--- | :--- |
| **美股物理行情 API** | 新浪财经美股网关 | `http://hq.sinajs.cn/list=gb_nvda,gb_tsm,gb_mu,gb_lite` | 毫秒级批量物理价格，用于早报表单零 null 填充 |
| **美股大盘行情** | Yahoo Finance 专栏 | [Yahoo Finance NVDA](https://finance.yahoo.com/quote/NVDA)<br>[Yahoo Finance TSM](https://finance.yahoo.com/quote/TSM) | 官方个股收盘与盘后行情页面 |
| **SEC 法定监管** | 美国证监会 EDGAR | [SEC EDGAR Company Search](https://www.sec.gov/edgar/searchedgar/companysearch)<br>[NVIDIA SEC 8-K Archive](https://www.sec.gov/edgar/browse/?CIK=1045810) | 法定 8-K / 10-Q 重大合同与业绩备案原始出处 |
| **深度买卖方研报** | Seeking Alpha 专栏 | [Seeking Alpha NVDA Analysis](https://seekingalpha.com/symbol/NVDA/analysis)<br>[Seeking Alpha NVDA Earnings](https://seekingalpha.com/symbol/NVDA/earnings) | 机构买卖方深度逻辑与 Q2/Q3 业绩指引观点拆解 |
| **华尔街大行评级** | TipRanks / MarketWatch | [MarketWatch NVDA Analyst Estimates](https://www.marketwatch.com/investing/stock/nvda/analystestimates)<br>[TipRanks NVDA Forecast](https://www.tipranks.com/stocks/nvda/forecast) | 高盛、大摩、美银等大行目标价与评级一致性预期 |
| **台湾官方高频营收** | 台湾公开资讯观测站 (MOPS) | [MOPS 官方首页](https://mops.twse.com.tw/)<br>[MOPS IFRS 营基月报](https://mops.twse.com.tw/mops/web/t05st10_ifrs) | 台股鸿海(2317)、广达(2382)、健策(3653)月度合并营收官方原抓手 |


