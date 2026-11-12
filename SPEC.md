# SPEC: Kalkulator Subnet & VLSM

Versi 1.0 | Status: menunggu persetujuan manusia (Tahap 2)

## 1. Tujuan

Membangun kalkulator subnet dan VLSM berbasis web untuk guru SMK TKJ.

- **Input:** alamat IPv4 dan prefix (mode Subnet); blok induk CIDR dan daftar kebutuhan host (mode VLSM).
- **Output:** mask, network address, broadcast address, range host (host pertama dan terakhir), dan jumlah host.
- **Prinsip utama:** kebenaran hasil harus bisa dinilai guru **tanpa membaca kode**. Karena itu seluruh perilaku didefinisikan lewat tabel test di Bagian 6, dengan angka yang bisa dicek manual.
- **Teknologi:** Python 3.12, FastAPI, satu halaman HTML (`index.html`). Logika di `main.py`, test di `test_main.py` (pytest).

## 2. Aturan Validasi

### 2.1 Alamat IP

| Aturan | Contoh ditolak |
|---|---|
| Tepat 4 oktet, dipisah titik | `192.168.1`, `192.168.1.1.1` |
| Tiap oktet bilangan bulat 0 sampai 255 | `256.1.1.1`, `192.168.a.1` |
| Tanpa angka nol di depan | `192.168.01.1` |
| Tanpa spasi (awal, akhir, atau tengah) | `" 192.168.1.1"` |
| Tidak boleh kosong | `""` |
| Hanya IPv4 | `2001:db8::1` |

### 2.2 Prefix

- Harus bilangan bulat **0 sampai 32**.
- Ditolak: `33`, `-1`, `abc`, `24.5`, kosong.

### 2.3 Kebutuhan host (VLSM)

- Setiap nilai harus bilangan bulat **>= 1**.
- Ditolak: `0`, `-5`, `2.5`, `"abc"`.
- Daftar kebutuhan tidak boleh kosong.

### 2.4 Blok induk VLSM

- Format CIDR `a.b.c.d/n`, dan harus berupa **alamat jaringan** (bit host bernilai 0).
- `192.168.1.0/24` valid; `192.168.1.10/24` **ditolak** (bukan alamat jaringan). Tidak ada normalisasi otomatis.

### 2.5 Penanganan kesalahan

- Fungsi melempar `ValueError` dengan pesan berbahasa Indonesia yang jelas.
- API mengubahnya menjadi **HTTP 400** dengan JSON `{"detail": "<pesan>"}`.

## 3. Kontrak Fungsi

### 3.1 `hitung_subnet(ip: str, prefix: int) -> dict`

Kunci hasil (semua bertipe string, kecuali yang disebut lain):

| Kunci | Isi |
|---|---|
| `mask` | Subnet mask desimal bertitik, mis. `255.255.255.128` |
| `network` | Network address = **IP AND subnet mask** (dihitung bitwise) |
| `broadcast` | Broadcast address; `None` untuk /31 dan /32 |
| `first_host` | Host pertama yang bisa dipakai |
| `last_host` | Host terakhir yang bisa dipakai |
| `usable_hosts` | Jumlah host (bilangan bulat) |

Aturan per rentang prefix:

| Prefix | usable_hosts | broadcast | first_host / last_host |
|---|---|---|---|
| 0 sampai 30 | 2^(32 - prefix) - 2 | network + (2^(32 - prefix) - 1) | network + 1 / broadcast - 1 |
| **/31** | **2** (RFC 3021, point-to-point) | `None` | network / network + 1 |
| **/32** | **1** | `None` | keduanya = IP itu sendiri |

Catatan:

- IP yang diberikan boleh berada di tengah blok (mis. `172.16.5.130/25`); hasilnya selalu dinormalkan ke network yang benar.
- IP yang sama dengan alamat network atau broadcast **tetap diproses tanpa peringatan**.
- /0 diterima (prefix valid 0 sampai 32).
- Tidak ada klasifikasi privat/publik atau label alamat khusus (di luar cakupan).

### 3.2 `alokasi_vlsm(network_cidr: str, kebutuhan_host: list[int]) -> list[dict]`

