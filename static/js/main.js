/* =============================================
   main.js — Kamus Indonesia–Korea
   ============================================= */

const $ = id => document.getElementById(id);

// ─── DOM refs ───
const searchInput  = $('searchInput');
const searchBtn    = $('searchBtn');
const resultSection = $('resultSection');
const errorBox     = $('errorBox');
const loading      = $('loading');
const connStatus   = $('connStatus');

// ─── Init ───
document.addEventListener('DOMContentLoaded', () => {
    searchInput.focus();
    checkFusekiHealth();
});

// Enter key to search
searchInput.addEventListener('keydown', e => {
    if (e.key === 'Enter') doSearch();
});

// ─── Search ───
async function doSearch() {
    const keyword = searchInput.value.trim();
    if (!keyword) {
        searchInput.focus();
        shakeInput();
        return;
    }
    showLoading();
    try {
        const res = await fetch(`/search?q=${encodeURIComponent(keyword)}`);
        const json = await res.json();

        if (!res.ok || json.error) {
            showError(json.error || 'Terjadi kesalahan tidak dikenal.');
        } else {
            showResult(json.data);
        }
    } catch (err) {
        showError('Tidak dapat terhubung ke server. Pastikan Flask berjalan.');
    }
}

// ─── Render Result ───
function showResult(data) {
    hide(loading);
    hide(errorBox);

    // Main word card
    $('resKorean').textContent   = data.korean       || '—';
    $('resRoman').textContent    = data.romanization  ? `[${data.romanization}]` : '';
    $('resMeaning').textContent  = data.meaning       || (data.indonesian ? data.indonesian : '—');

    // Category
    $('resCategory').textContent = data.category || '—';

    // Synonyms
    renderTags('resSynonym', data.synonyms);
    // Antonyms
    renderTags('resAntonym', data.antonyms);

    // Examples
    const exList = $('resExamples');
    exList.innerHTML = '';
    if (data.examples && data.examples.length > 0) {
        data.examples.forEach(ex => {
            const div = document.createElement('div');
            div.className = 'example-item';
            div.textContent = ex;
            exList.appendChild(div);
        });
        show($('exampleSection'));
    } else {
        const div = document.createElement('div');
        div.className = 'example-item';
        div.style.color = '#8a7f72';
        div.textContent = 'Tidak ada contoh kalimat.';
        exList.appendChild(div);
    }

    show(resultSection);
    resultSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function renderTags(elId, arr) {
    const el = $(elId);
    el.innerHTML = '';
    if (arr && arr.length > 0) {
        el.classList.add('tag-list');
        arr.forEach(val => {
            const span = document.createElement('span');
            span.className = 'tag';
            span.textContent = val;
            el.appendChild(span);
        });
    } else {
        el.classList.remove('tag-list');
        el.textContent = '—';
    }
}

// ─── Error ───
function showError(msg) {
    hide(loading);
    hide(resultSection);
    $('errorMsg').textContent = msg;
    show(errorBox);
}

// ─── Loading ───
function showLoading() {
    hide(resultSection);
    hide(errorBox);
    show(loading);
}

// ─── Health check ───
async function checkFusekiHealth() {
    try {
        const res = await fetch('/health');
        if (res.ok) {
            connStatus.className = 'conn-dot conn-ok';
            connStatus.title = 'Terhubung ke Fuseki ✓';
        } else {
            connStatus.className = 'conn-dot conn-error';
            connStatus.title = 'Fuseki tidak merespons';
        }
    } catch {
        connStatus.className = 'conn-dot conn-error';
        connStatus.title = 'Tidak dapat cek Fuseki';
    }
}

// Cek ulang saat klik badge
$('fusekiBadge').addEventListener('click', () => {
    connStatus.className = 'conn-dot conn-unknown';
    checkFusekiHealth();
});

// ─── Helpers ───
function show(el) { el.style.display = ''; }
function hide(el) { el.style.display = 'none'; }

function shakeInput() {
    searchInput.style.animation = 'none';
    searchInput.offsetHeight; // reflow
    searchInput.style.animation = 'shake 0.4s ease';
    searchInput.addEventListener('animationend', () => {
        searchInput.style.animation = '';
    }, { once: true });
}

// Inject shake keyframe dynamically
const style = document.createElement('style');
style.textContent = `
@keyframes shake {
    0%,100% { transform: translateX(0); }
    20%      { transform: translateX(-8px); }
    40%      { transform: translateX(8px); }
    60%      { transform: translateX(-5px); }
    80%      { transform: translateX(5px); }
}`;
document.head.appendChild(style);
