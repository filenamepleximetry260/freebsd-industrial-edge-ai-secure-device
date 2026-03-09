/* LICENSE UPL
 * Author: Mauro Risonho de Paula Assumpção
 * Description: Enterprise React Dashboard UI
 */

import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import {
  Activity,
  AlertTriangle,
  ShieldAlert,
  Radar,
  FlaskConical,
  ShieldCheck,
  LibraryBig,
  Scale,
  Binary,
  Bot,
  Link,
} from 'lucide-react';
import './App.css';

const API_BASE = 'http://localhost:8000/api';

const REDTEAM_PHASES = [
  {
    title: '1. Business Objectives',
    detail: 'Define abuse cases, policy boundaries, legal and brand risk acceptance criteria.',
    tag: 'Governance',
  },
  {
    title: '2. Threat Modeling',
    detail: 'Map adversarial, data, alignment, interaction and knowledge risks before deployment.',
    tag: 'Model Security',
  },
  {
    title: '3. Lab Simulation',
    detail: 'Run direct and indirect prompt injection, multi-turn bypass, and tool abuse scenarios.',
    tag: 'Adversarial Testing',
  },
  {
    title: '4. Guardrail Verification',
    detail: 'Validate defense-in-depth, policy graders and runtime mitigations against bypass attempts.',
    tag: 'Controls',
  },
  {
    title: '5. Continuous Operations',
    detail: 'Re-test after model, prompt, RAG corpus, or policy changes with post-deployment monitoring.',
    tag: 'SOC Loop',
  },
];

const THREAT_MATRIX = [
  { category: 'Prompt Injection', severity: 'High', area: 'Adversarial', owner: 'AppSec + AI Eng' },
  { category: 'Sensitive Data Disclosure', severity: 'Critical', area: 'Data', owner: 'Security + Data Gov' },
  { category: 'System Prompt Leakage', severity: 'High', area: 'Knowledge', owner: 'Platform Eng' },
  { category: 'Excessive Agency', severity: 'Critical', area: 'Agentic Runtime', owner: 'Platform + IAM' },
  { category: 'Misinformation / Hallucination', severity: 'Medium', area: 'Trustworthiness', owner: 'Model Ops' },
  { category: 'RAG Poisoning', severity: 'High', area: 'Retrieval Layer', owner: 'Data + MLOps' },
];

const FRAMEWORK_CARDS = [
  {
    icon: ShieldCheck,
    title: 'Microsoft AI Red Team',
    summary: 'Threat modeling, failure taxonomy, triage bug bar and operational lessons from large-scale exercises.',
    link: 'https://learn.microsoft.com/en-us/security/ai-red-team/',
  },
  {
    icon: LibraryBig,
    title: 'OWASP GenAI Red Teaming',
    summary: 'Holistic method across model evaluation, implementation testing, infrastructure and runtime behavior.',
    link: 'https://genai.owasp.org/resource/genai-red-teaming-guide/',
  },
  {
    icon: FlaskConical,
    title: 'Playground Labs',
    summary: 'Hands-on challenge patterns for direct/indirect injection, metaprompt extraction and guardrail bypass.',
    link: 'https://github.com/microsoft/AI-Red-Teaming-Playground-Labs',
  },
  {
    icon: Scale,
    title: 'Enterprise Readiness',
    summary: 'Connect technical findings to legal, compliance, reputation and business action controls.',
    link: 'https://genai.owasp.org/initiatives/red-teaming-initiative/',
  },
];

