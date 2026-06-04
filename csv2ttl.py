"""
csv_to_ttl.py
Mengubah dataset kosakata Korea (kkotkata-dataset.csv) ke format TTL (Turtle/RDF).

Penggunaan:
    python csv_to_ttl.py
    python csv_to_ttl.py --input data.csv --output output.ttl

Struktur ontologi:
    - kkot:Word           → tiap entri kosakata
    - kkot:hasSynonym     → relasi ke kata sinonim
    - kkot:hasAntonym     → relasi ke kata antonim
    - kkot:hasExample     → relasi ke contoh kalimat
"""

import pandas as pd
import argparse
import re
import sys
from pathlib import Path


# ─── Namespace & Prefix ───────────────────────────────────────────────────────

PREFIXES = """\
@prefix kkot:    <http://kkotkata.org/ontology#> .
@prefix kkotw:   <http://kkotkata.org/word/> .
@prefix kkote:   <http://kkotkata.org/example/> .
@prefix rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs:    <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd:     <http://www.w3.org/2001/XMLSchema#> .
@prefix skos:    <http://www.w3.org/2004/02/skos/core#> .
@prefix owl:     <http://www.w3.org/2002/07/owl#> .

"""

ONTOLOGY_HEADER = """\
# ──────────────────────────────────────────────────────────────────
#  KKotKata Vocabulary Dataset — Turtle/RDF Export
#  Source  : kkotkata-dataset.csv
#  Vocab   : 100 kata Korea beserta terjemahan, sinonim, antonim,
#             romanisasi, dan contoh kalimat
# ──────────────────────────────────────────────────────────────────

"""

CLASS_DEFINITIONS = """\
# ── Class & Property Definitions ──────────────────────────────────

kkot:Word a owl:Class ;
    rdfs:label "Korean Vocabulary Word" .

kkot:Example a owl:Class ;
    rdfs:label "Example Sentence" .

kkot:id a owl:DatatypeProperty ;
    rdfs:domain kkot:Word ;
    rdfs:range  xsd:integer ;
    rdfs:label  "numeric ID" .

kkot:korean a owl:DatatypeProperty ;
    rdfs:domain kkot:Word ;
    rdfs:range  xsd:string ;
    rdfs:label  "Korean word (hangul)" .

kkot:romanization a owl:DatatypeProperty ;
    rdfs:domain kkot:Word ;
    rdfs:range  xsd:string ;
    rdfs:label  "Romanization (RR)" .

kkot:bahasaIndonesia a owl:DatatypeProperty ;
    rdfs:domain kkot:Word ;
    rdfs:range  xsd:string ;
    rdfs:label  "Bahasa Indonesia translation" .

kkot:english a owl:DatatypeProperty ;
    rdfs:domain kkot:Word ;
    rdfs:range  xsd:string ;
    rdfs:label  "English translation" .

kkot:type a owl:DatatypeProperty ;
    rdfs:domain kkot:Word ;
    rdfs:range  xsd:string ;
    rdfs:label  "part of speech / word type" .

kkot:category a owl:DatatypeProperty ;
    rdfs:domain kkot:Word ;
    rdfs:range  xsd:string ;
    rdfs:label  "thematic category" .

kkot:hasSynonym a owl:ObjectProperty ;
    rdfs:domain kkot:Word ;
    rdfs:range  kkot:Word ;
    rdfs:label  "has synonym" ;
    owl:inverseOf kkot:isSynonymOf .

kkot:hasAntonym a owl:ObjectProperty ;
    rdfs:domain kkot:Word ;
    rdfs:range  kkot:Word ;
    rdfs:label  "has antonym" ;
    owl:inverseOf kkot:isAntonymOf .

kkot:hasExample a owl:ObjectProperty ;
    rdfs:domain kkot:Word ;
    rdfs:range  kkot:Example ;
    rdfs:label  "has example sentence" .

kkot:sentenceKorean a owl:DatatypeProperty ;
    rdfs:domain kkot:Example ;
    rdfs:range  xsd:string ;
    rdfs:label  "example sentence in Korean" .

kkot:sentenceRomanization a owl:DatatypeProperty ;
    rdfs:domain kkot:Example ;
    rdfs:range  xsd:string ;
    rdfs:label  "romanization of example sentence" .

kkot:sentenceIndonesia a owl:DatatypeProperty ;
    rdfs:domain kkot:Example ;
    rdfs:range  xsd:string ;
    rdfs:label  "Indonesian translation of example sentence" .

# ── Data ──────────────────────────────────────────────────────────

"""


