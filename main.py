import requests
from datetime import datetime

#
# Configuration
API_BASE = "https://api.croustillant.menu/v1"
RESTAURANT_PAR_DEFAUT = 1456

# Récupération des données de l'API
def api_get(endpoint):
    """Effectue une requête GET sur l'API CROUStillant."""
    url = f"{API_BASE}{endpoint}"
    try:
        response = requests.get(url, timeout=10)

        if response.status_code == 404:
            try:
                data = response.json()
                return None
            except ValueError:
                return None

        response.raise_for_status()
        data = response.json()
        if data.get("success"):
            return data.get("data")
        else:
            print(f"  Erreur API : {data.get('message', 'Inconnue')}")
            return None
    except requests.ConnectionError:
        print("  Erreur : impossible de se connecter à l'API. Vérifie ta connexion internet.")
        return None
    except requests.Timeout:
        print("  Erreur : l'API ne répond pas (timeout).")
        return None
    except requests.RequestException as e:
        print(f"  Erreur : {e}")
        return None


# Liste des régions
def lister_regions():
    """Liste toutes les régions CROUS disponibles."""
    regions = api_get("/regions")
    if not regions:
        return

    print("\n  ╔══════════════════════════════════════╗")
    print("  ║       RÉGIONS CROUS DISPONIBLES      ║")
    print("  ╚══════════════════════════════════════╝\n")

    for region in regions:
        print(f"    [{region['code']:>2}] {region['libelle']}")
    print()


def lister_restaurants(code_region):
    """Liste les restaurants d'une région donnée."""
    restaurants = api_get(f"/regions/{code_region}/restaurants")
    if not restaurants:
        print("  Aucun restaurant trouvé pour cette région.")
        return

    nom_region = restaurants[0]["region"]["libelle"]
    print(f"\n  ╔══════════════════════════════════════════════════╗")
    print(f"  ║  Restaurants - {nom_region:^33} ║")
    print(f"  ╚══════════════════════════════════════════════════╝\n")

    for r in restaurants:
        status = "ouvert" if r.get("ouvert") else "fermé"
        print(f"    [{r['code']:>4}] {r['nom']} ({status})")
    print()

# Rechercher un restaurant par nom
def chercher_restaurant(nom_recherche):
    """Recherche un restaurant par nom dans toute la France."""
    restaurants = api_get("/restaurants")
    if not restaurants:
        return []

    nom_lower = nom_recherche.lower()
    return [r for r in restaurants if nom_lower in r["nom"].lower()]

# Afficher le menu d'un restaurant
def afficher_menu(code_restaurant):
    """Récupère et affiche le menu d'un restaurant via l'API CROUStillant."""
    # Infos du restaurant
    info = api_get(f"/restaurants/{code_restaurant}")
    if not info:
        print("  Restaurant introuvable.")
        return

    # Menu
    menus = api_get(f"/restaurants/{code_restaurant}/menu")
    if not menus:
        print(f"  Aucun menu disponible pour '{info['nom']}'.")
        return

    # Header
    nom = info["nom"]
    largeur = max(50, len(nom) + 6)
    ligne = "═" * largeur

    print(f"\n  ╔{ligne}╗")
    print(f"  ║  {nom:^{largeur - 4}}  ║")
    print(f"  ╠{ligne}╣")
    if info.get("adresse"):
        adr = info["adresse"][:largeur - 4]
        print(f"  ║  {adr:^{largeur - 4}}  ║")
    if info.get("horaires"):
        for h in info["horaires"]:
            h_tronque = h[:largeur - 4]
            print(f"  ║  {h_tronque:^{largeur - 4}}  ║")
    print(f"  ╚{ligne}╝")

    # Menus par jour
    for menu in menus:
        date_str = menu["date"]
        print(f"\n  ┌{'─' * 48}┐")
        print(f"  │  {date_str:^44}  │")
        print(f"  └{'─' * 48}┘")

        for repas in menu.get("repas", []):
            type_repas = repas.get("type", "").capitalize()
            print(f"\n    {type_repas}")
            print(f"    {'─' * 40}")

            for categorie in repas.get("categories", []):
                libelle = categorie.get("libelle", "Sans catégorie")
                print(f"\n    [{libelle}]")

                for plat in categorie.get("plats", []):
                    nom_plat = plat.get("libelle", "").strip()
                    if nom_plat and nom_plat not in ("--", "Fermé", ""):
                        print(f"      - {nom_plat}")

    print()

