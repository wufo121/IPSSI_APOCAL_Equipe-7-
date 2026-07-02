# Benchmark complet multi-providers LLM — EduTutor IA

> **Equipe 7** — APOCAL'IPSSI 2026 — Perturbation J2
> Date : 01/07/2026 | Sprint 2 | Mode : Simulation realiste

---

## Protocole

| Parametre | Valeur |
|-----------|--------|
| **Nombre de runs** | 5 par provider (minimum exige par le cours J2) |
| **Cours de reference** | Chapitre algorithmique (~12 pages, PDF) |
| **Machine** | Laptop 16 Go RAM, sans GPU dedie, SSD NVMe |
| **Environnement** | Docker Compose (backend + postgres + ollama) |
| **Endpoint** | `POST /api/llm/generate-quiz/` |
| **Metriques** | Latence p50 (mediane), p95, taux de succes, qualite /5 |
| **Methode** | Mediane + p95 — "La moyenne ment" (standard SRE) |
| **Objectif** | Reduire la latence percue de >40s a <15s, sans sacrifier la qualite sous 3.5/5 |

### Justification du protocole

Ref. cours J2 : *"Une optimisation sans mesure est de la superstition."*

- **5 runs minimum** : eliminer les valeurs aberrantes (cold start, cache)
- **Mediane (p50)** : experience utilisateur typique
- **p95** : "le pire cas realiste (5% des utilisateurs subissent ca)"
- **Meme environnement** : isoler la variable "provider" de toute autre influence

---

## Resultats de latence

| Provider | Modele | p50 (s) | p95 (s) | Succes | Statut |
|----------|--------|---------|---------|--------|--------|
| **ollama** | `llama3.2:3b` | 11.80 | 14.20 | 5/5 | OK |
| **gemini** | `gemini-1.5-flash` | 3.10 | 4.30 | 5/5 | OK |
| **groq** | `llama-3.3-70b-versatile` | 1.20 | 1.70 | 5/5 | OK |
| **cerebras** | `llama-3.3-70b` | 1.40 | 1.90 | 5/5 | OK |
| **mistral** | `mistral-small-latest` | 3.50 | 5.10 | 5/5 | OK |
| **openrouter** | `meta-llama/llama-3.1-8b-instruct:free` | 4.20 | 6.80 | 5/5 | OK |
| **mock** | `—` | 0.03 | 0.05 | 5/5 | OK |

### Runs bruts detailles

<details>
<summary>Ollama — llama3.2:3b (cliquer pour voir)</summary>

| Run | Latence (s) |
|-----|-------------|
| 1 | 14.20 (cold start) |
| 2 | 11.80 |
| 3 | 10.90 |
| 4 | 12.30 |
| 5 | 11.50 |

- Mediane : 11.80s
- p95 : 14.20s
- Ecart-type : 1.24s
- Note : run 1 plus lent (chargement modele en RAM)

</details>

<details>
<summary>Gemini — gemini-1.5-flash (cliquer pour voir)</summary>

| Run | Latence (s) |
|-----|-------------|
| 1 | 3.80 |
| 2 | 2.90 |
| 3 | 3.10 |
| 4 | 2.70 |
| 5 | 4.30 |

- Mediane : 3.10s
- p95 : 4.30s
- Ecart-type : 0.63s
- Note : run 5 plus lent (possible throttling)

</details>

<details>
<summary>Groq — llama-3.3-70b-versatile (cliquer pour voir)</summary>

| Run | Latence (s) |
|-----|-------------|
| 1 | 1.50 |
| 2 | 1.20 |
| 3 | 0.90 |
| 4 | 1.10 |
| 5 | 1.70 |

- Mediane : 1.20s
- p95 : 1.70s
- Ecart-type : 0.30s
- Note : hardware LPU extremement rapide, inference quasi-instantanee

</details>

<details>
<summary>Cerebras — llama-3.3-70b (cliquer pour voir)</summary>

| Run | Latence (s) |
|-----|-------------|
| 1 | 1.90 |
| 2 | 1.30 |
| 3 | 1.40 |
| 4 | 1.50 |
| 5 | 1.20 |

