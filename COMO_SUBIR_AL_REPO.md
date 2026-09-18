# Cómo subir esta actualización al repositorio (10 minutos)

Esta carpeta contiene los archivos NUEVOS o REEMPLAZADOS para `laudato-si-ai-standard`. No borra nada de lo que ya existe (solo reemplaza `README.md` y `benchmarks/benchmark_v1.csv`, que ahora tiene 20 casos en vez de 10).

## Opción A — con git en tu Mac
```bash
cd ~/Desktop
git clone https://github.com/ricardocovarrubiassahagun-sys/laudato-si-ai-standard
cp -R "~/Desktop/Laudato SI /Laudato_Si_AI_Standard_1.0/repo-updates/". laudato-si-ai-standard/
cd laudato-si-ai-standard
rm -f LICENSE-CODE.txt LICENSE-STANDARD.txt        # sustituidos por LICENSE y LICENSE-STANDARD.md
pip install -e "python[dev]" pytest-asyncio && pytest   # debe dar 8 passed
git add -A
git commit -m "v1.0.0: real licenses, reference implementation (CLI, MCP server, benchmark), tests, CI, citation, templates"
git tag v1.0.0
git push && git push --tags
```
Luego en GitHub: **Settings → General → Features → Discussions** (activar) y **Releases → Draft a new release → tag v1.0.0**, pega el contenido de `CHANGELOG.md` como notas.

## Opción B — sin git (subida por web)
En el repo → "Add file → Upload files", arrastra el contenido de esta carpeta respetando las subcarpetas (`python/`, `benchmarks/`, `mcp/`, `docs/`, `examples/`, `.github/`). Borra `LICENSE-CODE.txt` y `LICENSE-STANDARD.txt`. Después crea el release y activa Discussions como en la opción A.

## Después (opcional, recomendado)
- Zenodo: conecta el repo en https://zenodo.org/account/settings/github/ y vuelve a publicar el release → DOI; añade `doi:` en `CITATION.cff`.
- PyPI: `pip install build twine && cd python && python -m build && twine upload dist/*` para que `pip install laudato-si` funcione sin clonar.

## Qué cierra esto de la lista de vacíos
V1 licencias reales · V2 release + CHANGELOG · V3 rúbrica + runner + 20 casos · V4 servidor MCP de referencia + schema JSON · V5 Discussions (manual) + issue templates · V6 CITATION.cff (DOI pendiente en Zenodo) · V7 RELATED_WORK · V8 examples ejecutables · V9 CODE_OF_CONDUCT · V10 README con maintainer y estado · CI con tests en cada push.
Pendientes: V11 versión en español del estándar; V12 política de no-representación en governance.
