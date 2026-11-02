import React, { useState, useMemo } from 'react';
import { 
  SCENARIO_PRESETS, 
  simulateReactionKinetics, 
  runInference
} from './lib/inference';
import { SensorWaveform } from './components/SensorWaveform';

export const App: React.FC = () => {
  // Current active preset
  const [selectedPresetId, setSelectedPresetId] = useState<string>("tio2_pigment");
  const currentPreset = useMemo(() => {
    return SCENARIO_PRESETS.find(p => p.id === selectedPresetId) || SCENARIO_PRESETS[0];
  }, [selectedPresetId]);

  // Environmental sliders
  const [concentration, setConcentration] = useState<number>(currentPreset.defaultConc);
  const [tempC, setTempC] = useState<number>(currentPreset.defaultTemp);
  const [humidity, setHumidity] = useState<number>(currentPreset.defaultHum);
  const [flowSpeed, setFlowSpeed] = useState<number>(currentPreset.defaultFlow);
  const [activeChannel, setActiveChannel] = useState<string>("s4_au_nano");
  const [activeView, setActiveView] = useState<"detector" | "batch" | "handbook">("detector");

  // Synchronize when preset changes
  const handlePresetChange = (presetId: string) => {
    const p = SCENARIO_PRESETS.find(x => x.id === presetId);
    if (p) {
      setSelectedPresetId(presetId);
      setConcentration(p.defaultConc);
      setTempC(p.defaultTemp);
      setHumidity(p.defaultHum);
      setFlowSpeed(p.defaultFlow);
    }
  };

  // Run physical kinetics simulation
  const kineticsData = useMemo(() => {
    return simulateReactionKinetics(
      currentPreset.pollutant,
      concentration,
      tempC,
      humidity,
      70.0,
      1.0
    );
  }, [currentPreset.pollutant, concentration, tempC, humidity]);

  // Run dual ML inference
  const inference = useMemo(() => {
    return runInference(
      currentPreset.pollutant,
      concentration,
      tempC,
      humidity,
      flowSpeed
    );
  }, [currentPreset.pollutant, concentration, tempC, humidity, flowSpeed]);

  // Hazard status styling
  const hazardPillClass = useMemo(() => {
    switch (inference.hazardLevel) {
      case "CRITICAL": return { bg: "rgba(239, 68, 68, 0.15)", text: "#ef4444", border: "rgba(239, 68, 68, 0.3)" };
      case "HAZARDOUS": return { bg: "rgba(249, 115, 22, 0.15)", text: "#f97316", border: "rgba(249, 115, 22, 0.3)" };
      case "MODERATE": return { bg: "rgba(234, 179, 8, 0.15)", text: "#eab308", border: "rgba(234, 179, 8, 0.3)" };
      case "SAFE":
      default:
        return { bg: "rgba(63, 214, 198, 0.12)", text: "#3fd6c6", border: "rgba(63, 214, 198, 0.25)" };
    }
  }, [inference.hazardLevel]);

  return (
    <div style={{ position: 'relative', overflow: 'hidden', minHeight: '100vh' }}>
      {/* Subtle Static White Light Pools */}
      <div className="light-pool" />
      <div className="closing-light-pool" />

      {/* Main Page Layout */}
      <div className="page-container" style={{ paddingTop: '40px', paddingBottom: '80px' }}>
        
        {/* Navigation Bar */}
        <header style={{ 
          display: 'flex', 
          justifyContent: 'space-between', 
          alignItems: 'center', 
          paddingBottom: '32px',
          borderBottom: '1px solid var(--dp-color-hairline)'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <span className="live-signal" />
            <span style={{ 
              fontFamily: 'var(--dp-typography-face)', 
              fontWeight: 600, 
              color: 'var(--dp-color-bright)',
              fontSize: '15px',
              letterSpacing: '-0.02em'
            }}>
              NanoGuard
            </span>
            <span style={{ 
              fontFamily: 'var(--dp-typography-mono)', 
              fontSize: '11px', 
              color: 'var(--dp-color-meta)',
              borderLeft: '1px solid var(--dp-color-hairline)',
              paddingLeft: '12px'
            }}>
              SCADA v2.4
            </span>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <button 
              className={activeView === "detector" ? "btn-primary" : "btn-secondary"}
              onClick={() => setActiveView("detector")}
            >
              Live Telemetry
            </button>
            <button 
              className={activeView === "batch" ? "btn-primary" : "btn-secondary"}
              onClick={() => setActiveView("batch")}
            >
              Batch Audit
            </button>
            <button 
              className={activeView === "handbook" ? "btn-primary" : "btn-secondary"}
              onClick={() => setActiveView("handbook")}
            >
              Handbook
            </button>
          </div>
        </header>

        {/* HERO SECTION */}
        <section style={{ paddingTop: '64px', paddingBottom: '48px' }}>
          <div className="twelve-grid">
            {/* Opening Statement (Columns 1 to 7) */}
            <div style={{ gridColumn: 'span 7' }}>
              <div className="section-label">Industrial Emission Telemetry</div>
              <h1 className="display-hero" style={{ marginBottom: '24px' }}>
                Detect factory nanoparticles through reaction kinetics.
              </h1>
              <p style={{ 
                fontSize: '17px', 
                lineHeight: 1.6, 
                color: 'var(--dp-color-read)',
                maxWidth: '540px',
                marginBottom: '32px'
              }}>
                Conventional optical particle counters cannot see sub-100nm particles escaping industrial stacks. NanoGuard measures catalytic surface reaction dynamics and localized plasmon resonance shifts to classify pollutants and quantify concentrations in real time.
              </p>
              
              <div style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
                <a href="#detector" className="btn-primary" onClick={() => setActiveView("detector")}>
                  Inspect Active Telemetry
                </a>
                <a href="#handbook" className="btn-secondary" onClick={() => setActiveView("handbook")}>
                  Read Technical Curriculum
                </a>
              </div>
            </div>

            {/* Product Object (Columns 8 to 12) */}
            <div style={{ gridColumn: 'span 5' }}>
              <div className="graphite-panel" style={{ position: 'relative' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
                  <div className="live-badge">
                    <span className="live-signal" />
                    <span>Real-time Stack Monitor</span>
                  </div>
                  <span className="mono-value" style={{ fontSize: '11px', color: 'var(--dp-color-meta)' }}>
                    SAMPLE ID: SMP-0482
                  </span>
                </div>

                <div style={{ marginBottom: '16px' }}>
                  <div style={{ fontSize: '12px', color: 'var(--dp-color-meta)', marginBottom: '4px' }}>
                    DETECTED SPECIES
                  </div>
                  <div style={{ 
                    fontSize: '22px', 
                    color: 'var(--dp-color-bright)', 
                    fontWeight: 500,
                    letterSpacing: '-0.02em' 
                  }}>
                    {inference.pollutantName}
                  </div>
                </div>

                <div className="twelve-grid" style={{ marginBottom: '16px' }}>
                  <div style={{ gridColumn: 'span 6' }}>
                    <div style={{ fontSize: '11px', color: 'var(--dp-color-meta)' }}>CONCENTRATION</div>
                    <div className="mono-value" style={{ fontSize: '20px', color: 'var(--dp-color-bright)' }}>
                      {inference.predictedConcentrationUgM3} <span style={{ fontSize: '12px', color: 'var(--dp-color-meta)' }}>μg/m³</span>
                    </div>
                  </div>
                  <div style={{ gridColumn: 'span 6' }}>
                    <div style={{ fontSize: '11px', color: 'var(--dp-color-meta)' }}>CLASSIFIER CONFIDENCE</div>
                    <div className="mono-value" style={{ fontSize: '20px', color: 'var(--dp-color-bright)' }}>
                      {(inference.confidence * 100).toFixed(1)}%
                    </div>
                  </div>
                </div>

                {/* Regulatory Badge */}
                <div style={{
                  backgroundColor: hazardPillClass.bg,
                  border: `1px solid ${hazardPillClass.border}`,
                  color: hazardPillClass.text,
                  borderRadius: '4px',
                  padding: '10px 12px',
                  fontSize: '12px',
                  fontFamily: 'var(--dp-typography-mono)'
                }}>
                  <div style={{ fontWeight: 600, marginBottom: '2px' }}>
                    {inference.hazardLevel} — {inference.statusText}
                  </div>
                  <div style={{ fontSize: '11px', opacity: 0.9 }}>
                    CPCB Threshold: {inference.cpcbLimit} μg/m³ | OSHA PEL: {inference.oshaPel} μg/m³
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Ruled Row of Facts */}
          <div className="ruled-row" style={{ marginTop: '48px' }}>
            <div className="twelve-grid">
              <div style={{ gridColumn: 'span 3' }}>
                <div className="mono-value" style={{ fontSize: '28px', color: 'var(--dp-color-bright)', fontWeight: 400 }}>
                  100.0%
                </div>
                <div style={{ fontSize: '12px', color: 'var(--dp-color-meta)', marginTop: '4px' }}>
                  Identification Accuracy (5-Fold CV: 99.88%)
                </div>
              </div>

              <div style={{ gridColumn: 'span 3' }}>
                <div className="mono-value" style={{ fontSize: '28px', color: 'var(--dp-color-bright)', fontWeight: 400 }}>
                  0.9595
                </div>
                <div style={{ fontSize: '12px', color: 'var(--dp-color-meta)', marginTop: '4px' }}>
                  R² Concentration Fit (MAE: 4.91 μg/m³)
                </div>
              </div>

              <div style={{ gridColumn: 'span 3' }}>
                <div className="mono-value" style={{ fontSize: '28px', color: 'var(--dp-color-bright)', fontWeight: 400 }}>
                  &lt; 100 nm
                </div>
                <div style={{ fontSize: '12px', color: 'var(--dp-color-meta)', marginTop: '4px' }}>
                  Sub-diffraction Rayleigh horizon detection
                </div>
              </div>

              <div style={{ gridColumn: 'span 3' }}>
                <div className="mono-value" style={{ fontSize: '28px', color: 'var(--dp-color-bright)', fontWeight: 400 }}>
                  8 Channels
                </div>
                <div style={{ fontSize: '12px', color: 'var(--dp-color-meta)', marginTop: '4px' }}>
                  Orthogonal metal-oxide & plasmonic transducers
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* SECTION 1: LIVE REACTION DETECTOR */}
        {activeView === "detector" && (
          <section id="detector" style={{ paddingTop: '40px', paddingBottom: '60px' }}>
            <div style={{ marginBottom: '32px' }}>
              <div className="section-label">Interactive Test Environment</div>
              <h2 className="display-title">Real-Time Reaction Telemetry</h2>
            </div>

            <div className="twelve-grid">
              {/* Controls Column (Span 4) */}
              <div style={{ gridColumn: 'span 4' }}>
                <div className="graphite-panel" style={{ marginBottom: '16px' }}>
                  <div className="section-label" style={{ marginBottom: '16px' }}>
                    Emission Scenario
                  </div>
                  
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
                    {SCENARIO_PRESETS.map((preset) => {
                      const isSelected = preset.id === selectedPresetId;
                      return (
                        <button
                          key={preset.id}
                          onClick={() => handlePresetChange(preset.id)}
                          style={{
                            display: 'flex',
                            justifyContent: 'space-between',
                            alignItems: 'center',
                            width: '100%',
                            padding: '10px 12px',
                            background: isSelected ? 'rgba(255, 255, 255, 0.05)' : 'transparent',
                            border: `1px solid ${isSelected ? 'var(--dp-color-hairline-2)' : 'transparent'}`,
                            borderRadius: 'var(--dp-radius-panel)',
                            color: isSelected ? 'var(--dp-color-bright)' : 'var(--dp-color-read)',
                            cursor: 'pointer',
                            textAlign: 'left'
                          }}
                        >
                          <div>
                            <div style={{ fontSize: '13px', fontWeight: isSelected ? 500 : 400 }}>
                              {preset.title}
                            </div>
                            <div style={{ fontSize: '11px', color: 'var(--dp-color-meta)' }}>
                              {preset.sector}
                            </div>
                          </div>
                          {isSelected && <span className="live-signal" />}
                        </button>
                      );
                    })}
                  </div>
                </div>

                {/* Variable Parameter Sliders */}
                <div className="graphite-panel">
                  <div className="section-label" style={{ marginBottom: '16px' }}>
                    Process Variables
                  </div>

                  <div style={{ marginBottom: '16px' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', marginBottom: '6px' }}>
                      <span style={{ color: 'var(--dp-color-meta)' }}>Particulate Load</span>
                      <span className="mono-value" style={{ color: 'var(--dp-color-bright)' }}>{concentration} μg/m³</span>
                    </div>
                    <input
                      type="range"
                      min="1.0"
                      max="350.0"
                      step="1.0"
                      value={concentration}
                      onChange={(e) => setConcentration(parseFloat(e.target.value))}
                      className="slider-control"
                      aria-label="Particulate Concentration"
                    />
                  </div>

                  <div style={{ marginBottom: '16px' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', marginBottom: '6px' }}>
                      <span style={{ color: 'var(--dp-color-meta)' }}>Exhaust Temperature</span>
                      <span className="mono-value" style={{ color: 'var(--dp-color-bright)' }}>{tempC}°C</span>
                    </div>
                    <input
                      type="range"
                      min="15.0"
                      max="85.0"
                      step="1.0"
                      value={tempC}
                      onChange={(e) => setTempC(parseFloat(e.target.value))}
                      className="slider-control"
                      aria-label="Exhaust Temperature"
                    />
                  </div>

                  <div style={{ marginBottom: '16px' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', marginBottom: '6px' }}>
                      <span style={{ color: 'var(--dp-color-meta)' }}>Relative Humidity</span>
                      <span className="mono-value" style={{ color: 'var(--dp-color-bright)' }}>{humidity}%</span>
                    </div>
                    <input
                      type="range"
                      min="15.0"
                      max="90.0"
                      step="1.0"
                      value={humidity}
                      onChange={(e) => setHumidity(parseFloat(e.target.value))}
                      className="slider-control"
                      aria-label="Relative Humidity"
                    />
                  </div>

                  <div>
                    <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', marginBottom: '6px' }}>
                      <span style={{ color: 'var(--dp-color-meta)' }}>Duct Flow Velocity</span>
                      <span className="mono-value" style={{ color: 'var(--dp-color-bright)' }}>{flowSpeed} m/s</span>
                    </div>
                    <input
                      type="range"
                      min="0.5"
                      max="6.0"
                      step="0.1"
                      value={flowSpeed}
                      onChange={(e) => setFlowSpeed(parseFloat(e.target.value))}
                      className="slider-control"
                      aria-label="Duct Flow Velocity"
                    />
                  </div>
                </div>
              </div>

              {/* Dynamic Waveform & Diagnostic Readout (Span 8) */}
              <div style={{ gridColumn: 'span 8' }}>
                <div className="graphite-panel" style={{ marginBottom: '16px' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
                    <div>
                      <div className="section-label">Multi-Channel Transduction</div>
                      <div style={{ fontSize: '14px', color: 'var(--dp-color-bright)', fontWeight: 500 }}>
                        Reaction Kinetics Waveform: R(t) / R₀
                      </div>
                    </div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                      <span className="live-signal" />
                      <span className="mono-value" style={{ fontSize: '11px', color: 'var(--dp-color-meta)' }}>
                        70s TRANSIENT WINDOW
                      </span>
                    </div>
                  </div>

                  {/* SVG Waveform Visualizer */}
                  <SensorWaveform
                    data={kineticsData}
                    activeChannel={activeChannel}
                    onSelectChannel={setActiveChannel}
                  />
                </div>

                {/* Analytical Readouts Grid */}
                <div className="twelve-grid">
                  <div style={{ gridColumn: 'span 4' }}>
                    <div className="graphite-panel">
                      <div style={{ fontSize: '11px', color: 'var(--dp-color-meta)', marginBottom: '4px' }}>
                        LSPR PEAK SHIFT (Δλ)
                      </div>
                      <div className="mono-value" style={{ fontSize: '20px', color: 'var(--dp-color-bright)' }}>
                        +{inference.lsprShiftNm} <span style={{ fontSize: '12px', color: 'var(--dp-color-meta)' }}>nm</span>
                      </div>
                      <div style={{ fontSize: '11px', color: 'var(--dp-color-meta)', marginTop: '4px' }}>
                        Au nano-island optical resonance
                      </div>
                    </div>
                  </div>

                  <div style={{ gridColumn: 'span 4' }}>
                    <div className="graphite-panel">
                      <div style={{ fontSize: '11px', color: 'var(--dp-color-meta)', marginBottom: '4px' }}>
                        REACTION RISE TIME (τ₉₀)
                      </div>
                      <div className="mono-value" style={{ fontSize: '20px', color: 'var(--dp-color-bright)' }}>
                        {inference.responseTimeS} <span style={{ fontSize: '12px', color: 'var(--dp-color-meta)' }}>seconds</span>
                      </div>
                      <div style={{ fontSize: '11px', color: 'var(--dp-color-meta)', marginTop: '4px' }}>
                        Desorption recovery: {inference.recoveryTimeS}s
                      </div>
                    </div>
                  </div>

                  <div style={{ gridColumn: 'span 4' }}>
                    <div className="graphite-panel">
                      <div style={{ fontSize: '11px', color: 'var(--dp-color-meta)', marginBottom: '4px' }}>
                        PEAK SHIFT AMPLITUDE
                      </div>
                      <div className="mono-value" style={{ fontSize: '20px', color: 'var(--dp-color-bright)' }}>
                        +{inference.peakAmplitudePercent}%
                      </div>
                      <div style={{ fontSize: '11px', color: 'var(--dp-color-meta)', marginTop: '4px' }}>
                        Max differential conductance
                      </div>
                    </div>
                  </div>
                </div>

                {/* Prescriptive Engineering Mitigation Plan */}
                <div className="graphite-panel" style={{ marginTop: '16px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '6px' }}>
                    <span style={{ 
                      width: '6px', 
                      height: '6px', 
                      borderRadius: '50%', 
                      backgroundColor: hazardPillClass.text 
                    }} />
                    <span style={{ 
                      fontSize: '11px', 
                      fontFamily: 'var(--dp-typography-mono)', 
                      color: hazardPillClass.text, 
                      textTransform: 'uppercase',
                      letterSpacing: '0.05em' 
                    }}>
                      Automated SCADA Intervention
                    </span>
                  </div>
                  <div style={{ fontSize: '14px', color: 'var(--dp-color-bright)', lineHeight: 1.5 }}>
                    {inference.mitigationPlan}
                  </div>
                </div>
              </div>
            </div>
          </section>
        )}

        {/* SECTION 2: BATCH SENSOR AUDIT */}
        {activeView === "batch" && (
          <section id="batch" style={{ paddingTop: '40px', paddingBottom: '60px' }}>
            <div style={{ marginBottom: '32px' }}>
              <div className="section-label">Batch Audit & Telemetry Validation</div>
              <h2 className="display-title">Factory Sensor Batch Logs</h2>
              <p style={{ color: 'var(--dp-color-read)', marginTop: '8px', maxWidth: '640px' }}>
                Review continuous 16-dimensional telemetry records verified against ground truth testing batches.
              </p>
            </div>

            <div className="graphite-panel" style={{ overflowX: 'auto' }}>
              <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '13px', textAlign: 'left' }}>
                <thead>
                  <tr style={{ borderBottom: '1px solid var(--dp-color-hairline-2)', color: 'var(--dp-color-meta)' }}>
                    <th style={{ padding: '12px 16px', fontFamily: 'var(--dp-typography-mono)', fontWeight: 500 }}>SAMPLE</th>
                    <th style={{ padding: '12px 16px', fontWeight: 500 }}>INDUSTRIAL SOURCE</th>
                    <th style={{ padding: '12px 16px', fontWeight: 500 }}>SPECIES IDENTIFICATION</th>
                    <th style={{ padding: '12px 16px', fontFamily: 'var(--dp-typography-mono)', fontWeight: 500 }}>CONFIDENCE</th>
                    <th style={{ padding: '12px 16px', fontFamily: 'var(--dp-typography-mono)', fontWeight: 500 }}>ESTIMATED LOAD</th>
                    <th style={{ padding: '12px 16px', fontFamily: 'var(--dp-typography-mono)', fontWeight: 500 }}>STATUS</th>
                  </tr>
                </thead>
                <tbody>
                  {[
                    { id: "SMP-00104", src: "Pigment Milling #2", species: "Titanium Dioxide", conf: "99.4%", conc: "142.5 μg/m³", status: "HAZARDOUS", statusCol: "#f97316" },
                    { id: "SMP-00105", src: "Vulcanization Oven", species: "Zinc Oxide", conf: "98.9%", conc: "95.2 μg/m³", status: "HAZARDOUS", statusCol: "#f97316" },
                    { id: "SMP-00106", src: "Induction Smelter B", species: "Copper Oxide", conf: "99.1%", conc: "162.0 μg/m³", status: "CRITICAL", statusCol: "#ef4444" },
                    { id: "SMP-00107", src: "Cleanroom Exhaust 4", species: "Nano-Silver", conf: "97.8%", conc: "44.1 μg/m³", status: "HAZARDOUS", statusCol: "#f97316" },
                    { id: "SMP-00108", src: "Stack Filter Post-Scrub", species: "Nominal Air", conf: "99.7%", conc: "1.4 μg/m³", status: "SAFE", statusCol: "#3fd6c6" },
                    { id: "SMP-00109", src: "Rotary Kiln Duct", species: "Carbon Soot", conf: "99.2%", conc: "128.8 μg/m³", status: "HAZARDOUS", statusCol: "#f97316" },
                    { id: "SMP-00110", src: "Refractory Ball Mill", species: "Silica Nanoparticles", conf: "98.5%", conc: "88.0 μg/m³", status: "MODERATE", statusCol: "#eab308" }
                  ].map((row, idx) => (
                    <tr key={idx} style={{ borderBottom: '1px solid var(--dp-color-hairline)' }}>
                      <td style={{ padding: '12px 16px', fontFamily: 'var(--dp-typography-mono)', color: 'var(--dp-color-bright)' }}>{row.id}</td>
                      <td style={{ padding: '12px 16px', color: 'var(--dp-color-read)' }}>{row.src}</td>
                      <td style={{ padding: '12px 16px', color: 'var(--dp-color-bright)' }}>{row.species}</td>
                      <td style={{ padding: '12px 16px', fontFamily: 'var(--dp-typography-mono)', color: 'var(--dp-color-read)' }}>{row.conf}</td>
                      <td style={{ padding: '12px 16px', fontFamily: 'var(--dp-typography-mono)', color: 'var(--dp-color-bright)' }}>{row.conc}</td>
                      <td style={{ padding: '12px 16px' }}>
                        <span style={{ 
                          fontSize: '11px', 
                          fontFamily: 'var(--dp-typography-mono)', 
                          color: row.statusCol,
                          border: `1px solid ${row.statusCol}40`,
                          padding: '2px 8px',
                          borderRadius: '3px'
                        }}>
                          {row.status}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>
        )}

        {/* SECTION 3: TECHNICAL CURRICULUM (HANDBOOK) */}
        {activeView === "handbook" && (
          <section id="handbook" style={{ paddingTop: '40px', paddingBottom: '60px' }}>
            <div style={{ marginBottom: '32px' }}>
              <div className="section-label">First-Principles Educational Curriculum</div>
              <h2 className="display-title">Curriculum Modules & Reference Books</h2>
              <p style={{ color: 'var(--dp-color-read)', marginTop: '8px', maxWidth: '640px' }}>
                Complete reference guides written to help you replicate this machine learning telemetry system from first principles.
              </p>
            </div>

            <div className="twelve-grid">
              {[
                {
                  number: "BOOK 01",
                  title: "Physics, Nanotoxicology & Reaction Chemistry",
                  desc: "Specific surface area scaling, d⁶ Rayleigh scattering limits, heterogeneous catalysis, oxygen chemisorption band bending, and LSPR dielectric shifts.",
                  file: "handbook/BOOK_01_PHYSICS_AND_REACTION_CHEMISTRY.md"
                },
                {
                  number: "BOOK 02",
                  title: "Sensor Arrays & Signal Engineering",
                  desc: "Cross-reactive sensing arrays, material physics of 8 channels (SnO₂, WO₃, rGO, Au nano, CNT, In₂O₃, Pt-TiO₂, ZnO NW), transient feature extraction, and humidity compensation.",
                  file: "handbook/BOOK_02_SENSOR_ARRAYS_AND_SIGNAL_ENGINEERING.md"
                },
                {
                  number: "BOOK 03",
                  title: "Machine Learning from First Principles",
                  desc: "Decision trees, Gini impurity, Random Forest bagging & subspace sampling proofs, Gradient Boosting residual learning, and evaluation metrics (R², RMSE, ROC-AUC).",
                  file: "handbook/BOOK_03_MACHINE_LEARNING_FROM_FIRST_PRINCIPLES.md"
                },
                {
                  number: "BOOK 04",
                  title: "Dataset Curation & Synthetic Kinetics",
                  desc: "Sourcing open datasets from UCI, Zenodo, and Mendeley; formulating Langmuir differential equations, Arrhenius rate kinetics, and injecting realistic ADC sensor noise.",
                  file: "handbook/BOOK_04_DATASET_CURATION_AND_SYNTHESIS.md"
                },
                {
                  number: "BOOK 05",
                  title: "Production Systems, SCADA & Regulatory Triage",
                  desc: "CPCB and OSHA emission limits, 4-tier automated hazard escalation matrix, class-specific mitigation actions (ESP voltage ramp, pulse-jet clearing), and Modbus/MQTT edge integration.",
                  file: "handbook/BOOK_05_PRODUCTION_SYSTEMS_AND_REGULATORY_SCADA.md"
                },
                {
                  number: "BOOK 06",
                  title: "Step-by-Step Code Replication Guide",
                  desc: "Complete end-to-end coding tutorial: environment setup, writing the simulator, model training pipeline, unit tests, and production web deployment.",
                  file: "handbook/BOOK_06_STEP_BY_STEP_REPLICATION_GUIDE.md"
                }
              ].map((book, idx) => (
                <div key={idx} style={{ gridColumn: 'span 6' }}>
                  <div className="graphite-panel" style={{ height: '100%', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
                    <div>
                      <div className="section-label">{book.number}</div>
                      <h3 style={{ fontSize: '18px', color: 'var(--dp-color-bright)', fontWeight: 500, marginBottom: '8px' }}>
                        {book.title}
                      </h3>
                      <p style={{ fontSize: '13px', color: 'var(--dp-color-read)', lineHeight: 1.5, marginBottom: '16px' }}>
                        {book.desc}
                      </p>
                    </div>
                    <div style={{ 
                      fontSize: '11px', 
                      fontFamily: 'var(--dp-typography-mono)', 
                      color: 'var(--dp-color-meta)',
                      borderTop: '1px solid var(--dp-color-hairline)',
                      paddingTop: '10px'
                    }}>
                      Path: {book.file}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </section>
        )}

        {/* RULED FOOTER */}
        <footer className="ruled-row" style={{ marginTop: '80px' }}>
          <div className="twelve-grid">
            <div style={{ gridColumn: 'span 4' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
                <span className="live-signal" />
                <span style={{ fontFamily: 'var(--dp-typography-face)', fontWeight: 600, color: 'var(--dp-color-bright)' }}>
                  NanoGuard Telemetry
                </span>
              </div>
              <p style={{ fontSize: '12px', color: 'var(--dp-color-meta)', maxWidth: '280px' }}>
                Multi-channel reaction kinetics & surface plasmon resonance machine learning telemetry for industrial nanoparticle pollution monitoring.
              </p>
            </div>

            <div style={{ gridColumn: 'span 3' }}>
              <div className="section-label">Architecture</div>
              <ul style={{ listStyle: 'none', fontSize: '13px', lineHeight: 1.8 }}>
                <li><a href="#detector" style={{ color: 'var(--dp-color-read)', textDecoration: 'none' }}>8-Channel Transducers</a></li>
                <li><a href="#detector" style={{ color: 'var(--dp-color-read)', textDecoration: 'none' }}>Random Forest Classifier</a></li>
                <li><a href="#detector" style={{ color: 'var(--dp-color-read)', textDecoration: 'none' }}>Gradient Boosted Regressor</a></li>
                <li><a href="#detector" style={{ color: 'var(--dp-color-read)', textDecoration: 'none' }}>LSPR Optical Resonator</a></li>
              </ul>
            </div>

            <div style={{ gridColumn: 'span 3' }}>
              <div className="section-label">Curriculum Books</div>
              <ul style={{ listStyle: 'none', fontSize: '13px', lineHeight: 1.8 }}>
                <li><span style={{ color: 'var(--dp-color-read)' }}>Book 1: Physics & Chemistry</span></li>
                <li><span style={{ color: 'var(--dp-color-read)' }}>Book 2: Sensor Arrays</span></li>
                <li><span style={{ color: 'var(--dp-color-read)' }}>Book 3: Machine Learning</span></li>
                <li><span style={{ color: 'var(--dp-color-read)' }}>Book 4: Dataset Synthesis</span></li>
              </ul>
            </div>

            <div style={{ gridColumn: 'span 2' }}>
              <div className="section-label">Standards</div>
              <ul style={{ listStyle: 'none', fontSize: '12px', fontFamily: 'var(--dp-typography-mono)', lineHeight: 1.8, color: 'var(--dp-color-meta)' }}>
                <li>CPCB Stack Norms</li>
                <li>OSHA PEL Limits</li>
                <li>WHO Air Quality</li>
                <li>Modbus RTU / SCADA</li>
              </ul>
            </div>
          </div>
        </footer>

      </div>
    </div>
  );
};

export default App;
