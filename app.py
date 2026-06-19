from flask import Flask, render_template, request, jsonify
import requests
import json

app = Flask(__name__)

# =============================================
# KONFIGURASI FUSEKI SERVER
# Ganti URL ini sesuai dengan server Fuseki Anda
# =============================================
FUSEKI_ENDPOINT = "http://localhost:3030/kkotkata/sparql"


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
    safe_keyword = keyword.replace('"', '\\"').replace('\\', '\\\\')
    return f"""
PREFIX kkot: <http://kkotkata.org/ontology#>

SELECT DISTINCT ?korean ?indonesian ?romanization ?category ?synonym ?antonym ?exKorean
WHERE {{
    ?word a kkot:Word ;
          kkot:korean ?korean ;
          kkot:bahasaIndonesia ?indonesian .
    
    OPTIONAL {{ ?word kkot:romanization ?romanization }}
    OPTIONAL {{ ?word kkot:category ?category }}
    
    # Ambil sinonim (Blank Node)
    OPTIONAL {{ ?word kkot:hasSynonym ?synNode . ?synNode kkot:korean ?synonym }}
    
    # Ambil antonim (URI)
    OPTIONAL {{ ?word kkot:hasAntonym ?antNode . ?antNode kkot:korean ?antonym }}
    
    # Ambil contoh kalimat
    OPTIONAL {{ ?word kkot:hasExample ?exNode . ?exNode kkot:sentenceKorean ?exKorean }}

    FILTER (
        CONTAINS(LCASE(STR(?korean)), LCASE("{safe_keyword}")) ||
        CONTAINS(LCASE(STR(?indonesian)), LCASE("{safe_keyword}"))
    )
}}
"""


def search_word(keyword: str) -> dict:
    query = build_sparql_query(keyword)
    raw = run_sparql_query(query)
    bindings = raw.get("results", {}).get("bindings", [])

    if not bindings:
        return None

    # Helper untuk mengambil data unik
    def get_unique(var):
        return list({b[var]["value"] for b in bindings if var in b})

    # Ambil baris pertama untuk data utama
    first_b = bindings[0]
    
    return {
        "korean":       first_b.get("korean", {}).get("value"),
        "indonesian":   first_b.get("indonesian", {}).get("value"),
        "romanization": first_b.get("romanization", {}).get("value"),
        "category":     first_b.get("category", {}).get("value"),
        "synonyms":     get_unique("synonym"),
        "antonyms":     get_unique("antonym"),
        "examples":     get_unique("exKorean"),
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
    app.run(debug=True, host="0.0.0.0", port=5001)
