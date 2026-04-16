from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from scapy.all import ARP , Ether , srp
import netifaces
import ipaddress
import urllib.request
import json
import os

app = FastAPI()

# ---------- OUI Vendor Database (local cache) ----------
OUI_CACHE_PATH = os.path.join(os.path.dirname(__file__), "oui_cache.json")
OUI_DOWNLOAD_URL = "https://maclookup.app/downloads/json-database/get-db"

def load_vendor_db() -> dict:
    """โหลด OUI database จาก local cache ถ้าไม่มีให้ดาวน์โหลดก่อน"""
    if os.path.exists(OUI_CACHE_PATH):
        print("[OUI] โหลด vendor database จาก local cache...")
        with open(OUI_CACHE_PATH, "r", encoding="utf-8") as f:
            raw = json.load(f)
        # แปลงเป็น dict: {"AABBCC": "Vendor Name"} เพื่อ O(1) lookup
        return {
            entry["macPrefix"].replace(":", "").upper(): entry["vendorName"]
            for entry in raw
            if "macPrefix" in entry and "vendorName" in entry
        }

    print("[OUI] ไม่พบ local cache — กำลังดาวน์โหลด OUI database...")
    try:
        req = urllib.request.Request(OUI_DOWNLOAD_URL, headers={"User-Agent": "ScanzinLAN/1.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = json.loads(resp.read().decode("utf-8"))
        with open(OUI_CACHE_PATH, "w", encoding="utf-8") as f:
            json.dump(raw, f)
        print(f"[OUI] ดาวน์โหลดสำเร็จ บันทึก {len(raw):,} รายการลง {OUI_CACHE_PATH}")
        return {
            entry["macPrefix"].replace(":", "").upper(): entry["vendorName"]
            for entry in raw
            if "macPrefix" in entry and "vendorName" in entry
        }
    except Exception as e:
        print(f"[OUI] ดาวน์โหลดไม่ได้: {e} — vendor จะแสดงเป็น Unknown")
        return {}

# โหลดครั้งเดียวตอน startup
VENDOR_DB: dict = load_vendor_db()

def get_vendor(mac: str) -> str:
    """ค้นหา vendor จาก MAC address โดยใช้ OUI prefix (3 bytes แรก)"""
    try:
        prefix = mac.replace(":", "").replace("-", "")[:6].upper()
        return VENDOR_DB.get(prefix, "Unknown")
    except Exception:
        return "Unknown"
        
#อนุญาตให้ frontend คุยกับ backend ได้
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# mock data สำหรับแสดงผล หรือตอนสแกนไม่ติด
MOCK_DEVICES = [
    {"-": "", "-": "", "-": "-", "-": "This is mock data, no devices found during scan, Please check your network connection or try again later."},
    {"ip": "192.168.1.1", "mac": "64:20:e1:9f:47:1a", "vendor": "TP-Link", "status": "online"},
    {"ip": "192.168.1.42", "mac": "14:98:77:51:51:0d", "vendor": "Apple Inc.", "status": "online"},
    {"ip": "192.168.1.215", "mac": "06:28:67:f8:b2:cd", "vendor": "Unknown", "status": "away"},
]

@app.get("/api/scan")
async def scan():
    try:
        # 1. หาข้อมูล Interface และ IP/Mask ของเรา
        gws = netifaces.gateways()
        interface = gws['default'][netifaces.AF_INET][1]
        addrs = netifaces.ifaddresses(interface)
        ip_info = addrs[netifaces.AF_INET][0]
        
        my_ip = ip_info['addr']
        my_mask = ip_info['netmask'] # ดึง Subnet Mask มาด้วย (สำคัญ!)

        # 2. คำนวณหา Network Range ที่แท้จริงจาก IP และ Mask
        # วิธีนี้จะทำให้ถ้า Mask เป็น 255.255.254.0 (/23) มันจะรวม 20.x และ 21.x ให้เองอัตโนมัติ
        network = ipaddress.IPv4Interface(f"{my_ip}/{my_mask}").network
        ip_range = str(network) # จะได้ค่าอย่างเช่น "192.168.20.0/23"

        # 3. รันการสแกนด้วย ip_range ที่คำนวณได้
        arp = ARP(pdst=ip_range)
        ether = Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = ether/arp
        
        # เพิ่ม timeout นิดนึงเพราะ /23 วงมันใหญ่ (512 IP)
        result = srp(packet, timeout=3, verbose=False)[0]

        clients = []
        for sent, received in result:
            clients.append({
                'ip': received.psrc,
                'mac': received.hwsrc, 
                'status': 'online',
                'vendor': get_vendor(received.hwsrc)
            })

        # ถ้าสแกนเจอ ให้ส่งค่าจริง ถ้าไม่เจอส่ง Mock (หรือตอนนี้จะบังคับส่ง Mock ไปก่อนเพื่อทำ UI ก็ได้)
        if len(clients) > 0:
            #TODO: เพิ่มการตรวจสอบ vendor จาก MAC address ด้วย (อาจใช้ไลบรารีหรือ API ที่มีอยู่)
            return {"status": "success", "data": clients , "mock": False}
            #return {"status": "success", "data": MOCK_DEVICES}
        else:
            return {"status": "success", "data": MOCK_DEVICES , "mock": True}
        

    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
        
