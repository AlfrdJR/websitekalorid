import json
import hashlib
import uuid
from datetime import date, datetime, timedelta
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components


st.set_page_config(
    page_title="NÕU · Calorie tracker",
    page_icon="◒",
    layout="centered",
    initial_sidebar_state="collapsed",
)


PRODUCTS = [
    {"name": "Kohuke vanilli", "brand": "Tere", "kcal": 170, "protein": 5, "carbs": 18, "fat": 8, "portion": "1 tk · 40 g"},
    {"name": "Kohuke klassikaline", "brand": "Farmi", "kcal": 180, "protein": 5, "carbs": 17, "fat": 10, "portion": "1 tk · 40 g"},
    {"name": "Rukkileib", "brand": "Leibur", "kcal": 210, "protein": 6, "carbs": 39, "fat": 3, "portion": "100 g"},
    {"name": "Kohupiim 5%", "brand": "Alma", "kcal": 120, "protein": 16, "carbs": 4, "fat": 5, "portion": "100 g"},
    {"name": "Skyr naturaalne", "brand": "Tere", "kcal": 62, "protein": 11, "carbs": 4, "fat": 0, "portion": "100 g"},
    {"name": "Kreeka jogurt", "brand": "Farmi", "kcal": 116, "protein": 8, "carbs": 4, "fat": 8, "portion": "100 g"},
    {"name": "Piim 2,5%", "brand": "Alma", "kcal": 52, "protein": 3, "carbs": 5, "fat": 3, "portion": "100 ml"},
    {"name": "Kohvijook Latte", "brand": "Cappy", "kcal": 57, "protein": 3, "carbs": 5, "fat": 3, "portion": "100 ml"},
    {"name": "Mulgipuder", "brand": "Salvest", "kcal": 116, "protein": 3, "carbs": 17, "fat": 4, "portion": "100 g"},
    {"name": "Hakkliha kodune", "brand": "Maks & Moorits", "kcal": 205, "protein": 18, "carbs": 0, "fat": 15, "portion": "100 g"},
    {"name": "Kanafilee", "brand": "Rakvere", "kcal": 110, "protein": 24, "carbs": 0, "fat": 1, "portion": "100 g"},
    {"name": "Viinerid", "brand": "Rakvere", "kcal": 250, "protein": 12, "carbs": 5, "fat": 20, "portion": "100 g"},
    {"name": "Munad", "brand": "Muna Liisu", "kcal": 143, "protein": 13, "carbs": 1, "fat": 10, "portion": "100 g"},
    {"name": "Külmsuitsu lõhe", "brand": "M.V.Wool", "kcal": 180, "protein": 22, "carbs": 0, "fat": 10, "portion": "100 g"},
    {"name": "Hapukoor 20%", "brand": "Farmi", "kcal": 206, "protein": 3, "carbs": 4, "fat": 20, "portion": "100 g"},
    {"name": "Must leib", "brand": "Eesti Pagar", "kcal": 222, "protein": 6, "carbs": 42, "fat": 3, "portion": "100 g"},
    {"name": "Kama", "brand": "Tartu Mill", "kcal": 335, "protein": 14, "carbs": 55, "fat": 5, "portion": "100 g"},
    {"name": "Kaerahelbed", "brand": "Veski Mati", "kcal": 366, "protein": 13, "carbs": 60, "fat": 7, "portion": "100 g"},
    {"name": "Värske salat", "brand": "Bonduelle", "kcal": 25, "protein": 1, "carbs": 4, "fat": 0, "portion": "100 g"},
    {"name": "Mustikad", "brand": "Eesti", "kcal": 57, "protein": 1, "carbs": 10, "fat": 1, "portion": "100 g"},
    {"name": "Halloweeni pitsa 700g", "brand": "Rimi", "kcal": 245, "protein": 10, "carbs": 28, "fat": 10, "portion": "100 g"},
    {"name": "Juust Atleet Eesti viilutatud", "brand": "Atleet", "kcal": 347, "protein": 25, "carbs": 1, "fat": 27, "portion": "100 g"},
    {"name": "Kohupiim metsmaasika", "brand": "Alma", "kcal": 130, "protein": 8, "carbs": 17, "fat": 3, "portion": "200 g"},
    {"name": "Krõbedad ahjuvorstid", "brand": "Rannarootsi", "kcal": 280, "protein": 13, "carbs": 4, "fat": 24, "portion": "100 g"},
    {"name": "Viinamari hele Sultan", "brand": "Rimi", "kcal": 69, "protein": 1, "carbs": 18, "fat": 0, "portion": "100 g"},
    {"name": "Kiivi Gold", "brand": "Rimi", "kcal": 61, "protein": 1, "carbs": 15, "fat": 1, "portion": "100 g"},
    {"name": "Brokoli", "brand": "Rimi", "kcal": 34, "protein": 3, "carbs": 7, "fat": 0, "portion": "100 g"},
    {"name": "Ploom punane", "brand": "Rimi", "kcal": 46, "protein": 1, "carbs": 11, "fat": 0, "portion": "100 g"},
    {"name": "Ploomtomat mini", "brand": "Rimi", "kcal": 18, "protein": 1, "carbs": 4, "fat": 0, "portion": "100 g"},
    {"name": "Juust Mozzarella 45%", "brand": "Rimi", "kcal": 280, "protein": 18, "carbs": 3, "fat": 22, "portion": "100 g"},
    {"name": "Kreeka jogurt maitsestamata", "brand": "Tere", "kcal": 118, "protein": 8, "carbs": 4, "fat": 8, "portion": "100 g"},
    {"name": "Vahukoor 35%", "brand": "Alma", "kcal": 330, "protein": 2, "carbs": 3, "fat": 35, "portion": "100 ml"},
    {"name": "Keefir Hellus pure", "brand": "Hellus", "kcal": 46, "protein": 3, "carbs": 4, "fat": 2, "portion": "100 g"},
    {"name": "Koorene jogurt must kirss", "brand": "Farmi", "kcal": 110, "protein": 3, "carbs": 14, "fat": 5, "portion": "100 g"},
    {"name": "Ökoloogiline mangopüree", "brand": "Salvest", "kcal": 63, "protein": 1, "carbs": 14, "fat": 0, "portion": "100 g"},
    {"name": "Pelmeenid Hiina", "brand": "Uvic", "kcal": 210, "protein": 9, "carbs": 30, "fat": 6, "portion": "100 g"},
    {"name": "Juustuvorst", "brand": "Rakvere", "kcal": 290, "protein": 14, "carbs": 2, "fat": 25, "portion": "100 g"},
    {"name": "Jogurt leiva-pähkli", "brand": "Farmi", "kcal": 118, "protein": 3, "carbs": 17, "fat": 4, "portion": "100 g"},
    {"name": "Lõhefilee", "brand": "Rimi", "kcal": 208, "protein": 20, "carbs": 0, "fat": 13, "portion": "100 g"},
    {"name": "Banaan", "brand": "Rimi", "kcal": 89, "protein": 1, "carbs": 23, "fat": 0, "portion": "100 g"},
    {"name": "Õun", "brand": "Eesti", "kcal": 52, "protein": 0, "carbs": 14, "fat": 0, "portion": "100 g"},
    {"name": "Kartul", "brand": "Eesti", "kcal": 77, "protein": 2, "carbs": 17, "fat": 0, "portion": "100 g"},
    {"name": "Porgand", "brand": "Eesti", "kcal": 41, "protein": 1, "carbs": 10, "fat": 0, "portion": "100 g"},
    {"name": "Kurk", "brand": "Eesti", "kcal": 15, "protein": 1, "carbs": 4, "fat": 0, "portion": "100 g"},
]

RECIPES = []

CUSTOM_PRODUCTS_FILE = Path(__file__).with_name("custom_products.json")
HIDDEN_PRODUCTS_FILE = Path(__file__).with_name("hidden_products.json")
CUSTOM_RECIPES_FILE = Path(__file__).with_name("custom_recipes.json")
DAILY_LOGS_FILE = Path(__file__).with_name("daily_logs.json")
GOALS_FILE = Path(__file__).with_name("goals.json")
WATER_LOGS_FILE = Path(__file__).with_name("water_logs.json")

DEFAULT_GOALS = {"kcal": 2200, "protein": 140, "carbs": 250, "fat": 70}


def load_custom_products():
    if not CUSTOM_PRODUCTS_FILE.exists():
        return []
    try:
        with CUSTOM_PRODUCTS_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
        return data if isinstance(data, list) else []
    except (OSError, json.JSONDecodeError):
        return []


def save_custom_product(product):
    custom_products = load_custom_products()
    custom_products = [p for p in custom_products if p.get("name", "").lower() != product["name"].lower()]
    custom_products.insert(0, product)
    hidden_products = load_hidden_products()
    hidden_products.discard(product["name"].lower())
    with HIDDEN_PRODUCTS_FILE.open("w", encoding="utf-8") as file:
        json.dump(sorted(hidden_products), file, ensure_ascii=False, indent=2)
    with CUSTOM_PRODUCTS_FILE.open("w", encoding="utf-8") as file:
        json.dump(custom_products, file, ensure_ascii=False, indent=2)


def delete_custom_product(name):
    custom_products = [p for p in load_custom_products() if p.get("name", "").lower() != name.lower()]
    with CUSTOM_PRODUCTS_FILE.open("w", encoding="utf-8") as file:
        json.dump(custom_products, file, ensure_ascii=False, indent=2)


def load_hidden_products():
    if not HIDDEN_PRODUCTS_FILE.exists():
        return set()
    try:
        with HIDDEN_PRODUCTS_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
        return {str(name).lower() for name in data} if isinstance(data, list) else set()
    except (OSError, json.JSONDecodeError):
        return set()


def hide_product(name):
    custom_products = [p for p in load_custom_products() if p.get("name", "").lower() != name.lower()]
    with CUSTOM_PRODUCTS_FILE.open("w", encoding="utf-8") as file:
        json.dump(custom_products, file, ensure_ascii=False, indent=2)
    hidden_products = load_hidden_products()
    hidden_products.add(name.lower())
    with HIDDEN_PRODUCTS_FILE.open("w", encoding="utf-8") as file:
        json.dump(sorted(hidden_products), file, ensure_ascii=False, indent=2)


def all_products():
    hidden_products = load_hidden_products()
    custom_products = load_custom_products()
    custom_names = {product.get("name", "").strip().lower() for product in custom_products}
    catalog_products = [
        product for product in PRODUCTS
        if product.get("name")
        and product["name"].strip().lower() not in hidden_products
        and product["name"].strip().lower() not in custom_names
    ]
    return [product for product in custom_products if product.get("name")] + catalog_products


def load_custom_recipes():
    if not CUSTOM_RECIPES_FILE.exists():
        return []
    try:
        with CUSTOM_RECIPES_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
        return data if isinstance(data, list) else []
    except (OSError, json.JSONDecodeError):
        return []


def save_custom_recipe(recipe, replace_name=None):
    recipes = load_custom_recipes()
    names_to_replace = {recipe["name"].strip().casefold()}
    if replace_name:
        names_to_replace.add(str(replace_name).strip().casefold())
    recipes = [
        r for r in recipes
        if r.get("name", "").strip().casefold() not in names_to_replace
    ]
    recipes.insert(0, recipe)
    with CUSTOM_RECIPES_FILE.open("w", encoding="utf-8") as file:
        json.dump(recipes, file, ensure_ascii=False, indent=2)


def delete_custom_recipe(name):
    recipes = [recipe for recipe in load_custom_recipes() if recipe.get("name", "").lower() != name.lower()]
    with CUSTOM_RECIPES_FILE.open("w", encoding="utf-8") as file:
        json.dump(recipes, file, ensure_ascii=False, indent=2)


def all_recipes():
    custom = load_custom_recipes()
    custom_names = {recipe.get("name", "").lower() for recipe in custom}
    return custom + [recipe for recipe in RECIPES if recipe["name"].lower() not in custom_names]


def load_daily_logs():
    if not DAILY_LOGS_FILE.exists():
        return {}
    try:
        with DAILY_LOGS_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
        return data if isinstance(data, dict) else {}
    except (OSError, json.JSONDecodeError):
        return {}


def save_daily_logs():
    with DAILY_LOGS_FILE.open("w", encoding="utf-8") as file:
        json.dump(st.session_state.daily_logs, file, ensure_ascii=False, indent=2)


def load_goals():
    if not GOALS_FILE.exists():
        return DEFAULT_GOALS.copy()
    try:
        with GOALS_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
        return {key: max(1, int(data.get(key, DEFAULT_GOALS[key]))) for key in DEFAULT_GOALS}
    except (OSError, json.JSONDecodeError, TypeError, ValueError):
        return DEFAULT_GOALS.copy()


def save_goals(goals):
    with GOALS_FILE.open("w", encoding="utf-8") as file:
        json.dump(goals, file, ensure_ascii=False, indent=2)


def load_water_logs():
    if not WATER_LOGS_FILE.exists():
        return {}
    try:
        with WATER_LOGS_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
        return data if isinstance(data, dict) else {}
    except (OSError, json.JSONDecodeError):
        return {}


def save_water_logs():
    with WATER_LOGS_FILE.open("w", encoding="utf-8") as file:
        json.dump(st.session_state.water_logs, file, ensure_ascii=False, indent=2)


def water_total(day=None):
    return int(st.session_state.water_logs.get((day or TODAY).isoformat(), 0))


def change_water(amount, day=None):
    key = (day or TODAY).isoformat()
    st.session_state.water_logs[key] = max(0, int(st.session_state.water_logs.get(key, 0)) + int(amount))
    save_water_logs()


def product_base_grams(product):
    portion = str(product.get("portion", "100 g"))
    if "portsjon" in portion.lower():
        return 100.0
    numbers = []
    current = ""
    for character in portion:
        if character.isdigit() or character == ".":
            current += character
        elif current:
            numbers.append(float(current))
            current = ""
    if current:
        numbers.append(float(current))
    return numbers[-1] if numbers else 100.0


def product_for_grams(product, grams):
    """Return a product scaled from its catalogue portion to the entered grams."""
    base_grams = product_base_grams(product)
    factor = float(grams) / base_grams if base_grams else 1.0
    scaled = {**product}
    for key in ("kcal", "protein", "carbs", "fat"):
        scaled[key] = round(float(product.get(key, 0)) * factor, 2)
    scaled["portion"] = f"{int(grams)} g"
    scaled["grams"] = float(grams)
    return scaled


def calculate_recipe_ingredients(ingredients):
    products = {product["name"]: product for product in all_products()}
    totals = {"kcal": 0.0, "protein": 0.0, "carbs": 0.0, "fat": 0.0}
    for ingredient in ingredients:
        product = products.get(ingredient.get("name"))
        if not product:
            continue
        factor = float(ingredient.get("grams", 0)) / product_base_grams(product)
        for key in totals:
            totals[key] += float(product.get(key, 0)) * factor
    return totals


def ensure_unique_edit_ids(items, namespace):
    """Give every editable ingredient a stable, unique ID for this draft."""
    used_ids = set()
    for item in items:
        item_id = str(item.get("_edit_id", "")).strip()
        if not item_id or item_id in used_ids:
            item_id = f"{namespace}-{uuid.uuid4().hex[:12]}"
            while item_id in used_ids:
                item_id = f"{namespace}-{uuid.uuid4().hex[:12]}"
            item["_edit_id"] = item_id
        used_ids.add(item_id)

TODAY = date.today()
TODAY_KEY = TODAY.isoformat()

if "daily_logs" not in st.session_state:
    st.session_state.daily_logs = load_daily_logs()
if "water_logs" not in st.session_state:
    st.session_state.water_logs = load_water_logs()
if "goals" not in st.session_state:
    st.session_state.goals = load_goals()
