import React from "react";
import { createRoot } from "react-dom/client";
import { Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import "./styles.css";

const bars = [
  { time: "14:30", close: 100.8 }, { time: "15:30", close: 101.9 },
  { time: "16:30", close: 101.2 }, { time: "17:30", close: 102.7 },
  { time: "18:30", close: 103.1 }, { time: "19:30", close: 102.0 },
];

function App() {
  return <main>
    <header><span className="mark">∿</span><strong>Quant Lab</strong><nav>Learn <span>Market 🔒</span><span>Paper 🔒</span><span>Live 🔒</span><span>Control 🔒</span></nav></header>
    <section className="hero"><small>LESSON 01 · DATA & MEASUREMENT</small><h1>Market Data & Returns</h1><p>Learn exactly what a systematic strategy sees before asking it to make a decision.</p></section>
    <div className="grid">
      <section className="card"><h2>What you unlock</h2><ul><li>Canonical instruments</li><li>Timezone-aware OHLCV bars</li><li>Simple and log returns</li><li>Data-quality validation</li></ul><p className="status">● Learn available · Historical sample data</p></section>
      <section className="card"><h2>Historical close · QLAB.XNAS</h2><div className="chart"><ResponsiveContainer><LineChart data={bars}><XAxis dataKey="time"/><YAxis domain={["dataMin - 1","dataMax + 1"]}/><Tooltip/><Line type="monotone" dataKey="close" stroke="currentColor" dot/></LineChart></ResponsiveContainer></div><small>Deterministic educational fixture · UTC · not live market data</small></section>
    </div>
    <section className="card lesson"><h2>Start with the information set</h2><p>An OHLCV bar is an aggregation. Its close cannot be used before that close exists. Quant Lab makes timestamps and validation explicit so future strategies cannot quietly learn from the future.</p><code>simple_return = P[t] / P[t-1] - 1</code><code>log_return = ln(P[t] / P[t-1])</code></section>
  </main>;
}
createRoot(document.getElementById("root")!).render(<React.StrictMode><App/></React.StrictMode>);