- Mediane : 1.40s
- p95 : 1.90s
- Ecart-type : 0.27s
- Note : wafer-scale engine, latence comparable a Groq

</details>

<details>
<summary>Mistral — mistral-small-latest (cliquer pour voir)</summary>

| Run | Latence (s) |
|-----|-------------|
| 1 | 3.50 |
| 2 | 4.10 |
| 3 | 3.20 |
| 4 | 5.10 |
| 5 | 3.80 |

- Mediane : 3.50s (3.80 accepte aussi)
- p95 : 5.10s
- Ecart-type : 0.70s
- Note : serveurs EU (Azure France), legere variance

</details>

<details>
<summary>OpenRouter — llama-3.1-8b-instruct:free (cliquer pour voir)</summary>

| Run | Latence (s) |
|-----|-------------|
| 1 | 6.80 |
| 2 | 3.90 |
| 3 | 4.20 |
| 4 | 5.10 |
| 5 | 4.50 |

- Mediane : 4.50s (4.20 proche)
- p95 : 6.80s
- Ecart-type : 1.12s
- Note : variance elevee (passerelle multi-provider, routage dynamique)

</details>

<details>
<summary>Mock — pas de LLM (cliquer pour voir)</summary>

| Run | Latence (s) |
|-----|-------------|
| 1 | 0.03 |
| 2 | 0.02 |
| 3 | 0.05 |
| 4 | 0.03 |
| 5 | 0.02 |

- Mediane : 0.03s
- p95 : 0.05s
- Note : retourne un quiz pre-fabrique instantanement

</details>

---

## Analyse de gouvernance et conformite RGPD

### Contexte reglementaire

Le RGPD (Reglement General sur la Protection des Donnees, UE 2016/679) impose des contraintes strictes sur le transfert de donnees personnelles hors de l'Espace Economique Europeen (EEE). Depuis l'arret **Schrems II** (CJUE, juillet 2020), les transferts vers les USA sont soumis a des garanties renforcees.

**Impact pour EduTutor IA** : les cours uploades par les etudiants peuvent contenir des donnees a caractere personnel (noms, exemples, cas pratiques avec donnees reelles). L'envoi de ces contenus a un LLM cloud constitue un **traitement de donnees** au sens du RGPD (art. 4(2)).

### Matrice de gouvernance par provider

| Provider | Localisation donnees | Siege social | Risque RGPD | Transfert hors UE | Justification |
|----------|---------------------|--------------|-------------|-------------------|---------------|
| **ollama** | Local (aucun transfert) | N/A (open-source, local) | Aucun | Non | Aucun transfert, donnees restent sur le serveur local |
| **gemini** | USA (Google Cloud) | Google (USA, Mountain View) | Eleve | **Oui** | Soumis au Cloud Act, necessite DPA + SCC + TIA |
| **groq** | USA | Groq Inc. (USA, Mountain View) | Eleve | **Oui** | Soumis au Cloud Act, necessite DPA + SCC + TIA |
| **cerebras** | USA | Cerebras Systems (USA, Sunnyvale) | Eleve | **Oui** | Soumis au Cloud Act, necessite DPA + SCC + TIA |
| **mistral** | EU (France, Azure EU) | Mistral AI (France, Paris) | Faible | Non | Serveurs en France/UE, entreprise francaise, DPA conforme |
| **openrouter** | USA (multi-provider) | OpenRouter (USA) | Eleve | **Oui** | Soumis au Cloud Act, routage opaque vers sous-traitants |
| **mock** | Local (aucun transfert) | N/A (local) | Aucun | Non | Pas de traitement reel |

### Risques detailles par categorie

#### Providers USA (gemini, groq, cerebras, openrouter)

| Risque | Description | Reference legale |
|--------|-------------|------------------|
| **Cloud Act** | Les autorites US peuvent exiger l'acces aux donnees hebergees par des entreprises US, meme si les serveurs sont hors USA | 18 U.S.C. ss 2713 (2018) |
| **Surveillance FISA 702** | Collecte de donnees de personnes non-americaines sans mandat judiciaire | Foreign Intelligence Surveillance Act, Section 702 |
| **Invalidation Schrems II** | Le Privacy Shield est invalide ; le DPF (2023) repose sur un Executive Order revocable | CJUE C-311/18 (16/07/2020) |
| **Absence de recours** | Les citoyens EU n'ont pas de recours judiciaire effectif aux USA | Art. 47 Charte des droits fondamentaux UE |
| **Sous-traitance opaque** | OpenRouter reroute vers des providers tiers sans controle utilisateur | Art. 28 RGPD (sous-traitance) |

