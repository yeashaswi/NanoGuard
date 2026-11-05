# Book 5: Theoretical SCADA Architectures & Regulatory Standards

> **Note**: This chapter examines how real-world industrial environmental monitoring and SCADA abatement systems are structured conceptually. NanoGuard is a software study/simulation and does not interface with physical factory machinery.

In high-volume manufacturing facilities, environmental telemetry systems must translate sensor readings into automated monitoring and compliance workflows. This section reviews relevant environmental thresholds and conceptual telemetry architectures.

---

## 1. Global Environmental & Occupational Standards

| Pollutant Class | CPCB Ambient Standard ($\mu\text{g/m}^3$) | OSHA Permissible Exposure Limit ($\mu\text{g/m}^3$) | Primary Target Organ System |
| :--- | :--- | :--- | :--- |
| **Titanium Dioxide ($\text{TiO}_2$)** | 100.0 | 250.0 | Respiratory Tract (Alveolar Deposition) |
| **Zinc Oxide ($\text{ZnO}$)** | 80.0 | 200.0 | Pulmonary Vasculature ("Metal Fume Fever") |
| **Copper Oxide ($\text{CuO}$)** | 50.0 | 150.0 | Cellular DNA / Liver / ROS Peroxidation |
| **Nano-Silver ($\text{Ag-NP}$)** | 25.0 | 75.0 | Biological Membranes / Aquatic Ecotoxicity |
| **Carbon Soot** | 60.0 | 180.0 | Chronic Bronchial / Alveolar Retention |
| **Silica ($\text{SiO}_2$)** | 90.0 | 220.0 | Interstitial Lung Tissue (Silicosis) |
| **Ambient Baseline (Clean)** | 15.0 | 50.0 | Background Control |

---

## 2. Conceptual Multi-Tier Hazard Escalation Matrix

A conceptual multi-tier regulatory triage pipeline:

```
Concentration
     ▲
     │  Tier 4: CRITICAL (C > OSHA PEL)
     │  Action: Automatic Pneumatic Damper Isolation & Emergency Line Shutoff
PEL  ┼───────────────────────────────────────────────────────────────────────
     │  Tier 3: HAZARDOUS (CPCB Limit < C ≤ OSHA PEL)
     │  Action: Maximize Electrostatic Precipitator & Pulse-Jet Scrubber Flush
CPCB ┼───────────────────────────────────────────────────────────────────────
     │  Tier 2: MODERATE (0.5 CPCB < C ≤ CPCB)
     │  Action: Flag Telemetry Log & Trigger Predictive Maintenance Alert
     │  Tier 1: SAFE (C ≤ 0.5 CPCB)
  0  ┴───────────────────────────────────────────────────────────────────────► Time
```

### Action Protocols by Chemical Class
* **$\text{TiO}_2$ Breach**: Increase Electrostatic Precipitator (ESP) corona voltage by $+15\text{ kV}$; engage secondary PTFE membrane bypass.
* **$\text{ZnO}$ Breach**: Activate wet scrubber alkaline dosing pump ($\text{pH} = 9.2$); inspect pulse-jet baghouse filter cloth integrity.
* **$\text{CuO}$ Breach**: Emergency protocol: Halt smelting furnace induction feed; isolate ductwork with pneumatic seal; activate HEPA line.
* **$\text{Ag-NP}$ Breach**: Critical containment breach: Divert exhaust to catalytic activated carbon bed; isolate cleanroom recirculating fans.
* **Carbon Soot Breach**: Modulate burner air-to-fuel ratio ($\lambda \uparrow 1.15$); initiate automatic pulse-jet sonic clearing of filter hoppers.
* **$\text{SiO}_2$ Breach**: Initiate high-pressure water mist cyclone suppression; inspect cyclone separator differential pressure ($\Delta P$).

---

## 3. Real-Time Telemetry & SCADA Integration

In factory process automation (SCADA / PLC systems), communication occurs via industrial protocols:
* **Modbus TCP / RTU**: Sensor readings sampled every $200\text{ ms}$ over RS-485 or Ethernet.
* **MQTT / OPC-UA**: Lightweight JSON telemetry payloads streamed to edge gateways.
* **Pneumatic Interlocks**: Hardwired digital output relays triggering fail-closed isolation dampers within $< 100\text{ ms}$ of a `CRITICAL` prediction.

---

## 4. Edge Deployment Strategies

Deploying an ML model in factory environments requires ultra-low latency and zero downtime:
1. **Python / FastAPI / Docker**: Suited for local SCADA servers and on-premise industrial PCs.
2. **WebAssembly / ONNX Runtime / Pure TypeScript**: Allows running the inference engine directly inside browser dashboards and edge serverless platforms (e.g. Vercel) without external server dependencies.
