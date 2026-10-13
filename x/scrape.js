// Coleta das médias do dia em thekingstats.com/dashboard (usuário free).
// Rodar no navegador com a página do dashboard aberta. Roda em segundo plano
// (rolagem lenta para não tomar 429) e grava o resultado em window.__kingScan.
// Depois de ~3-4 min, ler window.__kingScan.done / .rows.
(async () => {
  window.__kingScan = { done: false, started: Date.now() };
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  await sleep(4000);
  const el = [...document.querySelectorAll("h2,h3,div")].find(e => e.textContent.trim() === "Analyze any game yourself");
  if (el) el.scrollIntoView();
  for (let i = 0; i < 260; i++) {
    window.scrollBy(0, 700);
    await sleep(1100);
    if (window.innerHeight + window.scrollY >= document.body.scrollHeight - 5) break;
  }
  await sleep(6000);
  const lines = document.body.innerText.split("\n").map(s => s.trim()).filter(Boolean);
  const rows = []; let league = "";
  for (let i = 0; i < lines.length; i++) {
    if (/^\d+ games?$/.test(lines[i + 1] || "")) league = lines[i];
    if (/^\d{2}:\d{2}$/.test(lines[i]) && lines[i + 8] === "AVERAGE") {
      rows.push({ league, time: lines[i], home: lines[i + 1], away: lines[i + 15],
        hv: lines.slice(i + 2, i + 8), av: lines.slice(i + 9, i + 15), aw: lines.slice(i + 16, i + 22) });
    }
  }
  window.__kingScan = { done: true, total: rows.length,
    withData: rows.filter(r => /%/.test(r.av[3])).length, rows };
})();
"started";
