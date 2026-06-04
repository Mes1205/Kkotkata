from flask import Flask, render_template, request, jsonify
import requests
import json

app = Flask(__name__)

# =============================================
# KONFIGURASI FUSEKI SERVER
# Ganti URL ini sesuai dengan server Fuseki Anda
# =============================================
FUSEKI_ENDPOINT = "http://localhost:3030/kamus/sparql"
# Jika dataset Anda bernama berbeda, ganti "kamus" di atas


def run_sparql_query(query: str) -> dict:
    """Menjalankan SPARQL query ke Apache Jena Fuseki."""
    headers = {
        "Accept": "application/sparql-results+json",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    try:
        response = requests.post(
            FUSEKI_ENDPOINT,
            data={"query": query},
            headers=headers,
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        raise Exception("Tidak dapat terhubung ke Fuseki Server. Pastikan server berjalan di " + FUSEKI_ENDPOINT)
    except requests.exceptions.Timeout:
        raise Exception("Koneksi ke Fuseki Server timeout.")
    except requests.exceptions.HTTPError as e:
        raise Exception(f"Error dari Fuseki Server: {e}")


def extract_values(results: dict, var: str) -> list:
    """Mengambil semua nilai dari hasil SPARQL untuk satu variabel."""
    values = []
    for binding in results.get("results", {}).get("bindings", []):
        if var in binding:
            values.append(binding[var]["value"])
    return values


def build_sparql_query(keyword: str) -> str:
    """
    Membangun SPARQL query untuk mencari kata berdasarkan kata Indonesia atau Korea.
    
    Asumsi prefix/ontologi:
      - ex:   <http://example.org/kamus#>
      - kata memiliki properti:
          ex:korean       -> teks Korea (hangul)
          ex:indonesian   -> teks Indonesia
          ex:romanization -> romanisasi
          ex:meaning      -> arti/definisi
          ex:category     -> kategori kata
          ex:synonym      -> sinonim (Korean)
          ex:antonym      -> antonim (Korean)
          ex:example      -> contoh kalimat
    
    Sesuaikan PREFIX dan properti ini dengan ontologi Fuseki Anda!
    """
    # Escape untuk mencegah SPARQL injection sederhana
    safe_keyword = keyword.replace('"', '\\"').replace('\\', '\\\\')

    query = f"""
PREFIX ex: <http://example.org/kamus#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT
    ?korean
    ?indonesian
    ?romanization
    ?meaning
    ?category
    ?synonym
    ?antonym
    ?example
WHERE {{
    ?word a ex:Word .
    ?word ex:korean ?korean .
    OPTIONAL {{ ?word ex:indonesian   ?indonesian   }}
    OPTIONAL {{ ?word ex:romanization ?romanization }}
    OPTIONAL {{ ?word ex:meaning      ?meaning      }}
    OPTIONAL {{ ?word ex:category     ?category     }}
    OPTIONAL {{ ?word ex:synonym      ?synonym      }}
    OPTIONAL {{ ?word ex:antonym      ?antonym      }}
    OPTIONAL {{ ?word ex:example      ?example      }}

    FILTER (
        LCASE(STR(?korean))    = LCASE("{safe_keyword}") ||
        LCASE(STR(?indonesian)) = LCASE("{safe_keyword}")
    )
}}
"""
    return query


def search_word(keyword: str) -> dict:
    """Mencari kata dan mengembalikan hasil terstruktur."""
    query = build_sparql_query(keyword)
    raw = run_sparql_query(query)
    bindings = raw.get("results", {}).get("bindings", [])

    if not bindings:
        return None

    # Ambil nilai pertama untuk field singular, list untuk field plural
    def first(var):
        for b in bindings:
            if var in b:
                return b[var]["value"]
        return None

    def all_unique(var):
        seen = set()
        result = []
        for b in bindings:
            if var in b:
                v = b[var]["value"]
                if v not in seen:
                    seen.add(v)
                    result.append(v)
        return result

    return {
        "korean":       first("korean"),
        "indonesian":   first("indonesian"),
        "romanization": first("romanization"),
        "meaning":      first("meaning"),
        "category":     first("category"),
        "synonyms":     all_unique("synonym"),
        "antonyms":     all_unique("antonym"),
        "examples":     all_unique("example"),
    }


# =============================================
# ROUTES
# =============================================

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/search", methods=["GET"])
def search():
    keyword = request.args.get("q", "").strip()
    if not keyword:
        return jsonify({"error": "Kata kunci tidak boleh kosong."}), 400

    try:
        result = search_word(keyword)
        if result is None:
            return jsonify({"error": f"Kata '{keyword}' tidak ditemukan dalam kamus."}), 404
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/health")
def health():
    """Cek koneksi ke Fuseki."""
    try:
        test_query = "ASK { ?s ?p ?o }"
        run_sparql_query(test_query)
        return jsonify({"status": "ok", "fuseki": FUSEKI_ENDPOINT})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 503


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
