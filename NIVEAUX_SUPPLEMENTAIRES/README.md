# Niveaux LostAdventure

Ce dossier rassemble les aperçus des tables déjà présentes dans le dépôt,
50 nouveaux labyrinthes numérotés de 11 à 60, ainsi qu’une maquette de niveau 61.

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
  CPC composée le 28 octobre 2026, avec deux cœurs et des portes.

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

## Maquette du niveau 61

La table 61 est une proposition visuelle, non raccordée à la progression du
BASIC. Elle contient le titre `LOST ADVENTURE`, deux cœurs (`8`) et trois
portes (`3`). Le code du jeu traite une porte comme franchissable et déclenche
le niveau suivant quand le compteur de Miam atteint zéro ; il faudra distinguer
portes de passage et sortie si elles doivent garder des rôles différents.
Cette table n’utilise que le mur standard `1` ; les variantes `4` à `7` restent
prises en charge par le rendu et la simulation existants.

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
