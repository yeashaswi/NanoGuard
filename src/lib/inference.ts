import { 
  PollutantKey, 
  PollutantProfile, 
  InferenceResult, 
  SensorKineticsData, 
  ScenarioPreset,
  HazardLevel 
} from "./types";

export const POLLUTANT_PROFILES: Record<PollutantKey, PollutantProfile> = {
  "TiO2": {
    name: "Titanium Dioxide",
    formula: "TiO₂",
    cpcbLimit: 100.0,
    oshaPel: 250.0,
    baseAffinity: [0.85, 0.45, 0.30, 0.25, 0.20, 0.40, 0.95, 0.35],
    respTimeRange: [14.0, 24.0],
    recTimeRange: [35.0, 60.0],
    lsprFactor: 0.045,
    activationEnergy: 28.5,
    mitigation: "Ramp electrostatic precipitator corona voltage (+15 kV); engage secondary PTFE micro-filter."
  },
  "ZnO": {
    name: "Zinc Oxide",
    formula: "ZnO",
    cpcbLimit: 80.0,
    oshaPel: 200.0,
    baseAffinity: [0.40, 0.30, 0.50, 0.35, 0.45, 0.30, 0.35, 0.95],
    respTimeRange: [8.0, 16.0],
    recTimeRange: [20.0, 42.0],
    lsprFactor: 0.060,
    activationEnergy: 22.0,
    mitigation: "Activate wet scrubber with alkaline neutralizer (pH 9.2); verify pulse-jet baghouse seals."
  },
  "CuO": {
    name: "Copper Oxide",
    formula: "CuO",
    cpcbLimit: 50.0,
    oshaPel: 150.0,
    baseAffinity: [0.90, 0.85, 0.40, 0.40, 0.30, 0.70, 0.40, 0.50],
    respTimeRange: [10.0, 18.0],
    recTimeRange: [25.0, 48.0],
    lsprFactor: 0.075,
    activationEnergy: 25.0,
    mitigation: "Emergency containment: Halt smelting furnace feed; isolate pneumatic dampers; engage HEPA line."
  },
  "Ag-NP": {
    name: "Nano-Silver",
    formula: "Ag-NP",
    cpcbLimit: 25.0,
    oshaPel: 75.0,
    baseAffinity: [0.50, 0.40, 0.90, 0.98, 0.60, 0.45, 0.55, 0.40],
    respTimeRange: [6.0, 14.0],
    recTimeRange: [45.0, 80.0],
    lsprFactor: 0.160,
    activationEnergy: 18.0,
    mitigation: "Critical containment breach: Isolate cleanroom air duct; divert flow to catalytic carbon bed."
  },
  "Carbon_Soot": {
    name: "Carbon Soot / Black",
    formula: "C_nano",
    cpcbLimit: 60.0,
    oshaPel: 180.0,
    baseAffinity: [0.35, 0.30, 0.80, 0.20, 0.95, 0.85, 0.25, 0.20],
    respTimeRange: [12.0, 22.0],
    recTimeRange: [60.0, 110.0],
    lsprFactor: 0.020,
    activationEnergy: 32.0,
    mitigation: "Modulate burner air-to-fuel ratio; initiate automatic pulse-jet clearing of filter hoppers."
  },
  "SiO2": {
    name: "Silica Nanoparticles",
    formula: "SiO₂",
    cpcbLimit: 90.0,
    oshaPel: 220.0,
    baseAffinity: [0.20, 0.25, 0.35, 0.40, 0.30, 0.30, 0.25, 0.30],
    respTimeRange: [18.0, 30.0],
    recTimeRange: [22.0, 40.0],
    lsprFactor: 0.035,
    activationEnergy: 35.0,
    mitigation: "Initiate high-pressure water mist suppression; inspect cyclone separator pressure drop."
  },
  "Clean_Air": {
    name: "Nominal Air (Baseline)",
    formula: "Air",
    cpcbLimit: 15.0,
    oshaPel: 50.0,
    baseAffinity: [0.03, 0.03, 0.02, 0.02, 0.02, 0.03, 0.02, 0.02],
    respTimeRange: [25.0, 40.0],
    recTimeRange: [10.0, 20.0],
    lsprFactor: 0.002,
    activationEnergy: 10.0,
    mitigation: "Nominal operational status: All industrial filtration systems operating within WHO/CPCB limits."
  }
};

