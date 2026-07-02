/** Politique de confidentialité EduTutor IA — RGPD (J3-bis). */
export default function ConfidentialitePage() {
  return (
    <article className="max-w-3xl mx-auto">
      <h1 className="text-3xl font-bold text-slate-900 mb-2">Politique de confidentialité</h1>
      <p className="text-slate-600 mb-6">
        Comment les données personnelles des utilisateurs d'EduTutor IA sont collectées, utilisées
        et protégées, conformément au Règlement Général sur la Protection des Données (RGPD).
      </p>

      <div className="space-y-8">

        {/* 1. Responsable du traitement */}
        <section>
          <h2 className="text-lg font-semibold text-slate-900 mb-2">1. Responsable du traitement</h2>
          <p className="text-sm text-slate-700">
            Le responsable du traitement est l'équipe 7 IPSSI — projet EduTutor IA, développé dans
            le cadre pédagogique APOCAL'IPSSI 2026. Contact DPO fictif :{' '}
            <a href="mailto:dpo@edututor-ia.local" className="text-indigo-700 underline">
              dpo@edututor-ia.local
            </a>
            .
          </p>
        </section>

        {/* 2. Données collectées */}
        <section>
          <h2 className="text-lg font-semibold text-slate-900 mb-2">2. Données personnelles collectées</h2>
          <ul className="text-sm text-slate-700 list-disc list-inside space-y-1">
            <li>Données de compte : adresse email, prénom, nom, date d'inscription, statut de vérification email.</li>
            <li>Contenus uploadés : textes de cours soumis pour la génération de quiz.</li>
            <li>Quiz générés : titre, questions, options de réponse, bonne réponse.</li>
            <li>Réponses aux quiz : index sélectionné par question, score obtenu.</li>
            <li>Historique des demandes d'accès (SAR) : date, statut, hash du fichier exporté.</li>
          </ul>
        </section>

        {/* 3. Durées de conservation */}
        <section>
          <h2 className="text-lg font-semibold text-slate-900 mb-2">3. Durées de conservation</h2>
          <div className="overflow-x-auto">
            <table className="text-sm text-slate-700 w-full border border-slate-200 rounded">
              <thead className="bg-slate-50">
                <tr>
                  <th className="text-left px-3 py-2 font-semibold border-b border-slate-200">Type de donnée</th>
                  <th className="text-left px-3 py-2 font-semibold border-b border-slate-200">Durée de conservation</th>
                  <th className="text-left px-3 py-2 font-semibold border-b border-slate-200">Base légale (Art. 6 RGPD)</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                <tr>
                  <td className="px-3 py-2">Données de compte (email, nom, prénom)</td>
                  <td className="px-3 py-2">Durée d'activité du compte + 12 mois après suppression</td>
                  <td className="px-3 py-2">Art. 6(1)(b) — exécution du contrat</td>
                </tr>
                <tr>
                  <td className="px-3 py-2">Textes de cours uploadés</td>
                  <td className="px-3 py-2">Durée d'activité du compte (supprimés avec le compte)</td>
                  <td className="px-3 py-2">Art. 6(1)(b) — exécution du contrat</td>
                </tr>
                <tr>
                  <td className="px-3 py-2">Quiz générés et réponses</td>
                  <td className="px-3 py-2">Durée d'activité du compte (supprimés avec le compte)</td>
                  <td className="px-3 py-2">Art. 6(1)(f) — intérêt légitime (amélioration du service)</td>
                </tr>
                <tr>
                  <td className="px-3 py-2">Logs d'audit SAR (demandes d'accès)</td>
                  <td className="px-3 py-2">36 mois (prescription civile)</td>
                  <td className="px-3 py-2">Art. 6(1)(c) — obligation légale (conformité CNIL)</td>
                </tr>
                <tr>
                  <td className="px-3 py-2">Tokens d'authentification</td>
                  <td className="px-3 py-2">Invalidés à la déconnexion ou au changement de mot de passe</td>
                  <td className="px-3 py-2">Art. 6(1)(b) — exécution du contrat</td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        {/* 4. Motifs légaux */}
        <section>
          <h2 className="text-lg font-semibold text-slate-900 mb-2">4. Finalités et base légale du traitement</h2>
          <ul className="text-sm text-slate-700 list-disc list-inside space-y-1">
            <li><strong>Création et gestion du compte</strong> — exécution du contrat (Art. 6(1)(b)).</li>
            <li><strong>Génération de quiz personnalisés</strong> — exécution du contrat (Art. 6(1)(b)).</li>
            <li><strong>Amélioration du service et sécurité</strong> — intérêt légitime (Art. 6(1)(f)).</li>
            <li><strong>Audit trail des demandes d'accès</strong> — obligation légale (Art. 6(1)(c)).</li>
          </ul>
        </section>

        {/* 5. Modalités de suppression (Art. 17) */}
        <section>
          <h2 className="text-lg font-semibold text-slate-900 mb-2">5. Modalités de suppression (Art. 17 — droit à l'oubli)</h2>
          <p className="text-sm text-slate-700 mb-2">
            Vous pouvez supprimer votre compte à tout moment depuis la page{' '}
            <strong>Mon profil → Zone de danger</strong>. La suppression est immédiate et
            définitive : elle efface votre compte, vos cours uploadés, vos quiz et vos réponses.
          </p>
          <p className="text-sm text-slate-700 mb-2">
            Les logs d'audit SAR sont conservés 36 mois après la suppression du compte pour
            répondre à notre obligation de conformité CNIL, conformément à l'Art. 17(3)(b) RGPD
            (exception pour obligation légale).
          </p>
          <p className="text-sm text-slate-700">
            Pour toute demande de suppression partielle ou d'oubli, contactez :{' '}
            <a href="mailto:dpo@edututor-ia.local" className="text-indigo-700 underline">
              dpo@edututor-ia.local
            </a>
            . Délai de réponse : 30 jours.
          </p>
        </section>

        {/* 6. Vos droits */}
        <section>
          <h2 className="text-lg font-semibold text-slate-900 mb-2">6. Vos droits (Art. 15–22 RGPD)</h2>
          <ul className="text-sm text-slate-700 list-disc list-inside space-y-1">
            <li><strong>Art. 15 — Accès</strong> : obtenir une copie de toutes vos données (bouton "Exporter mes données" dans Mon profil).</li>
            <li><strong>Art. 16 — Rectification</strong> : corriger vos informations depuis Mon profil.</li>
            <li><strong>Art. 17 — Effacement</strong> : supprimer votre compte et toutes vos données depuis Mon profil.</li>
            <li><strong>Art. 18 — Limitation</strong> : demander la limitation du traitement au DPO.</li>
            <li><strong>Art. 20 — Portabilité</strong> : exporter vos données en JSON ou CSV (format machine-readable).</li>
            <li><strong>Art. 21 — Opposition</strong> : s'opposer à certains traitements fondés sur l'intérêt légitime.</li>
          </ul>
          <p className="text-sm text-slate-500 mt-2">
            Pour exercer vos droits :{' '}
            <a href="mailto:dpo@edututor-ia.local" className="text-indigo-700 underline">
              dpo@edututor-ia.local
            </a>
            . En cas de litige, vous pouvez saisir la{' '}
            <a
              href="https://www.cnil.fr"
              target="_blank"
              rel="noopener noreferrer"
              className="text-indigo-700 underline"
            >
              CNIL
            </a>
            .
          </p>
        </section>

        {/* 7. Destinataires */}
        <section>
          <h2 className="text-lg font-semibold text-slate-900 mb-2">7. Destinataires des données</h2>
          <p className="text-sm text-slate-700">
            Les données sont traitées par l'équipe de développement EduTutor IA. Le modèle LLM
            (Llama 3.2 via Ollama) est hébergé <strong>localement</strong> : aucune donnée de
            cours n'est envoyée à un fournisseur cloud tiers. Aucune revente ni partage commercial
            de données.
          </p>
        </section>

        {/* 8. Contact */}
        <section>
          <h2 className="text-lg font-semibold text-slate-900 mb-2">8. Contact &amp; réclamation</h2>
          <p className="text-sm text-slate-700">
            DPO fictif EduTutor IA :{' '}
            <a href="mailto:dpo@edututor-ia.local" className="text-indigo-700 underline">
              dpo@edututor-ia.local
            </a>
            . Autorité de contrôle compétente : Commission Nationale de l'Informatique et des
            Libertés (CNIL) —{' '}
            <a
              href="https://www.cnil.fr"
              target="_blank"
              rel="noopener noreferrer"
              className="text-indigo-700 underline"
            >
              www.cnil.fr
            </a>
            .
          </p>
        </section>

      </div>

      <p className="text-xs text-slate-400 mt-10 pt-4 border-t border-slate-200">
        Dernière mise à jour : 1er juillet 2026. Document rédigé dans le cadre pédagogique
        APOCAL'IPSSI 2026 — Équipe 7.
      </p>
    </article>
  );
}
