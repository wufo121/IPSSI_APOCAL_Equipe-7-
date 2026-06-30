# ADR-001 : Choix du modèle LLM local pour la génération de quiz

**Statut :** Validé · **Date :** 30/06/2026 · **Équipe :** 7 · **Sprint :** Sprint 2 (perturbation J2)

## Contexte

Le retour d'un beta-testeur (Master 2) signale un temps de génération de quiz de 45 secondes avec le modèle Llama 3.1 8B (Ollama local), perçu comme bloquant : l'utilisateur a cru l'application cassée et a failli abandonner. Le critère d'acceptation CA3 vise une génération en moins de 60 s, mais l'expérience utilisateur impose en réalité un seuil perçu beaucoup plus bas. Le sponsor exige une solution acceptable le soir même, avec une explication argumentée.

## Options envisagées

| Option | Latence p50 / p95 | Qualité subjective (/5, 3 testeurs) | RAM requise | Verdict |
|---|---|---|---|---|
| Llama 3.1 8B (actuel) | 42 s / 51 s | 4.5/5 | ~6 Go | Trop lent pour l'usage perçu |
| Llama 3.2 3B | 12 s / 18 s | 4/5 | < 2 Go | Gain ×3-4, qualité suffisante |
| Phi-3 mini | 14 s / 22 s | 3.8/5 | ~2.3 Go | Bon compromis, légèrement plus lent |
| Ne rien changer | 42 s / 51 s | 4.5/5 | ~6 Go | Écarté : ne répond pas à la perturbation |

Protocole : 5 runs par modèle, même cours de référence (chapitre d'algorithmique, ~12 pages), même machine (laptop 16 Go RAM, sans GPU dédié), mesures médiane et p95.

## Décision retenue

Bascule du modèle par défaut de **Llama 3.1 8B vers Llama 3.2 3B** via Ollama, intégrée derrière un feature-flag de configuration (variable d'environnement `LLM_MODEL`), sans modification du code d'appel LLM.

## Justification

Le gain de latence (×3,5 sur la médiane, 42 s → 12 s) passe largement sous le seuil de tolérance perçu par l'utilisateur, pour une perte de qualité subjective limitée (4,5 → 4/5 sur l'échantillon de 3 testeurs). La consommation RAM est également réduite (< 2 Go contre ~6 Go), ce qui sécurise la contrainte T7 (laptop 16 Go RAM, `docker compose up`). Phi-3 mini, bien que proche, n'apporte pas d'avantage suffisant pour justifier un changement de fournisseur de modèle plutôt qu'une simple bascule de taille au sein de la même famille Llama.

## Conséquences

**Positives** : génération perçue comme quasi-instantanée, RAM libérée pour les autres services Docker (PostgreSQL, backend, frontend), aucune dépendance externe ajoutée (toujours 100 % local, conformité RGPD préservée).

**Négatives** : légère baisse de qualité subjective sur certains QCM (formulations parfois moins nuancées), à surveiller sur l'audit qualité prévu en perturbation J4.

**À surveiller** : si l'audit qualité des 50 questions (J4) révèle un taux d'erreur factuelle significatif, réévaluer Phi-3 mini ou un retour conditionnel à Llama 3.1 8B sur les cours longs (> 20 pages) où la qualité prime sur la latence.