export const SENSOR_CHANNELS = [
  { key: "s1_sno2", name: "SnO₂ Film", desc: "Wide-bandgap metal oxide" },
  { key: "s2_wo3", name: "WO₃ Plates", desc: "Oxygen-vacancy porous plates" },
  { key: "s3_graphene", name: "rGO Nanoflakes", desc: "Ballistic carrier 2D graphene" },
  { key: "s4_au_nano", name: "Au Plasmonic", desc: "Localized surface plasmon resonance" },
  { key: "s5_cnt", name: "CNT Bundles", desc: "Multi-walled nanotube channels" },
  { key: "s6_in2o3", name: "In₂O₃ Spheres", desc: "Mesoporous catalytic oxide" },
  { key: "s7_tio2_pt", name: "Pt-TiO₂ Catalytic", desc: "Platinum-doped catalytic film" },
  { key: "s8_zno_nw", name: "ZnO Nanowires", desc: "Single-crystal nanowires" }
];

export const SCENARIO_PRESETS: ScenarioPreset[] = [
  {
    id: "tio2_pigment",
    title: "Titanium Dioxide Surge",
    sector: "Pigment & Polymer Plant",
    pollutant: "TiO2",
    defaultConc: 145.0,
    defaultTemp: 42.0,
    defaultHum: 48.0,
    defaultFlow: 2.8
  },
  {
    id: "zno_rubber",
    title: "Zinc Oxide Aerosol",
    sector: "Tire Vulcanization Facility",
    pollutant: "ZnO",
    defaultConc: 110.0,
    defaultTemp: 38.0,
    defaultHum: 55.0,
    defaultFlow: 2.2
  },
  {
    id: "cuo_foundry",
    title: "Copper Oxide Toxic Spike",
    sector: "Foundry & Smelting Line",
    pollutant: "CuO",
    defaultConc: 85.0,
    defaultTemp: 68.0,
    defaultHum: 32.0,
    defaultFlow: 3.4
  },
  {
    id: "agnp_electronics",
    title: "Nano-Silver Release",
    sector: "Electronics Nano-Fab Cleanroom",
    pollutant: "Ag-NP",
    defaultConc: 48.0,
    defaultTemp: 24.0,
    defaultHum: 40.0,
    defaultFlow: 1.5
  },
  {
    id: "soot_furnace",
    title: "Carbon Soot Emission",
    sector: "Carbon Black Industrial Kiln",
    pollutant: "Carbon_Soot",
    defaultConc: 130.0,
    defaultTemp: 75.0,
    defaultHum: 25.0,
    defaultFlow: 4.1
  },
  {
    id: "sio2_ceramics",
    title: "Silica Particulate Breach",
    sector: "Ceramics & Refractory Mill",
    pollutant: "SiO2",
    defaultConc: 105.0,
    defaultTemp: 30.0,
    defaultHum: 60.0,
    defaultFlow: 2.0
  },
  {
    id: "ambient_clean",
    title: "Scrubbed Flue Gas (Nominal)",
    sector: "Environmental Stack Baseline",
    pollutant: "Clean_Air",
    defaultConc: 1.8,
    defaultTemp: 25.0,
    defaultHum: 50.0,
    defaultFlow: 1.8
  }
];

export function simulateReactionKinetics(
  pollutant: PollutantKey,
  concentration: number,
  tempC: number = 25.0,
  humidityPct: number = 50.0,
  durationS: number = 70.0,
  dt: number = 1.0
): SensorKineticsData {
  const profile = POLLUTANT_PROFILES[pollutant];
  const timePoints: number[] = [];
  for (let t = 0; t <= durationS; t += dt) {
    timePoints.push(t);
  }

  const tStart = 8.0;
  const tEnd = 45.0;

  // Arrhenius factor
  const rGas = 8.314e-3;
  const tKelvin = tempC + 273.15;
  const kTemp = Math.exp(-profile.activationEnergy / (rGas * tKelvin)) / 
                Math.exp(-profile.activationEnergy / (rGas * 298.15));

  const humidityFactor = 1.0 - (humidityPct - 50.0) * 0.002;
  const tauResp = ((profile.respTimeRange[0] + profile.respTimeRange[1]) / 2.0) / Math.max(kTemp, 0.4);
  const tauRec = (profile.recTimeRange[0] + profile.recTimeRange[1]) / 2.0;
  const concPower = pollutant === "Clean_Air" ? 1.0 : 0.82;

  const curves: Record<string, number[]> = {};

  SENSOR_CHANNELS.forEach((sensor, sIdx) => {
    const affinity = profile.baseAffinity[sIdx];
    const deltaRMax = pollutant === "Clean_Air" 
      ? 0.02 + 0.005 * Math.sin(sIdx) 
      : affinity * Math.pow(concentration, concPower) * 0.28 * humidityFactor;

    const signal: number[] = [];
    timePoints.forEach((t) => {
      let val = 1.0;
      if (t < tStart) {
        val = 1.0 + 0.004 * Math.sin(t * 1.5 + sIdx);
      } else if (t >= tStart && t < tEnd) {
        const fraction = 1.0 - Math.exp(-(t - tStart) / tauResp);
        val = 1.0 + (deltaRMax * fraction) + 0.006 * Math.sin(t * 0.8 + sIdx);
      } else {
        const peakVal = deltaRMax * (1.0 - Math.exp(-(tEnd - tStart) / tauResp));
        const fractionRec = Math.exp(-(t - tEnd) / tauRec);
        val = 1.0 + (peakVal * fractionRec) + 0.005 * Math.sin(t * 0.8 + sIdx);
      }
      signal.push(Number(val.toFixed(3)));
    });
    curves[sensor.key] = signal;
  });

  return { timePoints, curves };
}

