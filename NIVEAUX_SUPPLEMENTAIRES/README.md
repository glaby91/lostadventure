# Niveaux LostAdventure

Ce dossier rassemble les aperçus de toutes les tables déjà présentes dans le
dépôt et 50 nouveaux labyrinthes, numérotés de 11 à 60.

## Contenu

- `tables/TABLE11.LAB` à `tables/TABLE60.LAB` : nouvelles grilles au format du
  jeu, soit 1 000 valeurs décimales pour une grille de 40 × 25 cases.
- `images/nouveaux/` : un rendu en mode caractères CPC pour chacune des
  50 nouvelles grilles.
- `images/existants/` : rendus de `TABLE.LAB`, `TABLE1.LAB` à `TABLE10.LAB`,
  ainsi que de la table binaire actuellement fournie avec le projet.
- `images/apercu_50_nouveaux_niveaux.png` et
  `images/apercu_tables_existantes.png` : planches de comparaison.
- `index.csv` : nombre de Miam, distance de sortie et contrôle d’accessibilité.
- `generate_levels.py` : générateur et outil de rendu reproductible.

## Règles des nouvelles grilles

Les niveaux sont construits comme des labyrinthes connectés. Le départ est
une petite zone ouverte au centre de l’écran, pour que les coordonnées de
départ usuelles restent praticables. Chaque Miam (`2`) et la sortie (`3`) ont
été vérifiés accessibles depuis cette zone. Le nombre de Miam et la distance
de sortie augmentent globalement au fil des niveaux.

Les nouveaux fichiers utilisent les mêmes codes que la routine d’affichage :

| Valeur | Rôle rendu |
|---:|---|
| 0 | case vide / passage |
| 1 | mur |
| 2 | Miam |
| 3 | porte / sortie |

La bordure est ajoutée par la routine ASM, comme dans le jeu. Les images sont
des rendus statiques de la première phase des couleurs clignotantes.

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
