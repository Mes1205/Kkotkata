# 사전 · Kamus Indonesia–Korea

Web pencarian kamus Indonesia–Korea menggunakan **Flask** + **Apache Jena Fuseki** (SPARQL).

---

## Struktur Proyek

```
kamus-app/
├── app.py               ← Flask backend + SPARQL query
├── requirements.txt
├── contoh_data.ttl      ← Contoh data Turtle untuk Fuseki
├── templates/
│   └── index.html
└── static/
    ├── css/style.css
    └── js/main.js
```

---

## Cara Setup

### 1. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 2. Setup Apache Jena Fuseki

1. Unduh Fuseki dari https://jena.apache.org/download/
2. Jalankan server:
   ```bash
   ./fuseki-server --update --mem /kamus
   ```
3. Buka `http://localhost:3030`
4. Buat dataset bernama `kamus` (jika belum ada)
5. Upload file `contoh_data.ttl` ke dataset tersebut

### 3. Sesuaikan konfigurasi (jika perlu)

Edit bagian ini di `app.py`:
```python
FUSEKI_ENDPOINT = "http://localhost:3030/kamus/sparql"
```
Ganti `kamus` dengan nama dataset Anda.

### 4. Jalankan Flask
```bash
python app.py
```
Buka browser: `http://localhost:5000`

---

## Struktur Ontologi (SPARQL)

Aplikasi menggunakan PREFIX dan properti berikut:

```turtle
PREFIX ex: <http://example.org/kamus#>

ex:Word          # Kelas kata
ex:korean        # Teks Hangul
ex:indonesian    # Teks Indonesia
ex:romanization  # Romanisasi (misal: sarang)
ex:meaning       # Arti/definisi
ex:category      # Kategori (noun, verb, emotion, dll.)
ex:synonym       # Sinonim (bisa lebih dari satu)
ex:antonym       # Antonim (bisa lebih dari satu)
ex:example       # Contoh kalimat (bisa lebih dari satu)
```

Jika ontologi Anda berbeda, sesuaikan fungsi `build_sparql_query()` di `app.py`.

---

## Fitur

- ✅ Cari berdasarkan kata Indonesia **atau** Hangul
- ✅ Tampilkan: arti, romanisasi, kategori, sinonim, antonim, contoh kalimat
- ✅ Indikator status koneksi Fuseki (pojok bawah)
- ✅ Endpoint `/health` untuk cek koneksi
