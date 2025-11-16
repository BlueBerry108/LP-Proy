// parseHorario: toma strings como "Lun 08:00-10:00; Mie 09:00-11:00" y retorna
// [{dia: "LUN", start: 480, end: 600}, ...] donde start/end en minutos desde 00:00

const DAY_NAMES = {
  lu: "LUN", lun: "LUN", lunes: "LUN",
  ma: "MAR", mar: "MAR", martes: "MAR",
  mi: "MIE", mie: "MIE", miercoles: "MIE", miércoles: "MIE",
  ju: "JUE", jue: "JUE", jueves: "JUE",
  vi: "VIE", vie: "VIE", viernes: "VIE",
  sa: "SAB", sab: "SAB", sabado: "SAB", sábado: "SAB",
  do: "DOM", dom: "DOM", domingo: "DOM"
};

function hhmmToMinutes(s) {
  // acepta "08:00" o "800"
  const m = s.match(/(\d{1,2}):?(\d{2})/);
  if (!m) return null;
  const h = parseInt(m[1], 10), mm = parseInt(m[2], 10);
  return h*60 + mm;
}

export function parseHorario(horarioStr) {
  if (!horarioStr) return [];
  const parts = horarioStr.split(/[;,/]/).map(p=>p.trim()).filter(Boolean);
  const out = [];
  for (let p of parts) {
    // separar día del rango de horas
    const pieces = p.split(/\s+/);
    if (pieces.length < 2) continue;
    const dayRaw = pieces[0].toLowerCase();
    let day = DAY_NAMES[dayRaw.slice(0,3)] || DAY_NAMES[dayRaw];
    if (!day) continue;
    // buscar rango como "08:00-10:00"
    const m = p.match(/(\d{1,2}:?\d{2})\s*-\s*(\d{1,2}:?\d{2})/);
    if (!m) continue;
    const start = hhmmToMinutes(m[1]);
    const end = hhmmToMinutes(m[2]);
    if (start !== null && end !== null) out.push({ dia: day, start, end });
  }
  return out;
}

export function intervalsOverlap(aStart, aEnd, bStart, bEnd) {
  return aStart < bEnd && bStart < aEnd;
}

export function schedulesConflict(h1, h2) {
  // h1, h2 arrays de {dia, start, end}
  for (const a of h1) {
    for (const b of h2) {
      if (a.dia === b.dia && intervalsOverlap(a.start, a.end, b.start, b.end)) return true;
    }
  }
  return false;
}