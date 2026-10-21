# Z80X FPGA — note de concept (en réserve)

Statut : **idée conservée, non planifiée, aucune implémentation engagée**.

## Objectif
Étudier ultérieurement le remplacement du Z80 physique d'un Amstrad CPC par un FPGA reproduisant le comportement original et offrant un mode d'exécution étendu. Ce document n'est pas une spécification validée.

## Principes
- **Compatibilité en priorité** : jeu d'instructions, opcodes documentés/non documentés utilisés par les logiciels, interruptions, bus, signaux et timing visibles par le CPC. Le mode compatible ne doit pas casser les jeux, démos et ROM existants.
- **Extensions optionnelles** : explorer des opcodes préfixés `ED` non affectés officiellement ; inventorier et tester les alias et comportements non documentés avant toute allocation. Activation explicite du mode étendu.
- **Arithmétique matérielle** : envisager MUL/DIV signées et non signées, accumulateurs élargis, virgule fixe 16/32 bits, racines carrées, opérations vectorielles/matricielles. Les formats, registres, flags et exceptions restent à définir.
- **Pipeline de calcul** : idée à conserver pour plus tard ; pas de développement maintenant. Le pipeline peut enchaîner des calculs sur données locales sans dialogue BASIC.
- **Mémoire locale rapide de plusieurs Mo** : stocker programmes, matrices, buffers et données dans une RAM associée au FPGA (éventuellement PSRAM/SDRAM externe), sans devoir utiliser la RAM CPC pour les calculs. Évaluer pagination et adressage physique étendu : le Z80 conserve un espace logique de 64 Ko.
- **Échanges avec le CPC** : garder le bus d'origine pour firmware, E/S, périphériques et RAM/vidéo ; étudier transferts par blocs et synchronisation avec le Gate Array. La copie d'un framebuffer local vers la RAM vidéo physique reste contrainte par les accès du CPC.
- **Deux modes au minimum** : Z80 compatible et Z80X accéléré, avec protocole de passage et détection. Évaluer un mode hybride.

## Points d'étude avant réalisation
1. Comparer des cœurs HDL compatibles Z80 (p. ex. T80 / TV80) et leurs licences.
2. Cartographier exhaustivement les 256 seconds octets des opcodes `ED` et leurs effets sur des Z80 réels.
3. Définir la topologie matériel : connecteur CPU, adaptation électrique, horloges, resets, arbitrage, mémoire locale et coût.
4. Spécifier le modèle mémoire et sa cohérence avec les accès ROM/RAM/vidéo du CPC.
5. Simuler les timings du bus et valider la compatibilité au moyen de logiciels et tests réels.
6. Prototyper et benchmarker uniquement après validation des contraintes de compatibilité.

## Lien avec la ROM mathématique
La bibliothèque mathématique Z80 actuelle sert de référence fonctionnelle et de benchmark. Le BASIC CPC est utile pour tests comparatifs, mais n'est **pas** la cible principale de cette ROM. Envisager à terme des implémentations accélérées tirant parti du Z80X sans modifier les interfaces existantes.

## Décision
**Ne pas entreprendre ce chantier maintenant.** Conserver le concept comme piste de recherche séparée des développements ROM/math et Lostadventure en cours.