Algoritma:

1. Validasi `network_cidr` dan `kebutuhan_host` (Bagian 2.3 dan 2.4).
2. Urutkan kebutuhan dari **terbesar ke terkecil**. Untuk kebutuhan yang sama besar, **urutan input dipertahankan** (pengurutan stabil).
3. Untuk tiap kebutuhan `n`, ukuran blok = **pangkat 2 terkecil yang >= n + 2**, dengan **minimal 4 alamat (/30)**.
4. Alokasikan berurutan, mulai dari alamat network blok induk, tanpa celah dan tanpa tumpang tindih.
5. Bila blok induk tidak cukup menampung semua kebutuhan, lempar `ValueError`.

Setiap elemen hasil memuat:

- `kebutuhan` (bilangan bulat, sesuai input)
- `network_cidr` (mis. `192.168.1.0/25`)
- semua kunci `hitung_subnet` untuk subnet itu (`mask`, `network`, `broadcast`, `first_host`, `last_host`, `usable_hosts`)

Hasil diurutkan sesuai urutan alokasi (terbesar dulu).

`ValueError` dilempar bila:

- `network_cidr` bukan alamat jaringan yang valid
- daftar kebutuhan kosong atau berisi nilai < 1 atau bukan bilangan bulat
- total blok yang dibutuhkan melebihi ukuran blok induk (termasuk induk /31 dan /32, karena blok minimum /30)

Asumsi: angka kebutuhan adalah **jumlah host yang bisa dipakai** (router/gateway sudah termasuk di dalamnya, tidak ditambah otomatis).

## 4. Kontrak API

| Endpoint | Parameter | Respons sukses | Respons gagal |
|---|---|---|---|
| `GET /api/subnet` | query `ip`, `prefix` | 200, JSON hasil `hitung_subnet` | 400, `{"detail": "..."}` |
| `POST /api/vlsm` | body JSON `{"network": "192.168.1.0/24", "kebutuhan_host": [100, 50, 20, 2]}` | 200, JSON array hasil `alokasi_vlsm` | 400, `{"detail": "..."}` |
| `GET /` | tidak ada | 200, isi `index.html` | tidak ada |

Ketentuan:

- Parameter yang hilang, bertipe salah, atau tidak valid menghasilkan **400** (bukan 422). Implementasi harus menangani validasi bawaan FastAPI agar keluaran tetap 400 dengan field `detail`.
- `prefix` pada query diterima sebagai teks lalu divalidasi sendiri, sehingga `abc` dan `24.5` menghasilkan 400.

## 5. Halaman Web

Satu halaman (`index.html`) dengan dua tab: **Subnet** dan **VLSM**. Desain mengikuti `DESIGN.md` (hasil Stitch).

**Tab Subnet**

- Isian: IP address, prefix (0 sampai 32), tombol "Calculate/Hitung".
- Kartu hasil: mask, network, broadcast, first host, last host, usable hosts.
- Untuk /31 dan /32, broadcast ditampilkan sebagai "tidak ada" (bukan kosong).

**Tab VLSM**

- Isian: blok induk (CIDR), daftar kebutuhan host yang bisa ditambah dan dihapus.
- Tabel hasil: kebutuhan, network CIDR, mask, range host, broadcast, jumlah host.

**Tiga keadaan** pada kedua tab: kosong, sukses, dan error. Pesan error diambil dari field `detail` respons API dan ditampilkan jelas di bawah isian.

## 6. Tabel Test Case

### 6.1 `hitung_subnet` (sukses)