# ─── Helpers ──────────────────────────────────────────────────────────────────

def slugify(text: str) -> str:
    """Ubah teks jadi slug aman untuk URI (tanpa karakter khusus)."""
    text = str(text).strip()
    # Hapus karakter non-ASCII, ganti spasi/tanda baca dengan underscore
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    text = re.sub(r"[\s/]+", "_", text)
    text = text.strip("_")
    return text or "unknown"


def ttl_literal(value, lang: str = None) -> str:
    """Bungkus nilai jadi Turtle string literal yang aman."""
    if pd.isna(value):
        return None
    s = str(value).replace("\\", "\\\\").replace('"', '\\"')
    if lang:
        return f'"{s}"@{lang}'
    return f'"{s}"'


def make_word_uri(word_id: int, korean: str) -> str:
    """Buat URI unik untuk tiap entri kata."""
    slug = slugify(korean)
    return f"kkotw:word_{word_id}_{slug}"


def make_example_uri(word_id: int) -> str:
    return f"kkote:example_{word_id}"


def find_word_uri_by_korean(df: pd.DataFrame, korean: str) -> str | None:
    """Cari URI kata berdasarkan teks hangul-nya."""
    match = df[df["Korean (한국어)"] == korean]
    if not match.empty:
        row = match.iloc[0]
        return make_word_uri(int(row["ID"]), row["Korean (한국어)"])
    return None


# ─── Core Converter ───────────────────────────────────────────────────────────

