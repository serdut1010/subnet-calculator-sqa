# [Feature] Kalkulator Subnet

## Deskripsi

Membuat kalkulator subnet IPv4 berbasis web untuk guru SMK TKJ. Pengguna memasukkan alamat IP dan prefix, lalu aplikasi menampilkan mask, network address, broadcast address, range host (host pertama dan terakhir), dan jumlah host. Hasil harus bisa dinilai guru tanpa membaca kode.

Spesifikasi lengkap ada di `SPEC.md`, desain tampilan ada di `index.html` dan `DESIGN.md`.

Cakupan issue ini: **mode Subnet saja** (fungsi `hitung_subnet`, endpoint `GET /api/subnet`, endpoint `GET /`, dan tab Subnet di halaman web). Mode VLSM dikerjakan di issue terpisah.

## Tugas

- [ ] Tulis test lebih dulu di `test_main.py` (pytest, `pytest.mark.parametrize`) untuk semua kasus pada tabel SPEC.md Bagian 6.1, 6.2, dan 6.5 (kasus API subnet dan `GET /`)
- [ ] Buat kerangka `main.py` (`app = FastAPI()` dan `hitung_subnet` yang hanya `raise NotImplementedError`), lalu tunjukkan test gagal (merah)
- [ ] Implementasikan `hitung_subnet(ip, prefix)` sesuai SPEC.md Bagian 3.1, dengan network = IP AND subnet mask (bitwise)
- [ ] Implementasikan `GET /api/subnet` dan `GET /` sesuai SPEC.md Bagian 4, kesalahan input menghasilkan HTTP 400 dengan field `detail`
- [ ] Hubungkan tab Subnet di `index.html` ke endpoint API, tampilkan hasil dan pesan error dari field `detail`
- [ ] Tambahkan pipeline CI (`.github/workflows/ci.yml`) setelah test ada
- [ ] Buka Pull Request ke `main` dan merge setelah CI hijau

## Kriteria Penerimaan

Merujuk pada tabel test di `SPEC.md`:

1. Semua kasus **T01 sampai T10** (Bagian 6.1) menghasilkan nilai yang persis sama dengan tabel.
2. Semua kasus **X01 sampai X12** (Bagian 6.2) ditolak dengan `ValueError`.
3. Semua kasus **A01 sampai A06 dan A10** (Bagian 6.5) lulus: sukses mengembalikan 200, input tidak valid mengembalikan 400 dengan field `detail`.
4. Aturan khusus berlaku: /31 memberi 2 host dan broadcast `None`; /32 memberi 1 host, broadcast `None`, first host = last host = IP itu.
5. `uv run pytest` hijau, dan `test_main.py` tidak diubah demi meloloskan test.
6. Halaman web menampilkan keadaan kosong, sukses, dan error pada tab Subnet.
7. CI di GitHub Actions hijau pada Pull Request.

## Alur Kerja

issue -> branch -> test dulu -> implementasi -> commit -> pull request -> CI -> merge

1. Issue ini dibuat dari dokumen ini.
2. Branch kerja: `feature/issue-<nomor>-subnet-calculator`, dibuat dari `main`.
3. Tulis test lebih dulu, pastikan merah.
4. Implementasi sampai semua test hijau (dilarang mengubah test agar lulus).
5. Commit dengan pesan yang jelas (`docs:`, `test:`, `feat:`, `ci:`).
6. Buka Pull Request ke `main` dengan deskripsi memuat `Closes #<nomor>`.
7. Tunggu CI hijau, lalu merge.