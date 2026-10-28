# Niveaux LostAdventure

Ce dossier rassemble les aperçus des tables déjà présentes dans le dépôt,
50 nouveaux labyrinthes numérotés de 11 à 60, ainsi que les maquettes de niveaux 61 et 62.

## Contenu

- `tables/TABLE11.LAB` à `tables/TABLE60.LAB` : nouvelles grilles au format du
  jeu, soit 1 000 valeurs décimales pour une grille de 40 × 25 cases.
- `images/nouveaux/` : un rendu en mode caractères CPC pour chacune des
  50 nouvelles grilles.
- `images/existants/` : rendus de `TABLE.LAB`, `TABLE1.LAB` à `TABLE10.LAB`,
  ainsi que de la table binaire actuellement fournie avec le projet.
- `images/apercu_50_nouveaux_niveaux.png` et
  `images/apercu_tables_existantes.png` : planches de comparaison.
- `index.csv` : motif mural, nombre de Miam, distance de sortie et contrôle
  d’accessibilité.
- `generate_levels.py` : générateur et outil de rendu reproductible.
- `propositions/TABLE61.LAB` et `images/propositions/TABLE61.png` : maquette
  CPC avec deux cœurs et des portes.
- `propositions/TABLE62.LAB` et `images/propositions/TABLE62.png` : nouveau
  labyrinthe CPC avec 36 Miam, deux cœurs, des portes et des murs variants.
- `propositions/TABLE63.LAB` et `images/propositions/TABLE63.png` : labyrinthe
  sans boucle, 155 Miam dans les impasses et aucun cœur.

## Règles des nouvelles grilles

Les niveaux sont construits comme des labyrinthes connectés. Le départ est
une petite zone ouverte au centre de l’écran, pour que les coordonnées de
départ usuelles restent praticables. Chaque niveau ajoute une petite forme en
pixel-art dessinée avec les murs : cœur, étoile, maison, clé, fusée, arbre,
fantôme, poisson, couronne, ancre et d’autres motifs. Les formes reviennent
en miroir pour varier leur orientation, tandis que le labyrinthe et leur
position changent.

Chaque Miam (`2`) et la sortie (`3`) ont été vérifiés accessibles depuis le
départ. Les Miam sont posés uniquement sur des cases atteignables, y compris
dans les salles décorées. Le nombre de Miam et la distance de sortie
augmentent globalement au fil des niveaux.

Les nouveaux fichiers utilisent les mêmes codes que la routine d’affichage :

| Valeur | Rôle rendu |
|---:|---|
| 0 | case vide / passage |
| 1 | mur |
| 2 | Miam |
| 3 | porte / sortie |

La bordure est ajoutée par la routine ASM, comme dans le jeu. Les images sont
des rendus statiques de la première phase des couleurs clignotantes. Le dessin
des motifs emploie les murs existants (`1`) : aucune nouvelle tuile ni routine
ASM n’est requise.

## Maquettes des niveaux 61 et 62

Les deux tables sont des propositions visuelles, non raccordées à la progression
du BASIC. TABLE61 reprend l’écran `LOST ADVENTURE` avec deux cœurs et des portes.
TABLE62 propose un labyrinthe jouable avec 36 Miam, deux cœurs (`8`), une porte
de sortie et des portes de passage (`3`). Les variantes de mur `4` à `7` sont
également utilisées dans TABLE62 et sont reconnues par l’affichage et la
simulation.

Le code du jeu traite une porte (`3`) comme franchissable et déclenche le niveau
suivant quand le compteur de Miam atteint zéro ; les portes de passage auront
donc aussi cet effet une fois tous les Miam ramassés. Les deux tables restent
des maquettes tant que cette règle n’est pas adaptée.

## Proposition TABLE63 — La carte de la mort

TABLE63 est une maquette 40 × 25 avec 551 cases accessibles reliées en arbre,
155 Miam placés aux impasses, aucun cœur et une sortie adjacente au départ.
Sans boucle ni raccourci, il faut explorer les branches puis revenir. La
simulation « Miam accessible le plus proche » atteint la sortie en 1 129
déplacements ; la borne minimale de parcours est de 1 099 déplacements.

Le générateur a comparé 1 000 labyrinthes-arbres et retenu le plus grand réseau
accessible trouvé. Ce résultat est le meilleur de cette recherche, pas une
preuve du maximum mathématique. La carte reste une proposition indépendante,
non raccordée à la progression BASIC. Le parcours et les résultats détaillés
sont dans `propositions/TABLE63_parcours.csv` et
`propositions/TABLE63_simulation.csv`.

## Utilisation dans le jeu

Les fichiers existants à la racine du dépôt restent à leur emplacement, pour
ne pas perturber les chargements actuels. Les 50 nouvelles tables sont
regroupées ici et prêtes à être converties avec `CONVERT.BAS` ou intégrées au
chargement des niveaux. Le programme BASIC actuel énumère explicitement les
fichiers `TABLE1.LAB` à `TABLE9.LAB` ; il faudra étendre cette progression pour
que les niveaux 11 à 60 s’enchaînent dans le jeu.

## Régénérer

Depuis la racine du dépôt :

```sh
python3 NIVEAUX_SUPPLEMENTAIRES/generate_levels.py
```

Le générateur a besoin de Python 3 et Pillow.
