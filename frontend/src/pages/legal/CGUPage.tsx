/** Conditions Générales d'Utilisation. */
import LegalScaffold, { type LegalSection } from './LegalScaffold';

const SECTIONS: LegalSection[] = [
  {
    title: 'Objet',
    hint: `Les présentes Conditions Générales d'Utilisation (ci-après « CGU ») ont pour objet de définir les modalités et conditions dans lesquelles les utilisateurs (ci-après « l'Utilisateur » ou « les Utilisateurs ») peuvent accéder et utiliser le service EduTutor IA (ci-après « le Service »), une plateforme d'assistance pédagogique s'appuyant sur des technologies d'intelligence artificielle, notamment pour la génération de quiz et de contenus d'entraînement.

Toute utilisation du Service implique l'acceptation pleine et entière des présentes CGU.`,
  },
  {
    title: 'Acceptation des conditions',
    hint: `L'accès et l'utilisation du Service sont subordonnés à l'acceptation et au respect des présentes CGU. En créant un compte, en cochant la case prévue à cet effet lors de l'inscription, ou simplement en utilisant le Service, l'Utilisateur reconnaît avoir pris connaissance des CGU et les accepter sans réserve.

Si l'Utilisateur n'accepte pas tout ou partie des présentes CGU, il ne doit pas accéder au Service ni l'utiliser.

Lorsque l'Utilisateur est mineur, l'inscription et l'utilisation du Service doivent se faire sous la supervision et avec l'autorisation d'un représentant légal.`,
  },
  {
    title: 'Accès au service',
    hint: `Le Service est accessible gratuitement ou selon les modalités tarifaires en vigueur, 24 heures sur 24 et 7 jours sur 7, sauf cas de force majeure, interruption programmée ou non programmée pour des raisons de maintenance, ou panne.

L'éditeur s'efforce d'assurer une disponibilité optimale du Service mais ne garantit pas une accessibilité continue et ininterrompue. L'éditeur ne saurait être tenu responsable des interruptions et de leurs conséquences pour l'Utilisateur.

L'accès au Service nécessite une connexion Internet et un équipement compatible dont l'Utilisateur doit faire l'acquisition et assurer le bon fonctionnement à ses frais exclusifs.`,
  },
  {
    title: 'Compte utilisateur',
    hint: `L'accès à certaines fonctionnalités du Service nécessite la création d'un compte personnel. L'Utilisateur s'engage à fournir des informations exactes, à jour et complètes lors de son inscription, et à les maintenir à jour.

L'Utilisateur est seul responsable de la confidentialité de ses identifiants de connexion (identifiant et mot de passe) et de toute activité réalisée depuis son compte. Il s'engage à informer immédiatement l'éditeur de toute utilisation non autorisée de son compte ou de toute atteinte à la sécurité de celui-ci.

L'éditeur se réserve le droit de suspendre ou de supprimer tout compte en cas de manquement aux présentes CGU ou en cas d'informations manifestement erronées ou frauduleuses.`,
  },
  {
    title: 'Comportements interdits',
    hint: `Dans le cadre de l'utilisation du Service, l'Utilisateur s'engage à ne pas :
- publier, transmettre ou générer des contenus illicites, diffamatoires, injurieux, discriminatoires, violents ou contraires à l'ordre public et aux bonnes mœurs ;
- utiliser le Service à des fins de tricherie académique en violation des règles de son établissement ;
- tenter de contourner, désactiver ou perturber les mesures de sécurité du Service ;
- extraire, copier ou réutiliser tout ou partie du Service sans autorisation, notamment à des fins commerciales ;
- utiliser des robots, scripts ou tout autre moyen automatisé pour accéder au Service ;
- porter atteinte aux droits de propriété intellectuelle de l'éditeur ou de tiers ;
- usurper l'identité d'un tiers ou fournir de fausses informations.

Tout manquement à ces règles pourra entraîner la suspension ou la suppression du compte de l'Utilisateur, sans préjudice de toute action judiciaire.`,
  },
  {
    title: 'Contenu généré par IA',
    hint: `Le Service s'appuie sur des technologies d'intelligence artificielle pour générer automatiquement des quiz, exercices et autres contenus pédagogiques. L'Utilisateur reconnaît et accepte que :
- ces contenus sont générés de manière automatisée et peuvent, malgré les efforts de l'éditeur, contenir des erreurs, imprécisions ou approximations ;
- les contenus générés ne sauraient se substituer à un enseignement dispensé par un professionnel qualifié et doivent être utilisés à titre d'aide complémentaire à l'apprentissage ;
- il appartient à l'Utilisateur de faire preuve d'esprit critique et de vérifier, le cas échéant, l'exactitude des informations et réponses fournies par le Service ;
- l'éditeur ne saurait être tenu responsable des conséquences directes ou indirectes résultant de l'utilisation ou de la confiance accordée aux contenus générés par le Service.`,
  },
  {
    title: 'Responsabilité',
    hint: `L'éditeur met en œuvre tous les moyens raisonnables pour assurer un Service de qualité, mais n'est tenu que d'une obligation de moyens.

L'éditeur ne saurait être tenu responsable :
- des dommages résultant d'une utilisation du Service non conforme aux présentes CGU ;
- des interruptions, dysfonctionnements ou pertes de données liés à des causes indépendantes de sa volonté (panne réseau, cas de force majeure, fait d'un tiers) ;
- des contenus générés automatiquement par l'intelligence artificielle et de leur exactitude, comme précisé à l'article « Contenu généré par IA » ;
- de l'usage qui est fait par l'Utilisateur des résultats obtenus via le Service, notamment dans un cadre scolaire ou académique.

En tout état de cause, la responsabilité de l'éditeur, si elle était retenue, serait limitée aux dommages directs et prévisibles, à l'exclusion de tout dommage indirect.`,
  },
  {
    title: 'Propriété intellectuelle',
    hint: `L'ensemble des éléments composant le Service (structure, textes, logos, graphismes, algorithmes, base de données, code source, etc.) sont protégés par le droit de la propriété intellectuelle et demeurent la propriété exclusive de l'éditeur ou de ses partenaires.

Toute reproduction, représentation, modification, publication ou adaptation de tout ou partie des éléments du Service, quel que soit le moyen ou le procédé utilisé, est interdite sans autorisation écrite préalable de l'éditeur.

Les contenus déposés, saisis ou téléversés par l'Utilisateur dans le cadre de l'utilisation du Service demeurent sa propriété. L'Utilisateur concède toutefois à l'éditeur une licence non exclusive, à des fins strictement nécessaires au fonctionnement et à l'amélioration du Service (notamment l'entraînement ou l'ajustement des fonctionnalités d'IA, sous réserve de la politique de confidentialité applicable).`,
  },
  {
    title: 'Modification des CGU',
    hint: `L'éditeur se réserve le droit de modifier à tout moment les présentes CGU, notamment afin de les adapter aux évolutions du Service ou aux évolutions légales et réglementaires.

Les Utilisateurs seront informés de toute modification substantielle par tout moyen approprié (notification sur le Service, courrier électronique, etc.) avant leur entrée en vigueur.

La poursuite de l'utilisation du Service après l'entrée en vigueur des nouvelles CGU vaut acceptation de celles-ci. Il est recommandé à l'Utilisateur de consulter régulièrement la version en vigueur des CGU.`,
  },
  {
    title: 'Droit applicable et litiges',
    hint: `Les présentes CGU sont soumises au droit français.

En cas de litige relatif à l'interprétation, l'exécution ou la validité des présentes CGU, les parties s'efforceront de trouver une solution amiable avant toute action contentieuse.

À défaut de résolution amiable, et sous réserve des règles de compétence légalement impératives (notamment celles protectrices des consommateurs), les tribunaux compétents seront ceux du ressort du siège social de l'éditeur.`,
  },
];

export default function CGUPage() {
  return (
    <LegalScaffold
      title="Conditions Générales d'Utilisation"
      intro="Les règles d'utilisation du service EduTutor IA, acceptées par chaque utilisateur."
      sections={SECTIONS}
    />
  );
}
