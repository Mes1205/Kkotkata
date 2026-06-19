# 🌸 KkotKata

## Sistem Pencarian Kosakata Indonesia–Korea Berbasis Semantic Web dan SPARQL

KkotKata adalah aplikasi kamus bilingual Bahasa Indonesia–Bahasa Korea berbasis **Semantic Web** yang memungkinkan pengguna mencari kosakata beserta informasi semantiknya. Sistem ini menggunakan **RDF (Resource Description Framework)**, **OWL (Web Ontology Language)**, dan **SPARQL Query Language** untuk menyimpan, menghubungkan, serta mengambil data kosakata secara terstruktur.

Nama **KkotKata** berasal dari gabungan kata **Kkot (꽃)** yang berarti *bunga* dalam Bahasa Korea dan **Kata** dalam Bahasa Indonesia. Filosofi nama ini menggambarkan proses berkembangnya pengetahuan bahasa seperti bunga yang terus tumbuh.

Berbeda dengan kamus biasa yang hanya menyimpan pasangan kata dan terjemahan, KkotKata menyimpan hubungan semantik seperti:

* Kategori kosakata
* Sinonim
* Antonim
* Romanisasi
* Pelafalan
* Contoh penggunaan dalam kalimat

---

# 📌 Fitur Utama

Fitur yang tersedia pada aplikasi KkotKata:

*  Pencarian kosakata Indonesia → Korea
*  Pencarian kosakata Korea → Indonesia
*  Menampilkan tulisan Hangul Korea
*  Menampilkan romanisasi
*  Menampilkan informasi pelafalan
*  Menampilkan kategori kosakata
*  Menampilkan contoh kalimat
*  Relasi semantik sinonim dan antonim
*  Penyimpanan data menggunakan RDF Turtle
*  Query data menggunakan SPARQL
*  Integrasi dengan Apache Jena Fuseki

---

# 🛠️ Teknologi yang Digunakan

| Komponen       | Teknologi             |
| -------------- | --------------------- |
| Backend        | Flask (Python)        |
| Frontend       | HTML, CSS, JavaScript |
| Semantic Web   | RDF, OWL              |
| RDF Format     | Turtle (.ttl)         |
| Query Language | SPARQL                |
| Triplestore    | Apache Jena Fuseki    |
| Dataset Awal   | CSV                   |
| HTTP Request   | Requests Library      |

---

# 📂 Struktur Folder Proyek

```text
Kkotkata-main/
│
├── csv2ttl.py
├── kkotkata-dataset.csv
│
├── kamus-app/
│   │
│   ├── app.py
│   ├── requirements.txt
│   ├── kkotkata.ttl
│   ├── contoh_data.ttl
│   │
│   ├── templates/
│   │   └── index.html
│   │
│   └── static/
│       │
│       ├── css/
│       │   └── style.css
│       │
│       └── js/
│           └── main.js
│
└── README.md
```

---

# 🏗️ Arsitektur Sistem

Alur kerja aplikasi:

```text
User
 |
 ▼
Frontend
(HTML, CSS, JavaScript)
 |
 ▼
Flask Backend
(Python)
 |
 ▼
SPARQL Query
 |
 ▼
Apache Jena Fuseki
 |
 ▼
RDF Dataset
(Turtle File)
```

Penjelasan:

1. User memasukkan kata melalui halaman website.
2. Frontend mengirim request pencarian ke Flask.
3. Flask membuat query SPARQL berdasarkan input.
4. Query dikirim menuju Apache Jena Fuseki.
5. Fuseki mencari data pada RDF Graph.
6. Data hasil pencarian dikembalikan dan ditampilkan kepada user.

---

# ⚙️ Panduan Instalasi

## 1. Clone Repository

Clone repository:

```bash
git clone <repository-url>
```

Masuk folder:

```bash
cd Kkotkata-main
```

---

# 2. Install Apache Jena Fuseki

Download Apache Jena Fuseki:

```
https://jena.apache.org/download/
```

Ekstrak file Fuseki.

Jalankan server:

Windows:

```bash
fuseki-server.bat
```

Linux/Mac:

```bash
./fuseki-server
```

Apabila berhasil, buka:

```text
http://localhost:3030
```

Akan muncul halaman dashboard Fuseki.

---

# 3. Membuat Dataset RDF di Fuseki

Pada dashboard Fuseki:

Klik:

```text
Manage Dataset
        ↓
Add New Dataset
```

Isi:

```text
Dataset Name : kkotkata
Dataset Type : Persistent (TDB2)
```

Klik:

```text
Create Dataset
```

---

## Upload Dataset RDF

Masuk dataset:

```text
kkotkata
```

Pilih:

```text
Upload Data
```

Upload file:

```text
kamus-app/kkotkata.ttl
```

Jika berhasil endpoint SPARQL tersedia:

```text
http://localhost:3030/kkotkata/sparql
```

---

# 4. Install Python Dependency

Masuk folder aplikasi:

