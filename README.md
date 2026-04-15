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
| Vendor Lookup | mac-vendor-lookup |

---

## โครงสร้างโปรเจค

```
scanzinLAN/
├── backend/
│   ├── main.py          # FastAPI server + ARP scan logic
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
pip install fastapi uvicorn scapy netifaces mac-vendor-lookup

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
| `/api/scan` | GET | สแกนอุปกรณ์ทั้งหมดใน LAN (subnet /24) |

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
- รองรับ 2 ภาษา: ไทย / อังกฤษ
- Fallback เป็น mock data เมื่อสแกนไม่เจออุปกรณ์

---

## หมายเหตุ

- การสแกนใช้ ARP ดังนั้นเห็นได้เฉพาะอุปกรณ์ใน subnet เดียวกัน
- Scapy บน Windows ต้องการ [Npcap](https://npcap.com/) ติดตั้งก่อน
- ครั้งแรกที่รัน อาจช้าเพราะต้อง update vendor database
