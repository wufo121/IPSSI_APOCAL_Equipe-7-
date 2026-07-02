/** Mentions légales —  avec les informations réelles de l'éditeur (champs []). */
import LegalScaffold, { type LegalSection } from './LegalScaffold';

const SECTIONS: LegalSection[] = [
  {
    title: 'Éditeur du site',
    hint: `Le site EduTutor IA (ci-après « le Site ») est édité par :

[] — Nom de la société, association ou de l'entrepreneur individuel
Forme juridique : [] (ex. SAS, auto-entrepreneur, association loi 1901…)
Numéro d'immatriculation : [] (SIREN/SIRET, ou n° RNA pour une association)
Capital social : [] (le cas échéant)
Siège social : [] (adresse postale complète)
Numéro de TVA intracommunautaire : [] (le cas échéant)
Adresse e-mail de contact : []
Téléphone : [] (facultatif mais recommandé)

Si l'éditeur est une personne physique n'agissant pas à titre professionnel, seules ses coordonnées peuvent être communiquées sur demande, conformément à la réglementation en vigueur.`,
  },
  {
    title: 'Directeur de la publication',
    hint: `Le Directeur de la publication du Site est :

[] — Nom et prénom du responsable
Qualité : [] (ex. président, gérant, responsable du projet…)
Contact : []

Conformément à l'article 6-III de la loi n° 2004-575 du 21 juin 2004 pour la confiance dans l'économie numérique, le Directeur de la publication est responsable du contenu diffusé sur le Site.`,
  },
  {
    title: 'Hébergeur',
    hint: `Le Site est hébergé par :

[] — Nom de l'hébergeur (ex. OVHcloud, Vercel Inc., AWS, Scaleway…)
Adresse : []
Téléphone : []
Site web : []

Note : si vous utilisez un service comme Vercel, Netlify, OVH ou AWS, vous trouverez généralement leur raison sociale, adresse et coordonnées légales dans les mentions légales ou conditions d'utilisation publiées sur leur propre site.`,
  },
  {
    title: 'Propriété intellectuelle',
    hint: `L'ensemble des éléments composant le Site (structure générale, textes, graphismes, images, logos, icônes, code source, base de données, et plus généralement tout contenu présent sur le Site) est protégé par le droit d'auteur, le droit des marques et/ou le droit des bases de données.

Ces éléments sont la propriété exclusive de [ — nom de l'éditeur], sauf mention contraire ou éléments appartenant à des tiers utilisés avec leur autorisation.

Toute reproduction, représentation, modification, publication, adaptation ou exploitation, totale ou partielle, des éléments du Site, par quelque procédé que ce soit, est strictement interdite sans l'autorisation écrite préalable de [ — nom de l'éditeur], sauf exceptions prévues par la loi.`,
  },
  {
    title: 'Contact',
    hint: `Pour toute question relative aux présentes mentions légales, au fonctionnement du Site ou à l'exercice de vos droits, vous pouvez contacter l'éditeur :

Par e-mail : []
Par courrier postal : [ — adresse complète]

Pour toute question relative à la protection de vos données personnelles, veuillez vous référer à la Politique de confidentialité du Site, ou contacter directement [ — adresse e-mail dédiée, ex. dpo@... ou contact@...].`,
  },
];

export default function MentionsLegalesPage() {
  return (
    <LegalScaffold
      title="Mentions légales"
      intro="Informations légales obligatoires identifiant l'éditeur et l'hébergeur du site."
      sections={SECTIONS}
    />
  );
}