```bash
cd kamus-app
```

Install library:

```bash
pip install -r requirements.txt
```

Dependency utama:

* Flask
* Requests

---

# 5. Konfigurasi Endpoint Fuseki

Buka:

```text
app.py
```

Pastikan endpoint:

```python
FUSEKI_ENDPOINT =
"http://localhost:3030/kkotkata/sparql"
```

Sesuai dengan alamat Fuseki.

---

# 6. Jalankan Aplikasi

Pastikan Fuseki sudah aktif.

Jalankan Flask:

```bash
python app.py
```

Output:

```text
Running on http://127.0.0.1:5000
```

Buka browser:

```text
http://localhost:5000
```

Aplikasi siap digunakan.

---

# 📖 Panduan Pengguna

## 1. Membuka Website

Buka aplikasi melalui browser:

```text
localhost:5000
```

Halaman utama KkotKata akan muncul.

---

## 2. Melakukan Pencarian Kata

Pada kolom pencarian:

Masukkan kata Bahasa Indonesia:

Contoh:

```text
apel
```

atau Bahasa Korea:

```text
사과
```

Klik tombol:

```text
Cari
```

---

## 3. Melihat Detail Kosakata

Sistem akan menampilkan:

| Informasi      | Contoh          |
| -------------- | --------------- |
| Kata Indonesia | Apel            |
| Hangul         | 사과              |
| Romanisasi     | Sagwa           |
| Pelafalan      | sa-gwa          |
| Kategori       | Food & Drink    |
| Sinonim        | Buah            |
| Antonim        | -               |
| Contoh Kalimat | Saya makan apel |

---

# 🔎 Contoh Hasil Penggunaan

## Contoh 1

Input:

```text
apel
```

Output:

```text
Kata Indonesia:
Apel

Bahasa Korea:
사과

Romanisasi:
Sagwa

Pelafalan:
sa-gwa

Kategori:
Food & Drink

Contoh:
Saya membeli apel merah.
```

---

## Contoh 2

Input:

```text
안녕하세요
```

Output:

```text
Kata Indonesia:
Halo

Bahasa Korea:
안녕하세요

Romanisasi:
Annyeonghaseyo

Kategori:
Greeting

Contoh:
안녕하세요, 만나서 반갑습니다.
```

---

# 🔄 Konversi CSV menjadi RDF

Dataset awal berbentuk:

```text
kkotkata-dataset.csv
```

Konversi menggunakan:

```text
csv2ttl.py
```

Jalankan:

```bash
python csv2ttl.py
```

Akan menghasilkan:

```text
kkotkata.ttl
```

File RDF tersebut digunakan oleh Fuseki.

---

# 💻 Contoh Query SPARQL

Query mencari kata:

```sparql
PREFIX kkotkata:
<http://www.kkotkata.org/ontology#>

SELECT ?kata ?terjemahan ?romanisasi
WHERE {

?s kkotkata:kataDasar ?kata ;
   kkotkata:terjemahanKorea ?terjemahan ;
   kkotkata:romanisasi ?romanisasi .

FILTER(CONTAINS(
LCASE(?kata),
LCASE("apel")
))

}
```

Output:

| Kata | Korea | Romanisasi |
| ---- | ----- | ---------- |
| apel | 사과    | sagwa      |

---

# 📚 Dataset

Dataset KkotKata terdiri dari:

* 100 kosakata Korea–Indonesia
* Terjemahan Bahasa Korea
* Terjemahan Bahasa Indonesia
* Romanisasi
* Pelafalan
* Kategori
* Sinonim
* Antonim
* Contoh kalimat

---

# 🏷️ Kategori Dataset

Kategori kosakata:

* Food & Drink
* Emotion & Trait
* Daily Object
* Daily Activity
* Place & Direction
* Number & Time
* Greeting
* Family & People

---

# 🧪 Pengujian Sistem

Pengujian dilakukan pada:

| Pengujian                   | Status   |
| --------------------------- | -------- |
| Pencarian Indonesia → Korea | Berhasil |
| Pencarian Korea → Indonesia | Berhasil |
| Query SPARQL                | Berhasil |
| Koneksi Fuseki              | Berhasil |
| Data RDF terbaca            | Berhasil |
| Kata tidak ditemukan        | Berhasil |

---

# 👩‍💻 Pengembang

Kelompok Proyek Semantic Web

| Nama                     | NPM          |
| ------------------------ | ------------ |
| Senia Nur Hasanah        | 140810230021 |
| Martha Meslina Florencia | 140810230037 |
| Alissa Indraputri        | 140810230064 |

Program Studi S-1 Teknik Informatika
Fakultas Matematika dan Ilmu Pengetahuan Alam
Universitas Padjadjaran

2026

---

# 📄 Lisensi

Proyek ini dibuat untuk kebutuhan akademik pada mata kuliah **Semantic Web** Program Studi Teknik Informatika Universitas Padjadjaran.
