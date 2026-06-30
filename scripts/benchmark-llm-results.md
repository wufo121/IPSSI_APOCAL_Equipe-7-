# Résultats du benchmark LLM — Perturbation J2

**Protocole** : 5 runs × 3 modèles, même cours de référence (chapitre d'algorithmique, ~12 pages, PDF), même machine (laptop 16 Go RAM, sans GPU dédié), via `benchmark-llm.sh`.

| Modèle | p50 (médiane) | p95 | Qualité subjective (/5, moy. 3 testeurs) | RAM observée |
|---|---|---|---|---|
| Llama 3.1 8B (référence) | 42 s | 51 s | 4.5/5 | ~6 Go |
| Llama 3.2 3B | 12 s | 18 s | 4.0/5 | < 2 Go |
| Phi-3 mini | 14 s | 22 s | 3.8/5 | ~2.3 Go |

**Verdict** : Llama 3.2 3B retenu (cf. ADR-001), gain de latence ×3,5 sur la médiane pour une perte de qualité limitée et un gain RAM substantiel. Détail des runs bruts disponibles dans les fichiers `benchmark-*.log` générés par le script.
