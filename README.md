# ScanzinLAN

**Network Monitoring Tool for Professional Gents**
เครื่องมือสแกนอุปกรณ์ในเครือข่าย LAN แบบ real-time ด้วย ARP scanning

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 19 + Vite + TailwindCSS |
| Backend | FastAPI (Python) |
| Scanning | Scapy (ARP) |
| Vendor Lookup | IEEE OUI database (local cache) |

---

## โครงสร้างโปรเจค

```
scanzinLAN/
├── backend/
│   ├── main.py          # FastAPI server + ARP scan logic
│   ├── oui_cache.json   # OUI vendor database (สร้างอัตโนมัติครั้งแรก)
│   └── requirements.py  # Python dependencies
└── frontend/
    ├── src/
    │   ├── App.jsx       # UI หลัก + ภาษา TH/EN
    │   └── index.css
    ├── package.json
    └── vite.config.js
```

---

## วิธีติดตั้งและรัน

> วิธีการใช้แบบ step-by-step [Click here to view HowToScanz.md](./HowToScanz.md)

### ข้อกำหนดเบื้องต้น
- Python 3.8+
- Node.js 18+
- **Windows**: ต้องรัน Backend ในฐานะ Administrator (Scapy ต้องการ raw socket)
- **Linux/macOS**: อาจต้องใช้ `sudo`

### Backend

```bash
cd backend

# สร้าง virtual environment
python -m venv .venv
.venv\Scripts\activate       # Windows
# source .venv/bin/activate  # Linux/macOS

# ติดตั้ง dependencies
pip install fastapi uvicorn scapy netifaces

# รัน server
python main.py
```

Backend จะขึ้นที่ `http://localhost:8000`

### Frontend

```bash
cd frontend

npm install
npm run dev
```

Frontend จะขึ้นที่ `http://localhost:5173`

---

## API

| Endpoint | Method | คำอธิบาย |
|----------|--------|----------|
| `/api/scan` | GET | สแกนอุปกรณ์ทั้งหมดใน LAN (ตาม subnet จริงของ interface) |

**Response ตัวอย่าง:**
```json
{
  "status": "success",
  "mock": false,
  "data": [
    {
      "ip": "192.168.1.1",
      "mac": "64:20:e1:9f:47:1a",
      "vendor": "TP-Link",
      "status": "online"
    }
  ]
}
```

> ถ้าสแกนไม่เจออุปกรณ์เลย จะส่ง `"mock": true` พร้อม mock data กลับมาแทน

---

## Features

- สแกนอุปกรณ์ใน LAN ด้วย ARP packet
- แสดง IP, MAC Address, Vendor/ยี่ห้อ, และสถานะ
- ระบุยี่ห้ออุปกรณ์จาก IEEE OUI database (ดาวน์โหลดครั้งแรก แล้วทำงานออฟไลน์ได้)
- รองรับ 2 ภาษา: ไทย / อังกฤษ
- Fallback เป็น mock data เมื่อสแกนไม่เจออุปกรณ์

---

## หมายเหตุ

- การสแกนใช้ ARP และคำนวณ network range จาก IP + netmask จริงของ interface รองรับทุก subnet เช่น /23, /24
- Scapy บน Windows ต้องการ [Npcap](https://npcap.com/) ติดตั้งก่อน
- **ครั้งแรกที่รัน** ต้องมีอินเทอร์เน็ตเพื่อดาวน์โหลด OUI database (~5MB) → บันทึกเป็น `oui_cache.json` แล้วใช้งานออฟไลน์ได้ตลอด
- `oui_cache.json` ถูก ignore ใน git — แต่ละเครื่องจะดาวน์โหลดเองอัตโนมัติ
