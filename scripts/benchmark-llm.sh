#!/usr/bin/env bash
# benchmark-llm.sh — Benchmark reproductible de latence pour la génération de quiz
# Usage: ./benchmark-llm.sh <modele_ollama> <nb_runs>
# Exemple: ./benchmark-llm.sh llama3.2:3b 5
#
# Mesure 5 runs (par défaut) de l'endpoint local de génération de quiz pour un
# modèle Ollama donné, sur le même cours de référence, et journalise les temps.
# Protocole équipe 7 : même machine (laptop 16 Go RAM, sans GPU dédié),
# même cours de référence (chapitre d'algorithmique, ~12 pages).

set -euo pipefail

MODEL="${1:-llama3.1:8b}"
RUNS="${2:-5}"
COURSE_FILE="./fixtures/cours-reference-algorithmie.pdf"
ENDPOINT="http://localhost:8000/api/quiz/generate/"
LOGFILE="benchmark-${MODEL//:/_}-$(date +%Y%m%d-%H%M%S).log"

echo "Modèle: $MODEL | Runs: $RUNS | Endpoint: $ENDPOINT" | tee "$LOGFILE"

# S'assure que le modèle Ollama ciblé est bien celui chargé
export LLM_MODEL="$MODEL"

for i in $(seq 1 "$RUNS"); do
  echo "--- Run $i/$RUNS ---" | tee -a "$LOGFILE"
  /usr/bin/time -f "real=%e s" curl -s -o /dev/null \
    -F "course=@${COURSE_FILE}" \
    -F "model=${MODEL}" \
    "$ENDPOINT" 2>> "$LOGFILE"
done

echo "Terminé. Résultats bruts dans $LOGFILE" 
echo "Calculer médiane / p95 avec: grep 'real=' $LOGFILE | awk -F'=' '{print \$2}' | sort -n"
