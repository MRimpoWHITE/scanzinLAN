import React, { useState } from "react";
import axios from "axios";
import { Search, Monitor, ShieldAlert, Cpu } from "lucide-react";
import "./index.css";

function App() {
  const [devices, setDevices] = useState([]);
  const [loading, setLoading] = useState(false);

  const translations = {
    en: {
      title: "ScanzinLAN",
      subtitle: "Network Monitoring Tool for Professional Gents",
      scanBtn: "Start Scan",
      scanningBtn: "Scanning...",
      statTotal: "Total Devices",
      statOnline: "Active Now",
      statUnknown: "Unknown Vendor",
      colStatus: "Status",
      colIP: "IP Address",
      colMAC: "MAC Address",
      colVendor: "Vendor",
      noData: "No devices found. Press Start Scan to begin.",
    },
    th: {
      title: "สแกนซินแลน",
      subtitle: "เครื่องมือตรวจสอบเครือข่ายสำหรับสายโปร",
      scanBtn: "เริ่มสแกน",
      scanningBtn: "กำลังสแกน...",
      statTotal: "อุปกรณ์ทั้งหมด",
      statOnline: "กำลังออนไลน์",
      statUnknown: "ไม่ระบุยี่ห้อ",
      colStatus: "สถานะ",
      colIP: "ไอพีแอดเดรส",
      colMAC: "แมคแอดเดรส",
      colVendor: "ผู้ผลิต/ยี่ห้อ",
      noData: "ไม่พบข้อมูล กดปุ่มเริ่มสแกนเพื่อตรวจสอบ",
    },
  };

  const [lang, setLang] = useState("en"); 
  const t = translations[lang]; 

  const scanNetwork = async () => {
    setLoading(true);
    try {
      const response = await axios.get("http://localhost:8000/api/scan");
      setDevices(response.data.data);
    } catch (error) {
      console.error("Error scanning:", error);
      alert(
        "เชื่อมต่อ Api Backend ไม่ได้! ลืมไรป่าว (บอกให้ก็ดะ รัน Python ยาง)",
      );
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-black text-slate-100 p-8 font-sans">
      {/* Header */}
      <div className="flex gap-2">
        <button
          onClick={() => setLang("th")}
          className={`px-3 py-1 rounded text-xs font-bold transition-all ${lang === "th" ? "bg-blue-600 text-white" : "bg-slate-800 text-slate-400"}`}
        >
          TH
        </button>
        <button
          onClick={() => setLang("en")}
          className={`px-3 py-1 rounded text-xs font-bold transition-all ${lang === "en" ? "bg-blue-600 text-white" : "bg-slate-800 text-slate-400"}`}
        >
          EN
        </button>
      </div>
      <div className="max-w-4xl mx-auto flex justify-between items-center mb-10">
        <div>
          <h1 className="text-3xl font-bold text-blue-400 flex items-center gap-2">
            <ShieldAlert size={32} /> {t.title}{" "}
            <span className="text-sm bg-blue-900 px-2 py-1 rounded text-blue-200">
              v1.0
            </span>
          </h1>
          <p className="text-slate-400 mt-1">
            {t.subtitle}
          </p>
        </div>

        <button
          onClick={scanNetwork}
          disabled={loading}
          className="bg-blue-600 hover:bg-blue-500 disabled:bg-slate-700 px-6 py-3 rounded-lg font-bold flex items-center gap-2 transition-all active:scale-95 shadow-lg shadow-blue-900/20"
        >
          {loading ? (
            "Scanning..."
          ) : (
            <>
              <Search size={20} /> {t.scanBtn}
            </>
          )}
        </button>
      </div>

      {/* Stats Table */}
      <div className="max-w-4xl mx-auto bg-slate-800 rounded-xl border border-slate-700 overflow-hidden">
        <table className="w-full text-left">
          <thead className="bg-slate-700/50 text-slate-300 text-sm uppercase">
            <tr>
              <th className="p-4">{t.colID}</th>
              <th className="p-4">{t.colStatus}</th>
              <th className="p-4">{t.colIP}</th>
              <th className="p-4">{t.colMAC}</th>
              <th className="p-4">{t.colVendor}</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-700">
            {devices.length > 0 ? (
              devices.map((dev, idx) => (
                <tr
                  key={idx}
                  className="hover:bg-blue-500/10 hover:shadow-[inset_0_0_20px_rgba(59,130,246,0.1)] transition-all"
                >
                  <td className="p-4">{idx + 1}</td>
                  <td className="p-4">
                    <span
                      className={`flex items-center gap-2 ${dev.status === "online" ? "text-green-400" : "text-amber-400"}`}
                    >
                      <div
                        className={`w-2 h-2 rounded-full ${dev.status === "online" ? "bg-green-400 animate-pulse" : "bg-amber-400"}`}
                      ></div>
                      {dev.status}
                    </span>
                  </td>
                  <td className="p-4 font-mono text-blue-300">{dev.ip}</td>
                  <td className="p-4 text-slate-400">{dev.mac}</td>
                  <td className="p-4 text-sm text-slate-300 italic">
                    {dev.vendor || "Unknown"}
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="4" className="p-10 text-center text-slate-500">
                  <div className="flex flex-col items-center gap-3">
                    <Cpu size={48} className="opacity-20" />
                    {t.noData}
                  </div>
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default App;
