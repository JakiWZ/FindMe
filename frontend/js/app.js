'use strict';
// Mostra il report esportato da Python (output/report.json). Nessun calcolo: solo lettura e filtri.
const $ = s => document.querySelector(s);
const STATI = ['trovato', 'restituito'];
let report = null;

// Restituisce '' se il report rispetta il formato di logic.esporta_report(), altrimenti il problema.
function valida(d) {
  if (!d || typeof d !== 'object' || Array.isArray(d)) return 'il file non contiene un oggetto JSON.';
  for (const k of ['generato_il', 'oggetti_aperti', 'riepilogo_per_luogo', 'oggetti'])
    if (!(k in d)) return `manca il campo "${k}".`;
  if (!Number.isInteger(d.oggetti_aperti)) return '"oggetti_aperti" deve essere un numero intero.';
  if (!Array.isArray(d.oggetti)) return '"oggetti" deve essere una lista.';
  if (!Array.isArray(d.riepilogo_per_luogo)) return '"riepilogo_per_luogo" deve essere una lista.';
  for (const [n, o] of d.oggetti.entries()) {
    const manca = ['id', 'descrizione', 'luogo', 'stato', 'data_ritrovamento'].filter(k => o?.[k] === undefined || o[k] === '');
    if (manca.length) return `oggetto ${n + 1}: mancano i campi ${manca.join(', ')}.`;
    if (!STATI.includes(o.stato)) return `oggetto ${n + 1}: stato "${o.stato}" non valido (trovato o restituito).`;
  }
  for (const [n, r] of d.riepilogo_per_luogo.entries())
    if (!r?.luogo || !Number.isInteger(r.da_restituire) || !Number.isInteger(r.restituiti))
      return `riepilogo, riga ${n + 1}: servono luogo, da_restituire e restituiti numerici.`;
  return '';
}

function messaggio(testo, ok = false) {
  $('#msg').textContent = testo;
  $('#msg').className = ok ? 'okmsg' : 'err';
}

function el(tag, testo, classe) {
  const e = document.createElement(tag);
  if (testo !== undefined) e.textContent = testo;
  if (classe) e.className = classe;
  return e;
}

function card(o) {
  const c = el('article', undefined, 'card');
  const aperto = o.stato === 'trovato';
  c.append(
    el('span', aperto ? 'Da restituire' : 'Restituito', 'pill ' + (aperto ? 'open' : 'done')),
    el('h3', o.descrizione),
    el('p', 'Trovato in: ' + o.luogo, 'mu'),
    el('p', `${o.data_ritrovamento} · #${o.id}`, 'mu'),
  );
  return c;
}

function renderOggetti() {
  const q = $('#q').value.trim().toLowerCase(), s = $('#fStato').value, l = $('#fLuogo').value;
  const lista = report.oggetti.filter(o =>
    (!q || `${o.descrizione} ${o.luogo}`.toLowerCase().includes(q)) &&
    (!s || o.stato === s) && (!l || o.luogo === l));
  $('#count').textContent = `${lista.length} di ${report.oggetti.length} oggetti`;
  $('#list').replaceChildren(...(lista.length ? lista.map(card) : [el('p', 'Nessun oggetto corrisponde ai filtri.', 'mu')]));
}

function mostra(d) {
  report = d;
  $('#generato').textContent = 'Report generato il ' + String(d.generato_il).replace('T', ' alle ');
  $('#sAperti').textContent = d.oggetti_aperti;
  $('#sTotale').textContent = d.oggetti.length;
  $('#sLuoghi').textContent = d.riepilogo_per_luogo.length;

  const luoghi = d.riepilogo_per_luogo.map(r => r.luogo);
  $('#fLuogo').replaceChildren(el('option', 'Tutti i luoghi'), ...luoghi.map(x => el('option', x)));
  $('#fLuogo').options[0].value = '';
  $('#q').value = ''; $('#fStato').value = '';

  $('#riepilogo').replaceChildren(...d.riepilogo_per_luogo.map(r => {
    const tr = el('tr');
    tr.append(el('td', r.luogo), el('td', r.da_restituire), el('td', r.restituiti));
    return tr;
  }));
  renderOggetti();
  $('#report').hidden = false;
}

$('#file').addEventListener('change', async e => {
  const file = e.target.files[0];
  if (!file) return;
  let d;
  try {
    const testo = await file.text();
    if (!testo.trim()) throw new Error('il file è vuoto.');
    d = JSON.parse(testo.replace(/^﻿/, ''));
  } catch (err) {
    return messaggio('File non valido: ' + (err instanceof SyntaxError ? 'non è un JSON leggibile.' : err.message));
  }
  const problema = valida(d);
  if (problema) return messaggio('File non valido: ' + problema + ' Seleziona il report generato da FindMe.');
  mostra(d);
  messaggio(`Caricato "${file.name}": ${d.oggetti.length} oggetti.`, true);
});
['#q', '#fStato', '#fLuogo'].forEach(s => $(s).addEventListener('input', () => report && renderOggetti()));
