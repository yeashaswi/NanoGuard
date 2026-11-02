export type PollutantKey = 
  | "TiO2" 
  | "ZnO" 
  | "CuO" 
  | "Ag-NP" 
  | "Carbon_Soot" 
  | "SiO2" 
  | "Clean_Air";

export type HazardLevel = "SAFE" | "MODERATE" | "HAZARDOUS" | "CRITICAL";

export interface PollutantProfile {
  name: string;
  formula: string;
  cpcbLimit: number;
  oshaPel: number;
  baseAffinity: number[]; // 8 channels
  respTimeRange: [number, number];
  recTimeRange: [number, number];
  lsprFactor: number;
  activationEnergy: number; // kJ/mol
  mitigation: string;
}

export interface SensorKineticsData {
  timePoints: number[];
  curves: Record<string, number[]>;
}

export interface InferenceResult {
  pollutant: PollutantKey;
  pollutantName: string;
  confidence: number;
  probabilities: Record<PollutantKey, number>;
  predictedConcentrationUgM3: number;
  hazardLevel: HazardLevel;
  statusText: string;
  cpcbLimit: number;
  oshaPel: number;
  mitigationPlan: string;
  peakAmplitudePercent: number;
  lsprShiftNm: number;
  responseTimeS: number;
  recoveryTimeS: number;
}

export interface ScenarioPreset {
  id: string;
  title: string;
  sector: string;
  pollutant: PollutantKey;
  defaultConc: number;
  defaultTemp: number;
  defaultHum: number;
  defaultFlow: number;
}