| ID | Input | mask | network | broadcast | first_host | last_host | usable_hosts |
|---|---|---|---|---|---|---|---|
| T01 | 172.16.5.130/25 | 255.255.255.128 | 172.16.5.128 | 172.16.5.255 | 172.16.5.129 | 172.16.5.254 | 126 |
| T02 | 10.0.0.0/30 | 255.255.255.252 | 10.0.0.0 | 10.0.0.3 | 10.0.0.1 | 10.0.0.2 | 2 |
| T03 | 192.168.1.0/31 | 255.255.255.254 | 192.168.1.0 | None | 192.168.1.0 | 192.168.1.1 | 2 |
| T04 | 192.168.1.5/32 | 255.255.255.255 | 192.168.1.5 | None | 192.168.1.5 | 192.168.1.5 | 1 |
| T05 | 192.168.1.10/24 | 255.255.255.0 | 192.168.1.0 | 192.168.1.255 | 192.168.1.1 | 192.168.1.254 | 254 |
| T06 | 192.168.1.100/26 | 255.255.255.192 | 192.168.1.64 | 192.168.1.127 | 192.168.1.65 | 192.168.1.126 | 62 |
| T07 | 172.16.50.1/20 | 255.255.240.0 | 172.16.48.0 | 172.16.63.255 | 172.16.48.1 | 172.16.63.254 | 4094 |
| T08 | 10.0.0.5/8 | 255.0.0.0 | 10.0.0.0 | 10.255.255.255 | 10.0.0.1 | 10.255.255.254 | 16777214 |
| T09 | 192.168.1.255/24 (IP = broadcast) | 255.255.255.0 | 192.168.1.0 | 192.168.1.255 | 192.168.1.1 | 192.168.1.254 | 254 |
| T10 | 0.0.0.0/0 | 0.0.0.0 | 0.0.0.0 | 255.255.255.255 | 0.0.0.1 | 255.255.255.254 | 4294967294 |

### 6.2 `hitung_subnet` (ditolak, `ValueError`)

| ID | Input | Alasan |
|---|---|---|
| X01 | 256.1.1.1/24 | oktet > 255 |
| X02 | 192.168.01.1/24 | nol di depan |
| X03 | 192.168.1/24 | oktet kurang |
| X04 | 192.168.1.1.1/24 | oktet berlebih |
| X05 | abc/24 | bukan IP |
| X06 | (kosong)/24 | IP kosong |
| X07 | 192.168.1.1/33 | prefix > 32 |
| X08 | 192.168.1.1/-1 | prefix negatif |
| X09 | 192.168.1.1/abc | prefix bukan angka |
| X10 | 192.168.1.1/24.5 | prefix desimal |
| X11 | " 192.168.1.1"/24 | ada spasi |
| X12 | 192.168.1.1 (prefix kosong) | prefix kosong |

### 6.3 `alokasi_vlsm`

| ID | Induk | Kebutuhan | Hasil yang diharapkan |
|---|---|---|---|
| V01 | 192.168.1.0/24 | 100, 50, 20, 2 | 192.168.1.0/25, 192.168.1.128/26, 192.168.1.192/27, 192.168.1.224/30 |
| V02 | 192.168.1.0/24 | 2, 20, 100, 50 (urutan acak) | Sama dengan V01 |
| V03 | 192.168.1.0/24 | 126 | 192.168.1.0/25 (pas, 126 host) |
| V04 | 192.168.1.0/24 | 127 | 192.168.1.0/24 (butuh 129 alamat) |
| V05 | 192.168.1.0/24 | 1 | 192.168.1.0/30 (minimal /30) |
| V06 | 192.168.1.0/24 | 126, 126 | 192.168.1.0/25 dan 192.168.1.128/25, sisa 0, tanpa error |
| V07 | 192.168.1.0/24 | 30, 30, 30 | 192.168.1.0/27, 192.168.1.32/27, 192.168.1.64/27 (urutan input dipertahankan) |
| V08 | 10.0.0.0/8 | 1000, 500 | 10.0.0.0/22 dan 10.0.4.0/23 |
| V09 | 192.168.1.0/30 | 2 | 192.168.1.0/30 (muat persis) |

Untuk V01, rincian lengkap tiap subnet:

| Kebutuhan | network_cidr | broadcast | first_host | last_host | usable_hosts |
|---|---|---|---|---|---|
| 100 | 192.168.1.0/25 | 192.168.1.127 | 192.168.1.1 | 192.168.1.126 | 126 |
| 50 | 192.168.1.128/26 | 192.168.1.191 | 192.168.1.129 | 192.168.1.190 | 62 |
| 20 | 192.168.1.192/27 | 192.168.1.223 | 192.168.1.193 | 192.168.1.222 | 30 |
| 2 | 192.168.1.224/30 | 192.168.1.227 | 192.168.1.225 | 192.168.1.226 | 2 |