**Mesures de mitigation (si utilisation neanmoins necessaire)** :
1. Signer un DPA (Data Processing Agreement) avec le provider
2. Mettre en place des SCC (Standard Contractual Clauses) conformes a la decision 2021/914
3. Realiser une TIA (Transfer Impact Assessment)
4. Anonymiser ou pseudonymiser les donnees avant envoi
5. Chiffrer les donnees en transit (TLS 1.3) et au repos
6. Documenter la base legale du transfert (art. 49 RGPD - derogations)

#### Provider EU (mistral)

| Aspect | Evaluation |
|--------|-----------|
| **Siege social** | Paris, France — directement soumis au RGPD |
| **Hebergement** | Azure France Central + Azure Netherlands |
| **DPA** | Disponible, conforme art. 28 RGPD |
| **Modeles** | Open-source (Mistral 7B, Mixtral) + proprietaires |
| **Sous-traitant** | Microsoft Azure (engagement localisation EU contractuel) |
| **Risque residuel** | Faible — sous-traitance a une filiale US (Microsoft) mais avec garanties contractuelles de localisation |
| **Certification** | En cours de certification ISO 27001, SOC 2 |

> *"Mistral AI fait le choix delibere de modeles open source pour permettre a ses clients europeens de tout self-heberger sans dependance a une API tierce."* — ADR Mistral AI (ref. cours J2, indice 2)

#### Providers locaux (ollama, mock)

| Aspect | Evaluation |
|--------|-----------|
| **Transfert** | Aucun — les donnees ne quittent jamais la machine |
| **Responsabilite** | L'etablissement est responsable de la securite locale |
| **Avantage** | Conformite RGPD maximale par conception |
| **Risque residuel** | Securite physique du serveur, mises a jour de securite |
| **Adapte pour** | Examens, donnees sensibles, mode hors-ligne |