def df_to_ttl(df: pd.DataFrame) -> str:
    lines = [ONTOLOGY_HEADER, PREFIXES, CLASS_DEFINITIONS]

    # Pass 1: tulis semua triple kkot:Word
    for _, row in df.iterrows():
        word_id   = int(row["ID"])
        korean    = str(row["Korean (한국어)"]).strip()
        word_uri  = make_word_uri(word_id, korean)
        ex_uri    = make_example_uri(word_id)

        triples = [f"{word_uri}"]
        triples.append(f"    a kkot:Word")
        triples.append(f"    ; kkot:id {word_id}")

        # Literal dasar
        for prop, col, lang in [
            ("kkot:korean",          "Korean (한국어)",   "ko"),
            ("kkot:romanization",    "Romanization",     None),
            ("kkot:bahasaIndonesia", "Bahasa Indonesia", "id"),
            ("kkot:english",         "English",          "en"),
            ("kkot:type",            "Type",             None),
            ("kkot:category",        "Category",         None),
        ]:
            val = ttl_literal(row.get(col), lang)
            if val:
                triples.append(f"    ; {prop} {val}")

        # Sinonim — referensi ke word URI jika ada di dataset,
        # fallback ke blank node literal kalau tidak ditemukan
        syn_kr = row.get("Sinonim (KR)")
        if not pd.isna(syn_kr) and str(syn_kr).strip():
            syn_uri = find_word_uri_by_korean(df, str(syn_kr).strip())
            if syn_uri:
                triples.append(f"    ; kkot:hasSynonym {syn_uri}")
            else:
                # Inline anonymous node dengan keterangan lengkap
                syn_ko_lit  = ttl_literal(syn_kr, "ko")
                syn_rom_lit = ttl_literal(row.get("Sinonim Romanization"))
                syn_id_lit  = ttl_literal(row.get("Sinonim (ID)"), "id")
                syn_en_lit  = ttl_literal(row.get("Sinonim (EN)"), "en")
                parts = ["a kkot:Word"]
                if syn_ko_lit:  parts.append(f"kkot:korean {syn_ko_lit}")
                if syn_rom_lit: parts.append(f"kkot:romanization {syn_rom_lit}")
                if syn_id_lit:  parts.append(f"kkot:bahasaIndonesia {syn_id_lit}")
                if syn_en_lit:  parts.append(f"kkot:english {syn_en_lit}")
                inline = " ; ".join(parts)
                triples.append(f"    ; kkot:hasSynonym [ {inline} ]")

        # Antonim — sama seperti sinonim
        ant_kr = row.get("Antonim (KR)")
        if not pd.isna(ant_kr) and str(ant_kr).strip() and str(ant_kr) != "nan":
            ant_uri = find_word_uri_by_korean(df, str(ant_kr).strip())
            if ant_uri:
                triples.append(f"    ; kkot:hasAntonym {ant_uri}")
            else:
                ant_ko_lit  = ttl_literal(ant_kr, "ko")
                ant_rom_lit = ttl_literal(row.get("Antonim Romanization"))
                ant_id_lit  = ttl_literal(row.get("Antonim (ID)"), "id")
                ant_en_lit  = ttl_literal(row.get("Antonim (EN)"), "en")
                parts = ["a kkot:Word"]
                if ant_ko_lit:  parts.append(f"kkot:korean {ant_ko_lit}")
                if ant_rom_lit: parts.append(f"kkot:romanization {ant_rom_lit}")
                if ant_id_lit:  parts.append(f"kkot:bahasaIndonesia {ant_id_lit}")
                if ant_en_lit:  parts.append(f"kkot:english {ant_en_lit}")
                inline = " ; ".join(parts)
                triples.append(f"    ; kkot:hasAntonym [ {inline} ]")

        # Contoh kalimat — linked ke node terpisah
        ex_kr  = row.get("Contoh Kalimat (KR)")
        ex_rom = row.get("Contoh Romanization")
        ex_id  = row.get("Contoh (ID)")
        if not pd.isna(ex_kr) and str(ex_kr).strip():
            triples.append(f"    ; kkot:hasExample {ex_uri}")

        triples.append("    .")
        lines.append("\n".join(triples))
        lines.append("")

        # Node contoh kalimat terpisah
        if not pd.isna(ex_kr) and str(ex_kr).strip():
            ex_triples = [f"{ex_uri}"]
            ex_triples.append("    a kkot:Example")
            ex_kr_lit  = ttl_literal(ex_kr, "ko")
            ex_rom_lit = ttl_literal(ex_rom)
            ex_id_lit  = ttl_literal(ex_id, "id")
            if ex_kr_lit:  ex_triples.append(f"    ; kkot:sentenceKorean {ex_kr_lit}")
            if ex_rom_lit: ex_triples.append(f"    ; kkot:sentenceRomanization {ex_rom_lit}")
            if ex_id_lit:  ex_triples.append(f"    ; kkot:sentenceIndonesia {ex_id_lit}")
            ex_triples.append("    .")
            lines.append("\n".join(ex_triples))
            lines.append("")

    return "\n".join(lines)


# ─── CLI ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Konversi kkotkata CSV ke format Turtle (TTL/RDF)"
    )
    parser.add_argument(
        "--input", "-i",
        default="kkotkata-dataset.csv",
        help="Path ke file CSV input (default: kkotkata-dataset.csv)"
    )
    parser.add_argument(
        "--output", "-o",
        default="kkotkata.ttl",
        help="Path ke file TTL output (default: kkotkata.ttl)"
    )
    args = parser.parse_args()

    input_path  = Path(args.input)
    output_path = Path(args.output)

    if not input_path.exists():
        print(f"[ERROR] File tidak ditemukan: {input_path}", file=sys.stderr)
        sys.exit(1)

    print(f"[INFO] Membaca CSV: {input_path}")
    df = pd.read_csv(input_path, dtype=str)
    df["ID"] = df["ID"].astype(int)
    print(f"[INFO] Total entri: {len(df)} kata")

    print("[INFO] Mengkonversi ke Turtle (TTL)...")
    ttl_content = df_to_ttl(df)

    output_path.write_text(ttl_content, encoding="utf-8")
    print(f"[OK]   File TTL disimpan ke: {output_path}")

    # Hitung triple (perkiraan)
    triple_count = ttl_content.count(" .")
    print(f"[INFO] Estimasi jumlah triple: ~{triple_count}")


if __name__ == "__main__":
    main()