# Exemples de questions / réponses

> **Projet personnel — données fictives.** Sorties réelles du script `src/rag_pipeline.py` sur la base de connaissances fictive de ce dépôt (génération simulée, voir le README).

## Q1 — « Combien de temps le code SMS reste-t-il valable ? »

**Passage retrouvé** : « Combien de temps le code est-il valable ? » (`code-otp.md`)

> Le code est valable **10 minutes**. Après expiration, vous pouvez demander un nouveau code depuis l'écran de signature.

✅ Réponse fondée sur un passage unique et pertinent : c'est le comportement attendu du pipeline.

## Q2 — « Ma pièce d'identité a été refusée, que faire ? »

**Passage retrouvé** : « Pourquoi ma pièce d'identité a-t-elle été refusée ? » (`verification-identite.md`)

> Les causes les plus fréquentes : photo floue ou reflets, document coupé, document expiré, nom ou date de naissance illisibles. Conseils : surface plane, pas de flash, quatre coins visibles.

✅ La recherche lexicale suffit ici car la question reprend le vocabulaire du document.

## Q3 — « Puis-je annuler mon financement après la signature ? »

**Passage retrouvé** : « Puis-je me rétracter après avoir signé ? » (`apres-signature.md`)

> Délai de rétractation de 14 jours calendaires à compter de la signature.

⚠️ Cas limite : « annuler » et « rétracter » sont synonymes pour un humain, pas pour un recouvrement lexical simple. En production, c'est exactement le problème que les **embeddings** résolvent (proximité sémantique, pas seulement mots partagés) — voir le README, section « Choix d'indexation ».

## Q4 — « Quel est le taux de mon financement ? »

**Passage retrouvé** : aucun au-dessus du seuil.

> « Je n'ai pas trouvé cette information dans la base d'aide. Un conseiller peut vous répondre — je ne préfère pas deviner. »

✅ Le garde-fou fonctionne : la base ne contient pas cette donnée (elle est propre à chaque dossier client), donc l'assistant **refuse de répondre** plutôt que d'inventer un taux.