# Remove only the exact meals that the first prototype inserted automatically.
# User-created meals are left untouched.
seed_meals = {
    ("Kaerahelbepuder marjadega", 385),
    ("Kana-riisi kauss", 560),
    ("Lõhe, kartul ja salat", 620),
    ("Kohupiim marjadega", 330),
}
if not st.session_state.get("seed_data_cleaned"):
    changed = False
    for log_key, log_entries in st.session_state.daily_logs.items():
        cleaned_entries = [entry for entry in log_entries if (entry.get("name"), int(entry.get("kcal", 0))) not in seed_meals]
        if len(cleaned_entries) != len(log_entries):
            st.session_state.daily_logs[log_key] = cleaned_entries
            changed = True
    st.session_state.seed_data_cleaned = True
    if changed:
        save_daily_logs()
if "active_date" not in st.session_state:
    st.session_state.active_date = TODAY
if "recipe_builder" not in st.session_state:
    st.session_state.recipe_builder = []
if "inline_create_food" not in st.session_state:
    st.session_state.inline_create_food = ""


def day_key(day=None):
    return (day or st.session_state.active_date).isoformat()


def entries_for(day=None):
    key = day_key(day)
    st.session_state.daily_logs.setdefault(key, [])
    return st.session_state.daily_logs[key]


def totals(day=None):
    return {key: sum(float(item.get(key, 0)) for item in entries_for(day)) for key in ("kcal", "protein", "carbs", "fat")}


def add_entry(item, meal="Vahepala", day=None, entry_type=None):
    entry = {**item, "meal": meal, "time": datetime.now().strftime("%H:%M")}
    if entry_type:
        entry["entry_type"] = entry_type
    entries_for(day).append(entry)
    save_daily_logs()
    st.session_state.highlight_added_food = item["name"]


def remove_entry(index, day=None):
    entries_for(day).pop(index)
    save_daily_logs()


def remove_entry_group(indices, day=None):
    entries = entries_for(day)
    for index in sorted(indices, reverse=True):
        entries.pop(index)
    save_daily_logs()


def entry_grams(entry):
    if entry.get("grams") is not None:
        return float(entry["grams"])
    product = next((product for product in all_products() if product.get("name") == entry.get("name")), None)
    return product_base_grams(product) if product else 0.0


def grouped_log_entries(entries):
    grouped = []
    grouped_by_name = {}
    for index, entry in enumerate(entries):
        # Recipes stay separate; normal foods with the same name are combined.
        if entry.get("meal") == "Retsept" or entry.get("entry_type") == "recipe":
            grouped.append({**entry, "count": 1, "_indices": [index], "_prototype": {**entry}})
            continue
        name_key = entry.get("name", "").strip().lower()
        if name_key not in grouped_by_name:
            grouped_by_name[name_key] = len(grouped)
            grouped.append({**entry, "count": 1, "grams": entry_grams(entry), "_indices": [index], "_prototype": {**entry}})
        else:
            item = grouped[grouped_by_name[name_key]]
            item["count"] += 1
            item["grams"] += entry_grams(entry)
            item["_indices"].append(index)
            for key in ("kcal", "protein", "carbs", "fat"):
                item[key] = float(item.get(key, 0)) + float(entry.get(key, 0))
    return grouped


def streak_count():
    count = 0
    cursor = TODAY
    while day_key(cursor) in st.session_state.daily_logs and st.session_state.daily_logs[day_key(cursor)]:
        count += 1
        cursor = cursor.fromordinal(cursor.toordinal() - 1)
    return count


