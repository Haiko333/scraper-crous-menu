# CROUS Menu Scraper

A small Python script to check university restaurant (resto U) menus from CROUS directly in the terminal.

I was tired of having to go to the CROUS website every time just to see what was for lunch, so I made this. It uses the [CROUStillant](https://croustillant.menu/) API (shoutout to them) to fetch menus from all CROUS restaurants across France.

By default it's set to the **RU GreEn-ER in Grenoble**, but it works with any university restaurant.

## Installation

```
pip install requests
```

## Usage

```
python main.py
```

The script is interactive — you pick what you want to do:

- **1** - View today's menu (GreEn-ER by default, or another restaurant if you enter its code)
- **2** - View a restaurant's menu by entering its code
- **3** - Search for a restaurant by name (e.g. type "diderot" or "green" and it finds all matching restaurants)
- **4** - List all restaurants in a region
- **5** - View the list of CROUS regions

## Changing the Default Restaurant

If you're not in Grenoble, open `main.py` and change the variable at the top:

```python
DEFAULT_RESTAURANT = 1456  # <- put your restaurant's code here
```

To find your restaurant's code, run the script and use the search feature (option 3).

## How It Works

The script hits the CROUStillant API (`https://api.croustillant.menu/v1`), which aggregates menus from all CROUS institutions. It's much more reliable than scraping the CROUS website directly (which loads everything via JS and is a pain to parse).

## Credits

- [CROUStillant](https://croustillant.menu/) for the API
