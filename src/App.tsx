/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { Play, CheckCircle, Clock, FileImage, ShieldAlert, Cpu } from 'lucide-react';

const MOCK_DATA = [
  { name: '08:00', processed: 12 },
  { name: '09:00', processed: 25 },
  { name: '10:00', processed: 16 },
  { name: '11:00', processed: 42 },
  { name: '12:00', processed: 38 },
  { name: '13:00', processed: 55 },
];

export default function App() {
  const [testLogs, setTestLogs] = useState<any[]>([]);
  const [testResult, setTestResult] = useState<{success: boolean, text: string, provider: string} | null>(null);
  const [isTesting, setIsTesting] = useState(false);
  const [timeSpent, setTimeSpent] = useState("0h 0m");

  useEffect(() => {
    // Mock simulation for time spent
    const start = Date.now() - 3600000 * 2.4; // 2.4 hours ago
    const interval = setInterval(() => {
      const diffStr = Math.floor((Date.now() - start) / 3600000) + "h " + Math.floor(((Date.now() - start) % 3600000) / 60000) + "m";
      setTimeSpent(diffStr);
    }, 60000);
    return () => clearInterval(interval);
  }, []);

  const handleTestAPI = async () => {
    setIsTesting(true);
    setTestLogs([]);
    setTestResult(null);
    try {
      const res = await fetch("/api/fallback-test", { method: "POST" });
      const data = await res.json();
      
      if (data.logs) {
        setTestLogs(data.logs);
      }
      
      if (data.success) {
        setTestResult({ success: true, text: data.text, provider: data.provider });
      } else {
        setTestResult({ success: false, text: data.error || "Semua fallback gagal dipanggil.", provider: "none" });
      }
    } catch (e: any) {
      setTestResult({ success: false, text: `FAILED: ${e.message}`, provider: "none" });
    }
    setIsTesting(false);
  };

  return (
    <div className="flex flex-col h-screen w-full bg-[#0B0C0E] text-[#D1D5DB] overflow-hidden select-none border-4 border-[#1A1C1E] font-mono">
      {/* HEADER */}
      <header className="h-12 bg-[#16181D] border-b border-[#2D2F36] flex items-center justify-between px-4 flex-shrink-0">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 bg-amber-400 rounded flex items-center justify-center">
            <span className="text-[#0B0C0E] font-black text-lg">★</span>
          </div>
          <div className="flex flex-col">
            <h1 className="text-sm font-bold tracking-tight text-white flex items-center">
              BINTANG OCR LOGICAL PINYIN 
              <span className="text-[10px] bg-amber-400/10 text-amber-400 px-1.5 py-0.5 rounded ml-2 border border-amber-400/20">V3.2 PRO</span>
            </h1>
            <p className="text-[9px] text-gray-500 uppercase tracking-widest">Senior Architect Environment v2024.1</p>
          </div>
        </div>
        <div className="flex items-center gap-4 text-[10px]">
          <div className="flex items-center gap-2 px-2 py-1 bg-[#23272E] rounded border border-[#3A3F4B]">
            <div className="w-2 h-2 rounded-full bg-green-500 shadow-[0_0_5px_rgba(34,197,94,0.5)]"></div>
            <span className="text-gray-300">SYSTEM STABLE</span>
          </div>
          <div className="text-right leading-tight">
            <p className="text-gray-400 italic">Dibuat oleh Irwan</p>
            <p className="text-[8px] text-gray-600">irwan.percetakanbintang@gmail.com</p>
          </div>
        </div>
      </header>

      <div className="flex flex-1 overflow-hidden">
        {/* LEFT SIDEBAR */}
        <aside className="w-60 bg-[#121418] border-r border-[#2D2F36] flex flex-col">
          <div className="p-3 border-b border-[#2D2F36]">
            <h2 className="text-[10px] font-bold text-amber-400 uppercase tracking-tighter mb-2">Batch Processing Queue</h2>
            <div className="bg-[#1E2229] border border-[#3A3F4B] p-2 rounded text-center cursor-pointer hover:bg-[#2A2F3A] transition-colors">
              <p className="text-[11px] text-amber-400 flex items-center justify-center gap-1">
                <FileImage size={12} /> + Add Files (PNG, JPG, PDF)
              </p>
            </div>
          </div>
          <div className="flex-1 overflow-y-auto space-y-px">
            <div className="p-2.5 bg-[#1C1F26] border-l-2 border-amber-400 flex flex-col gap-1">
              <div className="flex justify-between text-[11px]">
                <span className="truncate font-medium text-white">sutra_diaman_01.jpg</span>
                <span className="text-amber-400">45%</span>
              </div>
              <div className="w-full bg-gray-800 h-1 rounded-full overflow-hidden">
                <div className="bg-amber-400 h-full w-[45%]"></div>
              </div>
            </div>
            <div className="p-2.5 border-b border-[#2D2F36] opacity-60 flex flex-col gap-1">
              <div className="flex justify-between text-[11px]">
                <span className="truncate">lotus_sutra_p82.pdf</span>
                <span className="text-gray-500">Queued</span>
              </div>
            </div>
          </div>
        </aside>

        {/* MAIN AREA */}
        <main className="flex-1 flex flex-col bg-[#0F1115]">
          <div className="p-4 bg-[#16181D] border-b border-[#2D2F36] flex gap-4">
            {/* STATS WIDGET */}
            <div className="flex-1 p-3 bg-[#1A1C22] border border-[#2D2F36] rounded shadow-lg flex items-center justify-between">
              <div className="flex flex-col">
                <span className="text-[10px] text-gray-500 uppercase tracking-widest font-bold">Total Processed</span>
                <span className="text-2xl text-white font-bold flex items-center gap-2">1,248 <CheckCircle size={16} className="text-green-500"/></span>
              </div>
              <div className="h-10 w-px bg-[#2D2F36]"></div>
              <div className="flex flex-col">
                <span className="text-[10px] text-gray-500 uppercase tracking-widest font-bold">Success Rate</span>
                <span className="text-2xl text-amber-400 font-bold">99.8%</span>
              </div>
              <div className="h-10 w-px bg-[#2D2F36]"></div>
              <div className="flex flex-col">
                <span className="text-[10px] text-gray-500 uppercase tracking-widest font-bold">Current Time Spent</span>
                <span className="text-2xl text-white font-bold flex items-center gap-2"><Clock size={16} className="text-blue-400"/> {timeSpent}</span>
              </div>
            </div>
          </div>
          
          <div className="flex-1 p-4 relative overflow-hidden bg-[radial-gradient(#1E2229_1px,transparent_1px)] bg-[size:20px_20px] flex flex-col gap-4 overflow-y-auto">
            <div className="absolute inset-0 bg-black/40 pointer-events-none"></div>
            
            {/* RECHARTS SUMMARY */}
            <div className="relative z-10 w-full h-48 border border-[#2D2F36] bg-[#16181D] shadow-2xl p-4">
               <h3 className="text-[10px] text-gray-500 uppercase tracking-widest mb-2 font-bold flex items-center gap-2">
                 <ShieldAlert size={12}/> Processing Volume Over Time
               </h3>
               <ResponsiveContainer width="100%" height="100%">
                <LineChart data={MOCK_DATA}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#2D2F36" />
                  <XAxis dataKey="name" stroke="#6B7280" fontSize={10} tickLine={false} axisLine={false} />
                  <YAxis stroke="#6B7280" fontSize={10} tickLine={false} axisLine={false} />
                  <Tooltip contentStyle={{ backgroundColor: '#1A1C22', borderColor: '#3A3F4B', fontSize: '12px' }} />
                  <Line type="monotone" dataKey="processed" stroke="#FBBF24" strokeWidth={2} dot={{ fill: '#FBBF24', r: 3 }} activeDot={{ r: 5 }} />
                </LineChart>
              </ResponsiveContainer>
            </div>

            {/* API TESTING SECTION */}
            <div className="relative z-10 w-full border border-[#2D2F36] bg-[#16181D] shadow-2xl flex flex-col p-4 shrink-0">
               <h3 className="text-[10px] text-gray-500 uppercase tracking-widest mb-4 font-bold flex items-center gap-2">
                 <Cpu size={12}/> API Cascading Fallback Testing
               </h3>
               <p className="text-xs text-gray-400 mb-4 leading-relaxed max-w-xl">
                 Sistem siap diuji. Mekanisme <strong>Cascading Fallback</strong> akan mencoba mengontak provider AI berdasarkan urutan prioritas: <br/> 
                 <strong className="text-amber-400 text-[10px] bg-amber-400/10 px-1 py-0.5 rounded border border-amber-400/20">1. GEMINI</strong> ➔ 
                 <strong className="text-gray-300 text-[10px] bg-gray-800 px-1 py-0.5 rounded border border-gray-700 mx-1">2. OPENROUTER</strong> ➔ 
                 <strong className="text-gray-300 text-[10px] bg-gray-800 px-1 py-0.5 rounded border border-gray-700">3. GROQ</strong>
               </p>
               <button 
                onClick={handleTestAPI}
                disabled={isTesting}
                className="self-start text-[11px] bg-amber-400 text-[#0B0C0E] font-bold px-6 py-2 rounded uppercase flex items-center gap-2 hover:bg-amber-300 disabled:opacity-50 transition-colors"
              >
                <Play size={14} /> {isTesting ? "Executing Fallback Engine..." : "Test AI Logic Connection"}
              </button>

              {testLogs.length > 0 && (
                <div className="mt-4 space-y-1.5 bg-[#0B0C0E] p-3 rounded border border-[#2D2F36]">
                  <p className="text-[9px] text-gray-500 uppercase font-bold mb-2">Execution Pipeline Logs:</p>
                  {testLogs.map((log, i) => (
                    <div key={i} className={`p-2 rounded border text-[10px] leading-relaxed flex items-center justify-between ${
                      log.status === 'Success' ? 'bg-green-900/20 border-green-800/50 text-green-400' :
                      log.status === 'Skipped' ? 'bg-gray-800/50 border-gray-700/50 text-gray-500' :
                      'bg-red-900/20 border-red-800/50 text-red-400'
                    }`}>
                      <div className="flex flex-col gap-0.5">
                        <span className="font-bold opacity-80 uppercase text-[9px] mb-0.5">PRIORITY {i + 1}: {log.provider}</span>
                        <span>{log.status === 'Failed' ? `Exception: ${log.error}` : log.status === 'Success' ? `Response: ${log.text.substring(0,60)}${log.text.length > 60 ? '...' : ''}` : 'Action: Skipped (No valid API Key detected in Secrets)'}</span>
                      </div>
                      <span className="font-bold uppercase tracking-widest text-[9px]">{log.status}</span>
                    </div>
                  ))}
                </div>
              )}

              {testResult && testResult.success && (
                <div className="mt-3 p-3 rounded border bg-green-900/20 border-green-800/50 text-green-400 text-xs leading-relaxed flex justify-between items-center">
                  <span><strong>FINAL STATUS:</strong> Seamless connection established securely via <strong>{testResult.provider}</strong>.</span>
                  <CheckCircle size={16} />
                </div>
              )}
            </div>
            
          </div>
        </main>

        {/* RIGHT SIDEBAR */}
        <aside className="w-72 bg-[#121418] border-l border-[#2D2F36] flex flex-col">
          <div className="p-3 border-b border-[#2D2F36] bg-[#16181D]">
            <div className="flex justify-between items-center mb-1">
              <h2 className="text-[10px] font-bold text-gray-400">OUTPUT CONSOLE</h2>
              <button className="text-[9px] text-amber-400 hover:underline">EXPORT .TXT</button>
            </div>
            <p className="text-[9px] text-gray-600 italic">Halaman 82 (Visual)</p>
          </div>
          <div className="flex-1 p-3 overflow-y-auto text-[11px] leading-relaxed relative">
             <div className="absolute inset-0 bg-gradient-to-b from-[#121418]/0 to-[#121418] pointer-events-none z-10 bottom-0 top-auto h-12"></div>
             <p className="text-gray-500 italic">Waiting for processing...</p>
          </div>
          <div className="p-3 bg-[#0B0C0E] border-t border-[#2D2F36] h-32 overflow-y-auto">
            <p className="text-[9px] font-bold text-red-400 mb-1 tracking-tighter">INTERNAL ERROR LOG</p>
            <div className="space-y-1 text-[8px] opacity-60">
              <p>[System] Express + Vite backend active.</p>
              <p>[System] Recharts Summary Widget Initialized.</p>
              <p>[Network] Status: Waiting for API Ping.</p>
            </div>
          </div>
        </aside>
      </div>

      {/* FOOTER */}
      <footer className="h-8 bg-[#16181D] border-t border-[#2D2F36] flex items-center px-4 justify-between flex-shrink-0 text-[10px]">
        <div className="flex items-center gap-4 text-gray-500">
          <div className="flex gap-1.5 items-center">
            <span>STATUS:</span>
            <span className="text-amber-400 font-bold uppercase">IDLE</span>
          </div>
        </div>
        <div className="flex gap-4 text-gray-500 font-mono">
          <span>CPU: 12%</span>
          <span>RAM: 452MB</span>
          <span>V:3.2.0-STABLE</span>
        </div>
      </footer>
    </div>
  );
}

