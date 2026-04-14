const BATCH = 20;

let allEvents   = [];
let filtered    = [];
let cursor      = 0;
let loading     = false;
let finished    = false;
let rowCount    = 0;
let searchQuery = '';

function rocYear(dateStr) {
  return parseInt(dateStr.split('-')[0]) - 1911;
}
function fmtDate(dateStr) {
  const [y, m, d] = dateStr.split('-');
  return `${y}年${parseInt(m)}月${parseInt(d)}日`;
}
function fmtRoc(dateStr) {
  const [y, m, d] = dateStr.split('-');
  return `民國${parseInt(y) - 1911}年${parseInt(m)}月${parseInt(d)}日`;
}

function buildRow(ev, side, staggerIdx) {
  const row = document.createElement('div');
  row.className = `ev-row side-${side}`;

  const nodeDiv = document.createElement('div');
  nodeDiv.className = 'ev-node';
  const dot = document.createElement('div');
  dot.className = 'ev-dot';
  nodeDiv.appendChild(dot);

  const yearDiv = document.createElement('div');
  yearDiv.innerHTML = `
    <div class="ruler"></div>
    <div class="year-lbl">
      <span class="yr-w">${ev.date.split('-')[0]}</span>
      <span class="yr-r">民${rocYear(ev.date)}</span>
    </div>`;

  const cardWrap = document.createElement('div');
  const card = document.createElement('div');
  card.className = 'ev-card';
  card.style.setProperty('--stagger', `${staggerIdx * 80}ms`);
  const sourceHtml = ev.source_url
    ? `<div class="c-source"><a href="${ev.source_url}" target="_blank" rel="noopener noreferrer">📰 新聞來源</a></div>`
    : '';
  card.innerHTML = `
    <div class="c-date">${fmtDate(ev.date)}　${fmtRoc(ev.date)}</div>
    <div class="c-title">${ev.title}</div>
    <div class="c-desc">${ev.desc || ''}</div>
    <div class="c-tags">${(ev.tags || []).map(t => `<span class="c-tag">${t}</span>`).join('')}</div>
    ${sourceHtml}`;
  cardWrap.appendChild(card);

  if (side === 'left') {
    cardWrap.className = 'ev-left-card';
    yearDiv.className  = 'ev-year ev-left-year';
    row.appendChild(cardWrap);
    row.appendChild(nodeDiv);
    row.appendChild(yearDiv);
  } else {
    cardWrap.className = 'ev-right-card';
    yearDiv.className  = 'ev-year ev-right-year';
    row.appendChild(yearDiv);
    row.appendChild(nodeDiv);
    row.appendChild(cardWrap);
  }

  return row;
}

function loadBatch() {
  if (loading || finished) return;
  loading = true;
  showLoader(true);

  const batch = filtered.slice(cursor, cursor + BATCH);
  cursor += batch.length;

  setTimeout(() => {
    renderBatch(batch, cursor < filtered.length);
  }, 120);
}

function renderBatch(events, hasMore) {
  const container = document.getElementById('events-container');

  if (events.length === 0 && cursor === 0) {
    container.innerHTML = `<div class="no-results">找不到「${searchQuery}」相關事件</div>`;
    loading  = false;
    finished = true;
    showLoader(false);
    return;
  }

  events.forEach((ev, i) => {
    const side = rowCount % 2 === 0 ? 'right' : 'left';
    const row  = buildRow(ev, side, i);
    container.appendChild(row);
    rowCount++;
    cardObserver.observe(row.querySelector('.ev-card'));
  });

  loading  = false;
  finished = !hasMore;
  showLoader(false);

  if (finished) {
    document.getElementById('loader-area').innerHTML =
      '<div class="all-done">── 已顯示所有歷史事件 ──</div>';
  }
}

function showLoader(visible) {
  const el = document.getElementById('loader');
  if (el) el.style.display = visible ? 'flex' : 'none';
}

function applySearch(q) {
  if (!q) {
    filtered = allEvents;
  } else {
    const lower = q.toLowerCase();
    filtered = allEvents.filter(ev =>
      ev.title.toLowerCase().includes(lower) ||
      (ev.desc  || '').toLowerCase().includes(lower) ||
      (ev.tags  || []).some(t => t.toLowerCase().includes(lower)) ||
      ev.date.includes(lower) ||
      fmtDate(ev.date).includes(q) ||
      fmtRoc(ev.date).includes(q)
    );
  }
}

function doSearch() {
  const q = document.getElementById('search-input').value.trim();
  searchQuery = q;
  cursor   = 0;
  rowCount = 0;
  finished = false;
  loading  = false;

  applySearch(q);

  document.getElementById('events-container').innerHTML = '';
  document.getElementById('loader-area').innerHTML = `
    <div class="loader-inner" id="loader">
      <div class="spin-ring"></div>
      <div class="load-txt">載入歷史事件中…</div>
    </div>`;

  const badge = document.getElementById('search-badge');
  if (q) {
    badge.textContent = `搜尋：${q}　✕`;
    badge.style.display = 'block';
    badge.classList.add('visible');
    badge.onclick = clearSearch;
  } else {
    badge.classList.remove('visible');
    badge.style.display = 'none';
  }

  window.scrollTo({ top: 0, behavior: 'smooth' });
  refreshLayout();

  setTimeout(() => {
    io.unobserve(document.getElementById('loader-area'));
    loadBatch();
    io.observe(document.getElementById('loader-area'));
  }, 500);
}

function clearSearch() {
  document.getElementById('search-input').value = '';
  doSearch();
}

document.getElementById('search-input').addEventListener('keydown', e => {
  if (e.key === 'Enter') doSearch();
});

const sentinel = document.getElementById('loader-area');
const io = new IntersectionObserver(entries => {
  if (entries[0].isIntersecting) loadBatch();
}, { rootMargin: '300px 0px', threshold: 0 });

const cardObserver = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    const card = entry.target;
    if (entry.isIntersecting) {
      card.classList.remove('is-hiding-up', 'is-hiding-down');
      card.classList.add('is-visible');
    } else {
      card.classList.remove('is-visible');
      if (entry.boundingClientRect.top < 0) {
        card.classList.add('is-hiding-up');
      } else {
        card.classList.add('is-hiding-down');
      }
    }
  });
}, { threshold: 0.1 });

const searchWrap = document.getElementById('search-wrap');
const headerEl   = document.querySelector('header');

function refreshLayout() {
  const scrolled = window.scrollY > 60;
  const hasQuery = !!searchQuery;
  headerEl.style.transform = (scrolled || hasQuery) ? 'translateY(-100%)' : '';
  searchWrap.classList.toggle('visible', scrolled || hasQuery);
}

window.addEventListener('scroll', () => {
  refreshLayout();

  const badge = document.getElementById('search-badge');
  if (searchQuery) {
    badge.style.display = 'block';
    badge.classList.add('visible');
  } else {
    badge.classList.remove('visible');
    setTimeout(() => { if (!searchQuery) badge.style.display = 'none'; }, 300);
  }
}, { passive: true });

fetch('data/events.json')
  .then(r => {
    if (!r.ok) throw new Error(`HTTP ${r.status}`);
    return r.json();
  })
  .then(data => {
    allEvents = Array.isArray(data) ? data : [];
    filtered  = allEvents;
    loadBatch();
    io.observe(sentinel);
  })
  .catch(err => {
    console.error('Failed to load events.json:', err);
    document.getElementById('events-container').innerHTML =
      '<div class="no-results">無法載入事件資料</div>';
    showLoader(false);
  });
