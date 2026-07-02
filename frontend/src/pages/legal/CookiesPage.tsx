/** Politique de gestion des cookies. */
import LegalScaffold, { type LegalSection } from './LegalScaffold';

const SECTIONS: LegalSection[] = [
  {
    title: "Qu'est-ce qu'un cookie ?",
    hint: `Un cookie est un petit fichier texte déposé et stocké sur votre ordinateur, tablette ou smartphone lors de la consultation d'un site internet. Il permet au site de reconnaître votre navigateur et de conserver certaines informations d'une visite à l'autre (préférences, état de connexion, etc.).

Par extension, la présente politique couvre également les autres technologies de stockage utilisées par le site, telles que le « localStorage » ou le « sessionStorage » du navigateur, qui remplissent des fonctions similaires en conservant des données localement sur votre appareil.`,
  },
  {
    title: 'Cookies et stockage utilisés',
    hint: `Le site EduTutor IA utilise les traceurs suivants :

- Un jeton d'authentification (token) stocké dans le localStorage du navigateur, permettant de maintenir votre session connectée entre deux visites.
- Des cookies techniques nécessaires au bon fonctionnement du site (préférences d'affichage, langue, etc.), le cas échéant.
- Le cas échéant, des cookies de mesure d'audience permettant d'établir des statistiques de fréquentation anonymisées.

Cette liste sera mise à jour à chaque évolution des outils et technologies utilisés par le site.`,
  },
  {
    title: 'Finalité de chaque cookie',
    hint: `Chaque traceur déposé répond à une finalité précise :

- Jeton d'authentification (localStorage) : finalité strictement technique, permettant de vous identifier en tant qu'utilisateur connecté et d'accéder aux fonctionnalités réservées à votre compte. Ce stockage est indispensable au fonctionnement du Service.
- Cookies de préférences : mémoriser vos choix d'affichage ou de configuration afin d'améliorer votre expérience de navigation.
- Cookies de mesure d'audience (le cas échéant) : comprendre l'usage du site (pages consultées, parcours de navigation) à des fins statistiques, sous une forme anonymisée ou pseudonymisée dans la mesure du possible.

Aucun traceur n'est utilisé à des fins de publicité ciblée par l'éditeur.`,
  },
  {
    title: 'Consentement',
    hint: `Conformément à la réglementation applicable (notamment la directive ePrivacy et les recommandations de la CNIL), une distinction est faite entre :

- Les cookies et traceurs strictement nécessaires au fonctionnement du site (tel que le jeton d'authentification), qui ne nécessitent pas de consentement préalable et sont déposés dès l'utilisation du Service.
- Les cookies non essentiels (notamment les cookies de mesure d'audience non exemptés ou tout traceur à visée statistique/publicitaire), qui nécessitent votre consentement préalable, recueilli via une bannière d'information dédiée lors de votre première visite.

Vous pouvez à tout moment retirer votre consentement ou modifier vos choix via le module de gestion des cookies accessible depuis le site.`,
  },
  {
    title: 'Durée de conservation',
    hint: `Les traceurs déposés sont conservés pour une durée limitée, proportionnée à leur finalité :

- Jeton d'authentification (localStorage) : conservé jusqu'à votre déconnexion volontaire, la suppression manuelle des données du navigateur, ou l'expiration technique du jeton.
- Cookies de préférences : conservés pour une durée maximale de 13 mois, conformément aux recommandations de la CNIL.
- Cookies de mesure d'audience (le cas échéant) : conservés pour une durée maximale de 13 mois, votre consentement étant redemandé à l'expiration de ce délai.

À l'expiration de ces durées, votre consentement sera à nouveau sollicité avant tout nouveau dépôt de traceurs non essentiels.`,
  },
  {
    title: 'Gérer ou refuser les cookies',
    hint: `Vous disposez de plusieurs moyens pour gérer les traceurs déposés sur votre appareil :

- Via la bannière ou le module de gestion des cookies du site, accessible à tout moment, qui vous permet d'accepter, refuser ou personnaliser vos choix par finalité.
- Via les paramètres de votre navigateur, qui vous permettent de bloquer, supprimer ou être averti du dépôt de cookies. La procédure varie selon le navigateur utilisé (Chrome, Firefox, Safari, Edge, etc.) ; consultez la rubrique d'aide de votre navigateur pour plus de détails.
- Pour les données stockées en localStorage, la suppression des données de navigation via les paramètres de votre navigateur effacera également ces informations (ce qui entraînera votre déconnexion du Service).

Veuillez noter que le refus de certains traceurs strictement nécessaires (comme le jeton d'authentification) peut empêcher l'accès à certaines fonctionnalités du Service, notamment celles nécessitant d'être connecté.`,
  },
];

export default function CookiesPage() {
  return (
    <LegalScaffold
      title="Politique de gestion des cookies"
      intro="Les cookies et technologies de stockage utilisés par le site, et comment les gérer."
      sections={SECTIONS}
    >
      <div className="mt-6 p-3 bg-slate-50 border border-slate-200 rounded text-sm text-slate-600">
        💡 Indice pour votre équipe : ce kit stocke actuellement le{' '}
        <code className="bg-slate-200 px-1 rounded">token</code> d'authentification dans le{' '}
        <code className="bg-slate-200 px-1 rounded">localStorage</code> du navigateur. C'est un bon
        point de départ à documenter ici.
      </div>
    </LegalScaffold>
  );
}
