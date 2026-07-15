from pathlib import Path
import re

src = Path('/Users/Andre.Wolff/Documents/005___data/git/001_podman_runtime/claudeCodeCamp/week0_explore/logs/mud-session-2026-07-15.log')
dst = Path('/Users/Andre.Wolff/Documents/005___data/git/001_podman_runtime/claudeCodeCamp/week0_explore/logs/mud-journeys-2026-07-15.log')

lines = src.read_text(encoding='utf-8').splitlines()

# Extract canonical top metadata from source.
title = lines[0] if lines else '# MUD-Session-Log'
meta = []
for line in lines[1:20]:
    if line.startswith('- **Datum:**') or line.startswith('- **Quelle:**') or line.startswith('- **Hinweis:**'):
        meta.append(line)

# Parse movement rows from source table.
row_re = re.compile(r'^\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*`([^`]+)`\s*\|\s*([^|]+?)\s*\|\s*(.*?)\s*\|\s*$')
rows = []
for line in lines:
    m = row_re.match(line)
    if m:
        _idx, _zeit, cmd, ziel, erg = m.groups()
        rows.append((cmd.strip(), ziel.strip(), erg.strip()))

# Deduplicate by command + target + result (keep first occurrence order).
seen = set()
uniq = []
for row in rows:
    if row in seen:
        continue
    seen.add(row)
    uniq.append(row)

out = [title, '']
out.extend(meta)
out.append('- **Bereinigung:** Doppelte Bewegungsschritte entfernt (exakter Abgleich: Kommando + Zielraum + Ergebnis).')
out.extend(['', '---', '', '## Bewegungen (automatisch)', '', '| # | Kommando | Zielraum | Ergebnis |', '|---|----------|----------|----------|'])

for i, (cmd, ziel, erg) in enumerate(uniq, start=1):
    out.append(f'| {i} | `{cmd}` | {ziel} | {erg} |')
out.append('')

dst.write_text('\n'.join(out), encoding='utf-8')
print(f'written: {dst}')
print(f'rows total: {len(rows)}')
print(f'rows unique: {len(uniq)}')