# 美股：技术策源与全球需求总量 (US Market Knowledge Base)

美股市场代表着全球 AI 算力架构的技术源头（IP & Chip Design）以及终端需求（Cloud Service Providers Capex）的总量沉淀。

---

## 1. 核心芯片与平台 (Compute & System Architects)

### 英伟达 (NVIDIA, NVDA)
- **架构演进路线**：
  - Hopper (H100/H200) → Blackwell (B100/B200/GB200/NVL72) → Blackwell Ultra (B300/GB300) → Rubin (R100/NVL144/HBM4).
- **研判重点**：
  - 核心架构量产进度与放量瓶颈（CoWoS-L 产能约束、封测 Yield、液冷冷板漏液/CDU供应）。
  - 机柜形态占比：NVL72 vs NVL36 单柜 ASP 与 BOM 组件用量变化。

### AMD (AMD)
- **产品线**：MI300X/MI325X 系列 → MI350/MI400 系列。
- **研判重点**：在非 NVDA 阵营（如 Meta, Microsoft, Oracle 等）的替代份额，HBM 内存容量与带宽优势比拼。

---

## 2. 核心基础设施与物理层芯片 (Interconnect & Power/Cooling)

### 博通 (Broadcom, AVGO) / 迈威尔 (Marvell, MRVL)
- **定位**：垄断级 DSP 电芯片、交换芯片 (Tomahawk 5/6, Jericho 3-X) 与 ASIC 定制芯片领军者。
- **周期风向标**：
  - 800G 光模块向 1.6T 演进中的 DSP 芯片交货期。
  - CPO（光电共封装）、硅光子 (SiPh) 技术对传统可插拔光模块的侵蚀进度。

### 安费诺 (Amphenol, APH)
- **定位**：NVL72 机柜级 Backplane 铜互联（Overpass / Cartridge / Copper Cables）绝对龙头。
- **研判重点**：短距铜连接（DAC/ACC）在机柜内部对光纤连接的替代边界（如 2-3 米内无源铜缆绝对统治力）。

### 维谛技术 (Vertiv, VRT)
- **定位**：数据中心液冷 CDU (Cooling Distribution Unit)、冷板系统与高阶电源/PDU 定价权者。
- **研判重点**：单机柜功耗从 40kW (H100) 跃升升至 120kW+ (NVL72) 时，风冷向液冷（Direct-to-Chip / Immersion）渗透率与定价拉升。

---

## 3. 终端需求总量：四大 CSP Capex

监控四大超大规模云厂商（Hyperscalers）季度财报中的 Capital Expenditures 指引：

1. **微软 (Microsoft, MSFT)**：Azure AI 算力集群建设、OpenAI 专属集群扩张。
2. **谷歌 (Google, GOOGL)**：TPU v5p/v6 定制芯片与 GPU 混合部署 Capex。
3. **亚马逊 (Amazon, AMZN)**：AWS Trainium/Inferentia 及第三方 NVDA 集群 Capex。
4. **Meta (META)**：Llama 3/4 开源模型训练所需的超级算力基础设施投入。

---

## 4. 时间错配推演法则

- **美股预期（Capex 指引 & NVDA 财报指引）**：先行指标，预示 3-4 个季度后的整体需求总量上限。
- **验证方法**：美股发布 Capex 上修 → 传导至台股供应链月度营收放量（时延约 1-2 个季度）→ 传导至 A 股光模块/PCB 业绩对现。