def css():
    st.markdown(
        """
        <style>
        :root { --ink:#17231d; --muted:#000000; --mint:#dff3e8; --green:#217a52; --cream:#ffffff; --line:#dfe8e1; --surface:#ffffff; --surface-soft:#eef7f1; --input:#ffffff; --shadow:#1c3a2714; }
        .stApp { background:#f7fbf8; color:var(--ink); font-family:'DM Sans',sans-serif; }
        [data-testid="stHeader"] { background:transparent; }
        .block-container { max-width:720px; padding:1.5rem 1rem 5rem; }
        h1,h2,h3 { font-family:'Space Grotesk',sans-serif; letter-spacing:-.04em; color:var(--ink); }
        h1 { font-size:2.15rem; margin-bottom:.2rem; } h2 { font-size:1.45rem; } h3 { font-size:1.05rem; }
        .eyebrow { color:var(--green); text-transform:uppercase; font-size:.7rem; font-weight:700; letter-spacing:.16em; }
        .hero { background:linear-gradient(135deg,#173f2d,#286d4d); color:white; border-radius:26px; padding:1.15rem 1.25rem 1.25rem; margin:.65rem 0 1rem; box-shadow:0 10px 28px #2a765026; }
        .hero-title { font-family:'Space Grotesk'; font-weight:700; font-size:1.85rem; letter-spacing:-.06em; }
        .brand-card { display:flex; align-items:center; gap:.75rem; width:100%; box-sizing:border-box; padding:.7rem 1.1rem .7rem .7rem; margin:.05rem 0 1.25rem; background:linear-gradient(135deg,#e9f8ef,#d7f0e2); border:1px solid #c8e6d3; border-radius:22px; color:#1f704b; font:700 1.3rem 'Space Grotesk',sans-serif; letter-spacing:-.04em; box-shadow:0 10px 24px #287a561c; }
        .brand-mark { display:grid; place-items:center; width:2.45rem; height:2.45rem; border-radius:15px; background:linear-gradient(145deg,#287a56,#165338); color:white; font:700 1.25rem 'Space Grotesk',sans-serif; box-shadow:0 4px 10px #173f2d38; }
        .hero-sub { color:#c4e4d1; margin-top:.3rem; font-size:.88rem; }
        .metric-card { background:white; border:1px solid var(--line); border-radius:20px; padding:1rem; min-height:98px; box-shadow:0 3px 12px #1c3a2710; }
        .metric-card.macro-complete { background:#dff3e8; border-color:#8fd0a8; }
        .metric-card.macro-complete .metric-label, .metric-card.macro-complete .metric-value { color:#217a52; }
        .metric-label { color:var(--muted); font-size:.76rem; font-weight:600; } .metric-value { font:700 1.5rem 'Space Grotesk'; margin-top:.35rem; }
        .macro-value { display:flex; align-items:baseline; gap:.25rem; white-space:nowrap; } .macro-goal { color:var(--muted); font-size:.72em; font-weight:500; }
        .metric-note { color:var(--muted); font-size:.72rem; margin-top:.15rem; }
        .progress { height:9px; background:#e7eee9; border-radius:99px; overflow:hidden; margin-top:.7rem; } .progress > div { height:100%; background:#287a56; border-radius:99px; }
        .food-row { display:flex; justify-content:space-between; align-items:center; padding:.95rem 1rem; background:white; border-bottom:1px solid var(--line); }
        .food-row:first-child { border-radius:18px 18px 0 0; } .food-row:last-child { border-radius:0 0 18px 18px; border-bottom:0; }
        .food-name { font-weight:600; margin-top:.45rem; } .food-meta { color:var(--muted); font-size:.78rem; margin-top:.15rem; } .food-kcal { font-weight:700; white-space:nowrap; }
        .pill { display:inline-block; padding:.3rem .65rem; border-radius:99px; background:#edf5ef; color:#287a56; font-weight:600; font-size:.72rem; }
        div.stButton > button { border-radius:14px; border:1px solid #dce7de; min-height:2.7rem; font-weight:600; }
        div.stButton > button[kind="primary"] { background:#287a56; color:white; border-color:#287a56; }
        div[data-testid="stMetric"] { background:white; border-radius:18px; padding:1rem; border:1px solid #e7ece7; }
        .stTabs [data-baseweb="tab-list"] { gap:1.35rem; border-bottom:1px solid var(--line); } .stTabs [data-baseweb="tab"] { min-height:3.2rem; padding:.15rem 0 .85rem; font-size:1.2rem; font-weight:800 !important; font-family:'DM Sans',sans-serif; } .stTabs [data-baseweb="tab"] * { font-weight:800 !important; }
        .stTabs [aria-selected="true"] { color:var(--green); }
        .section-title { display:flex; align-items:end; justify-content:space-between; margin:1.25rem 0 .65rem; }
        .today-section-title { margin-top:.25rem !important; }
        .section-title h2 { margin:0; } .section-hint { color:var(--muted); font-size:.78rem; }
        .goal-card { background:white; border:1px solid var(--line); border-radius:24px; padding:1rem 1.1rem; display:flex; align-items:center; gap:1rem; box-shadow:0 3px 12px #1c3a2710; }
        .goal-card.goal-complete { background:#dff3e8; border-color:#8fd0a8; }
        .goal-card.goal-complete .goal-ring { background:conic-gradient(#217a52 100%, #bfe5ca 0); }
        .goal-card.goal-complete .goal-ring:after { background:#dff3e8; }
        .goal-ring { width:86px; height:86px; border-radius:50%; display:grid; place-items:center; flex:0 0 auto; background:conic-gradient(#287a56 var(--percent), #e7eee9 0); position:relative; }
        .goal-ring:after { content:''; width:66px; height:66px; border-radius:50%; background:white; position:absolute; }
        .goal-ring span { z-index:1; font:700 1rem 'Space Grotesk'; color:#287a56; }
        .calendar-macro-grid { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:.55rem; margin:0; }
        .today-macro-grid { margin-top:-1.25rem; margin-bottom:1rem; }
        .calendar-page-macro-grid { margin-bottom:1rem; }
        .calendar-summary-card { margin-top:1rem; }
        .calendar-macro-card { min-width:0; padding:.8rem .45rem; text-align:center; background:var(--surface); border:1px solid var(--line); border-radius:18px; }
        .calendar-macro-ring { width:58px; height:58px; margin:.35rem auto .5rem; display:grid; place-items:center; position:relative; }
        .calendar-macro-ring svg { position:absolute; inset:0; width:100%; height:100%; transform:rotate(-90deg); overflow:visible; }
        .calendar-macro-ring .ring-track, .calendar-macro-ring .ring-progress { fill:none; stroke-width:10; }
        .calendar-macro-ring .ring-track { stroke:var(--line); }
        .calendar-macro-ring .ring-progress { stroke:var(--ring-color); stroke-linecap:round; stroke-dasharray:100; stroke-dashoffset:calc(100 - var(--progress)); }
        .calendar-macro-card.macro-complete { background:#e5f4eb; border-color:#b9dfc5; }
        .calendar-macro-card.macro-complete .ring-track { stroke:#bfe5ca; }
        html[data-theme="dark"] .calendar-macro-card.macro-complete { background:#173d2c; border-color:#315b43; }
        html[data-theme="dark"] .calendar-macro-card.macro-complete .ring-track { stroke:#2d6548; }
        .calendar-macro-ring span { z-index:1; color:var(--ring-color); font:700 .72rem 'Space Grotesk'; }
        .calendar-macro-label { color:var(--muted); font-size:.66rem; font-weight:800; text-transform:uppercase; letter-spacing:.04em; }
        .calendar-macro-value { margin-top:.15rem; color:var(--ink); font:700 .8rem 'Space Grotesk'; white-space:nowrap; }
        .water-card { display:grid; grid-template-columns:92px 1fr; gap:1rem; align-items:center; margin:0; padding:1rem; background:var(--surface); border:1px solid var(--line); border-radius:20px; }
        .water-glass { position:relative; width:72px; height:112px; margin:auto; overflow:hidden; border:3px solid #8fc9e8; border-top:0; border-radius:0 0 22px 22px; background:#eef8fd; }
        .water-fill { position:absolute; right:0; bottom:0; left:0; height:var(--water-percent); background:linear-gradient(180deg,#8fd8f4,#43a9d7); }
        .water-glass::before { content:''; position:absolute; z-index:1; top:0; right:0; left:0; height:3px; background:#8fc9e8; }
        .water-copy h3 { margin:0; color:var(--ink); font:700 1.05rem 'Space Grotesk'; }
        .water-amount { margin:.25rem 0 .65rem; color:#2584ad; font:700 1.35rem 'Space Grotesk'; }
        .water-amount span { color:var(--muted); font:500 .78rem 'DM Sans'; }
        [class*="st-key-water-actions"] [data-testid="stHorizontalBlock"] { flex-wrap:wrap !important; gap:.35rem !important; }
        [class*="st-key-water-actions"] { margin-bottom:0 !important; }
        [class*="st-key-water-actions"] button { min-height:2.3rem !important; padding:.35rem .55rem !important; font-size:.75rem !important; }
        [class*="st-key-water-actions"] [data-testid="stNumberInput"] input { min-height:2.3rem !important; font-size:16px !important; }
        @media (max-width:600px) { .water-card { grid-template-columns:76px 1fr; gap:.7rem; padding:.8rem; } .water-glass { width:62px; height:102px; } .water-copy h3 { font-size:.95rem; } .water-amount { font-size:1.15rem; } }
        .goal-copy { flex:1; } .goal-copy .metric-value { margin:0; font-size:1.35rem; }
        .add-card { background:#e5f4eb; border-radius:20px; padding:1rem; margin-top:1rem; }
        .add-card-title { font-weight:700; font-size:1rem; } .add-card-sub { font-size:.8rem; color:#547063; margin:.2rem 0 .8rem; }
        .streak-card { display:flex; align-items:center; gap:.8rem; background:var(--surface); border:1px solid var(--line); color:var(--ink); border-radius:20px; padding:1rem 1.1rem; margin:.8rem 0 0; box-shadow:0 3px 12px #1c3a2709; }
        .streak-card .streak-fire { font-size:1.7rem; line-height:1; }
        .streak-card .streak-label { color:var(--muted); font-size:.65rem; font-weight:800; letter-spacing:.12em; text-transform:uppercase; }
        .streak-card .streak-value { margin-top:.15rem; font:700 1.35rem 'Space Grotesk'; }
        .ingredient-header { display:grid; grid-template-columns:4fr 1.5fr .8fr; gap:.5rem; padding:.35rem .6rem; color:var(--muted); text-transform:uppercase; font-size:.68rem; font-weight:700; letter-spacing:.08em; border-bottom:1px solid var(--line); }
        .recipe-read-row { display:grid; grid-template-columns:minmax(0, 1fr) auto; align-items:center; gap:.75rem; padding:.7rem .6rem; border-bottom:1px solid var(--line); color:var(--ink); }
        .recipe-read-row strong { color:var(--muted); white-space:nowrap; font-weight:600; }
        .metric-label, .metric-note, .food-meta, .section-hint, .table-note, .add-card-sub, .week-day, .builder-weight, .recipe-read-row strong,
        .stCaption, [data-testid="stCaptionContainer"], .stMarkdown span[style*="718078"], .stMarkdown span[style*="78857d"] { color:#000000 !important; }
        input::placeholder, textarea::placeholder { color:#000000 !important; opacity:1 !important; }
        .recipe-edit-row input { border-radius:12px !important; }
        .table-note { color:var(--muted); font-size:.78rem; margin:.2rem 0 .6rem; }
        .recipe-macros { display:flex; flex-wrap:wrap; gap:.4rem; margin:.65rem 0 .8rem; }
        .recipe-macro { background:#f1f7f2; border:1px solid #e1eee3; border-radius:10px; padding:.35rem .55rem; color:#287a56; font-size:.75rem; font-weight:700; }
        .overview-card { background:#fff; border:1px solid var(--line); border-radius:20px; padding:1rem; box-shadow:0 3px 12px #1c3a2710; }
        .protein-table-wrap { overflow:hidden; background:var(--surface); border:1px solid var(--line); border-radius:20px; box-shadow:0 6px 18px #1c3a270c; }
        .protein-table { width:100%; border-collapse:separate; border-spacing:0; font-size:.82rem; }
        .protein-table th { padding:.85rem 1rem; background:#f1f3f5; color:var(--ink); font-size:.66rem; text-align:left; text-transform:uppercase; letter-spacing:.06em; white-space:nowrap; }
        .protein-table th:last-child, .protein-table td:last-child { text-align:right; }
        .protein-table td { padding:.8rem 1rem; border-top:1px solid var(--line); color:var(--ink); }
        .protein-table tbody tr:nth-child(even) td { background:#fafdfb; }
        .protein-table tr:first-child td { font-weight:700; background:#f0faf3; }
        .protein-table tr:first-child td:first-child::before { content:'①'; margin-right:.4rem; color:var(--muted); }
        .protein-table tr:hover td { background:var(--surface-soft); }
        .protein-table .protein-total { color:var(--ink); font:700 .95rem 'Space Grotesk'; }
        .protein-table td:first-child { white-space:nowrap; font-weight:650; }
        html[data-theme="dark"] .protein-table th { background:#27312c; color:var(--ink); }
        html[data-theme="dark"] .protein-table tr:first-child td { background:#1b3326; }
        html[data-theme="dark"] .protein-table tbody tr:nth-child(even) td { background:#18221d; }
        @media (max-width:600px) { .protein-table { font-size:.72rem; } .protein-table th, .protein-table td { padding:.65rem .55rem; } }
        .protein-top-grid { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:.65rem; }
        .protein-top-card { min-width:0; padding:.9rem; background:var(--surface); border:1px solid var(--line); border-radius:18px; box-shadow:0 3px 12px #1c3a2709; }
        .protein-top-label { color:var(--muted); font-size:.62rem; font-weight:800; text-transform:uppercase; letter-spacing:.06em; }
        .protein-top-value { margin:.35rem 0 .15rem; color:var(--ink); font:700 1.35rem 'Space Grotesk'; }
        .protein-top-note { color:var(--muted); font-size:.75rem; }
        .protein-best-card { display:grid; grid-template-columns:1fr 1fr; align-items:center; padding:1.1rem 1.25rem; }
        .protein-best-date, .protein-best-amount { color:var(--ink); font:700 1.25rem 'Space Grotesk'; }
        .protein-best-amount { padding-left:1.25rem; }
        .protein-top-grid.single { grid-template-columns:minmax(0,1fr); }
        @media (max-width:600px) { .protein-top-grid { grid-template-columns:1fr; gap:.5rem; } .protein-top-card { padding:.75rem .85rem; } .protein-top-value { font-size:1.15rem; } .protein-best-card { padding:1rem; } .protein-best-date, .protein-best-amount { font-size:1rem; } .protein-best-amount { padding-left:1rem; } }
        .week-bars { display:flex; align-items:end; justify-content:space-between; gap:.45rem; height:145px; padding:.8rem .35rem .2rem; }
        .week-day { display:flex; flex-direction:column; align-items:center; gap:.35rem; flex:1; height:100%; justify-content:end; color:var(--muted); font-size:.68rem; }
        .week-track { height:105px; width:100%; max-width:28px; background:#edf3ee; border-radius:9px; display:flex; align-items:end; overflow:hidden; }
        .week-fill { width:100%; background:#71b58b; border-radius:9px; min-height:4px; }
        .week-fill.today { background:#287a56; }
        div[data-testid="stRadio"] > div { gap:.45rem; } div[data-testid="stRadio"] label { background:white; border:1px solid var(--line); border-radius:12px; padding:.45rem .65rem; }
        .mobile-footer { position:fixed; z-index:20; bottom:0; left:0; right:0; background:#f7f8f4ed; border-top:1px solid #e6ebe6; padding:.65rem .75rem calc(.65rem + env(safe-area-inset-bottom)); text-align:center; color:#718078; font-size:.72rem; backdrop-filter:blur(12px); }
        [class*="food-actions"] { display:flex; width:100%; background:transparent; border:0; padding:0; box-shadow:none; }
        [class*="food-adjust"] { display:flex; width:max-content; background:#ffffff; border:1px solid #dfe9e1; border-radius:15px; padding:.22rem; box-shadow:0 3px 10px #1c3a2710; }
        [class*="food-remove"] { display:flex; width:max-content; background:#ffffff; border:1px solid #f0d9d9; border-radius:15px; padding:.22rem; box-shadow:0 3px 10px #1c3a2710; }
        [class*="food-adjust"] [data-testid="stHorizontalBlock"], [class*="food-remove"] [data-testid="stHorizontalBlock"] { gap:.2rem !important; }
        [class*="food-adjust"] button, [class*="food-remove"] button { min-width:2.35rem !important; min-height:2.25rem !important; border:0 !important; background:transparent !important; border-radius:11px !important; box-shadow:none !important; font-size:1rem !important; }
        [class*="food-adjust"] { display:inline-flex !important; flex:0 0 auto !important; width:5.6rem !important; max-width:5.6rem !important; overflow:hidden !important; box-sizing:border-box !important; }
        [class*="food-adjust"] [data-testid="stHorizontalBlock"] { display:flex !important; flex:0 0 auto !important; width:5rem !important; max-width:5rem !important; flex-wrap:nowrap !important; justify-content:flex-start !important; gap:0 !important; }
        [class*="food-adjust"] [data-testid="stHorizontalBlock"] > [data-testid="column"] { flex:0 0 2.5rem !important; width:2.5rem !important; min-width:2.5rem !important; padding:0 !important; }
        [class*="food-adjust"] [data-testid="stHorizontalBlock"] > [data-testid="column"]:nth-child(2) { transform:none !important; }
        [class*="food-adjust"] [data-testid="stHorizontalBlock"], [class*="food-adjust"] [data-testid="column"], [class*="food-adjust"] [data-testid="stElementContainer"] { outline:none !important; border:none !important; box-shadow:none !important; }
        [class*="food-adjust"] button { box-sizing:border-box !important; width:2.5rem !important; min-width:2.5rem !important; height:2.8rem !important; min-height:2.8rem !important; padding:0 !important; font-size:1.35rem !important; }
        [class*="food-adjust"] button { background:#eaf6ed !important; }
        [class*="food-adjust"] button:focus, [class*="food-adjust"] button:focus-visible, [class*="food-adjust"] button:active { background:#eaf6ed !important; border-radius:11px !important; outline:none !important; }
        [class*="food-adjust"] button p { display:flex !important; align-items:center !important; justify-content:center !important; width:100% !important; height:100% !important; margin:0 !important; font-size:1.35rem !important; }
        [class*="food-adjust"] button { color:#287a56 !important; }
        [class*="food-remove"] button { color:#b45d5d !important; }
        [class*="food-adjust"] button:hover { background:#eaf6ed !important; color:#173f2d !important; }
        [class*="food-remove"] button:hover { background:#fff0f0 !important; color:#8d3f3f !important; }
        [class*="food-adjust"] button:focus-visible, [class*="food-remove"] button:focus-visible { outline:2px solid #76b58c !important; outline-offset:-2px; }
        [class*="product-actions"] { display:flex; width:100%; }
        [class*="recipe-actions"] { display:block; width:100%; }
        [class*="st-key-edit_recipe_"], [class*="st-key-close_recipe_editor_"], [class*="st-key-delete_recipe_"] { display:inline-block !important; width:auto !important; max-width:100% !important; vertical-align:middle !important; margin-right:.35rem !important; }
        [class*="st-key-edit_recipe_"] button, [class*="st-key-close_recipe_editor_"] button, [class*="st-key-delete_recipe_"] button { width:auto !important; min-width:2.5rem !important; }
        [class*="product-actions"] button, [class*="recipe-actions"] button { min-height:2.25rem !important; border-radius:11px !important; }
        [class*="product-actions"] [data-testid="stHorizontalBlock"], [class*="recipe-actions"] [data-testid="stHorizontalBlock"] { width:100% !important; }
        [class*="st-key-remove_today_"] button, [class*="st-key-remove_one_today_"] button,
        [class*="st-key-delete_product_"] button, [class*="st-key-remove_calendar_"] button,
        [class*="st-key-remove_recipe_row_"] button, [class*="st-key-delete_recipe_"] button,
        [class*="st-key-remove_recipe_ingredient_"] button { font-size:0 !important; color:transparent !important; text-shadow:none !important; }
        [class*="st-key-remove_today_"] button::after, [class*="st-key-delete_product_"] button::after,
        [class*="st-key-remove_calendar_"] button::after, [class*="st-key-remove_recipe_row_"] button::after,
        [class*="st-key-delete_recipe_"] button::after, [class*="st-key-remove_recipe_ingredient_"] button::after { content:"X"; color:#b45d5d; font-size:1rem; }
        [class*="st-key-remove_one_today_"] button::after { content:"-"; color:#287a56; font-size:1rem; }
        [class*="st-key-remove_one_today_"] button::after { content:none !important; }
        [class*="st-key-remove_one_today_"] button p { font-size:0 !important; color:transparent !important; }
        [class*="st-key-remove_one_today_"] button p::after { content:"−"; color:#287a56 !important; font-size:1.35rem !important; }
        [class*="st-key-add_recipe_row_"] button { font-size:0 !important; color:transparent !important; }
        [class*="st-key-add_recipe_row_"] button::after { content:"+ Lisa toode"; position:absolute !important; left:.7rem !important; top:50% !important; transform:translateY(-50%) !important; display:block !important; width:auto !important; color:#287a56; font-size:.82rem; text-align:left !important; }
        [class*="st-key-add_recipe_row_"] { margin-top:.65rem !important; margin-bottom:.55rem !important; padding:.15rem 0 !important; }
        [class*="st-key-add_recipe_row_"] button { min-height:3rem !important; height:3rem !important; padding:.55rem .9rem !important; border:1px solid #d8e7dc !important; border-radius:14px !important; background:var(--surface) !important; box-shadow:0 2px 8px #1c3a270d !important; }
        [class*="food-remove"] button { font-size:0 !important; color:transparent !important; }
        [class*="food-remove"] button::after { content:"X"; color:#b45d5d !important; font-size:1rem !important; }
        [class*="product-actions"] button:not([kind="primary"]), [class*="product-actions"] [data-testid="stBaseButton-secondary"] { font-size:0 !important; color:transparent !important; text-shadow:none !important; }
        [class*="product-actions"] button:not([kind="primary"])::after, [class*="product-actions"] [data-testid="stBaseButton-secondary"]::after { content:"X"; color:#b45d5d !important; font-size:1rem !important; }
        [class*="product-actions"] button:not([kind="primary"]), [class*="product-actions"] [data-testid="stBaseButton-secondary"] { width:2.5rem !important; min-width:2.5rem !important; height:2.5rem !important; min-height:2.5rem !important; padding:0 !important; border-radius:12px !important; }
        [class*="food-remove"] button { width:2.5rem !important; min-width:2.5rem !important; height:2.5rem !important; min-height:2.5rem !important; padding:0 !important; border-radius:12px !important; }
        /* Streamlit places button text inside a nested paragraph. Hide the original
           mojibake icon and draw one stable icon there instead of on the button. */
        [class*="product-actions"] button::after, [class*="food-remove"] button::after,
        [class*="st-key-remove_today_"] button::after, [class*="st-key-delete_product_"] button::after,
        [class*="st-key-remove_calendar_"] button::after, [class*="st-key-remove_recipe_row_"] button::after,
        [class*="st-key-delete_recipe_"] button::after, [class*="st-key-remove_recipe_ingredient_"] button::after { content:none !important; }
        [class*="product-actions"] button:not([kind="primary"]) p, [class*="food-remove"] button p,
        [class*="st-key-remove_today_"] button p, [class*="st-key-delete_product_"] button p,
        [class*="st-key-remove_calendar_"] button p, [class*="st-key-remove_recipe_row_"] button p,
        [class*="st-key-delete_recipe_"] button p, [class*="st-key-remove_recipe_ingredient_"] button p { font-size:0 !important; color:transparent !important; }
        [class*="product-actions"] button:not([kind="primary"]) p::after, [class*="food-remove"] button p::after,
        [class*="st-key-remove_today_"] button p::after, [class*="st-key-delete_product_"] button p::after,
        [class*="st-key-remove_calendar_"] button p::after, [class*="st-key-remove_recipe_row_"] button p::after,
        [class*="st-key-delete_recipe_"] button p::after, [class*="st-key-remove_recipe_ingredient_"] button p::after { content:"X"; color:#b45d5d !important; font-size:1rem !important; }
        [class*="st-key-remove_recipe_row_"] button p { font-size:.72rem !important; color:#b45d5d !important; white-space:nowrap !important; }
        [class*="st-key-remove_recipe_row_"] button p::after { content:none !important; }
        [class*="st-key-recipe-edit-row-"] [data-testid="stHorizontalBlock"] > [data-testid="column"]:nth-child(3) { flex:0 0 5.5rem !important; width:5.5rem !important; min-width:5.5rem !important; }
        [class*="st-key-recipe-builder-row-"] [data-testid="stHorizontalBlock"] { flex-wrap:nowrap !important; align-items:center !important; gap:.35rem !important; }
        [class*="st-key-recipe-builder-row-"] [data-testid="stHorizontalBlock"] > [data-testid="column"]:nth-child(1) { flex:1 1 auto !important; width:auto !important; min-width:0 !important; }
        [class*="st-key-recipe-builder-row-"] [data-testid="stHorizontalBlock"] > [data-testid="column"]:nth-child(2) { flex:0 0 7rem !important; width:7rem !important; min-width:7rem !important; }
        [class*="st-key-recipe-builder-row-"] [data-testid="stHorizontalBlock"] > [data-testid="column"]:nth-child(3) { flex:0 0 5.5rem !important; width:5.5rem !important; min-width:5.5rem !important; }
        [class*="st-key-recipe-builder-row-"] [class*="st-key-remove_recipe_ingredient_"] button p { font-size:.72rem !important; color:#b45d5d !important; white-space:nowrap !important; }
        [class*="st-key-recipe-builder-row-"] [class*="st-key-remove_recipe_ingredient_"] button p::after { content:none !important; }
        [class*="st-key-recipe-builder-row-"] .builder-product { flex:1 1 auto; min-width:0; overflow-wrap:anywhere; background:#f1f3f7; border-radius:12px; padding:.85rem .7rem; }
        [class*="st-key-recipe-builder-row-"] .builder-weight { flex:0 1 7rem; min-width:0; white-space:nowrap; color:var(--ink); font-size:.82rem; background:#f1f3f7; border-radius:12px; padding:.85rem .7rem; }
        [class*="st-key-recipe-builder-row-"] [data-testid="stNumberInput"] > div { min-height:46px !important; height:46px !important; border-radius:14px !important; background:#f1f3f7 !important; }
        [class*="st-key-recipe-builder-row-"] [data-testid="stNumberInput"] input { height:46px !important; min-height:46px !important; border:0 !important; border-radius:14px !important; background:#f1f3f7 !important; color:var(--ink) !important; font-size:16px !important; }
        [class*="st-key-recipe-builder-row-"] [data-testid="stNumberInput"] button { display:none !important; }
        [class*="st-key-recipe-builder-row-"] [data-testid="stNumberInput"] input[type="number"] { -moz-appearance:textfield !important; appearance:textfield !important; }
        [class*="st-key-recipe-builder-row-"] [data-testid="stNumberInput"] input[type="number"]::-webkit-inner-spin-button,
        [class*="st-key-recipe-builder-row-"] [data-testid="stNumberInput"] input[type="number"]::-webkit-outer-spin-button { -webkit-appearance:none !important; appearance:none !important; margin:0 !important; }
        [class*="st-key-recipe-builder-row-"] [data-testid="stElementContainer"] { min-width:0 !important; }
        [class*="st-key-recipe-builder-row-"] [data-testid="stElementContainer"]:has(.builder-product) { flex:1 1 auto !important; min-width:0 !important; }
        [class*="st-key-recipe-builder-row-"] [data-testid="stElementContainer"]:has(.builder-weight) { flex:0 1 7rem !important; min-width:0 !important; }
        [class*="st-key-recipe-builder-row-"] [data-testid="stElementContainer"]:has(button) { flex:0 0 2.5rem !important; width:2.5rem !important; min-width:2.5rem !important; }
        [class*="st-key-recipe-edit-row-"] [class*="st-key-remove_recipe_row_"] button { width:2.5rem !important; min-width:2.5rem !important; padding:0 !important; }
        [class*="st-key-recipe-edit-row-"] [class*="st-key-remove_recipe_row_"] button p { font-size:0 !important; }
        [class*="st-key-recipe-edit-row-"] [class*="st-key-remove_recipe_row_"] button p::after { content:"×" !important; color:#b45d5d !important; font-size:1.1rem !important; }
        [class*="st-key-recipe-edit-row-"] [data-testid="stElementContainer"] { min-width:0 !important; }
        [class*="st-key-recipe-edit-row-"] [data-testid="stElementContainer"]:has([data-testid="stSelectbox"]) { flex:1 1 auto !important; min-width:0 !important; }
        [class*="st-key-recipe-edit-row-"] [data-testid="stElementContainer"]:has([data-testid="stNumberInput"]) { flex:0 1 7rem !important; min-width:0 !important; }
        [class*="st-key-recipe-edit-row-"] [class*="st-key-remove_recipe_row_"] { flex:0 0 2.5rem !important; width:2.5rem !important; min-width:2.5rem !important; }
        [class*="product-actions"] button:not([kind="primary"]) p, [class*="food-remove"] button p,
        [class*="st-key-remove_today_"] button p, [class*="st-key-delete_product_"] button p,
        [class*="st-key-remove_calendar_"] button p, [class*="st-key-remove_recipe_row_"] button p,
        [class*="st-key-delete_recipe_"] button p, [class*="st-key-remove_recipe_ingredient_"] button p { display:flex !important; align-items:center !important; justify-content:center !important; width:100% !important; height:100% !important; margin:0 !important; }
        html[data-theme="dark"] {
            :root { --ink:#edf5ef; --muted:#aabbb1; --mint:#173d2c; --green:#72d09b; --cream:#111714; --line:#2b3b33; --surface:#1b2520; --surface-soft:#20382a; --input:#202b25; --shadow:#00000035; }
            .stApp, [data-testid="stAppViewContainer"], [data-testid="stMainBlockContainer"] { background:var(--cream); color:var(--ink); }
            [data-testid="stHeader"] { background:transparent; }
            h1, h2, h3, p, label, .stMarkdown, [data-testid="stWidgetLabel"] { color:var(--ink); }
            .metric-card, .food-row, .goal-card, .overview-card, div[data-testid="stMetric"], div[data-testid="stExpander"],
            [data-testid="stRadio"] label, [class*="food-adjust"], [class*="food-remove"] { background:var(--surface) !important; color:var(--ink); border-color:var(--line) !important; }
            .metric-card.macro-complete { background:#173d2c !important; border-color:#3d815a !important; }
            .metric-card.macro-complete .metric-label, .metric-card.macro-complete .metric-value { color:#72d09b !important; }
            .food-row { border-bottom-color:var(--line); }
            .pill { background:#214b35; color:#9ae6b7; }
            .add-card { background:#173d2c; }
            .add-card-sub, .table-note, .section-hint, .metric-label, .metric-note, .food-meta, .week-day { color:var(--muted); }
            .metric-label, .metric-note, .food-meta, .section-hint, .table-note, .add-card-sub, .week-day, .builder-weight, .recipe-read-row strong,
            .stCaption, [data-testid="stCaptionContainer"], .stMarkdown span[style*="718078"], .stMarkdown span[style*="78857d"] { color:var(--muted) !important; }
            .streak-card { background:var(--surface); border-color:var(--line); color:var(--ink); }
            .recipe-macro { background:#1d3a29; border-color:#2c5a3e; color:#8ee0ac; }
            .builder-product, .builder-weight { background:var(--input) !important; color:var(--ink) !important; }
            .brand-card { background:linear-gradient(135deg,#1d3d2c,#173025); border-color:#315b43; color:#9ae6b7; box-shadow:0 6px 18px #00000035; }
            .brand-mark { background:linear-gradient(145deg,#72d09b,#287a56); color:#102219; }
            .progress, .week-track { background:#2a3931; }
            .goal-ring { background:conic-gradient(#72d09b var(--percent), #2a3931 0); }
            .goal-ring:after { background:var(--surface); }
            .goal-card.goal-complete { background:#173d2c !important; border-color:#3d815a !important; }
            .goal-card.goal-complete .goal-ring:after { background:#173d2c; }
            .goal-ring span { color:#72d09b; }
            .mobile-footer { background:#111714e8; border-top-color:var(--line); color:var(--muted); }
            div.stButton > button, [data-testid="stDownloadButton"] button { background:var(--surface); color:var(--ink); border-color:var(--line); }
            div.stButton > button[kind="primary"] { background:#287a56; color:white; border-color:#287a56; }
            [class*="product-actions"] button:not([kind="primary"]), [class*="product-actions"] [data-testid="stBaseButton-secondary"] { background:#202b25 !important; border:1px solid #405047 !important; color:transparent !important; box-shadow:none !important; }
            [class*="product-actions"] button:not([kind="primary"]):hover, [class*="product-actions"] [data-testid="stBaseButton-secondary"]:hover { background:#293b31 !important; border-color:#72d09b !important; }
            [class*="food-adjust"] button { color:#72d09b !important; }
            [class*="food-remove"] button { color:#f08b8b !important; }
            [class*="food-adjust"] button:hover { background:#214b35 !important; color:#b7f3ca !important; }
            [class*="food-remove"] button:hover { background:#4a2929 !important; color:#ffb1b1 !important; }
            input, textarea, [data-baseweb="select"] > div, [data-testid="stNumberInput"] button { background:var(--input) !important; color:var(--ink) !important; border-color:var(--line) !important; }
            input::placeholder, textarea::placeholder { color:#aabbb1 !important; opacity:1 !important; }
            [data-baseweb="popover"] [role="listbox"], [data-baseweb="menu"] { background:var(--surface) !important; color:var(--ink) !important; }
            [data-baseweb="popover"] [role="option"]:hover, [data-baseweb="menu"] [role="option"]:hover { background:#294333 !important; }
            .stTabs [data-baseweb="tab-list"] { border-bottom-color:var(--line); }
            .stTabs [data-baseweb="tab"] { color:var(--muted); }
            .stTabs [aria-selected="true"] { color:#72d09b; }
            [data-testid="stAlert"] { background:#1d3328; color:var(--ink); }
        }
        @media (max-width:600px) {
            .block-container { width:100%; max-width:100%; padding:.8rem .7rem 5.3rem; }
            h1 { font-size:1.65rem; } h2 { font-size:1.25rem; } h3 { font-size:1rem; }
            .eyebrow { font-size:.6rem; letter-spacing:.13em; }
            .hero { border-radius:20px; padding:1rem; margin:.45rem 0 .8rem; }
            .hero-title { font-size:1.48rem; line-height:1.1; } .hero-sub { font-size:.78rem; }
            .stTabs [data-baseweb="tab-list"] { overflow-x:auto; flex-wrap:nowrap; gap:1rem; scrollbar-width:none; padding-bottom:.1rem; }
            .stTabs [data-baseweb="tab-list"]::-webkit-scrollbar { display:none; }
            .stTabs [data-baseweb="tab"] { min-width:max-content; font-size:1.1rem !important; font-weight:800 !important; padding-bottom:.65rem; }
            [data-testid="stHorizontalBlock"] { gap:clamp(.15rem, 1.6vw, .45rem) !important; flex-wrap:wrap !important; max-width:100% !important; }
            [data-testid="stHorizontalBlock"] > [data-testid="column"] { min-width:0 !important; max-width:100% !important; flex:1 1 100% !important; width:100% !important; }
            [class*="st-key-recipe-read-row-"] [data-testid="stHorizontalBlock"],
            [class*="st-key-recipe-edit-row-"] [data-testid="stHorizontalBlock"] { flex-wrap:nowrap !important; align-items:center !important; gap:.35rem !important; }
            [class*="st-key-recipe-read-row-"] [data-testid="stHorizontalBlock"] > [data-testid="column"]:nth-child(1),
            [class*="st-key-recipe-edit-row-"] [data-testid="stHorizontalBlock"] > [data-testid="column"]:nth-child(1) { flex:1 1 auto !important; width:auto !important; min-width:0 !important; }
            [class*="st-key-recipe-read-row-"] [data-testid="stHorizontalBlock"] > [data-testid="column"]:nth-child(2),
            [class*="st-key-recipe-edit-row-"] [data-testid="stHorizontalBlock"] > [data-testid="column"]:nth-child(2) { flex:0 0 4.5rem !important; width:4.5rem !important; min-width:4.5rem !important; }
            [class*="st-key-recipe-edit-row-"] [data-testid="stHorizontalBlock"] > [data-testid="column"]:nth-child(3) { flex:0 0 5.5rem !important; width:5.5rem !important; min-width:5.5rem !important; }
            [class*="st-key-recipe-edit-row-"] [data-testid="stHorizontalBlock"] > [data-testid="column"]:nth-child(3) { flex:0 0 2.2rem !important; width:2.2rem !important; min-width:2.2rem !important; }
            [class*="st-key-recipe-edit-row-"] [data-testid="stHorizontalBlock"] { width:100% !important; max-width:100% !important; overflow:hidden !important; gap:.2rem !important; }
            [class*="st-key-recipe-edit-row-"] [data-testid="stElementContainer"]:has([data-testid="stSelectbox"]) { flex:1 1 0% !important; min-width:0 !important; overflow:hidden !important; }
            [class*="st-key-recipe-edit-row-"] [data-testid="stElementContainer"]:has([data-testid="stNumberInput"]) { flex:0 1 5rem !important; width:5rem !important; min-width:5rem !important; }
            [class*="st-key-recipe-edit-row-"] [class*="st-key-remove_recipe_row_"] { flex:0 0 2.3rem !important; width:2.3rem !important; min-width:2.3rem !important; }
            [class*="st-key-recipe-builder-row-"] [data-testid="stHorizontalBlock"] { flex-wrap:nowrap !important; }
            [class*="st-key-recipe-builder-row-"] { width:100% !important; max-width:100% !important; overflow:hidden !important; }
            [class*="st-key-recipe-builder-row-"] [data-testid="stHorizontalBlock"] { width:100% !important; max-width:100% !important; flex-wrap:nowrap !important; gap:.2rem !important; }
            [class*="st-key-recipe-builder-row-"] [data-testid="stHorizontalBlock"] > [data-testid="column"]:nth-child(1) { flex:1 1 auto !important; width:auto !important; min-width:0 !important; overflow:hidden !important; }
            [class*="st-key-recipe-builder-row-"] [data-testid="stHorizontalBlock"] > [data-testid="column"]:nth-child(2) { flex:0 0 5rem !important; width:5rem !important; min-width:5rem !important; }
            [class*="st-key-recipe-builder-row-"] [data-testid="stHorizontalBlock"] > [data-testid="column"]:nth-child(3) { flex:0 0 2.2rem !important; width:2.2rem !important; min-width:2.2rem !important; }
            [class*="st-key-recipe-builder-row-"] [data-testid="stHorizontalBlock"] > [data-testid="column"]:nth-child(2) { flex:0 0 6.5rem !important; width:6.5rem !important; min-width:6.5rem !important; }
            [class*="st-key-recipe-builder-row-"] [data-testid="stHorizontalBlock"] > [data-testid="column"]:nth-child(3) { flex:0 0 2.5rem !important; width:2.5rem !important; min-width:2.5rem !important; }
            [class*="st-key-recipe-builder-row-"] [data-testid="column"] [data-testid="stMarkdownContainer"] { overflow-wrap:anywhere !important; word-break:break-word !important; white-space:normal !important; }
            [class*="st-key-recipe-builder-row-"] [class*="st-key-remove_recipe_ingredient_"] button { width:2.5rem !important; min-width:2.5rem !important; padding:0 !important; }
            [class*="st-key-recipe-builder-row-"] [class*="st-key-remove_recipe_ingredient_"] button p { font-size:0 !important; }
            [class*="st-key-recipe-builder-row-"] [class*="st-key-remove_recipe_ingredient_"] button p::after { content:"×" !important; color:#b45d5d !important; font-size:1.1rem !important; }
            [class*="st-key-recipe-builder-row-"] [data-testid="stHorizontalBlock"] { overflow:hidden !important; box-sizing:border-box !important; }
            [class*="st-key-recipe-builder-row-"] [data-testid="stHorizontalBlock"] > [data-testid="column"] { box-sizing:border-box !important; max-width:100% !important; min-width:0 !important; padding:0 !important; }
            [class*="st-key-recipe-builder-row-"] [data-testid="stHorizontalBlock"] > [data-testid="column"]:nth-child(1) { flex:1 1 0% !important; width:auto !important; }
            [class*="st-key-recipe-builder-row-"] [data-testid="stHorizontalBlock"] > [data-testid="column"]:nth-child(2) { flex:0 1 clamp(4rem, 24vw, 6rem) !important; width:clamp(4rem, 24vw, 6rem) !important; min-width:4rem !important; }
            [class*="st-key-recipe-builder-row-"] [data-testid="stHorizontalBlock"] > [data-testid="column"]:nth-child(3) { flex:0 0 2.5rem !important; width:2.5rem !important; min-width:2.5rem !important; }
            [class*="st-key-recipe-builder-row-"] [data-testid="stMarkdownContainer"] { font-size:.78rem !important; line-height:1.2 !important; overflow-wrap:anywhere !important; }
            [class*="st-key-recipe-builder-row-"] .builder-product, [class*="st-key-recipe-builder-row-"] .builder-weight { padding:.75rem .65rem !important; }
            [class*="st-key-recipe-builder-row-"] .builder-weight { flex:0 1 clamp(4rem, 24vw, 5rem) !important; font-size:.74rem !important; white-space:normal !important; overflow-wrap:anywhere !important; }
            [class*="st-key-recipe-builder-row-"] [data-testid="stElementContainer"]:has(.builder-weight) { flex:0 1 clamp(4rem, 24vw, 5rem) !important; }
            [class*="st-key-recipe-builder-row-"] [data-testid="stElementContainer"]:has(button) { flex:0 0 2.3rem !important; width:2.3rem !important; min-width:2.3rem !important; }
            [class*="st-key-recipe-edit-row-"] [data-testid="stHorizontalBlock"] [data-testid="stButton"] button { width:2.5rem !important; min-width:2.5rem !important; padding:0 !important; }
            [data-testid="stAppViewContainer"], [data-testid="stMainBlockContainer"] { max-width:100% !important; overflow-x:hidden !important; }
            [class*="st-key-food_actions_"] [data-testid="stHorizontalBlock"] { flex-wrap:nowrap !important; justify-content:flex-start !important; gap:clamp(.2rem, 2vw, .7rem) !important; }
            [class*="st-key-food_actions_"] [data-testid="stHorizontalBlock"] > [data-testid="column"] { flex:0 1 clamp(2.4rem, 13vw, 3.4rem) !important; width:clamp(2.4rem, 13vw, 3.4rem) !important; min-width:0 !important; padding:0 !important; }
            [class*="st-key-food_actions_"] button { width:100% !important; min-width:0 !important; padding:.35rem .2rem !important; font-size:clamp(.78rem, 3.5vw, 1rem) !important; }
            [class*="st-key-macro-cards"] { width:100% !important; max-width:100% !important; overflow:hidden !important; }
        [class*="st-key-macro-cards"] { display:none !important; }
            [class*="st-key-macro-cards"] [data-testid="stHorizontalBlock"] { flex-wrap:nowrap !important; gap:.35rem !important; width:100% !important; max-width:100% !important; }
            [class*="st-key-macro-cards"] [data-testid="stHorizontalBlock"] > [data-testid="column"] { flex:1 1 0% !important; width:0 !important; min-width:0 !important; padding:0 !important; overflow:hidden !important; }
            [class*="st-key-macro-cards"] .calendar-macro-card { width:100% !important; min-height:0 !important; padding:.8rem .45rem !important; }
            [class*="food-actions"] [data-testid="stHorizontalBlock"] { flex-wrap:nowrap !important; justify-content:flex-start !important; gap:clamp(.2rem, 2vw, .7rem) !important; }
            [class*="food-actions"] [data-testid="stHorizontalBlock"] > [data-testid="column"] { flex:0 0 clamp(2.4rem, 13vw, 3.4rem) !important; width:clamp(2.4rem, 13vw, 3.4rem) !important; min-width:0 !important; padding:0 !important; }
            [class*="food-actions"] button { width:100% !important; min-width:0 !important; padding:.35rem .2rem !important; font-size:clamp(.78rem, 3.5vw, 1rem) !important; }
            [class*="food-adjust"] { display:inline-flex !important; flex:0 0 auto !important; width:5.6rem !important; max-width:5.6rem !important; padding:.3rem !important; border-radius:18px !important; overflow:hidden !important; box-sizing:border-box !important; }
            [class*="food-adjust"] [data-testid="stHorizontalBlock"] { display:flex !important; flex:0 0 auto !important; width:5rem !important; max-width:5rem !important; flex-wrap:nowrap !important; justify-content:flex-start !important; gap:0 !important; }
            [class*="food-adjust"] [data-testid="stHorizontalBlock"] > [data-testid="column"] { flex:0 0 2.5rem !important; width:2.5rem !important; min-width:2.5rem !important; padding:0 !important; }
            [class*="food-adjust"] [data-testid="stHorizontalBlock"] > [data-testid="column"]:nth-child(2) { transform:none !important; }
            [class*="food-adjust"] button { box-sizing:border-box !important; width:2.5rem !important; min-width:2.5rem !important; height:2.8rem !important; min-height:2.8rem !important; padding:0 !important; font-size:1.35rem !important; background:#214b35 !important; }
            [class*="food-adjust"] button p { display:flex !important; align-items:center !important; justify-content:center !important; width:100% !important; height:100% !important; margin:0 !important; font-size:1.35rem !important; }
        [class*="food-adjust"] [data-testid="stHorizontalBlock"] { position:relative !important; height:2.8rem !important; }
        [class*="food-adjust"] [data-testid="stHorizontalBlock"] > [data-testid="column"] { position:absolute !important; top:0 !important; }
        [class*="food-adjust"] [data-testid="stHorizontalBlock"] > [data-testid="column"]:nth-child(1) { left:0 !important; }
        [class*="food-adjust"] [data-testid="stHorizontalBlock"] > [data-testid="column"]:nth-child(2) { left:1.5rem !important; transform:none !important; }
            .goal-card { border-radius:20px; padding:.8rem; gap:.7rem; }
            .goal-ring { width:72px; height:72px; } .goal-ring:after { width:55px; height:55px; }
            .goal-copy .metric-value { font-size:1.2rem; } .metric-note { font-size:.68rem; }
            .metric-card { min-height:82px; padding:.75rem .65rem; border-radius:16px; }
            .metric-value { font-size:1.15rem; }
            .food-row { padding:.78rem .7rem; }
            .food-name { font-size:.9rem; } .food-meta { font-size:.68rem; }
            .food-kcal { font-size:.82rem; }
            .add-card { margin-top:.8rem; padding:.85rem; border-radius:17px; }
            .streak-card { padding:.8rem .85rem; } .streak-card .streak-value { font-size:1.15rem; }
            .ingredient-header { grid-template-columns:3fr 1.3fr .5fr; font-size:.6rem; padding:.3rem .25rem; }
            .ingredient-header { grid-template-columns:minmax(0, 1fr) 6.5rem 2.5rem; gap:.35rem; }
            [class*="st-key-recipe-edit-row-"] [data-testid="stHorizontalBlock"] { width:100% !important; max-width:100% !important; display:flex !important; flex-wrap:nowrap !important; gap:.35rem !important; overflow:hidden !important; }
            [class*="st-key-recipe-edit-row-"] [data-testid="stElementContainer"]:has([data-testid="stSelectbox"]) { flex:1 1 0% !important; width:auto !important; min-width:0 !important; overflow:hidden !important; }
            [class*="st-key-recipe-edit-row-"] [data-testid="stElementContainer"]:has([data-testid="stNumberInput"]) { flex:0 0 6.5rem !important; width:6.5rem !important; min-width:6.5rem !important; }
            [class*="st-key-recipe-edit-row-"] [class*="st-key-remove_recipe_row_"] { flex:0 0 2.5rem !important; width:2.5rem !important; min-width:2.5rem !important; }
            [class*="st-key-recipe-edit-row-"] [data-testid="stSelectbox"] [data-baseweb="select"] > div,
            [class*="st-key-recipe-edit-row-"] [data-testid="stNumberInput"] input { min-height:50px !important; border-radius:12px !important; }
            .recipe-read-row { grid-template-columns:minmax(0, 1fr) 4.5rem; gap:.35rem; padding:.65rem .25rem; font-size:.88rem; }
            .recipe-read-row strong { text-align:right; font-size:.82rem; }
            .food-row { min-height:64px; }
            .food-row + div { min-width:116px !important; }
            .food-row + div button { min-width:32px; padding-left:.15rem; padding-right:.15rem; }
            [data-testid="stTextInput"] input, [data-testid="stNumberInput"] input, [data-testid="stTextArea"] textarea, [data-testid="stSelectbox"] div[data-baseweb="select"] { min-height:46px; font-size:16px; }
            div.stButton > button { min-height:46px; border-radius:13px; padding:.55rem .65rem; font-size:.82rem; }
            div[data-testid="stRadio"] > div { flex-wrap:wrap; }
            div[data-testid="stRadio"] label { font-size:.78rem; padding:.55rem .6rem; }
            [data-testid="stFileUploader"] section { padding:.75rem; }
            .stCaption, [data-testid="stCaptionContainer"] { font-size:.72rem; }
            [class*="product-actions"] button:not([kind="primary"]) p::after,
            [class*="food-remove"] button p::after,
            [class*="st-key-remove_today_"] button p::after,
            [class*="st-key-delete_product_"] button p::after,
            [class*="st-key-remove_calendar_"] button p::after,
            [class*="st-key-remove_recipe_row_"] button p::after,
            [class*="st-key-delete_recipe_"] button p::after,
            [class*="st-key-remove_recipe_ingredient_"] button p::after {
                display:inline-block !important;
                font-family:Arial, sans-serif !important;
                font-size:20px !important;
                font-weight:400 !important;
                line-height:1 !important;
                -webkit-text-size-adjust:100% !important;
                text-size-adjust:100% !important;
                transform:none !important;
            }
            [class*="product-actions"] button:not([kind="primary"]), [class*="product-actions"] [data-testid="stBaseButton-secondary"] { width:2.5rem !important; min-width:2.5rem !important; height:2.5rem !important; min-height:2.5rem !important; padding:0 !important; }
        }
        /* Final, simple layout for one-by-one quantity controls. */
        [class*="food-adjust"] { display:flex !important; position:static !important; width:5rem !important; max-width:5rem !important; height:2.8rem !important; padding:0 !important; overflow:visible !important; box-sizing:border-box !important; background:transparent !important; border:0 !important; box-shadow:none !important; }
        [class*="food-adjust"] [data-testid="stHorizontalBlock"] { display:flex !important; position:static !important; width:5rem !important; max-width:5rem !important; height:2.8rem !important; flex-wrap:nowrap !important; gap:0 !important; }
        [class*="food-adjust"] [data-testid="stHorizontalBlock"] > [data-testid="column"] { position:static !important; flex:0 0 2.5rem !important; width:2.5rem !important; min-width:2.5rem !important; height:2.8rem !important; padding:0 !important; transform:none !important; }
        [class*="food-adjust"] button { display:flex !important; align-items:center !important; justify-content:center !important; box-sizing:border-box !important; width:2.5rem !important; min-width:2.5rem !important; height:2.8rem !important; min-height:2.8rem !important; margin:0 !important; padding:0 !important; border:0 !important; border-radius:11px !important; background:transparent !important; color:#287a56 !important; outline:none !important; }
        [class*="food-adjust"] button p { display:block !important; width:auto !important; height:auto !important; margin:0 !important; font-size:1.35rem !important; line-height:1 !important; }
        [class*="food-adjust"] button p { color:#287a56 !important; font-family:inherit !important; font-weight:600 !important; text-align:center !important; }
        [class*="food-adjust"] button p::after { content:none !important; }
        [class*="food-adjust"] button:focus, [class*="food-adjust"] button:focus-visible, [class*="food-adjust"] button:active { outline:none !important; box-shadow:none !important; background:#eaf6ed !important; }
        [class*="st-key-meal-categories-"] [data-testid="stHorizontalBlock"] { flex-wrap:nowrap !important; gap:.35rem !important; width:100% !important; }
        [class*="st-key-meal-categories-"] [data-testid="stHorizontalBlock"] > [data-testid="column"] { flex:1 1 0% !important; width:0 !important; min-width:0 !important; padding:0 !important; }
        [class*="st-key-meal-categories-"] button { width:100% !important; min-width:0 !important; min-height:2.35rem !important; padding:.35rem .2rem !important; border-radius:11px !important; font-size:.72rem !important; }
        [class*="st-key-meal-categories-"] button[kind="primary"] { background:#e5f4eb !important; color:#287a56 !important; border-color:#b9dfc5 !important; }
        [class*="st-key-meal-boxes"] [data-testid="stHorizontalBlock"] { flex-wrap:nowrap !important; gap:.45rem !important; width:100% !important; }
        [class*="st-key-meal-boxes"] [data-testid="stHorizontalBlock"] > [data-testid="column"] { flex:1 1 0% !important; width:0 !important; min-width:0 !important; padding:0 !important; }
        .meal-box { min-height:96px; padding:.65rem; background:#f4f8f5; border:1px solid #dfe8e1; border-radius:15px; }
        .meal-box-title { display:flex; align-items:center; justify-content:space-between; gap:.35rem; margin-bottom:.6rem; padding-bottom:.5rem; border-bottom:2px solid #d9eee0; color:#17633f; font-size:.82rem; font-weight:800; letter-spacing:-.02em; }
        .meal-box-title span:first-child::before { content:' '; display:inline-block; width:.5rem; height:.5rem; margin-right:.35rem; border-radius:50%; background:#72b98d; vertical-align:middle; }
        .meal-box-title span:last-child { min-width:1.35rem; padding:.12rem .35rem; border-radius:99px; background:#e5f4eb; color:#287a56; font-size:.65rem; text-align:center; font-weight:700; }
        .meal-box-item { margin:.35rem 0; padding:.55rem .6rem; background:#fff; border:1px solid #e4eee7; border-radius:11px; color:#17231d; font-size:.72rem; box-shadow:0 2px 7px #1c3a2709; }
        .meal-box-item-top { display:flex; justify-content:space-between; align-items:flex-start; gap:.35rem; }
        .meal-box-item-top span { min-width:0; overflow-wrap:anywhere; font-weight:650; }
        .meal-box-item-top strong { flex:0 0 auto; white-space:nowrap; color:#287a56; font-size:.68rem; font-weight:800; }
        .meal-box-macros { display:flex; flex-wrap:wrap; gap:.25rem .4rem; margin-top:.35rem; color:#000 !important; font-size:.6rem; line-height:1.2; }
        .meal-box-macros span { white-space:nowrap; }
        .meal-box-empty { padding:.65rem .1rem; color:#8aa094; font-size:.68rem; line-height:1.25; text-align:center; }
        [class*="st-key-meal-box-"] { min-height:96px !important; padding:.75rem !important; background:linear-gradient(180deg,#f4fbf6,#eef7f1) !important; border:1px solid #d5e9da !important; border-radius:18px !important; box-shadow:0 5px 16px #1c3a270c !important; }
        [class*="st-key-meal-box-"] [data-testid="stSelectbox"] { margin-top:.35rem !important; }
        [class*="st-key-meal-box-"] .meal-box-item { margin:.25rem 0 .55rem !important; padding:.45rem 0 .7rem !important; background:transparent !important; border:0 !important; border-bottom:1px solid #d5e9da !important; border-radius:0 !important; box-shadow:none !important; }
        [class*="st-key-meal-box-"] [data-baseweb="select"] > div { min-height:2rem !important; border-radius:9px !important; font-size:.7rem !important; background:transparent !important; border:1px solid #d5e9da !important; box-shadow:none !important; }
        [class*="st-key-meal-box-actions-"] { min-height:0 !important; padding:0 !important; background:transparent !important; border:0 !important; border-radius:0 !important; box-shadow:none !important; }
        [class*="st-key-meal-box-actions-"] button { background:transparent !important; border:1px solid #c8dfcf !important; box-shadow:none !important; }
        [class*="st-key-meal-controls-"] [data-testid="stHorizontalBlock"] { flex-wrap:nowrap !important; align-items:center !important; gap:.45rem !important; width:100% !important; min-height:2.6rem !important; }
        [class*="st-key-meal-controls-"] [data-testid="stHorizontalBlock"] > [data-testid="column"] { align-self:center !important; }
        [class*="st-key-meal-controls-"] [data-testid="stSelectbox"] { margin-top:0 !important; padding-top:0 !important; align-self:center !important; }
        [class*="st-key-meal-box-actions-"] [data-testid="stHorizontalBlock"] { align-items:center !important; height:2.6rem !important; }
        [class*="st-key-meal-controls-"] [data-testid="stHorizontalBlock"] > [data-testid="column"]:first-child { flex:0 0 7rem !important; width:7rem !important; min-width:7rem !important; }
        [class*="st-key-meal-controls-"] [data-testid="stHorizontalBlock"] > [data-testid="column"]:last-child { flex:1 1 auto !important; width:auto !important; min-width:0 !important; }
        [class*="st-key-meal-controls-"] [data-testid="stSelectbox"] { width:100% !important; }
        [class*="st-key-meal-controls-"] [data-baseweb="select"] > div { min-height:2.6rem !important; background:#f1f2f7 !important; border:0 !important; border-radius:10px !important; box-shadow:none !important; }
        [class*="st-key-calendar-meal-box-"] { min-height:96px !important; padding:.75rem !important; background:linear-gradient(180deg,#f4fbf6,#eef7f1) !important; border:1px solid #d5e9da !important; border-radius:18px !important; box-shadow:0 5px 16px #1c3a270c !important; }
        [class*="st-key-calendar-meal-box-"] .meal-box-item { margin:.25rem 0 .55rem !important; padding:.45rem 0 .7rem !important; background:transparent !important; border:0 !important; border-bottom:1px solid #d5e9da !important; border-radius:0 !important; box-shadow:none !important; }
        [class*="st-key-calendar-meal-boxes"] [data-testid="stHorizontalBlock"] { flex-wrap:nowrap !important; gap:.45rem !important; width:100% !important; }
        [class*="st-key-calendar-meal-boxes"] [data-testid="stHorizontalBlock"] > [data-testid="column"] { flex:1 1 0% !important; width:0 !important; min-width:0 !important; padding:0 !important; }
        [class*="st-key-meal-box-actions-"] [data-testid="stHorizontalBlock"] { gap:.25rem !important; }
        [class*="st-key-meal-box-actions-"] button { min-width:2.1rem !important; min-height:2.6rem !important; height:2.6rem !important; padding:.25rem .4rem !important; border-radius:9px !important; }
        [class*="st-key-add_recipe_row_"] { display:flex !important; justify-content:flex-start !important; align-self:flex-start !important; width:100% !important; margin-left:0 !important; margin-right:auto !important; }
        [class*="st-key-add_recipe_row_"] > div { display:flex !important; justify-content:flex-start !important; width:100% !important; margin-left:0 !important; margin-right:auto !important; }
        [class*="st-key-add_recipe_row_"] button { position:relative !important; width:7.5rem !important; min-width:7.5rem !important; height:3rem !important; padding:.45rem .55rem !important; white-space:nowrap !important; text-align:left !important; justify-content:flex-start !important; margin-left:0 !important; margin-right:auto !important; align-self:flex-start !important; }
        @media (max-width:600px) {
            [class*="st-key-meal-boxes"] [data-testid="stHorizontalBlock"] { flex-wrap:wrap !important; }
            [class*="st-key-meal-boxes"] [data-testid="stHorizontalBlock"] > [data-testid="column"] { flex:1 1 calc(50% - .25rem) !important; width:calc(50% - .25rem) !important; min-width:0 !important; }
            [class*="st-key-calendar-meal-boxes"] [data-testid="stHorizontalBlock"] { flex-wrap:wrap !important; }
            [class*="st-key-calendar-meal-boxes"] [data-testid="stHorizontalBlock"] > [data-testid="column"] { flex:1 1 calc(50% - .25rem) !important; width:calc(50% - .25rem) !important; min-width:0 !important; }
        }
        /* Search results: exact weight first, then add, then remove. */
        [class*="st-key-product-actions-"] [data-testid="stHorizontalBlock"] { flex-wrap:nowrap !important; align-items:center !important; gap:.45rem !important; width:100% !important; }
        [class*="st-key-product-actions-"] [data-testid="stHorizontalBlock"] > [data-testid="column"] { min-width:0 !important; padding:0 !important; }
        [class*="st-key-product-actions-"] [data-testid="stHorizontalBlock"] > [data-testid="column"]:nth-child(1) { flex:1 1 7rem !important; width:auto !important; }
        [class*="st-key-product-actions-"] [data-testid="stHorizontalBlock"] > [data-testid="column"]:nth-child(2) { flex:0 0 4.2rem !important; width:4.2rem !important; }
        [class*="st-key-product-actions-"] [data-testid="stHorizontalBlock"] > [data-testid="column"]:nth-child(3) { flex:0 0 2.5rem !important; width:2.5rem !important; }
        [class*="st-key-product-actions-"] [data-testid="stNumberInput"] { width:100% !important; }
        [class*="st-key-product-actions-"] [data-testid="stNumberInput"] input { min-height:46px !important; padding-left:.7rem !important; padding-right:.35rem !important; font-size:16px !important; }
        [class*="st-key-product-actions-"] input[type="number"] { -moz-appearance:textfield !important; appearance:textfield !important; }
        [class*="st-key-product-actions-"] input[type="number"]::-webkit-inner-spin-button,
        [class*="st-key-product-actions-"] input[type="number"]::-webkit-outer-spin-button { -webkit-appearance:none !important; appearance:none !important; margin:0 !important; }
        [class*="st-key-product-actions-"] [data-testid="stNumberInput"] button { display:none !important; }
        [class*="st-key-product-actions-"] [data-testid="stNumberInput"] [data-testid="stNumberInput-StepDown"],
        [class*="st-key-product-actions-"] [data-testid="stNumberInput"] [data-testid="stNumberInput-StepUp"] { display:none !important; }
        [class*="st-key-product-actions-"] button { width:100% !important; min-width:0 !important; }
        /* Give every searched food a single connected card. */
        div[data-testid="stElementContainer"]:has(.product-card-meta) {
            margin-top:0 !important;
            margin-bottom:0 !important;
            padding:1rem 1rem .35rem !important;
            background:var(--surface) !important;
            border:1px solid var(--line) !important;
            border-bottom:0 !important;
            border-radius:18px 18px 0 0 !important;
            box-shadow:none !important;
        }
        [class*="st-key-product-actions-"] {
            margin-top:-.9rem !important;
            margin-bottom:-.35rem !important;
            padding:.1rem 1rem .9rem !important;
            background:var(--surface) !important;
            border:1px solid var(--line) !important;
            border-top:0 !important;
            border-radius:0 0 18px 18px !important;
            box-shadow:none !important;
        }
        [class*="st-key-product-actions-"] [data-testid="stHorizontalBlock"] { margin:0 !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )


css()
st.markdown(
    """
    <style>
    [class*="st-key-recipe-builder-row-"] [data-testid="stHorizontalBlock"] {
        display:grid !important;
        grid-template-columns:minmax(0, 1fr) clamp(5.5rem, 18vw, 8rem) 2rem !important;
        gap:clamp(.25rem, 1.5vw, .6rem) !important;
        width:100% !important;
        align-items:center !important;
    }
    [class*="st-key-recipe-builder-row-"] [data-testid="stHorizontalBlock"] > [data-testid="column"] {
        width:auto !important;
        min-width:0 !important;
        max-width:none !important;
        flex:none !important;
        padding:0 !important;
    }
    [class*="st-key-recipe-builder-row-"] [data-testid="stNumberInput"],
    [class*="st-key-recipe-builder-row-"] [data-testid="stNumberInput"] > div,
    [class*="st-key-recipe-builder-row-"] [data-testid="stNumberInput"] input { width:100% !important; box-sizing:border-box !important; }
    [class*="st-key-recipe-builder-row-"] {
        padding:0 !important;
        margin:0 !important;
        background:transparent !important;
        border:0 !important;
        border-bottom:1px solid var(--line) !important;
        border-radius:0 !important;
        box-shadow:none !important;
    }
    [class*="st-key-recipe-builder-row-"] .builder-product,
    [class*="st-key-recipe-builder-row-"] [data-testid="stNumberInput"] > div {
        min-height:46px !important;
        height:46px !important;
        display:flex !important;
        align-items:center !important;
        border:0 !important;
        border-radius:0 !important;
        background:transparent !important;
        color:var(--ink) !important;
    }
    [class*="st-key-recipe-builder-row-"] .builder-product { padding:.65rem 0 !important; font-weight:600 !important; overflow:hidden !important; text-overflow:ellipsis !important; white-space:nowrap !important; background:transparent !important; }
    [class*="st-key-recipe-builder-row-"] .builder-product,
    [class*="st-key-recipe-builder-row-"] [data-testid="stNumberInput"] input,
    [class*="st-key-recipe-builder-row-"] [data-testid="stButton"] button { font-family:'DM Sans',sans-serif !important; }
    [class*="st-key-recipe-builder-row-"] .builder-product { font-size:1.05rem !important; }
    [class*="st-key-recipe-builder-row-"] [data-testid="stNumberInput"] input { min-height:46px !important; height:46px !important; border:0 !important; border-radius:0 !important; background:transparent !important; color:var(--ink) !important; text-align:right !important; font-size:1.05rem !important; font-weight:700 !important; }
    [class*="st-key-recipe-builder-row-"] [data-testid="stButton"] button { width:100% !important; min-height:32px !important; height:32px !important; border-radius:8px !important; border:0 !important; background:transparent !important; color:#b45d5d !important; font-size:0 !important; }
    [class*="st-key-recipe-builder-row-"] [data-testid="stButton"] button p::after { font-family:'DM Sans',sans-serif !important; font-weight:500 !important; }
    .ingredient-header { min-height:2.15rem !important; margin-bottom:.45rem !important; align-items:center !important; box-sizing:border-box !important; font-family:'DM Sans',sans-serif !important; font-size:1rem !important; line-height:1.5 !important; font-weight:400 !important; text-transform:none !important; letter-spacing:0 !important; color:var(--muted) !important; }
    .recipe-edit-header { border-bottom:0 !important; margin-bottom:.15rem !important; }
    .recipe-add-heading { margin-top:1.35rem !important; margin-bottom:.55rem !important; }
    [class*="st-key-recipe-edit-row-"] { margin-top:.35rem !important; }
    [class*="st-key-recipe-builder-row-"] [data-testid="stButton"] button p { font-size:0 !important; }
    [class*="st-key-recipe-builder-row-"] [data-testid="stButton"] button p::after { content:"×"; font-size:1.25rem !important; line-height:1 !important; }
    [class*="st-key-recipe-builder-row-"] [data-testid="stButton"] button:hover { background:#fff0f0 !important; }
    [class*="st-key-recipe-builder-row-"] [data-testid="stNumberInput"]:focus-within > div { border-color:var(--green) !important; box-shadow:0 0 0 3px #287a5618 !important; }
    html[data-theme="dark"] [class*="st-key-recipe-builder-row-"] [data-testid="stButton"] button { background:#2b2020 !important; border-color:#714343 !important; color:#f08b8b !important; }
    html[data-theme="dark"] [class*="st-key-recipe-builder-row-"] .builder-product,
    html[data-theme="dark"] [class*="st-key-recipe-builder-row-"] [data-testid="stNumberInput"] > div { background:var(--input) !important; }
    [class*="st-key-recipe-builder-row-"] + div [data-testid="stAlert"] { margin-top:.75rem !important; border-radius:16px !important; border:1px solid #cfe2f2 !important; box-shadow:0 4px 14px #2b6da00d !important; }
    @media (max-width:600px) {
        [class*="st-key-recipe-builder-row-"] { padding:0 !important; margin:0 !important; }
        [class*="st-key-recipe-builder-row-"] .builder-product,
        [class*="st-key-recipe-builder-row-"] [data-testid="stNumberInput"] > div,
        [class*="st-key-recipe-builder-row-"] [data-testid="stNumberInput"] input,
        [class*="st-key-recipe-builder-row-"] [data-testid="stButton"] button { min-height:46px !important; height:46px !important; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)
st.markdown('<div class="brand-card"><span class="brand-mark">N</span><span>NÕU</span></div>', unsafe_allow_html=True)
tab_today, tab_add, tab_calendar, tab_recipes, tab_insights = st.tabs(["Täna", "Lisa toit", "Kalender", "Retseptid", "Ülevaade"])

if st.session_state.pop("focus_recipes_after_save", False):
    components.html("""
        <script>
        setTimeout(() => {
            const parentDocument = window.parent.document;
            parentDocument.dispatchEvent(new KeyboardEvent('keydown', {key: 'Escape', bubbles: true}));
            const openPopoverTrigger = parentDocument.querySelector('button[aria-haspopup="dialog"][aria-expanded="true"]');
            if (openPopoverTrigger) openPopoverTrigger.click();
            const recipeTab = [...parentDocument.querySelectorAll('[data-baseweb="tab"]')]
                .find(tab => tab.textContent.includes('Retseptid'));
            if (recipeTab) recipeTab.click();
        }, 80);
        </script>
    """, height=0)

with tab_today:
    today_entries = entries_for(TODAY)
    displayed_today_entries = grouped_log_entries(today_entries)
    t = totals(TODAY)
    goal = st.session_state.goals["kcal"]
    remaining = max(0, goal - int(t["kcal"]))
    percent = min(100, int(t["kcal"] / goal * 100))
    goal_class = "goal-card goal-complete" if t["kcal"] >= goal else "goal-card"
    st.markdown(f'<div class="{goal_class}"><div class="goal-ring" style="--percent:{percent}%"><span>{percent}%</span></div><div class="goal-copy"><div class="metric-label">PÄEVA EESMÄRK</div><div class="metric-value">{int(t["kcal"]):,} <span style="font-size:.85rem;color:#000000;font-weight:500">/ {goal:,} kcal</span></div><div class="metric-note">{remaining:,} kcal alles · {len(today_entries)} toidukirjet</div></div></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="streak-card"><span class="streak-fire">🔥</span><div><div class="streak-label">Streak</div><div class="streak-value">{streak_count()} päeva</div></div></div>', unsafe_allow_html=True)
    st.write("")
    # Keep the wrapper as a normal full-width container. A horizontal wrapper
    # around st.columns makes the first card keep its desktop width on phones.
    with st.container(key="macro-cards", width="stretch"):
        c1, c2, c3 = st.columns(3)
        macro_goal_values = iter((st.session_state.goals["protein"], st.session_state.goals["carbs"], st.session_state.goals["fat"]))
        for col, label, value, goal_value in [(c1, "Valk", t["protein"], 140), (c2, "Süsivesikud", t["carbs"], 250), (c3, "Rasv", t["fat"], 70)]:
            with col:
                goal_value = next(macro_goal_values)
                macro_percent = min(100, int(float(value) / goal_value * 100)) if goal_value else 0
                macro_card_class = "calendar-macro-card macro-complete" if macro_percent >= 100 else "calendar-macro-card"
                st.markdown(f'<div class="{macro_card_class}"><div class="calendar-macro-label">{label}</div><div class="calendar-macro-ring" style="--progress:{macro_percent};--ring-color:#287a56"><svg viewBox="0 0 100 100" aria-hidden="true"><circle class="ring-track" cx="50" cy="50" r="40"></circle><circle class="ring-progress" cx="50" cy="50" r="40" pathLength="100"></circle></svg><span>{macro_percent}%</span></div><div class="calendar-macro-value">{int(value)}g / {int(goal_value)}g</div></div>', unsafe_allow_html=True)
    today_macro_data = [("Valk", t["protein"], st.session_state.goals["protein"], "#287a56"), ("Süsivesikud", t["carbs"], st.session_state.goals["carbs"], "#d28a32"), ("Rasv", t["fat"], st.session_state.goals["fat"], "#bd6262")]
    today_macro_cards = []
    for macro_label, macro_value, macro_goal, macro_color in today_macro_data:
        macro_percent = min(100, int(float(macro_value) / macro_goal * 100)) if macro_goal else 0
        macro_card_class = "calendar-macro-card macro-complete" if macro_percent >= 100 else "calendar-macro-card"
        today_macro_cards.append(f'<div class="{macro_card_class}"><div class="calendar-macro-label">{macro_label}</div><div class="calendar-macro-ring" style="--progress:{macro_percent};--ring-color:{macro_color}"><svg viewBox="0 0 100 100" aria-hidden="true"><circle class="ring-track" cx="50" cy="50" r="40"></circle><circle class="ring-progress" cx="50" cy="50" r="40" pathLength="100"></circle></svg><span>{macro_percent}%</span></div><div class="calendar-macro-value">{int(macro_value)}g / {int(macro_goal)}g</div></div>')
    st.markdown(f'<div class="calendar-macro-grid today-macro-grid">{"".join(today_macro_cards)}</div>', unsafe_allow_html=True)
    water_ml = water_total(TODAY)
    water_percent = min(100, int(water_ml / 3000 * 100))
    water_over_goal = max(0, water_ml - 3000)
    water_note = f"{water_over_goal} ml üle eesmärgi" if water_over_goal else f"{3000 - water_ml} ml veel eesmärgini"
    st.markdown(f'<div class="water-card"><div class="water-glass" style="--water-percent:{water_percent}%"><div class="water-fill"></div></div><div class="water-copy"><h3>Joodik</h3><div class="water-amount">{water_ml} ml <span>/ 3000 ml</span></div><div class="metric-note">{water_note}</div></div></div>', unsafe_allow_html=True)
    with st.container(key="water-actions", horizontal=True, width="stretch", gap="small", vertical_alignment="center"):
        water_input = st.number_input("Vee kogus (ml)", min_value=1, value=250, step=50, key="water_input", label_visibility="collapsed")
        if st.button("+ Lisa", key="water-add", type="primary"):
            change_water(water_input, TODAY)
            st.rerun()
        if st.button("250 ml", key="water-quick-250"):
            change_water(250, TODAY)
            st.rerun()
        if st.button("500 ml", key="water-quick-500"):
            change_water(500, TODAY)
            st.rerun()
        if st.button("−", key="water-remove", help="Eemalda viimane sisestatud kogus"):
            change_water(-water_input, TODAY)
            st.rerun()
    st.markdown(f'<div class="section-title today-section-title"><h2>Päeva toidud</h2><span class="section-hint">{TODAY.strftime("%d. %b")}</span></div>', unsafe_allow_html=True)
    if not today_entries:
        st.info("Sinu päev on tühi. Lisa esimene toit allpool.")
    meal_categories = [("Hommikusöök", "Hommik"), ("Lõuna", "Lõuna"), ("Õhtusöök", "Õhtu"), ("Vahepala", "Snäkk")]
    with st.container(key="meal-boxes", horizontal=True, width="stretch", gap="small"):
        meal_box_columns = st.columns(4)
        for box_column, (meal_value, meal_label) in zip(meal_box_columns, meal_categories):
            with box_column:
                with st.container(key=f"meal-box-{meal_value}", width="stretch"):
                    box_items = [item for item in displayed_today_entries if item.get("meal") == meal_value]
                    st.markdown(f'<div class="meal-box-title"><span>{meal_label}</span><span>{len(box_items)}</span></div>', unsafe_allow_html=True)
                    if not box_items:
                        st.markdown('<div class="meal-box-empty">Lisa toit siia</div>', unsafe_allow_html=True)
                    for box_index, item in enumerate(box_items):
                        item_macros = f'<div class="meal-box-macros"><span>Valk {int(item.get("protein", 0))}g</span><span>Süsivesikud {int(item.get("carbs", 0))}g</span><span>Rasv {int(item.get("fat", 0))}g</span></div>'
                        item_quantity = f'{int(item["grams"])} g' if item.get("grams", 0) else f'{item.get("count", 1)}×'
                        st.markdown(f'<div class="meal-box-item"><div class="meal-box-item-top"><span>{item_quantity} {item["name"]}</span><strong>{int(item.get("kcal", 0))} kcal</strong></div>{item_macros}</div>', unsafe_allow_html=True)
                        with st.container(key=f"meal-controls-{meal_value}-{box_index}-{item['_indices'][0]}", horizontal=True, width="stretch", gap="small"):
                            with st.container(key=f"meal-box-actions-{meal_value}-{box_index}-{item['_indices'][0]}", horizontal=True, width="content", gap="small"):
                                if st.button("+", key=f"box-add-{meal_value}-{box_index}-{item['_indices'][0]}", help="Lisa üks sama toit"):
                                    add_entry(item["_prototype"], meal_value, TODAY)
                                    st.rerun()
                                if st.button("−", key=f"box-subtract-{meal_value}-{box_index}-{item['_indices'][0]}", help="Eemalda üks kogus"):
                                    remove_entry_group([item["_indices"][-1]], TODAY)
                                    st.rerun()
                                if st.button("×", key=f"box-remove-{meal_value}-{box_index}-{item['_indices'][0]}", help="Eemalda kogu toit"):
                                    remove_entry_group(item["_indices"], TODAY)
                                    st.rerun()
                            selected_meal = st.selectbox(
                                "Liiguta kasti",
                                [value for value, _ in meal_categories],
                                index=[value for value, _ in meal_categories].index(meal_value),
                                format_func=lambda value: dict(meal_categories)[value],
                                key=f"move-meal-{meal_value}-{box_index}-{item['_indices'][0]}",
                                label_visibility="collapsed",
                            )
                        if selected_meal != meal_value:
                            for index in item["_indices"]:
                                today_entries[index]["meal"] = selected_meal
                            save_daily_logs()
                            st.rerun()
    # Meal boxes above are the single source of truth for today's food log.
    for i, item in enumerate([]):
        is_recipe = item.get("meal") == "Retsept" or item.get("entry_type") == "recipe"
        if not is_recipe:
            continue
        quantity_label = f'{item["count"]}× ' if item.get("count", 1) > 1 else ""
        meal_label = "Päeva jooksul" if item.get("count", 1) > 1 and item.get("meal") != "Retsept" else item.get("meal", "Toit")
        st.markdown(f'<div class="food-row"><div><div class="pill">{meal_label}</div><div class="food-name">{quantity_label}{item["name"]}</div><div class="food-meta">{item.get("time", "")} · {int(item.get("protein", 0))}g valku · {int(item.get("carbs", 0))}g süsivesikuid</div></div><div class="food-kcal">{int(item["kcal"])} kcal</div></div>', unsafe_allow_html=True)
        if is_recipe:
            remove_col, spacer = st.columns([1, 5])
            with remove_col:
                if st.button("×", key=f"remove_today_{i}", help="Eemalda kogu see toidugrupp"):
                    remove_entry_group(item["_indices"], TODAY)
                    st.rerun()
        else:
            with st.container(key=f"food-actions-{i}", horizontal=True, width="stretch", horizontal_alignment="distribute", gap="small", vertical_alignment="center"):
                with st.container(key=f"food-adjust-{i}", horizontal=True, width="content", gap="small"):
                    if st.button("+", key=f"add_one_today_{i}", help="Lisa üks sama toit"):
                        add_entry(item["_prototype"], item["_prototype"].get("meal", "Vahepala"), TODAY)
                        st.rerun()
                    if st.button("−", key=f"remove_one_today_{i}", help="Eemalda üks kogus"):
                        remove_entry_group([item["_indices"][-1]], TODAY)
                        st.rerun()
                with st.container(key=f"food-remove-{i}", horizontal=True, width="content"):
                    if st.button("×", key=f"remove_today_{i}", help="Eemalda kogu see toidugrupp"):
                        remove_entry_group(item["_indices"], TODAY)
                        st.rerun()
if st.session_state.pop("open_food_search_after_manual", False):
    st.session_state.add_mode = "Otsi toitu"
    st.session_state.food_search_query = st.session_state.pop("manual_saved_food_name", "")

with tab_add:
    st.markdown("## Lisa toit")
    add_mode = st.radio("Vali viis", ["Otsi toitu", "Sisesta ise"], horizontal=True, label_visibility="collapsed", key="add_mode")
    if add_mode == "Otsi toitu":
        query = st.text_input("Otsi toodet", placeholder="nt kohuke, rukkileib, skyr…", key="food_search_query")
        filtered = [p for p in all_products() if not query or query.lower() in (p["name"] + " " + p["brand"]).lower()]
        visible_products = filtered[:15]
        highlighted_index = next((idx for idx, product in enumerate(visible_products) if product["name"] == st.session_state.get("highlight_added_food")), None)
        highlighted_style = "" if highlighted_index is None else f'[class*="st-key-product-actions-{highlighted_index}"] button[kind="primary"] {{ background:#e5f4eb !important; color:#287a56 !important; border-color:#b9dfc5 !important; }}'
        st.markdown(f'<style>{highlighted_style}</style>', unsafe_allow_html=True)
        for idx, product in enumerate(visible_products):
            st.markdown(f'**{product["name"]}**  \n<span class="product-card-meta" style="color:#000000;font-size:.8rem">{product["brand"]} · {product["portion"]} · {product["kcal"]} kcal</span>  \n<span class="product-card-macros" style="color:#000000;font-size:.75rem;font-weight:600">Valk {product["protein"]}g · Süsivesikud {product["carbs"]}g · Rasv {product["fat"]}g</span>', unsafe_allow_html=True)
            with st.container(key=f"product-actions-{idx}", horizontal=True, width="stretch", horizontal_alignment="distribute", gap="small", vertical_alignment="center"):
                weight_key = f"add_weight_{idx}_{product['name']}_{st.session_state.get('add_weight_version', 0)}"
                product_weight = st.number_input(
                    "Kaal (g)",
                    min_value=0.0,
                    value=0.0,
                    step=1.0,
                    format="%.0f",
                    key=weight_key,
                    label_visibility="collapsed",
                )
                if st.button("Lisa", type="primary", key=f"add_{idx}_{product['name']}"):
                    if product_weight > 0:
                        add_entry(product_for_grams(product, product_weight), day=TODAY)
                    st.session_state.add_weight_version = st.session_state.get('add_weight_version', 0) + 1
                    st.rerun()
                if st.button("×", key=f"delete_product_{idx}_{product['name']}", help="Eemalda see toode otsingust"):
                    hide_product(product["name"])
                    st.rerun()
        if query and not filtered:
            st.info(f'Toodet “{query}” kataloogist ei leitud.')
            if st.button(f"＋ Loo “{query}”", type="primary", use_container_width=True, key="create_missing_food"):
                st.session_state.inline_create_food = query.strip()
                st.rerun()
        if st.session_state.inline_create_food:
            st.markdown("### Lisa uus toit")
            with st.form("inline_create_food_form"):
                inline_name = st.text_input("Toidu nimi", value=st.session_state.inline_create_food)
                inline_basis = st.selectbox("Toiteväärtus käib", ["100 g", "100 ml", "1 tk", "1 portsjon"])
                inline_a, inline_b = st.columns(2)
                with inline_a:
                    inline_kcal = st.number_input("Kalorid", min_value=0, value=0)
                    inline_protein = st.number_input("Valk (g)", min_value=0, value=0)
                with inline_b:
                    inline_carbs = st.number_input("Süsivesikud (g)", min_value=0, value=0)
                    inline_fat = st.number_input("Rasv (g)", min_value=0, value=0)
                if st.form_submit_button("Salvesta ja lisa tänasesse", type="primary", use_container_width=True) and inline_name.strip():
                    new_product = {"name": inline_name.strip(), "brand": "Minu toit", "kcal": inline_kcal, "protein": inline_protein, "carbs": inline_carbs, "fat": inline_fat, "portion": inline_basis}
                    save_custom_product(new_product)
                    add_entry(new_product, "Vahepala", TODAY)
                    st.session_state.inline_create_food = ""
                    st.rerun()
    else:
        manual_form_key = f"manual_food_{st.session_state.get('manual_food_form_version', 0)}"
        with st.form(manual_form_key):
            name = st.text_input("Toidu nimi", placeholder="nt õhtusöök")
            nutrition_basis = st.selectbox("Toiteväärtus käib", ["100 g", "100 ml", "1 tk", "1 portsjon"], index=0, help="Märgi, mille kohta pakendil või sinu andmetes kalorid ja makrod käivad.")
            c1, c2 = st.columns(2)
            with c1:
                kcal = st.number_input("Kalorid", min_value=0, value=0)
                protein = st.number_input("Valk (g)", min_value=0, value=0)
            with c2:
                carbs = st.number_input("Süsivesikud (g)", min_value=0, value=0)
                fat = st.number_input("Rasv (g)", min_value=0, value=0)
            save_product = st.checkbox("Salvesta see toit toodete alla järgmiseks korraks", value=True)
            if st.form_submit_button("Salvesta toode", type="primary", use_container_width=True) and name.strip():
                new_product = {"name": name, "brand": "Minu toit", "kcal": kcal, "protein": protein, "carbs": carbs, "fat": fat, "portion": nutrition_basis}
                save_custom_product(new_product)
                st.session_state.manual_saved_food_name = new_product["name"].strip()
                st.session_state.highlight_added_food = new_product["name"].strip()
                st.session_state.open_food_search_after_manual = True
                st.session_state.manual_food_form_version = st.session_state.get("manual_food_form_version", 0) + 1
                st.rerun()

with tab_calendar:
    st.markdown("## Kalender")
    selected_day = st.date_input("Vali päev", value=TODAY, min_value=TODAY - timedelta(days=365), max_value=TODAY, format="DD.MM.YYYY", key="calendar_day")
    st.session_state.active_date = selected_day
    selected_entries = entries_for(selected_day)
    selected_totals = totals(selected_day)
    calendar_macro_data = [("Valk", selected_totals["protein"], st.session_state.goals["protein"], "#287a56"), ("Süsivesikud", selected_totals["carbs"], st.session_state.goals["carbs"], "#d28a32"), ("Rasv", selected_totals["fat"], st.session_state.goals["fat"], "#bd6262")]
    calendar_macro_cards = []
    for macro_label, macro_value, macro_goal, macro_color in calendar_macro_data:
        macro_percent = min(100, int(float(macro_value) / macro_goal * 100)) if macro_goal else 0
        macro_card_class = "calendar-macro-card macro-complete" if macro_percent >= 100 else "calendar-macro-card"
        calendar_macro_cards.append(f'<div class="{macro_card_class}"><div class="calendar-macro-label">{macro_label}</div><div class="calendar-macro-ring" style="--progress:{macro_percent};--ring-color:{macro_color}"><svg viewBox="0 0 100 100" aria-hidden="true"><circle class="ring-track" cx="50" cy="50" r="40"></circle><circle class="ring-progress" cx="50" cy="50" r="40" pathLength="100"></circle></svg><span>{macro_percent}%</span></div><div class="calendar-macro-value">{int(macro_value)}g / {int(macro_goal)}g</div></div>')
    st.markdown(f'<div class="calendar-macro-grid calendar-page-macro-grid">{"".join(calendar_macro_cards)}</div>', unsafe_allow_html=True)
    calendar_water_ml = water_total(selected_day)
    calendar_water_percent = min(100, int(calendar_water_ml / 3000 * 100))
    calendar_water_over_goal = max(0, calendar_water_ml - 3000)
    calendar_water_note = f"{calendar_water_over_goal} ml üle eesmärgi" if calendar_water_over_goal else f"{3000 - calendar_water_ml} ml veel eesmärgini"
    st.markdown(f'<div class="water-card"><div class="water-glass" style="--water-percent:{calendar_water_percent}%"><div class="water-fill"></div></div><div class="water-copy"><h3>Joodik</h3><div class="water-amount">{calendar_water_ml} ml <span>/ 3000 ml</span></div><div class="metric-note">{calendar_water_note}</div></div></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="goal-card calendar-summary-card"><div class="goal-copy"><div class="metric-label">{selected_day.strftime("%d. %B %Y").upper()}</div><div class="metric-value">{int(selected_totals["kcal"]):,} kcal</div><div class="metric-note">{len(selected_entries)} toidukirjet · {int(selected_totals["protein"])}g valku</div></div></div>', unsafe_allow_html=True)
    st.markdown("### Selle päeva toit")
    if not selected_entries:
        st.info("Sellel päeval pole veel toite logitud.")
    calendar_items = grouped_log_entries(selected_entries)
    calendar_categories = [("Hommikusöök", "Hommik"), ("Lõuna", "Lõuna"), ("Õhtusöök", "Õhtu"), ("Vahepala", "Snäkk")]
    with st.container(key=f"calendar-meal-boxes-{selected_day}", horizontal=True, width="stretch", gap="small"):
        calendar_columns = st.columns(4)
        for box_column, (meal_value, meal_label) in zip(calendar_columns, calendar_categories):
            with box_column:
                with st.container(key=f"calendar-meal-box-{selected_day}-{meal_value}", width="stretch"):
                    box_items = [item for item in calendar_items if item.get("meal") == meal_value]
                    st.markdown(f'<div class="meal-box-title"><span>{meal_label}</span><span>{len(box_items)}</span></div>', unsafe_allow_html=True)
                    if not box_items:
                        st.markdown('<div class="meal-box-empty">Tühi</div>', unsafe_allow_html=True)
                    for box_index, item in enumerate(box_items):
                        item_macros = f'<div class="meal-box-macros"><span>Valk {int(item.get("protein", 0))}g</span><span>Süsivesikud {int(item.get("carbs", 0))}g</span><span>Rasv {int(item.get("fat", 0))}g</span></div>'
                        item_quantity = f'{int(item["grams"])} g' if item.get("grams", 0) else f'{item.get("count", 1)}×'
                        st.markdown(f'<div class="meal-box-item"><div class="meal-box-item-top"><span>{item_quantity} {item["name"]}</span><strong>{int(item.get("kcal", 0))} kcal</strong></div>{item_macros}</div>', unsafe_allow_html=True)
    logged_days = sorted(st.session_state.daily_logs.keys(), reverse=True)

with tab_recipes:
    st.markdown("## Retseptid")
    if st.session_state.pop("recipe_saved_message", None):
        st.success("Uus retsept on kohe nimekirjas.")
    recipe_query = st.text_input("Otsi retsepti", placeholder="nt kana, hommikusöök…", key="recipe_query")
    visible_recipes = [r for r in all_recipes() if not recipe_query or recipe_query.lower() in (r.get("name", "") + " " + r.get("ingredients", "")).lower()]
    for index, recipe in enumerate(visible_recipes):
        recipe_token = hashlib.sha1(recipe.get("name", "").strip().casefold().encode("utf-8")).hexdigest()[:12]
        with st.expander(f'{recipe["name"]} · {recipe["kcal"]} kcal', expanded=False):
            st.markdown(f'<div class="recipe-macros"><span class="recipe-macro">{int(recipe["kcal"])} kcal</span><span class="recipe-macro">Valk {int(recipe["protein"])} g</span><span class="recipe-macro">Süsivesikud {int(recipe["carbs"])} g</span><span class="recipe-macro">Rasv {int(recipe["fat"])} g</span></div>', unsafe_allow_html=True)
            recipe_ingredients = recipe.get("ingredients_data", [])
            if recipe_ingredients:
                st.markdown('<div class="ingredient-header"><span>Toode</span><span>Kaal</span><span></span></div>', unsafe_allow_html=True)
                for ingredient in recipe_ingredients:
                    st.markdown(f'<div class="recipe-read-row"><span>{ingredient["name"]}</span><strong>{ingredient["grams"]} g</strong></div>', unsafe_allow_html=True)
            else:
                st.write("")
            with st.container(key=f"recipe-actions-{recipe_token}", width="stretch"):
                if st.button("✎", key=f"edit_recipe_{recipe_token}", help="Muuda retsepti"):
                    st.session_state.active_recipe_editor = recipe_token
                    st.rerun()
                if st.session_state.get("active_recipe_editor") == recipe_token:
                    edit_key = f"recipe_edit_data_{recipe_token}"
                    if edit_key not in st.session_state:
                        st.session_state[edit_key] = json.loads(json.dumps(recipe))
                    edit_data = st.session_state[edit_key]
                    edited_ingredients_data = edit_data.setdefault("ingredients_data", [])
                    ensure_unique_edit_ids(edited_ingredients_data, f"recipe-{recipe_token}")
                    if st.button("Sulge muutmine", key=f"close_recipe_editor_{recipe_token}"):
                        st.session_state.pop("active_recipe_editor", None)
                        st.session_state.pop(edit_key, None)
                        st.rerun()
                    edit_name = st.text_input("Retsepti nimi", value=edit_data["name"], key=f"recipe_name_{recipe_token}")
                    st.markdown("### Koostisosad")
                    recipe_products = all_products()
                    recipe_labels = [f'{product["name"]} · {product["brand"]}' for product in recipe_products]
                    used_recipe_names = {item.get("name", "").strip().casefold() for item in edited_ingredients_data}
                    st.markdown('<div class="ingredient-header recipe-edit-header"><span>Toode</span><span>Kaal</span><span></span></div>', unsafe_allow_html=True)
                    for ingredient_index, ingredient in enumerate(edited_ingredients_data):
                        ingredient_token = ingredient["_edit_id"]
                        other_recipe_names = used_recipe_names - {ingredient.get("name", "").strip().casefold()}
                        current_recipe_name = ingredient.get("name", "").strip().casefold()
                        ingredient_products = [product for product in recipe_products if product["name"].strip().casefold() == current_recipe_name or product["name"].strip().casefold() not in other_recipe_names]
                        ingredient_labels = [f'{product["name"]} · {product["brand"]}' for product in ingredient_products]
                        recipe_labels = ingredient_labels
                        with st.container(key=f"recipe-edit-row-{recipe_token}-{ingredient_token}", horizontal=True, width="stretch", gap="small", vertical_alignment="center"):
                            current_label = next((label for label in recipe_labels if label.startswith(f'{ingredient["name"]} ·')), recipe_labels[0] if recipe_labels else "")
                            selected_label = st.selectbox("Toode", recipe_labels, index=recipe_labels.index(current_label) if current_label in recipe_labels else 0, key=f"recipe_product_{recipe_token}_{ingredient_token}", label_visibility="collapsed") if recipe_labels else ""
                            if selected_label:
                                ingredient["name"] = selected_label.rsplit(" · ", 1)[0]
                            ingredient["grams"] = st.number_input("Kaal (g)", min_value=1, value=int(ingredient.get("grams", 100)), step=5, key=f"recipe_grams_{recipe_token}_{ingredient_token}", label_visibility="collapsed")
                            if st.button("×", key=f"remove_recipe_row_{recipe_token}_{ingredient_token}", help="Eemalda koostisosa"):
                                edited_ingredients_data.pop(ingredient_index)
                                st.rerun()
                    st.markdown('<h3 class="recipe-add-heading">Lisa koostisosa</h3>', unsafe_allow_html=True)
                    recipe_add_query = st.text_input("Otsi toodet", placeholder="nt kana, kartul, jogurt…", key=f"recipe_add_query_{recipe_token}")
                    filtered_recipe_products = [
                        product for product in recipe_products
                        if product["name"].strip().casefold() not in used_recipe_names
                        and (not recipe_add_query or recipe_add_query.lower() in (product["name"] + " " + product["brand"]).lower())
                    ]
                    if filtered_recipe_products:
                        filtered_recipe_labels = [f'{product["name"]} · {product["brand"]}' for product in filtered_recipe_products]
                        add_product_key = f"recipe_add_product_{recipe_token}"
                        if st.session_state.get(add_product_key) not in filtered_recipe_labels:
                            st.session_state[add_product_key] = filtered_recipe_labels[0]
                        selected_add_label = st.selectbox("Vali toode", filtered_recipe_labels, key=add_product_key)
                        recipe_add_grams = st.number_input("Kaal (g)", min_value=1, value=100, step=5, key=f"recipe_add_grams_{recipe_token}")
                        if st.button("+ Lisa toode", key=f"add_recipe_row_{recipe_token}", width="content"):
                            selected_product = filtered_recipe_products[filtered_recipe_labels.index(selected_add_label)]
                            edited_ingredients_data.append({"name": selected_product["name"], "grams": int(recipe_add_grams), "_edit_id": f"recipe-{recipe_token}-{uuid.uuid4().hex[:12]}"})
                            st.rerun()
                    else:
                        st.info("Selle otsinguga toodet ei leitud.")
                    auto_totals = calculate_recipe_ingredients(edited_ingredients_data)
                    st.info(f'Kokku: {int(auto_totals["kcal"])} kcal · {int(auto_totals["protein"])}g valku · {int(auto_totals["carbs"])}g süsivesikuid · {int(auto_totals["fat"])}g rasva')
                    edit_ingredients = " · ".join(f'{item["name"]} ({item["grams"]} g)' for item in edited_ingredients_data)
                    if st.button("Salvesta retsept", type="primary", use_container_width=True, key=f"save_recipe_{recipe_token}"):
                        if not edit_name.strip():
                            st.warning("Retseptil peab olema nimi.")
                        elif not edited_ingredients_data:
                            st.warning("Retseptil peab olema vähemalt üks toode.")
                        else:
                            normalized_ingredients = [{"name": item["name"], "grams": int(item["grams"])} for item in edited_ingredients_data]
                            save_custom_recipe({"name": edit_name.strip(), "tag": "", "kcal": int(auto_totals["kcal"]), "protein": int(auto_totals["protein"]), "carbs": int(auto_totals["carbs"]), "fat": int(auto_totals["fat"]), "time": "", "ingredients": edit_ingredients, "ingredients_data": normalized_ingredients}, replace_name=recipe["name"])
                            del st.session_state[edit_key]
                            st.session_state.pop("active_recipe_editor", None)
                            st.session_state.focus_recipes_after_save = True
                            st.rerun()
                if st.button("🗑", key=f"delete_recipe_{recipe_token}", help="Kustuta retsept"):
                    delete_custom_recipe(recipe["name"])
                    st.rerun()
            if st.button("Lisa tänasesse", key=f"recipe_add_{recipe_token}", use_container_width=True):
                add_entry(recipe, "Vahepala", TODAY, entry_type="recipe")
                st.rerun()

    st.markdown("### Lisa uus retsept")
    new_name = st.text_input("Retsepti nimi", placeholder="nt minu õhtusöök", key="new_recipe_name")
    recipe_products = all_products()
    if recipe_products:
        recipe_product_query = st.text_input("Otsi toodet", placeholder="nt kana, kartul, jogurt...", key="new_recipe_product_query")
        filtered_recipe_products = [
            product for product in recipe_products
            if not recipe_product_query or recipe_product_query.lower() in (product["name"] + " " + product["brand"]).lower()
        ]
        if not filtered_recipe_products:
            st.info("Selle otsinguga toodet ei leitud.")
            filtered_recipe_products = recipe_products[:1]
        recipe_products = filtered_recipe_products
        used_builder_names = {item.get("name", "").strip().casefold() for item in st.session_state.recipe_builder}
        available_recipe_products = [
            product for product in recipe_products
            if product["name"].strip().casefold() not in used_builder_names
        ]
        recipe_labels = [f'{p["name"]} · {p["brand"]}' for p in recipe_products]
        recipe_labels = [f'{p["name"]} · {p["brand"]}' for p in available_recipe_products] or ["Kõik selle otsingu tooted on juba lisatud"]
        if st.session_state.get("recipe_ingredient_product") not in recipe_labels:
            st.session_state.recipe_ingredient_product = recipe_labels[0]
        ingredient_col, grams_col, add_col = st.columns([4, 2, 1])
        with ingredient_col:
            selected_ingredient_label = st.selectbox("Toode", recipe_labels, key="recipe_ingredient_product", disabled=not available_recipe_products)
        with grams_col:
            ingredient_grams = st.number_input("Grammid", min_value=1, value=100, step=5, key="recipe_ingredient_grams")
        with add_col:
            st.write("")
            if st.button("Lisa", key="recipe_add_ingredient"):
                if available_recipe_products:
                    selected_product = available_recipe_products[recipe_labels.index(selected_ingredient_label)]
                    builder_id = f"builder-{uuid.uuid4().hex[:12]}"
                    st.session_state.recipe_builder.append({"name": selected_product["name"], "grams": ingredient_grams, "_edit_id": builder_id})
                    st.rerun()

    if st.session_state.recipe_builder:
        st.markdown("### Koostisosad")
        st.markdown('<div class="ingredient-header"><span>Toode</span><span>Kaal</span><span></span></div>', unsafe_allow_html=True)
        ensure_unique_edit_ids(st.session_state.recipe_builder, "builder")
        for ingredient_index, ingredient in enumerate(st.session_state.recipe_builder):
            ingredient_token = ingredient["_edit_id"]
            ingredient_product = next((p for p in recipe_products if p["name"] == ingredient["name"]), None)
            with st.container(key=f"recipe-builder-row-{ingredient_token}", width="stretch"):
                product_col, weight_col, remove_col = st.columns([6, 2, 1], gap="small")
                with product_col:
                    st.markdown(f'<div class="builder-product">{ingredient["name"]}</div>', unsafe_allow_html=True)
                with weight_col:
                    ingredient["grams"] = st.number_input(
                        "Kaal (g)",
                        min_value=1,
                        value=int(ingredient["grams"]),
                        step=1,
                        key=f"recipe_builder_grams_{ingredient_token}",
                        label_visibility="collapsed",
                    )
                with remove_col:
                    if st.button("×", key=f"remove_recipe_ingredient_{ingredient_token}"):
                        st.session_state.recipe_builder.pop(ingredient_index)
                        st.rerun()
        builder_totals = calculate_recipe_ingredients(st.session_state.recipe_builder)
        st.info(f'Kokku: {int(builder_totals["kcal"])} kcal · {int(builder_totals["protein"])}g valku · {int(builder_totals["carbs"])}g süsivesikuid · {int(builder_totals["fat"])}g rasva')

    if st.button("Salvesta uus retsept", type="primary", use_container_width=True, key="save_new_recipe"):
        if not new_name.strip():
            st.warning("Lisa retseptile nimi.")
        elif not st.session_state.recipe_builder:
            st.warning("Lisa vähemalt üks toode koos grammidega.")
        else:
            builder_totals = calculate_recipe_ingredients(st.session_state.recipe_builder)
            ingredients_text = " · ".join(f'{item["name"]} ({item["grams"]} g)' for item in st.session_state.recipe_builder)
            normalized_ingredients = [{"name": item["name"], "grams": int(item["grams"])} for item in st.session_state.recipe_builder]
            save_custom_recipe({"name": new_name.strip(), "tag": "", "kcal": int(builder_totals["kcal"]), "protein": int(builder_totals["protein"]), "carbs": int(builder_totals["carbs"]), "fat": int(builder_totals["fat"]), "time": "", "ingredients": ingredients_text, "ingredients_data": normalized_ingredients})
            st.session_state.recipe_builder = []
            st.session_state.recipe_saved_message = True
            st.rerun()

with tab_insights:
    st.markdown("## Sinu ülevaade")
    last_seven_days = [TODAY - timedelta(days=offset) for offset in range(7)]
    logged_last_7 = [day for day in last_seven_days if st.session_state.daily_logs.get(day_key(day), [])]
    weekly_average = int(sum(totals(day)["kcal"] for day in logged_last_7) / len(logged_last_7)) if logged_last_7 else 0
    weekly_totals = {key: sum(totals(day)[key] for day in logged_last_7) for key in ("protein", "carbs", "fat")}
    average_protein = int(weekly_totals["protein"] / len(logged_last_7)) if logged_last_7 else 0
    average_carbs = int(weekly_totals["carbs"] / len(logged_last_7)) if logged_last_7 else 0
    average_fat = int(weekly_totals["fat"] / len(logged_last_7)) if logged_last_7 else 0
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f'<div class="overview-card"><div class="metric-label">NÄDALA KESKMINE</div><div class="metric-value">{weekly_average:,} kcal</div><div class="metric-note">{len(logged_last_7)} / 7 päeva logitud</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="overview-card"><div class="metric-label">STREAK</div><div class="metric-value">🔥 {streak_count()} päeva</div><div class="metric-note">järjest logitud</div></div>', unsafe_allow_html=True)
    st.write("")
    st.markdown("### Viimased 7 päeva")
    day_labels = ["E", "T", "K", "N", "R", "L", "P"]
    bars = []
    for day in reversed(last_seven_days):
        day_total = int(totals(day)["kcal"]) if st.session_state.daily_logs.get(day_key(day), []) else 0
        height = min(100, max(4, int(day_total / st.session_state.goals["kcal"] * 100))) if day_total else 4
        today_class = " today" if day == TODAY else ""
        bars.append(f'<div class="week-day"><div class="week-track"><div class="week-fill{today_class}" style="height:{height}%"></div></div><span>{day_labels[day.weekday()]}</span></div>')
    st.markdown(f'<div class="overview-card"><div class="week-bars">{"".join(bars)}</div></div>', unsafe_allow_html=True)
    st.write("")
    m1, m2, m3 = st.columns(3)
    for col, label, value in [(m1, "Valk", average_protein), (m2, "Süsivesikud", average_carbs), (m3, "Rasv", average_fat)]:
        with col:
            st.markdown(f'<div class="metric-card"><div class="metric-label">KESKMINE {label.upper()}</div><div class="metric-value">{value}g</div><div class="metric-note">logitud päevadel</div></div>', unsafe_allow_html=True)
    protein_days = []
    for log_day, entries in st.session_state.daily_logs.items():
        if not entries:
            continue
        try:
            parsed_day = date.fromisoformat(log_day)
        except ValueError:
            continue
        day_totals = totals(parsed_day)
        protein_days.append((parsed_day, day_totals))
    protein_days.sort(key=lambda item: item[1]["protein"], reverse=True)
    top_protein_days = protein_days[:1]
    st.markdown("### Laksud sisse")
    if top_protein_days:
        protein_cards = []
        for place, (parsed_day, day_totals) in enumerate(top_protein_days, start=1):
            protein_cards.append(f'<div class="protein-top-card protein-best-card"><div class="protein-best-date">{parsed_day.strftime("%d.%m.%Y")}</div><div class="protein-best-amount">{int(day_totals["protein"])} g valku</div></div>')
        grid_class = "protein-top-grid single" if len(protein_cards) == 1 else "protein-top-grid"
        st.markdown(f'<div class="{grid_class}">{"".join(protein_cards)}</div>', unsafe_allow_html=True)
    else:
        st.info("Päevade andmed ilmuvad siia pärast toitude logimist.")
    st.markdown("### Päevased eesmärgid")
    goal_left, goal_right = st.columns(2)
    with goal_left:
        goal_kcal = st.number_input("Kalorid päevas", min_value=1, max_value=10000, value=int(st.session_state.goals["kcal"]), step=50, key="goal_kcal")
        goal_protein = st.number_input("Valk (g)", min_value=1, max_value=1000, value=int(st.session_state.goals["protein"]), step=5, key="goal_protein")
    with goal_right:
        goal_carbs = st.number_input("Süsivesikud (g)", min_value=1, max_value=1500, value=int(st.session_state.goals["carbs"]), step=5, key="goal_carbs")
        goal_fat = st.number_input("Rasv (g)", min_value=1, max_value=500, value=int(st.session_state.goals["fat"]), step=5, key="goal_fat")
    if st.button("Salvesta eesmärgid", type="primary", use_container_width=True, key="save_goals"):
        st.session_state.goals = {"kcal": int(goal_kcal), "protein": int(goal_protein), "carbs": int(goal_carbs), "fat": int(goal_fat)}
        save_goals(st.session_state.goals)
        st.rerun()

