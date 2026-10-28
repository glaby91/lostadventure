# TABLE63 — Le grand détour

Carte CPC 40 × 25 conçue pour obliger les retours en arrière. Les passages forment un arbre sans raccourci, la sortie est juste à côté du départ, et chaque impasse porte un Miam. Il y a 155 Miam et aucun cœur.

## Résultat

- 551 cases accessibles, reliées en 550 arêtes sans boucle.
- Les 155 impasses sont des Miam ; pour les ramasser toutes, le joueur doit explorer chaque branche puis revenir.
- Simulation avec choix du Miam accessible le plus proche : **1 129 déplacements**, sans collision, puis sortie atteinte.
- Borne minimale pour finir : **1 099 déplacements** (chaque branche doit être parcourue et remontée ; le passage vers la sortie, adjacent au départ, ne se parcourt qu’une fois).

Le générateur a comparé 1 000 labyrinthes-arbres aléatoires et gardé la carte au plus grand réseau accessible parmi ceux essayés. C’est le meilleur résultat de cette recherche, pas une preuve du maximum mathématique sur toutes les cartes possibles.

`parcours_force.csv` contient la simulation pas à pas. `TABLE63.LAB` est autonome ; la carte n’est pas encore branchée dans la progression du jeu.
