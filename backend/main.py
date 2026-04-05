from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from scapy.all import ARP , Ether , srp
import random
import netifaces
from mac_vendor_lookup import MacLookup

app = FastAPI()

vendor_lookup = MacLookup()
try:
    vendor_lookup.update_vendors()
except:
    pass

def get_vendor(mac):
    try:
        mac_lookup = MacLookup()

        mac_lookup.update_vendors()
        
        # ค้นหา vendor
        vendor = mac_lookup.lookup(mac)
        return vendor
    except Exception as e:
        return f"Unknown Device ({e})"
        
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
        # หา GW และ interface ที่่ใช่อยู่
        gws = netifaces.gateways()
        interface = gws['default'][netifaces.AF_INET][1]
        addrs = netifaces.ifaddresses(interface)
        ip_info = addrs[netifaces.AF_INET][0]
        
        # แปลงไอพีตัวเองให้เป็น วงเน็ต
        ip_parts = ip_info['addr'].split('.')
        network_range = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.0/24"

        # ip range ที่จะสแกน (ในที่นี้คือ /24 ของ IP ที่เราได้มา) หรือจะใช้ IP range อื่นก็ได้ตามต้องการ
        ip_range = network_range
        
        arp = ARP(pdst=ip_range)
        ether = Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = ether/arp
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
        