Sifat umum yang berlaku untuk **semua** kasus VLSM yang sukses:

- Tidak ada dua subnet yang saling tumpang tindih.
- Semua subnet berada di dalam blok induk.
- Network tiap subnet rata terhadap batas prefix-nya.

### 6.4 `alokasi_vlsm` (ditolak, `ValueError`)

| ID | Induk | Kebutuhan | Alasan |
|---|---|---|---|
| W01 | 192.168.1.0/24 | 200, 100 | total 384 alamat > 256, tidak muat |
| W02 | 192.168.1.0/24 | 300 | satu kebutuhan melebihi induk |
| W03 | 192.168.1.0/24 | 126, 126, 2 | subnet ketiga tidak muat |
| W04 | 192.168.1.0/24 | (daftar kosong) | daftar kosong |
| W05 | 192.168.1.0/24 | 0 | nilai < 1 |
| W06 | 192.168.1.0/24 | -5 | nilai < 1 |
| W07 | 192.168.1.0/24 | 2.5 | bukan bilangan bulat |
| W08 | 192.168.1.10/24 | 10 | induk bukan alamat jaringan |
| W09 | 192.168.1.0/33 | 10 | prefix tidak valid |
| W10 | abc | 10 | induk bukan CIDR |
| W11 | 192.168.1.0/31 | 2 | induk lebih kecil dari blok minimum /30 |

### 6.5 API

| ID | Permintaan | Hasil yang diharapkan |
|---|---|---|
| A01 | `GET /api/subnet?ip=172.16.5.130&prefix=25` | 200, sama dengan T01 |
| A02 | `GET /api/subnet?ip=192.168.1.0&prefix=31` | 200, sama dengan T03 (broadcast `null`) |
| A03 | `GET /api/subnet?ip=256.1.1.1&prefix=24` | 400, ada field `detail` |
| A04 | `GET /api/subnet?ip=192.168.01.1&prefix=24` | 400, ada field `detail` |
| A05 | `GET /api/subnet?ip=192.168.1.1&prefix=abc` | 400, ada field `detail` |
| A06 | `GET /api/subnet?ip=192.168.1.1` (prefix hilang) | 400, ada field `detail` |
| A07 | `POST /api/vlsm` induk 192.168.1.0/24, kebutuhan 100, 50, 20, 2 | 200, sama dengan V01 |
| A08 | `POST /api/vlsm` induk 192.168.1.0/24, kebutuhan 200, 100 | 400, ada field `detail` |
| A09 | `POST /api/vlsm` body tidak lengkap | 400, ada field `detail` |
| A10 | `GET /` | 200, berisi HTML |

## 7. Di Luar Cakupan

- IPv6.
- Input subnet mask bertitik (mis. `255.255.255.0`); hanya notasi `/prefix`.
- Klasifikasi privat/publik (RFC 1918) dan label alamat khusus (loopback, APIPA, multicast).
- Peringatan bila IP sama dengan alamat network atau broadcast.
- Normalisasi otomatis blok induk VLSM yang tidak rata.
- Nama subnet dan penanganan nama duplikat.
- Menambahkan alamat gateway/router secara otomatis ke kebutuhan host.
- Autentikasi, database, dan penyimpanan riwayat.
- Ekspor hasil (PDF, CSV).

## Keputusan yang Dikunci

| Topik | Keputusan |
|---|---|
| /31 | RFC 3021: 2 host, broadcast `None` |
| /32 | 1 host, broadcast `None`, first = last = IP |
| /0 | Diterima |
| Nol di depan dan spasi | Ditolak |
| Subnet mask sebagai input | Tidak didukung |
| Blok minimum VLSM | /30 (kebutuhan 1 host menghasilkan /30) |
| Induk VLSM tidak rata | Ditolak |
| Kebutuhan sama besar | Urutan input dipertahankan |
| Kesalahan validasi API | HTTP 400 dengan field `detail` |