# Afficher le menu d'un restaurant pour une date donnée
def afficher_menu_date(code_restaurant, date_str):
    """Affiche le menu d'un restaurant pour une date donnée (format DD-MM-YYYY)."""
    info = api_get(f"/restaurants/{code_restaurant}")
    if not info:
        print("  Restaurant introuvable.")
        return

    menu_data = api_get(f"/restaurants/{code_restaurant}/menu/{date_str}")
    if not menu_data:
        print(f"  Aucun menu trouvé pour le {date_str}.")
        return

    nom = info["nom"]
    print(f"\n  {nom} - Menu du {date_str}")
    print(f"  {'═' * 45}")

    for repas in menu_data.get("repas", []):
        type_repas = repas.get("type", "").capitalize()
        print(f"\n    {type_repas}")
        print(f"    {'─' * 40}")

        for categorie in repas.get("categories", []):
            libelle = categorie.get("libelle", "Sans catégorie")
            print(f"\n    [{libelle}]")

            for plat in categorie.get("plats", []):
                nom_plat = plat.get("libelle", "").strip()
                if nom_plat and nom_plat not in ("--", "Fermé", ""):
                    print(f"      - {nom_plat}")

    print()


# Menu principal interactif
def menu_principal():
    print()
    print("  ╔══════════════════════════════════════╗")
    print("  ║       CROUS MENU SCANNER             ║")
    print("  ╚══════════════════════════════════════╝")
    print()
    print("  1. Menu du jour (GreEn-ER par défaut)")
    print("  2. Menu d'un restaurant (par code)")
    print("  3. Chercher un restaurant par nom")
    print("  4. Lister les restaurants d'une région")
    print("  5. Lister les régions")
    print("  0. Quitter")
    print()

    while True:
        choix = input("  > ").strip()

        if choix == "1":
            code = input(f"  Code du restaurant [{RESTAURANT_PAR_DEFAUT}] > ").strip()
            if not code:
                code = RESTAURANT_PAR_DEFAUT
            elif code.isdigit():
                code = int(code)
            else:
                print("  Code invalide.")
                continue
            afficher_menu(code)

        elif choix == "2":
            code = input("  Code du restaurant > ").strip()
            if code.isdigit():
                afficher_menu(int(code))
            else:
                print("  Le code doit être un nombre.")

        elif choix == "3":
            nom = input("  Rechercher > ").strip()
            if not nom:
                continue
            resultats = chercher_restaurant(nom)
            if resultats:
                print(f"\n  {len(resultats)} résultat(s) :\n")
                for r in resultats:
                    print(f"    [{r['code']:>4}] {r['nom']} ({r['region']['libelle']})")
                print()
                voir = input("  Voir le menu ? (entrer le code ou 'n') > ").strip()
                if voir.isdigit():
                    afficher_menu(int(voir))
            else:
                print("  Aucun résultat.")

        elif choix == "4":
            code = input("  Code de la région (5 pour les voir) > ").strip()
            if code.isdigit():
                lister_restaurants(int(code))

        elif choix == "5":
            lister_regions()

        elif choix == "0":
            print("\n  Au revoir !")
            break

        else:
            print("  Choix invalide. (1-5 ou 0)")

        print("  ─────────────────────────────────────")
        print("  1=Menu  2=Code  3=Chercher  4=Région  5=Régions  0=Quitter")


if __name__ == "__main__":
    menu_principal()