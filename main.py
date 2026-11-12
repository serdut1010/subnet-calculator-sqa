import re
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

app = FastAPI()

BASE_DIR = Path(__file__).parent


def _ip_ke_angka(ip):
    """Ubah 'a.b.c.d' menjadi bilangan 32 bit, setelah divalidasi."""
    if not isinstance(ip, str) or ip == "":
        raise ValueError("Alamat IP tidak boleh kosong.")
    bagian = ip.split(".")
    if len(bagian) != 4:
        raise ValueError("Alamat IP harus terdiri dari 4 oktet yang dipisah titik.")
    angka_ip = 0
    for oktet in bagian:
        if not (oktet.isascii() and oktet.isdigit()):
            raise ValueError("Setiap oktet harus berupa angka tanpa spasi.")
        if len(oktet) > 1 and oktet.startswith("0"):
            raise ValueError("Oktet tidak boleh diawali angka nol.")
        nilai = int(oktet)
        if nilai > 255:
            raise ValueError("Setiap oktet harus antara 0 dan 255.")
        angka_ip = (angka_ip << 8) | nilai
    return angka_ip


def _angka_ke_ip(angka):
    """Ubah bilangan 32 bit menjadi teks 'a.b.c.d'."""
    return ".".join(str((angka >> geser) & 255) for geser in (24, 16, 8, 0))


def hitung_subnet(ip: str, prefix: int) -> dict:
    angka_ip = _ip_ke_angka(ip)

    if isinstance(prefix, bool) or not isinstance(prefix, int):
        raise ValueError("Prefix harus bilangan bulat 0 sampai 32.")
    if prefix < 0 or prefix > 32:
        raise ValueError("Prefix harus antara 0 dan 32.")

    # Subnet mask: 'prefix' bit 1 di kiri, sisanya bit 0
    mask = (0xFFFFFFFF << (32 - prefix)) & 0xFFFFFFFF
    # Network address: IP AND subnet mask
    network = angka_ip & mask
    # Broadcast: semua bit host bernilai 1
    broadcast = network | (~mask & 0xFFFFFFFF)

    if prefix == 32:
        return {
            "mask": _angka_ke_ip(mask),
            "network": _angka_ke_ip(network),
            "broadcast": None,
            "first_host": _angka_ke_ip(angka_ip),
            "last_host": _angka_ke_ip(angka_ip),
            "usable_hosts": 1,
        }
    if prefix == 31:
        return {
            "mask": _angka_ke_ip(mask),
            "network": _angka_ke_ip(network),
            "broadcast": None,
            "first_host": _angka_ke_ip(network),
            "last_host": _angka_ke_ip(network + 1),
            "usable_hosts": 2,
        }
    return {
        "mask": _angka_ke_ip(mask),
        "network": _angka_ke_ip(network),
        "broadcast": _angka_ke_ip(broadcast),
        "first_host": _angka_ke_ip(network + 1),
        "last_host": _angka_ke_ip(broadcast - 1),
        "usable_hosts": 2 ** (32 - prefix) - 2,
    }


def _baca_prefix(teks):
    if not isinstance(teks, str) or not re.fullmatch(r"[0-9]{1,3}", teks):
        raise ValueError("Prefix harus bilangan bulat 0 sampai 32.")
    return int(teks)


@app.get("/api/subnet")
def api_subnet(ip: str = "", prefix: str = ""):
    try:
        return hitung_subnet(ip, _baca_prefix(prefix))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/", response_class=HTMLResponse)
def halaman_utama():
    return (BASE_DIR / "index.html").read_text(encoding="utf-8")