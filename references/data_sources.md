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
