# วิธีใช้งาน ScanzinLAN

คู่มือการใช้งานแบบ step-by-step สำหรับการสแกนอุปกรณ์ในเครือข่าย LAN

---

## ก่อนเริ่ม — สิ่งที่ต้องมี

- [x] Python 3.8 ขึ้นไป
- [x] Node.js 18 ขึ้นไป
- [x] **Npcap** (Windows เท่านั้น) — ดาวน์โหลดที่ [npcap.com](https://npcap.com/)
- [x] เชื่อมต่อ WiFi หรือ LAN อยู่
- [x] รัน Terminal/CMD **ในฐานะ Administrator** (สำคัญมาก!)

---

## ขั้นตอนที่ 1 — เปิด Backend

1. เปิด Terminal ในฐานะ **Administrator**

2. เข้าไปที่โฟลเดอร์ `backend`
   ```bash
   cd path/to/scanzinLAN/backend
   ```

3. เปิดใช้งาน virtual environment
   ```bash
   .venv\Scripts\activate
   ```
   > ถ้ายังไม่เคยสร้าง venv ให้รัน `python -m venv .venv` ก่อน

4. ติดตั้ง dependencies (ทำครั้งแรกครั้งเดียวพอ)
   ```bash
   pip install fastapi uvicorn scapy netifaces mac-vendor-lookup
   ```

5. รัน server
   ```bash
   python main.py
   ```

6. ถ้าขึ้นแบบนี้แปลว่าพร้อมแล้ว
   ```
   INFO:     Uvicorn running on http://0.0.0.0:8000
   ```

---

## ขั้นตอนที่ 2 — เปิด Frontend

1. เปิด Terminal ใหม่อีกอัน (ไม่ต้อง Admin)

2. เข้าไปที่โฟลเดอร์ `frontend`
   ```bash
   cd path/to/scanzinLAN/frontend
   ```

3. ติดตั้ง node modules (ทำครั้งแรกครั้งเดียวพอ)
   ```bash
   npm install
   ```

4. รัน dev server
   ```bash
   npm run dev
   ```

5. เปิดเบราว์เซอร์ไปที่ `http://localhost:5173`

---

## ขั้นตอนที่ 3 — เริ่มสแกน

1. เข้าหน้าเว็บ `http://localhost:5173`
2. กดปุ่ม **"Start Scan"** (หรือ **"เริ่มสแกน"** ถ้าเลือกภาษาไทย)
3. รอสักครู่ — การสแกนใช้เวลาประมาณ 3–10 วินาที
4. ผลลัพธ์จะแสดงเป็นตาราง พร้อม IP, MAC, Vendor, และสถานะ

---

## การสลับภาษา

กดปุ่ม **TH** / **EN** ที่มุมบนซ้ายของหน้าเว็บ

---

## อ่านผลลัพธ์

| คอลัมน์ | ความหมาย |
|---------|----------|
| Status | `online` = เปิดอยู่ตอนสแกน |
| IP Address | IP ของอุปกรณ์นั้นในเครือข่าย |
| MAC Address | Hardware address ของ network card |
| Vendor | ยี่ห้อ/ผู้ผลิตอุปกรณ์ (จาก MAC) |

> ถ้าเห็นข้อความ **"This is mock data"** แปลว่าสแกนไม่เจออุปกรณ์จริง ลองเช็คการเชื่อมต่อเน็ตหรือลองสแกนใหม่

---

## แก้ปัญหาเบื้องต้น

| ปัญหา | วิธีแก้ |
|-------|---------|
| `เชื่อมต่อ API Backend ไม่ได้` | ตรวจสอบว่า `python main.py` รันอยู่ที่ port 8000 |
| สแกนเจอแค่ mock data | รัน backend ในฐานะ Administrator |
| `import scapy` error | ติดตั้ง Npcap ก่อนแล้วรีสตาร์ท terminal |
| ผล vendor แสดง Unknown | ปกติถ้าไม่มีอินเทอร์เน็ตตอนดึง vendor database |
