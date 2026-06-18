# KkotKata

Sistem Pencarian Kosakata Indonesia–Korea Berbasis Semantic Web dan SPARQL

## Deskripsi Proyek

KkotKata merupakan aplikasi kamus bilingual Bahasa Indonesia dan Bahasa Korea yang dibangun menggunakan teknologi Semantic Web. Sistem memanfaatkan RDF (Resource Description Framework), OWL (Web Ontology Language), dan SPARQL untuk merepresentasikan serta mengakses data kosakata secara terstruktur.

Nama **KkotKata** berasal dari gabungan kata *Kkot* (꽃) yang berarti bunga dalam Bahasa Korea dan *Kata* dalam Bahasa Indonesia. Proyek ini bertujuan untuk menyediakan media pembelajaran kosakata Indonesia–Korea yang tidak hanya menyimpan data terjemahan, tetapi juga hubungan semantik seperti kategori, sinonim, antonim, dan contoh kalimat.

---

## Fitur Utama

* Pencarian kosakata Indonesia → Korea
* Pencarian kosakata Korea → Indonesia
* Menampilkan terjemahan Hangul
* Menampilkan romanisasi
* Menampilkan pelafalan
* Menampilkan kategori kosakata
* Menampilkan contoh kalimat
* Query data menggunakan SPARQL
* Penyimpanan data berbasis RDF
* Integrasi Apache Jena Fuseki

---

## Teknologi yang Digunakan

| Komponen       | Teknologi             |
| -------------- | --------------------- |
| Backend        | Flask (Python)        |
| Frontend       | HTML, CSS, JavaScript |
| Triplestore    | Apache Jena Fuseki    |
| Semantic Web   | RDF, OWL, Turtle      |
| Query Language | SPARQL                |
| Dataset        | CSV                   |
| HTTP Client    | Requests              |

---

## Struktur Proyek

```text
Kkotkata-main/
│
├── csv2ttl.py
├── kkotkata-dataset.csv
│
├── kamus-app/
│   ├── app.py
│   ├── requirements.txt
│   ├── kkotkata.ttl
│   ├── contoh_data.ttl
│   │
│   ├── templates/
│   │   └── index.html
│   │
│   └── static/
│       ├── css/
│       │   └── style.css
│       │
│       └── js/
│           └── main.js
│
└── README.md
```

---

## Arsitektur Sistem

```text
Pengguna
    │
    ▼
Frontend (HTML/CSS/JS)
    │
    ▼
Flask Backend
    │
    ▼
SPARQL Query
    │
    ▼
Apache Jena Fuseki
    │
    ▼
Dataset RDF (.ttl)
```

---

## Instalasi dan Menjalankan Proyek

### 1. Clone Repository

```bash
git clone <repository-url>
cd Kkotkata-main
```

---

### 2. Install Apache Jena Fuseki

Download Apache Jena Fuseki:

https://jena.apache.org/download/

Ekstrak file hasil download.

Jalankan Fuseki:

```bash
fuseki-server
```

Buka browser:

```text
http://localhost:3030
```

---

### 3. Membuat Dataset Fuseki

Masuk ke dashboard Fuseki.

Buat dataset baru:

```text
Dataset Name: kkotkata
Dataset Type: Persistent (TDB2)
```

Upload file:

```text
kkotkata.ttl
```

Pastikan endpoint tersedia pada:

```text
http://localhost:3030/kkotkata/sparql
```

---

### 4. Install Dependency Python

Masuk ke folder aplikasi:

```bash
cd kamus-app
```

Install dependency:

```bash
pip install -r requirements.txt
```

---

### 5. Jalankan Aplikasi

```bash
python app.py
```

Server Flask akan berjalan pada:

```text
http://127.0.0.1:5000
```

atau

```text
http://localhost:5000
```

---

## Konfigurasi Endpoint Fuseki

Pada file:

```python
app.py
```

terdapat konfigurasi:

```python
FUSEKI_ENDPOINT = "http://localhost:3030/kkotkata/sparql"
```

Sesuaikan apabila menggunakan server atau port yang berbeda.

---

## Konversi Dataset CSV ke RDF

Proyek menyediakan script:

```text
csv2ttl.py
```

yang digunakan untuk mengubah dataset CSV menjadi RDF Turtle.

Menjalankan script:

```bash
python csv2ttl.py
```

Output:

```text
kkotkata.ttl
```

---

## Contoh Query SPARQL

```sparql
PREFIX kkotkata: <http://www.kkotkata.org/ontology#>

SELECT ?kata ?terjemahan ?romanisasi
WHERE {
    ?s kkotkata:kataDasar ?kata ;
       kkotkata:terjemahanKorea ?terjemahan ;
       kkotkata:romanisasi ?romanisasi .

    FILTER(CONTAINS(LCASE(?kata), LCASE("apel")))
}
```

---

## Dataset

Dataset terdiri dari:

* 100 kosakata Bahasa Korea
* Terjemahan Bahasa Indonesia
* Terjemahan Bahasa Inggris
* Romanisasi
* Pelafalan
* Kategori
* Sinonim
* Antonim
* Contoh kalimat

Kategori yang digunakan:

* Food & Drink
* Emotion & Trait
* Daily Object
* Daily Activity
* Place & Direction
* Number & Time
* Greeting
* Family & People

---

## Pengujian Sistem

Pengujian dilakukan terhadap fitur:

* Pencarian kata valid
* Pencarian kata tidak ditemukan
* Filter kategori
* Koneksi Fuseki
* Pencarian Korea → Indonesia

Seluruh skenario pengujian berhasil dijalankan dengan status lulus.

---

## Pengembang

Kelompok Proyek Semantic Web

* Senia Nur Hasanah (140810230021)
* Martha Meslina Florencia (140810230037)
* Alissa Indraputri (140810230064)

Program Studi S-1 Teknik Informatika

Fakultas Matematika dan Ilmu Pengetahuan Alam

Universitas Padjadjaran

2026

---

## Lisensi

Proyek ini dikembangkan untuk keperluan akademik pada mata kuliah Semantic Web, Program Studi Teknik Informatika Universitas Padjadjaran.