function App() {
  const [telemetry, setTelemetry] = useState([]);
  const [stats, setStats] = useState({ total_packets: 0, anomalies: 0, attacks: 0 });
  const [alerts, setAlerts] = useState([]);

  const fetchData = async () => {
    try {
      // Fetch Stats
      const statRes = await fetch(`${API_BASE}/stats`);
      if (statRes.ok) {
        const statData = await statRes.json();
        setStats(statData);
      }

      // Fetch Live Telemetry
      const teleRes = await fetch(`${API_BASE}/telemetry?limit=50`);
      if (teleRes.ok) {
        let teleData = await teleRes.json();
        teleData = teleData.reverse();
        setTelemetry(teleData);

        const newAlerts = teleData
          .filter((t) => t.malicious_flag)
          .map((t) => ({
            id: t.id,
            time: new Date(t.timestamp * 1000).toLocaleTimeString(),
            type: t.malicious_flag.includes('ATTACK') ? 'danger' : 'warning',
            msg: `[${t.malicious_flag}] from ${t.device_id} (Temp: ${t.temperature}°C, Vib: ${t.vibration})`
          }))
          .reverse();
        setAlerts(newAlerts);
      }
    } catch (err) {
      console.error("Failed to fetch data:", err);
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 2000);
    return () => clearInterval(interval);
  }, []);

  const riskIndex = Math.min(100, stats.attacks * 9 + stats.anomalies * 5);
  const guardrailEffectiveness = Math.max(0, 100 - riskIndex);
  const redteamCoverage = Math.min(100, 58 + stats.total_packets / 8);

  return (
    <div className="soc-shell">
      <div className="ambient-bg" aria-hidden="true" />
      <header className="topbar">
        <div>
          <p className="eyebrow">Industrial Edge AI SOC</p>
          <h1>Enterprise RedTeamAI Command Center</h1>
          <p className="subtitle">
            Real-time telemetry analytics with AI adversarial validation aligned to Microsoft AI Red Team and OWASP GenAI guidance.
          </p>
        </div>
        <div className="status-pill">
          <span className="pulse" />
          System Online
        </div>
      </header>

      <section className="kpi-grid">
        <article className="card kpi-card">
          <p className="kpi-label"><Activity size={16} /> Telemetry Processed</p>
          <p className="kpi-number">{stats.total_packets.toLocaleString()}</p>
        </article>
        <article className="card kpi-card">
          <p className="kpi-label"><AlertTriangle size={16} /> AI Anomalies</p>
          <p className="kpi-number warning">{stats.anomalies.toLocaleString()}</p>
        </article>
        <article className="card kpi-card">
          <p className="kpi-label"><ShieldAlert size={16} /> Confirmed Attacks</p>
          <p className="kpi-number danger">{stats.attacks.toLocaleString()}</p>
        </article>
        <article className="card kpi-card">
          <p className="kpi-label"><Radar size={16} /> RedTeam Coverage</p>
          <p className="kpi-number success">{Math.round(redteamCoverage)}%</p>
        </article>
      </section>

      <section className="ops-grid">
        <article className="card chart-card">
          <div className="panel-head">
            <h2>Live Telemetry Stream</h2>
            <span className="panel-tag"><Binary size={14} /> edge-arm64</span>
          </div>

          <div className="chart-wrap">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={telemetry} margin={{ top: 10, right: 20, bottom: 5, left: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#21414f" opacity={0.45} />
                <XAxis
                  dataKey="timestamp"
                  tickFormatter={(unixTime) => new Date(unixTime * 1000).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' })}
                  stroke="#8fb5bf"
                  minTickGap={18}
                />
                <YAxis yAxisId="left" stroke="#4fb8d6" />
                <YAxis yAxisId="right" orientation="right" stroke="#ffb25b" />
                <Tooltip
                  contentStyle={{ backgroundColor: '#0f2c38', borderColor: '#2f5f6f', color: '#dff2f7', borderRadius: 10 }}
                  labelFormatter={(unixTime) => new Date(unixTime * 1000).toLocaleTimeString()}
                />
                <Legend />
                <Line yAxisId="left" type="monotone" dataKey="vibration" stroke="#4fb8d6" strokeWidth={2.5} dot={false} isAnimationActive={false} />
                <Line yAxisId="right" type="monotone" dataKey="temperature" stroke="#ffb25b" strokeWidth={2.5} dot={false} isAnimationActive={false} />
              </LineChart>
            </ResponsiveContainer>
          </div>

          <div className="micro-kpis">
            <div>
              <span>Risk Index</span>
              <strong>{riskIndex}</strong>
            </div>
            <div>
              <span>Guardrail Effectiveness</span>
              <strong>{guardrailEffectiveness}%</strong>
            </div>
            <div>
              <span>Telemetry Freshness</span>
              <strong>{telemetry.length ? 'Live' : 'No Data'}</strong>
            </div>
          </div>
        </article>

        <article className="card feed-card">
          <div className="panel-head">
            <h2>Security & RedTeam Feed</h2>
            <span className="panel-tag"><Bot size={14} /> continuous</span>
          </div>
          <div className="feed-container">
            {alerts.length === 0 ? (
              <p className="muted">No active incidents detected in the current telemetry window.</p>
            ) : (
              alerts.map((alert, idx) => (
                <div key={`${alert.id}-${idx}`} className={`alert-item ${alert.type}`}>
                  <div className="alert-time">{alert.time}</div>
                  <div className="alert-msg">{alert.msg}</div>
                </div>
              ))
            )}
          </div>
        </article>
      </section>

      <section className="redteam-grid">
        <article className="card framework-card">
          <h2>RedTeamAI Framework Alignment</h2>
          <div className="framework-list">
            {FRAMEWORK_CARDS.map((item) => {
              const Icon = item.icon;
              return (
                <a className="framework-item" href={item.link} target="_blank" rel="noreferrer" key={item.title}>
                  <div className="framework-icon"><Icon size={18} /></div>
                  <div>
                    <h3>{item.title}</h3>
                    <p>{item.summary}</p>
                  </div>
                  <Link size={14} className="link-icon" />
                </a>
              );
            })}
          </div>
        </article>

        <article className="card phases-card">
          <h2>Operational Red Teaming Lifecycle</h2>
          <div className="phase-list">
            {REDTEAM_PHASES.map((phase) => (
              <div className="phase-item" key={phase.title}>
                <p className="phase-title">{phase.title}</p>
                <p className="phase-detail">{phase.detail}</p>
                <span className="phase-tag">{phase.tag}</span>
              </div>
            ))}
          </div>
        </article>
      </section>

      <section className="card matrix-card">
        <h2>Threat Prioritization Matrix</h2>
        <p className="muted matrix-subtitle">
          Prioritized by business impact, exploitability and operational exposure, following OWASP-style threat grouping.
        </p>
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Category</th>
                <th>Severity</th>
                <th>Surface</th>
                <th>Control Owner</th>
              </tr>
            </thead>
            <tbody>
              {THREAT_MATRIX.map((row) => (
                <tr key={row.category}>
                  <td>{row.category}</td>
                  <td>
                    <span className={`severity ${row.severity.toLowerCase()}`}>{row.severity}</span>
                  </td>
                  <td>{row.area}</td>
                  <td>{row.owner}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}

export default App;
