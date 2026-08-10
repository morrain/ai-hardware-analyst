# 美股：技术策源与全球需求总量 (US Market Knowledge Base - 2026 Updated)

美股市场代表着全球 AI 算力架构的技术源头（IP & Chip Design）以及终端需求（Cloud Service Providers Capex）的总量沉淀。

---

## 1. 核心芯片与平台 (Compute & System Architects)

### 英伟达 (NVIDIA, NVDA)
- **架构代际演进路线**：
  - Hopper (H100/H200) → Blackwell (B100/B200/GB200/NVL72) → **Blackwell Ultra (B300/GB300, HBM3e 12H)** → **Vera Rubin (R100/Vera CPU/NVL144/HBM4)** → **Rubin Ultra (2027, 4 Dies/16 HBM4e)**.
- **Vera Rubin (R100) 核心技术参数**：
  - **工艺与封装**：台积电 3nm (N3P) 制程，CoWoS-L 先进封装。
  - **内存架构**：288GB HBM4 (2048-bit 接口，带宽提升至 22 TB/s)。
  - **网络与系统**：配搭 Arm 架构 Vera CPU，NVLink 6 单 GPU 带宽达到 3.6 TB/s；支持 NVL144 144芯片机柜集群；ConnectX-9 与 Spectrum-X Ethernet 硅光/CPO 整合。

### AMD (AMD)
- **产品线**：MI300X/MI325X 系列 → MI350/MI400 系列。
- **研判重点**：在非 NVDA 阵营（如 Meta, Microsoft, Oracle 等）的替代份额，HBM4 时代内存带宽比拼与开放光网络生态。

---

## 2. 核心基础设施、物理层芯片与高速扩展 (Interconnect, Power & Material)

### 博通 (Broadcom, AVGO) / 迈威尔 (Marvell, MRVL)
- **定位**：垄断级 DSP 电芯片、交换芯片 (Tomahawk 5/6, Jericho 3-X) 与定制 ASIC 领军者。
- **周期风向标**：
  - 800G 向 1.6T 可插拔光模块过渡，硅光子 (SiPh) 成为主力方案。
  - **CPO（光电共封装）与 TSMC COUPE 平台**：CPO 引擎直接装配在 switch ASIC 封装上，降低 3.5x-5x 功耗。
  - **自研 ASIC 提速**：承接 4 大 CSP (Google TPU v6, Meta MTIA, OpenAI 自研芯片) 的定制 ASIC 订单，在总 Capex 中份额持续抬升。

### 信号扩展与 Retimer / AEC：Astera Labs (ALAB) & Credo (CRDO)
- **Astera Labs (ALAB.US)**：PCIe 6.0 Retimer (Aries 系列) 及 Fabric Switch (Scorpio 系列) 绝对领军者。解决 CPU-GPU、GPU-NIC、CXL 存储通道在超大机柜中的信号衰减与重构。
- **Credo Semiconductor (CRDO.US)**：AEC (Active Electrical Cable 有源铜缆) 与 1.6T DSP / PCIe 6.0 重构芯片核心提供商。

### 物理层铜连接与散热/电源：Amphenol (APH), Vertiv (VRT) & Eaton (ETN)
- **安费诺 (Amphenol, APH)**：NVL72 / NVL144 机柜级 Backplane 铜连接（Overpass / Cartridge / Copper Cables）绝对龙头。
- **维谛技术 (Vertiv, VRT) & 伊顿 (Eaton, ETN)**：数据中心液冷 CDU (Cooling Distribution Unit)、冷板系统与 800V DC 直流高压电源/变压设备定价权者。单机柜功耗突破 120kW~200kW 时 800V 高压直流母线 (DC Busbar) 普及。
- **美超微 (Supermicro, SMCI.US)**：GPU 服务器集群交付大厂（需跟踪合规财报披露进度）。

### 材料变革：玻璃基板 (Glass Substrates)
- **趋势**：Intel、Samsung、SK Absolics 在 2026 进入试产阶段，解决 100mm+ 超大芯片的“翘曲墙”与高热损耗。

---

## 3. 终端需求总量：四大 CSP Capex 与 ASIC 比例

监控四大超大规模云厂商（Hyperscalers）季度财报中的 Capital Expenditures 及 GPU vs ASIC 结构：

1. **微软 (Microsoft, MSFT)**：Azure AI 算力集群建设、OpenAI 专属集群与 Maia 自研芯片。
2. **谷歌 (Google, GOOGL)**：TPU v5p/v6 定制芯片与 GPU 混合部署 Capex。
3. **亚马逊 (Amazon, AMZN)**：AWS Trainium/Inferentia 及第三方 NVDA 集群 Capex。
4. **Meta (META)**：Llama 3/4/5 训练所需的超级算力基础设施与 MTIA 自研芯片投入。

---

## 4. 时间错配推演法则

- **美股预期（Capex 指引 & NVDA/AVGO/ALAB 财报指引）**：先行指标，预示 3-4 个季度后的整体需求总量上限。
- **验证方法**：美股 Capex 与 Retimer 需求上修 → 传导至台股供应链月度营收放量（时延约 1-2 个季度）→ 传导至 A 股 1.6T 光模块/高阶 PCB 业绩对现。
