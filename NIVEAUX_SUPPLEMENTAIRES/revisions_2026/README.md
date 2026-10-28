# Révision des 40 cartes déjà créées

Cette révision porte sur `TABLE11` à `TABLE50` uniquement. Les fichiers d’origine ne sont pas écrasés : les grilles proposées sont dans `tables/` et leurs aperçus CPC dans `images/`.

## Principes de révision

- Les labyrinthes et leurs parcours d’origine sont conservés ; des murs graphiques (codes 4 à 7) apportent des variations visuelles.
- Le nombre de cœurs varie selon la difficulté : 13 cartes proposent deux cœurs et 27 n’en proposent aucun.
- Huit cartes cachent un mot formé de Miam : TABLE15 `RUN`, TABLE20 `SOS`, TABLE25 `FUN`, TABLE30 `WIN`, TABLE35 `JOY`, TABLE40 `RUN`, TABLE45 `SOS`, TABLE50 `FUN`.
- Les dix cartes les plus difficiles selon le score de classement sont TABLE20, TABLE30, TABLE35, TABLE40, TABLE43, TABLE45, TABLE46, TABLE47, TABLE49 et TABLE50. Elles n’ont aucun cœur et contiennent de 27 à 49 Miam.

## Simulation

`simulation_40.csv` donne le résultat des 40 parcours ; `simulation_10_super_durs.csv` détaille les dix cartes difficiles. `apercu_40_tables_revisees.png` et `apercu_10_niveaux_super_durs.png` donnent les vues d’ensemble.

La simulation suit les règles relevées dans `EDLABY.BAS`, avec départ en (2,24) : les codes 1 et 4 à 7 sont des murs mortels, 2 est un Miam, 8 un cœur, et 3 la porte de sortie (atteinte lorsque tous les Miam sont ramassés). Les 40 cartes atteignent la sortie sans collision simulée. C’est une simulation de graphe de déplacement, pas une exécution du jeu sur CPC.

`revise_and_simulate.py` documente et reproduit la génération à partir des tables de départ présentes dans `../tables/`.
