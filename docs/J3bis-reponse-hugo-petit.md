# Réponse à la demande d'accès RGPD (Art. 15) — Hugo Petit

---

**De :** EduTutor IA — DPO fictif \<dpo@edututor-ia.local\>
**À :** Hugo Petit \<hugo.petit@test.local\>
**Date :** 1er juillet 2026
**Objet :** Réponse à votre demande d'accès à vos données personnelles (RGPD Art. 15)

---

Monsieur Petit,

Nous avons bien reçu votre demande d'accès à vos données personnelles formulée le mercredi 1er juillet 2026 à 10h30, conformément à l'article 15 du Règlement Général sur la Protection des Données (RGPD).

Nous sommes heureux de vous confirmer que votre demande a été traitée **dans les délais légaux** (réponse dans les 48h, bien en deçà du délai légal de 30 jours prévu par l'Art. 12(3) RGPD).

---

## 1. Fichier d'export joint

Votre export de données personnelles est disponible en téléchargement depuis votre espace personnel sur EduTutor IA :

**Lien :** `GET /api/accounts/me/export/` (authentification requise avec votre compte `hugo.petit@test.local`)

Deux formats sont proposés, conformément à l'Art. 20 RGPD (droit à la portabilité) :

- **JSON** : `export_rgpd_<horodatage>.json` — format structuré, lisible par machine
- **CSV** : `export_rgpd_<horodatage>.csv` — compatible Excel et tout tableur

---

## 2. Données transmises

Le fichier d'export contient l'intégralité des données vous concernant, réparties en catégories :

| Catégorie | Contenu |
|---|---|
| **Données de compte** | Email, prénom, nom, date d'inscription, statut de vérification email |
| **Quiz générés** | Titre, texte source du cours, date de création, score obtenu |
| **Questions & réponses** | Énoncé, 4 options, bonne réponse, réponse que vous avez donnée |
| **Signalements** | Aucun signalement enregistré à votre nom |
| **Historique SAR** | Date de la présente demande, statut « Répondue », hash SHA-256 du fichier |

---

## 3. Vos droits complémentaires

En complément du droit d'accès (Art. 15), nous vous rappelons que vous disposez des droits suivants :

- **Art. 16 — Rectification** : corriger vos informations directement depuis la page Mon profil.
- **Art. 17 — Effacement (droit à l'oubli)** : supprimer définitivement votre compte et toutes vos données depuis Mon profil → Zone de danger.
- **Art. 18 — Limitation** : demander la limitation du traitement de vos données en nous contactant.
- **Art. 20 — Portabilité** : l'export ci-dessus répond à ce droit (format JSON / CSV machine-readable).

---

## 4. Contact DPO & réclamation

Pour toute question complémentaire, contactez notre délégué à la protection des données :
**dpo@edututor-ia.local**

Si vous estimez que vos droits ne sont pas respectés, vous avez le droit de saisir la **Commission Nationale de l'Informatique et des Libertés (CNIL)** :
🔗 [www.cnil.fr/fr/saisir-la-cnil](https://www.cnil.fr/fr/saisir-la-cnil)

---

Nous restons à votre disposition pour tout renseignement complémentaire.

Cordialement,

**L'équipe EduTutor IA — Équipe 7 IPSSI**
DPO fictif : dpo@edututor-ia.local
Date de réponse : 1er juillet 2026

---

*Ce document constitue l'audit trail SAR enregistré en base de données (modèle `DataRequest`) avec statut « Répondue » et hash SHA-256 du fichier exporté.*