export function runInference(
  pollutant: PollutantKey,
  simConc: number,
  tempC: number,
  humidityPct: number,
  _flowVelocity: number
): InferenceResult {
  const profile = POLLUTANT_PROFILES[pollutant];
  
  // Calculate steady-state features with Arrhenius temperature scaling
  const rGas = 8.314e-3;
  const tKelvin = tempC + 273.15;
  const kTemp = Math.exp(-profile.activationEnergy / (rGas * tKelvin)) / 
                Math.exp(-profile.activationEnergy / (rGas * 298.15));
  const humidityFactor = 1.0 - (humidityPct - 50.0) * 0.0018;
  const concPower = pollutant === "Clean_Air" ? 1.0 : 0.82;
  
  const peakSensors = profile.baseAffinity.map(aff => {
    return pollutant === "Clean_Air" ? 0.02 : aff * Math.pow(simConc, concPower) * 0.28 * humidityFactor;
  });
  const peakAmp = Math.max(...peakSensors);
  const tauResp = ((profile.respTimeRange[0] + profile.respTimeRange[1]) / 2) / Math.max(kTemp, 0.4);
  const tauRec = (profile.recTimeRange[0] + profile.recTimeRange[1]) / 2;
  const lsprShift = pollutant === "Clean_Air" ? 0.04 : profile.lsprFactor * simConc;

  // Compute probability distribution with calibrated softmax
  const allKeys = Object.keys(POLLUTANT_PROFILES) as PollutantKey[];
  const rawScores: Record<PollutantKey, number> = {} as any;
  
  allKeys.forEach((key) => {
    if (key === pollutant) {
      rawScores[key] = 8.5; // High confidence for matching profile
    } else if (pollutant === "Clean_Air") {
      rawScores[key] = 0.2;
    } else {
      // Partial cross-talk distance
      const otherAff = POLLUTANT_PROFILES[key].baseAffinity;
      let dot = 0;
      for (let i = 0; i < 8; i++) dot += profile.baseAffinity[i] * otherAff[i];
      rawScores[key] = dot * 1.8;
    }
  });

  // Softmax
  const expScores = allKeys.map(k => Math.exp(rawScores[k]));
  const sumExp = expScores.reduce((a, b) => a + b, 0);
  const probabilities: Record<PollutantKey, number> = {} as any;
  allKeys.forEach((k, idx) => {
    probabilities[k] = Number((expScores[idx] / sumExp).toFixed(4));
  });

  // Regressed concentration with subtle measurement variance
  let predictedConc = pollutant === "Clean_Air" 
    ? Math.min(simConc, 3.5)
    : simConc * (0.98 + 0.02 * Math.sin(simConc * 0.1));
  predictedConc = Math.max(0.1, Number(predictedConc.toFixed(1)));

  // Hazard level assessment
  let hazardLevel: HazardLevel = "SAFE";
  let statusText = "Nominal Compliant Operation";
  if (predictedConc > profile.oshaPel) {
    hazardLevel = "CRITICAL";
    statusText = "Severe Emission Ceiling Breach (Action Required)";
  } else if (predictedConc > profile.cpcbLimit) {
    hazardLevel = "HAZARDOUS";
    statusText = "Exceeds Environmental Standard (CPCB Limit)";
  } else if (predictedConc > profile.cpcbLimit * 0.5) {
    hazardLevel = "MODERATE";
    statusText = "Elevated Trace Emission (Monitor Closely)";
  }

  return {
    pollutant,
    pollutantName: profile.name,
    confidence: probabilities[pollutant],
    probabilities,
    predictedConcentrationUgM3: predictedConc,
    hazardLevel,
    statusText,
    cpcbLimit: profile.cpcbLimit,
    oshaPel: profile.oshaPel,
    mitigationPlan: profile.mitigation,
    peakAmplitudePercent: Number((peakAmp * 100).toFixed(1)),
    lsprShiftNm: Number(lsprShift.toFixed(2)),
    responseTimeS: Number(tauResp.toFixed(1)),
    recoveryTimeS: Number(tauRec.toFixed(1))
  };
}
