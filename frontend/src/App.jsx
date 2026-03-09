/* LICENSE UPL
 * Author: Mauro Risonho de Paula Assumpção
 * Description: Enterprise React Dashboard UI
 */

import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { Activity, AlertTriangle, ShieldAlert } from 'lucide-react';

const API_BASE = "http://localhost:8000/api";

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
        teleData = teleData.reverse(); // Chronological for graph
        setTelemetry(teleData);

        // Build Alerts feed from malicious flags
        const newAlerts = teleData
          .filter(t => t.malicious_flag)
          .map(t => ({
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

  return (
    <div className="dashboard-container">
      <header className="header">
        <h1>Industrial Edge AI SOC</h1>
        <div style={{display: 'flex', gap: '1rem', color: 'var(--text-muted)'}}>
          <span style={{display: 'flex', alignItems: 'center', gap: '0.5rem'}}>
            <div style={{width: 8, height: 8, borderRadius: '50%', background: '#10b981', boxShadow: '0 0 10px #10b981'}}></div>
            System Online
          </span>
        </div>
      </header>

      {/* KPI Cards */}
      <div className="kpi-grid">
        <div className="glass-panel kpi-card">
          <div className="kpi-title" style={{display: 'flex', gap: '0.5rem', alignItems: 'center'}}>
            <Activity size={18} /> Total Packets Processed
          </div>
          <div className="kpi-value kpi-primary">{stats.total_packets.toLocaleString()}</div>
        </div>
        
        <div className="glass-panel kpi-card">
          <div className="kpi-title" style={{display: 'flex', gap: '0.5rem', alignItems: 'center'}}>
            <AlertTriangle size={18} /> AI Anomalies
          </div>
          <div className="kpi-value kpi-warning">{stats.anomalies.toLocaleString()}</div>
        </div>

        <div className="glass-panel kpi-card">
          <div className="kpi-title" style={{display: 'flex', gap: '0.5rem', alignItems: 'center'}}>
            <ShieldAlert size={18} /> Blocked Attacks
          </div>
          <div className="kpi-value kpi-danger">{stats.attacks.toLocaleString()}</div>
        </div>
      </div>

      <div className="main-grid">
        {/* Graph Section */}
        <div className="glass-panel chart-container">
          <h2>Live Vibration & Temperature Data</h2>
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={telemetry} margin={{ top: 5, right: 20, bottom: 5, left: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey="timestamp" tickFormatter={(unixTime) => new Date(unixTime * 1000).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit', second:'2-digit'})} stroke="#94a3b8" />
              <YAxis yAxisId="left" stroke="#3b82f6" />
              <YAxis yAxisId="right" orientation="right" stroke="#f59e0b" />
              <Tooltip 
                contentStyle={{backgroundColor: 'var(--bg-base)', borderColor: 'var(--glass-border)', color: '#fff'}}
                labelFormatter={(unixTime) => new Date(unixTime * 1000).toLocaleTimeString()}
              />
              <Legend />
              <Line yAxisId="left" type="monotone" dataKey="vibration" stroke="#3b82f6" strokeWidth={3} dot={false} isAnimationActive={false} />
              <Line yAxisId="right" type="monotone" dataKey="temperature" stroke="#f59e0b" strokeWidth={3} dot={false} isAnimationActive={false} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Security Alert Feed */}
        <div className="glass-panel">
          <h2>Security & RedTeam Feed</h2>
          <div className="feed-container">
            {alerts.length === 0 ? (
              <p style={{color: 'var(--text-muted)'}}>No anomalies detected.</p>
            ) : (
              alerts.map((alert, idx) => (
                <div key={`${alert.id}-${idx}`} className={`alert-item ${alert.type}`}>
                  <div className="alert-time">{alert.time}</div>
                  <div className="alert-msg">{alert.msg}</div>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
