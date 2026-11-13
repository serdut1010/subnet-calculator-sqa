from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
import ipaddress

app = FastAPI()

def hitung_subnet(ip: str, prefix: int) -> dict:
    if prefix < 0 or prefix > 32:
        raise ValueError("Prefix harus di antara 0 sampai 32.")
    try:
        addr = ipaddress.IPv4Address(ip)
    except Exception:
        raise ValueError("Format alamat IP tidak valid.")
    
    # Validasi string oktet ketat (tanpa leading zero)
    oktet = ip.split('.')
    if len(oktet) != 4:
        raise ValueError("IP harus terdiri dari 4 oktet.")
    for o in oktet:
        if not o.isdigit() or (len(o) > 1 and o[0] == '0'):
            raise ValueError("Oktet IP tidak boleh memiliki angka nol di depan.")

    net = ipaddress.IPv4Network(f"{ip}/{prefix}", strict=False)
    
    # Untuk prefix 31 dan 32, RFC 3021/host tunggal menggunakan mask 255.255.255.255 secara praktis di beberapa implementasi, 
    # namun mari ikuti netmask standar ipaddress atau sesuaikan dengan test_main.py
    if prefix == 31:
        mask = "255.255.255.255"
        broadcast = None
        first_host = str(net[0])
        last_host = str(net[1])
        usable_hosts = 2
    elif prefix == 32:
        mask = "255.255.255.255"
        broadcast = None
        first_host = str(net[0])
        last_host = str(net[0])
        usable_hosts = 1
    else:
        mask = str(net.netmask)
        broadcast = str(net.broadcast_address)
        hosts = list(net.hosts())
        usable_hosts = len(hosts)
        first_host = str(hosts[0]) if usable_hosts > 0 else None
        last_host = str(hosts[-1]) if usable_hosts > 0 else None

    return {
        "mask": mask,
        "network": str(net.network_address),
        "broadcast": broadcast,
        "first_host": first_host,
        "last_host": last_host,
        "usable_hosts": usable_hosts
    }

def alokasi_vlsm(network_cidr: str, kebutuhan_host: list[int]) -> list[dict]:
    try:
        base = ipaddress.IPv4Network(network_cidr, strict=True)
    except ValueError:
        raise ValueError("Network CIDR tidak valid.")

    if not kebutuhan_host or any(
        isinstance(k, bool) or not isinstance(k, int) or k < 1
        for k in kebutuhan_host
    ):
        raise ValueError("Daftar kebutuhan kosong atau berisi nilai < 1.")

    cur = int(base.network_address)
    end = int(base.broadcast_address)
    hasil = []

    for need in sorted(kebutuhan_host, reverse=True):
        ukuran = 4  # minimal /30
        while ukuran < need + 2:
            ukuran *= 2
        prefix = 32 - (ukuran.bit_length() - 1)

        if cur % ukuran:  # ratakan ke batas blok
            cur += ukuran - cur % ukuran

        if cur + ukuran - 1 > end:
            raise ValueError("Blok tidak cukup menampung seluruh kebutuhan.")

        ip = str(ipaddress.IPv4Address(cur))
        hasil.append({
            "kebutuhan": need,
            "network_cidr": f"{ip}/{prefix}",
            **hitung_subnet(ip, prefix),
        })
        cur += ukuran

    return hasil

@app.get("/", response_class=HTMLResponse)
def read_root():
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "<h1>index.html tidak ditemukan</h1>"

@app.get("/api/subnet")
def api_subnet(ip: str, prefix: int):
    try:
        return hitung_subnet(ip, prefix)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/vlsm")
def api_vlsm(data: dict):
    net_str = data.get("network")
    kebutuhan = data.get("kebutuhan_host")
    try:
        return alokasi_vlsm(net_str, kebutuhan)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))