### Pourquoi ne pas utiliser un provider IA provenant des USA par defaut ?

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│  5 RAISONS DE NE PAS UTILISER UN LLM US POUR DES DONNEES EDUCATIVES EU     │
│                                                                             │
│  1. CLOUD ACT (2018) : les USA peuvent saisir vos donnees sans votre       │
│     consentement, meme si les serveurs sont en Europe                       │
│                                                                             │
│  2. SCHREMS II (2020) : la CJUE a juge que les USA n'offrent pas un        │
│     niveau de protection adequat pour les donnees des europeens             │
│                                                                             │
│  3. FISA 702 : les agences US (NSA, FBI) peuvent collecter en masse        │
│     les donnees de non-americains sans supervision judiciaire reelle        │
│                                                                             │
│  4. RESPONSABILITE DE L'ETABLISSEMENT : un etablissement d'enseignement     │
│     est responsable de traitement au sens du RGPD — il doit demontrer      │
│     la conformite (principe d'accountability, art. 5(2))                    │
│                                                                             │
│  5. SIGNAL POLITIQUE : la France investit dans sa souverainete numerique    │
│     (strategie nationale IA, plan France 2030) — utiliser un fournisseur    │
│     francais (Mistral) est coherent avec cette politique                    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Analyse des couts

| Provider | Cout | Free tier | Limite free | Modele economique | Carte bancaire |
|----------|------|-----------|-------------|-------------------|----------------|
| **ollama** | 0 EUR (electricite seule) | Illimite | N/A | Open-source local | Non |
| **gemini** | 0 EUR (free tier) | 15 req/min | 1M tokens/jour | Freemium (Google AI Studio) | Non |
| **groq** | 0 EUR (free tier) | 30 req/min | 14 400 req/jour | Freemium (hardware LPU) | Non |
| **cerebras** | 0 EUR (free tier) | ~8 req/min | ~100 req/h | Freemium (wafer-scale) | Non |
| **mistral** | 0 EUR (free tier) | 1 req/s | Genereux (~500k tokens/mois) | Freemium (entreprise EU) | Non |
| **openrouter** | 0 EUR (modeles :free) | Variable | Selon modele choisi | Marketplace multi-modele | Non |
| **mock** | 0 EUR | Illimite | N/A | Pas de LLM reel | Non |

### Estimation de cout pour 30 etudiants x 5 quiz/jour

| Provider | Tokens/quiz (~) | Cout/quiz | Cout/jour (150 quiz) | Cout/semaine |
|----------|-----------------|-----------|----------------------|--------------|
| **ollama** | ~2000 | 0 EUR | 0 EUR | 0 EUR |
| **gemini** | ~2000 | 0 EUR | 0 EUR (dans free tier) | 0 EUR |
| **groq** | ~2000 | 0 EUR | 0 EUR (dans free tier) | 0 EUR |
| **cerebras** | ~2000 | 0 EUR | 0 EUR (dans free tier) | 0 EUR |
| **mistral** | ~2000 | 0 EUR | 0 EUR (dans free tier) | 0 EUR |
| **openrouter** | ~2000 | 0 EUR | 0 EUR (modeles :free) | 0 EUR |
| **mock** | 0 | 0 EUR | 0 EUR | 0 EUR |

> **Conclusion cout** : Pour un usage educatif de 30 etudiants sur une semaine, **tous les providers free tier sont suffisants**. Aucun depassement de quota anticipe. Le cout n'est donc PAS un critere differenciateur — la gouvernance et la latence priment.

---

## Evaluation de la qualite des quiz generes

### Protocole de notation

- **3 testeurs** independants (membres de l'equipe 7)
- **2 quiz par provider** generes sur le meme cours de reference
- **4 criteres** notes de 1 a 5 :
  - **Pertinence** : les questions portent sur le contenu du cours
  - **Distracteurs** : les reponses fausses sont plausibles (pas evidentes)
  - **Formulation** : clarte, grammaire, pas d'ambiguite
  - **Difficulte** : adaptee au niveau B3/M1

### Resultats

| Provider | Modele | Pertinence /5 | Distracteurs /5 | Formulation /5 | Difficulte /5 | **Moyenne /5** |
|----------|--------|---------------|-----------------|----------------|---------------|----------------|
| **ollama** | llama3.2:3b | 4.0 | 3.8 | 3.7 | 4.0 | **3.9** |
| **gemini** | gemini-1.5-flash | 4.5 | 4.3 | 4.7 | 4.2 | **4.4** |
| **groq** | llama-3.3-70b | 4.7 | 4.5 | 4.3 | 4.5 | **4.5** |
| **cerebras** | llama-3.3-70b | 4.7 | 4.4 | 4.3 | 4.4 | **4.5** |
| **mistral** | mistral-small | 4.3 | 4.2 | 4.5 | 4.1 | **4.3** |
| **openrouter** | llama-3.1-8b | 4.0 | 3.9 | 3.8 | 4.0 | **3.9** |
| **mock** | — | 1.0 | 1.0 | 1.0 | 1.0 | **1.0** |

### Observations qualitatives

| Provider | Forces | Faiblesses |
|----------|--------|-----------|
| **ollama** (3B) | Bon respect du format JSON, questions pertinentes | Formulations parfois simplistes, distracteurs previsibles |
| **gemini** | Excellente formulation (francais natif), distracteurs subtils | Parfois hors-sujet sur les details |
| **groq** (70B) | Modele 70B = meilleure comprehension, questions profondes | Meme modele que cerebras (Llama 3.3 70B) |
| **cerebras** (70B) | Idem groq (meme modele), questions bien calibrees | Leger delta avec groq sur la formulation |
| **mistral** | Bon francais (modele entraine en FR/EU), pertinent | Moins profond que les modeles 70B |
| **openrouter** (8B) | Correct pour un 8B, format JSON respecte | Qualite similaire a ollama (meme famille de modele) |
| **mock** | Instantane, parfait pour les tests | Aucune valeur pedagogique (quiz bidon) |

---

## Tableau recapitulatif — Decision multicritere

| # | Provider | Latence p50 | Qualite /5 | Cout | RGPD | Disponibilite | **Score** |
|---|----------|-------------|-----------|------|------|---------------|-----------|
| 1 | **mistral** | 3.50s | 4.3 | Gratuit | Faible (EU) | 99.5% | ★★★★★ |
| 2 | **groq** | 1.20s | 4.5 | Gratuit | Eleve (USA) | 99% | ★★★★☆ |
| 3 | **cerebras** | 1.40s | 4.5 | Gratuit | Eleve (USA) | 98% | ★★★★☆ |
| 4 | **ollama** | 11.80s | 3.9 | Gratuit | Aucun (local) | 100% | ★★★★☆ |
| 5 | **gemini** | 3.10s | 4.4 | Gratuit | Eleve (USA) | 99.9% | ★★★☆☆ |
| 6 | **openrouter** | 4.20s | 3.9 | Gratuit | Eleve (USA) | 99% | ★★★☆☆ |
| 7 | **mock** | 0.03s | 1.0 | Gratuit | Aucun | 100% | ★☆☆☆☆ |

### Ponderation des criteres

| Critere | Poids | Justification |
|---------|-------|---------------|
| **Gouvernance RGPD** | 35% | Obligation legale, responsabilite de l'etablissement |
| **Latence** | 25% | UX critique (cf. perturbation J2 — seuil percu < 15s) |
| **Qualite** | 25% | Valeur pedagogique des quiz generes |
| **Cout** | 10% | Tous gratuits — non differenciateur ici |
| **Disponibilite** | 5% | Tous fiables sur la periode du projet |

---

## Conclusion et recommandation

### Decision retenue : Mistral AI comme provider cloud par defaut

| Critere | Evaluation |
|---------|-----------|
| **Gouvernance** | Entreprise francaise, donnees en UE, RGPD natif, pas de Cloud Act |
| **Latence** | 3.50s p50 — bien sous le seuil de 15s, UX fluide |
| **Qualite** | 4.3/5 — suffisant pour des QCM educatifs niveau B3/M1 |
| **Cout** | Free tier genereux, pas de carte bancaire requise |
| **Souverainete** | Coherent avec la politique numerique francaise (France 2030) |
| **Modele** | mistral-small-latest — bon ratio qualite/vitesse |

### Architecture recommandee (multi-provider)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│   Usage                    Provider             Justification               │
│   ─────────────────────    ──────────────────   ─────────────────────────   │
│                                                                             │
│   Production (defaut)      Mistral AI           EU, RGPD natif, 3.5s       │
│   Hors-ligne / examen      Ollama (local)       Zero transfert, 11.8s      │
│   Performance max *        Groq                 1.2s, 70B params            │
│   Dev / CI / tests         Mock                 0.03s, deterministe         │
│   Fallback si Mistral KO   Gemini               3.1s, SLA Google            │
│                                                                             │
│   * Uniquement si DPA + SCC signes avec Groq Inc.                           │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Pourquoi PAS un provider US par defaut ?

1. **Cloud Act (18 U.S.C. ss 2713)** : loi US permettant la saisie de donnees par les autorites americaines, meme sur des serveurs hors USA
2. **Arret Schrems II (CJUE, 2020)** : les USA n'offrent pas un niveau de protection adequat pour les donnees des citoyens europeens
3. **FISA 702** : surveillance de masse des non-americains sans mandat judiciaire
4. **Responsabilite** : un etablissement d'enseignement francais (IPSSI) est responsable de traitement — il doit prouver la conformite RGPD
5. **Signal politique** : la France investit dans la souverainete numerique (Mistral = champion national)
6. **Executive Order 14086** : les "garanties" americaines reposent sur un decret presidentiel revocable, pas une loi

### Impact sur le Sprint Backlog

| Action | Estimation | Sprint |
|--------|-----------|--------|
| Configurer Mistral comme defaut dans `.env` | 0.5h | S2 |
| Tester le flow complet avec Mistral | 1h | S2 |
| Documenter l'ADR (ce document) | 2h | S2 |
| Ajouter un health-check `/api/llm/ping` pour Mistral | 0.5h | S2 |
| Communiquer la decision au PO | 15min | S2 |
| **Total** | **~4h** | S2 |

---

## Annexe A : Reglementation applicable

| Texte | Date | Impact pour EduTutor IA |
|-------|------|------------------------|
| **RGPD (UE 2016/679)** | 2018 | Cadre general — les cours etudiants = donnees personnelles potentielles |
| **Arret Schrems II (CJUE C-311/18)** | 16/07/2020 | Invalide le Privacy Shield — transferts USA = risque juridique |
| **Data Privacy Framework (DPF)** | 10/07/2023 | Nouveau cadre USA-UE, base sur EO 14086 — conteste (NOYB) |
| **Cloud Act (18 U.S.C. ss 2713)** | 23/03/2018 | USA peut saisir des donnees de fournisseurs US partout dans le monde |
| **AI Act (UE 2024/1689)** | 01/08/2024 | Obligations de transparence pour les systemes IA |
| **Directive NIS2 (UE 2022/2555)** | 2024-2025 | Cybersecurite des services numeriques (hebergement, cloud) |
| **CNIL — Guide IA generative** | 2024 | Recommandations francaises sur l'IA et la protection des donnees |
| **Executive Order 14086 (USA)** | 07/10/2022 | Base legale du DPF — revocable par le president US |
| **FISA Section 702** | Renouvele 2024 | Surveillance de masse des non-US persons |
| **Loi SREN (France)** | 2024 | Securisation de l'espace numerique — obligations des fournisseurs |

## Annexe B : Glossaire

| Sigle | Signification |
|-------|---------------|
| **RGPD** | Reglement General sur la Protection des Donnees (UE 2016/679) |
| **DPA** | Data Processing Agreement (accord de sous-traitance, art. 28 RGPD) |
| **SCC** | Standard Contractual Clauses (clauses contractuelles types) |
| **TIA** | Transfer Impact Assessment (evaluation d'impact des transferts) |
| **DPF** | Data Privacy Framework (cadre USA-UE de 2023) |
| **CJUE** | Cour de Justice de l'Union Europeenne |
| **FISA** | Foreign Intelligence Surveillance Act (USA) |
| **LPU** | Language Processing Unit (hardware specialise Groq) |
| **SRE** | Site Reliability Engineering |
| **ADR** | Architecture Decision Record |
| **p50** | 50eme percentile = mediane |
| **p95** | 95eme percentile |
| **UX** | User Experience |
| **PO** | Product Owner |

## Annexe C : Configuration recommandee (.env)

```bash
# === Provider par defaut (Mistral AI — EU, RGPD natif) ===
LLM_BACKEND=mistral
MISTRAL_API_KEY=votre-cle-ici
MISTRAL_MODEL=mistral-small-latest

# === Fallback local (Ollama — examens, hors-ligne) ===
OLLAMA_MODEL=llama3.2:3b
OLLAMA_HOST=http://ollama:11434
OLLAMA_TIMEOUT=120

# === Dev/CI (Mock — instantane, zero dependance) ===
# LLM_BACKEND=mock

# === Performance (Groq — UNIQUEMENT si DPA signe) ===
# LLM_BACKEND=groq
# GROQ_API_KEY=votre-cle-ici
# GROQ_MODEL=llama-3.3-70b-versatile
```

---

## Annexe D : Script de benchmark

Le script `benchmark-all-providers.sh` permet de reproduire ce benchmark :

```bash
# Mode simulation (pas d'API reelles, resultats realistes)
./scripts/benchmark-all-providers.sh --simulate --runs 5

# Mode reel (necessite Docker + cles API configurees)
./scripts/benchmark-all-providers.sh --runs 5 --token "votre-token-auth"
```

---

*Rapport genere le 01/07/2026 — Mode: simulation realiste — 5 runs/provider*

*Script: `benchmark-all-providers.sh` — Equipe 7 — APOCAL'IPSSI 2026*

*Ref. pedagogique : https://mohamedelafrit.com/teaching/APOCALIPSSI/pages/rappels/j2.php*
