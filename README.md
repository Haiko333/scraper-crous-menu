# crous-scanner

Un petit script Python pour checker les menus des restos U du CROUS directement depuis le terminal.

J'en avais marre de devoir aller sur le site du CROUS à chaque fois pour voir ce qu'il y avait à manger le midi, du coup j'ai fait ce truc. Ca utilise l'API [CROUStillant](https://croustillant.menu/) (merci à eux) pour récupérer les menus de tous les restaurants CROUS de France.

Par défaut c'est configuré sur le **RU GreEn-ER à Grenoble** mais ça marche avec n'importe quel resto U.

## Installation

```
pip install requests
```

## Utilisation

```
python main.py
```

Le script est interactif, tu choisis ce que tu veux faire :

- **1** - Voir le menu du jour (GreEn-ER par défaut, ou un autre resto si tu tapes son code)
- **2** - Voir le menu d'un resto en tapant son code
- **3** - Chercher un resto par nom (genre tape "diderot" ou "green" et il te trouve tous les restos qui matchent)
- **4** - Lister tous les restos d'une région
- **5** - Voir la liste des régions CROUS

## Changer le resto par défaut

Si t'es pas à Grenoble, ouvre `main.py` et change la variable en haut :

```python
RESTAURANT_PAR_DEFAUT = 1456  # <- mets le code de ton resto ici
```

Pour trouver le code de ton resto, lance le script et utilise la recherche (option 3).

## Comment ça marche

Le script tape sur l'API CROUStillant (`https://api.croustillant.menu/v1`) qui centralise les menus de tous les CROUS. C'est beaucoup plus fiable que de scraper le site du CROUS directement (qui charge tout en JS et qui est assez galère à parser).

## Crédits

- [CROUStillant](https://croustillant.menu/) pour l'API