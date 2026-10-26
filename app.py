import json
from datetime import date, datetime, timedelta
from pathlib import Path

import streamlit as st


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
    return [product for product in load_custom_products() + PRODUCTS if product.get("name") and product["name"].lower() not in hidden_products]


def load_custom_recipes():
    if not CUSTOM_RECIPES_FILE.exists():
        return []
    try:
        with CUSTOM_RECIPES_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
        return data if isinstance(data, list) else []
    except (OSError, json.JSONDecodeError):
        return []


def save_custom_recipe(recipe):
    recipes = load_custom_recipes()
    recipes = [r for r in recipes if r.get("name", "").lower() != recipe["name"].lower()]
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

TODAY = date.today()
TODAY_KEY = TODAY.isoformat()

if "daily_logs" not in st.session_state:
    st.session_state.daily_logs = load_daily_logs()
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


def add_entry(item, meal="Vahepala", day=None):
    entries_for(day).append({**item, "meal": meal, "time": datetime.now().strftime("%H:%M")})
    save_daily_logs()
    st.session_state.last_added_message = f'{item["name"]} lisati tänasesse.'


def remove_entry(index, day=None):
    entries_for(day).pop(index)
    save_daily_logs()


def remove_entry_group(indices, day=None):
    entries = entries_for(day)
    for index in sorted(indices, reverse=True):
        entries.pop(index)
    save_daily_logs()


def grouped_log_entries(entries):
    grouped = []
    grouped_by_name = {}
    for index, entry in enumerate(entries):
        # Recipes stay separate; normal foods with the same name are combined.
        if entry.get("meal") == "Retsept":
            grouped.append({**entry, "count": 1, "_indices": [index], "_prototype": {**entry}})
            continue
        name_key = entry.get("name", "").strip().lower()
        if name_key not in grouped_by_name:
            grouped_by_name[name_key] = len(grouped)
            grouped.append({**entry, "count": 1, "_indices": [index], "_prototype": {**entry}})
        else:
            item = grouped[grouped_by_name[name_key]]
            item["count"] += 1
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
        :root { --ink:#17231d; --muted:#68776e; --mint:#dff3e8; --green:#217a52; --cream:#ffffff; --line:#dfe8e1; --surface:#ffffff; --surface-soft:#eef7f1; --input:#ffffff; --shadow:#1c3a2714; }
        .stApp { background:var(--cream); color:var(--ink); font-family:'DM Sans',sans-serif; }
        [data-testid="stHeader"] { background:transparent; }
        .block-container { max-width:720px; padding:1.5rem 1rem 5rem; }
        h1,h2,h3 { font-family:'Space Grotesk',sans-serif; letter-spacing:-.04em; color:var(--ink); }
        h1 { font-size:2.15rem; margin-bottom:.2rem; } h2 { font-size:1.45rem; } h3 { font-size:1.05rem; }
        .eyebrow { color:var(--green); text-transform:uppercase; font-size:.7rem; font-weight:700; letter-spacing:.16em; }
        .hero { background:linear-gradient(135deg,#173f2d,#286d4d); color:white; border-radius:26px; padding:1.15rem 1.25rem 1.25rem; margin:.65rem 0 1rem; box-shadow:0 10px 28px #2a765026; }
        .hero-title { font-family:'Space Grotesk'; font-weight:700; font-size:1.85rem; letter-spacing:-.06em; }
        .hero-sub { color:#c4e4d1; margin-top:.3rem; font-size:.88rem; }
        .metric-card { background:white; border:1px solid var(--line); border-radius:20px; padding:1rem; min-height:98px; box-shadow:0 3px 12px #1c3a2710; }
        .metric-label { color:var(--muted); font-size:.76rem; font-weight:600; } .metric-value { font:700 1.5rem 'Space Grotesk'; margin-top:.35rem; }
        .metric-note { color:var(--muted); font-size:.72rem; margin-top:.15rem; }
        .progress { height:9px; background:#e7eee9; border-radius:99px; overflow:hidden; margin-top:.7rem; } .progress > div { height:100%; background:#287a56; border-radius:99px; }
        .food-row { display:flex; justify-content:space-between; align-items:center; padding:.95rem 1rem; background:white; border-bottom:1px solid var(--line); }
        .food-row:first-child { border-radius:18px 18px 0 0; } .food-row:last-child { border-radius:0 0 18px 18px; border-bottom:0; }
        .food-name { font-weight:600; margin-top:.45rem; } .food-meta { color:var(--muted); font-size:.78rem; margin-top:.15rem; } .food-kcal { font-weight:700; white-space:nowrap; }
        .pill { display:inline-block; padding:.3rem .65rem; border-radius:99px; background:#edf5ef; color:#287a56; font-weight:600; font-size:.72rem; }
        div.stButton > button { border-radius:14px; border:1px solid #dce7de; min-height:2.7rem; font-weight:600; }
        div.stButton > button[kind="primary"] { background:#287a56; color:white; border-color:#287a56; }
        div[data-testid="stMetric"] { background:white; border-radius:18px; padding:1rem; border:1px solid #e7ece7; }
        .stTabs [data-baseweb="tab-list"] { gap:1.25rem; border-bottom:1px solid var(--line); } .stTabs [data-baseweb="tab"] { padding:0 0 .75rem; font-weight:600; }
        .stTabs [aria-selected="true"] { color:var(--green); }
        .section-title { display:flex; align-items:end; justify-content:space-between; margin:1.25rem 0 .65rem; }
        .section-title h2 { margin:0; } .section-hint { color:var(--muted); font-size:.78rem; }
        .goal-card { background:white; border:1px solid var(--line); border-radius:24px; padding:1rem 1.1rem; display:flex; align-items:center; gap:1rem; box-shadow:0 3px 12px #1c3a2710; }
        .goal-ring { width:86px; height:86px; border-radius:50%; display:grid; place-items:center; flex:0 0 auto; background:conic-gradient(#287a56 var(--percent), #e7eee9 0); position:relative; }
        .goal-ring:after { content:''; width:66px; height:66px; border-radius:50%; background:white; position:absolute; }
        .goal-ring span { z-index:1; font:700 1rem 'Space Grotesk'; color:#287a56; }
        .goal-copy { flex:1; } .goal-copy .metric-value { margin:0; font-size:1.35rem; }
        .add-card { background:#e5f4eb; border-radius:20px; padding:1rem; margin-top:1rem; }
        .add-card-title { font-weight:700; font-size:1rem; } .add-card-sub { font-size:.8rem; color:#547063; margin:.2rem 0 .8rem; }
        .streak-card { background:#fff3db; border:1px solid #f1dfb9; color:#805c1d; border-radius:18px; padding:.7rem .9rem; font-size:.83rem; margin:.8rem 0; }
        .ingredient-header { display:grid; grid-template-columns:4fr 1.5fr .8fr; gap:.5rem; padding:.35rem .6rem; color:var(--muted); text-transform:uppercase; font-size:.68rem; font-weight:700; letter-spacing:.08em; border-bottom:1px solid var(--line); }
        .table-note { color:var(--muted); font-size:.78rem; margin:.2rem 0 .6rem; }
        .recipe-macros { display:flex; flex-wrap:wrap; gap:.4rem; margin:.65rem 0 .8rem; }
        .recipe-macro { background:#f1f7f2; border:1px solid #e1eee3; border-radius:10px; padding:.35rem .55rem; color:#287a56; font-size:.75rem; font-weight:700; }
        .overview-card { background:#fff; border:1px solid var(--line); border-radius:20px; padding:1rem; box-shadow:0 3px 12px #1c3a2710; }
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
        [class*="food-adjust"] button { color:#287a56 !important; }
        [class*="food-remove"] button { color:#b45d5d !important; }
        [class*="food-adjust"] button:hover { background:#eaf6ed !important; color:#173f2d !important; }
        [class*="food-remove"] button:hover { background:#fff0f0 !important; color:#8d3f3f !important; }
        [class*="food-adjust"] button:focus-visible, [class*="food-remove"] button:focus-visible { outline:2px solid #76b58c !important; outline-offset:-2px; }
        [class*="product-actions"], [class*="recipe-actions"] { display:flex; width:100%; }
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
        [class*="st-key-add_recipe_row_"] button { font-size:0 !important; color:transparent !important; }
        [class*="st-key-add_recipe_row_"] button::after { content:"+ Lisa toode"; color:#287a56; font-size:.82rem; }
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
            .food-row { border-bottom-color:var(--line); }
            .pill { background:#214b35; color:#9ae6b7; }
            .add-card { background:#173d2c; }
            .add-card-sub, .table-note, .section-hint, .metric-label, .metric-note, .food-meta, .week-day { color:var(--muted); }
            .streak-card { background:#3b301d; border-color:#665027; color:#f1ca77; }
            .recipe-macro { background:#1d3a29; border-color:#2c5a3e; color:#8ee0ac; }
            .progress, .week-track { background:#2a3931; }
            .goal-ring { background:conic-gradient(#72d09b var(--percent), #2a3931 0); }
            .goal-ring:after { background:var(--surface); }
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
            input::placeholder, textarea::placeholder { color:#8da097 !important; }
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
            .stTabs [data-baseweb="tab"] { min-width:max-content; font-size:.82rem; padding-bottom:.65rem; }
            [data-testid="stHorizontalBlock"] { gap:clamp(.15rem, 1.6vw, .45rem) !important; flex-wrap:wrap !important; max-width:100% !important; }
            [data-testid="stHorizontalBlock"] > [data-testid="column"] { min-width:0 !important; max-width:100% !important; flex:1 1 100% !important; width:100% !important; }
            [data-testid="stAppViewContainer"], [data-testid="stMainBlockContainer"] { max-width:100% !important; overflow-x:hidden !important; }
            [class*="st-key-food_actions_"] [data-testid="stHorizontalBlock"] { flex-wrap:nowrap !important; justify-content:flex-start !important; gap:clamp(.2rem, 2vw, .7rem) !important; }
            [class*="st-key-food_actions_"] [data-testid="stHorizontalBlock"] > [data-testid="column"] { flex:0 1 clamp(2.4rem, 13vw, 3.4rem) !important; width:clamp(2.4rem, 13vw, 3.4rem) !important; min-width:0 !important; padding:0 !important; }
            [class*="st-key-food_actions_"] button { width:100% !important; min-width:0 !important; padding:.35rem .2rem !important; font-size:clamp(.78rem, 3.5vw, 1rem) !important; }
            [class*="food-actions"] [data-testid="stHorizontalBlock"] { flex-wrap:nowrap !important; justify-content:flex-start !important; gap:clamp(.2rem, 2vw, .7rem) !important; }
            [class*="food-actions"] [data-testid="stHorizontalBlock"] > [data-testid="column"] { flex:0 0 clamp(2.4rem, 13vw, 3.4rem) !important; width:clamp(2.4rem, 13vw, 3.4rem) !important; min-width:0 !important; padding:0 !important; }
            [class*="food-actions"] button { width:100% !important; min-width:0 !important; padding:.35rem .2rem !important; font-size:clamp(.78rem, 3.5vw, 1rem) !important; }
            .goal-card { border-radius:20px; padding:.8rem; gap:.7rem; }
            .goal-ring { width:72px; height:72px; } .goal-ring:after { width:55px; height:55px; }
            .goal-copy .metric-value { font-size:1.2rem; } .metric-note { font-size:.68rem; }
            .metric-card { min-height:82px; padding:.75rem .65rem; border-radius:16px; }
            .metric-value { font-size:1.15rem; }
            .food-row { padding:.78rem .7rem; }
            .food-name { font-size:.9rem; } .food-meta { font-size:.68rem; }
            .food-kcal { font-size:.82rem; }
            .add-card { margin-top:.8rem; padding:.85rem; border-radius:17px; }
            .streak-card { font-size:.76rem; padding:.65rem .75rem; }
            .ingredient-header { grid-template-columns:3fr 1.3fr .5fr; font-size:.6rem; padding:.3rem .25rem; }
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
        </style>
        """,
        unsafe_allow_html=True,
    )


css()
st.markdown(f'<div class="hero"><div class="hero-title">Tere hommikust, Alfred ✦</div></div>', unsafe_allow_html=True)

tab_today, tab_add, tab_calendar, tab_recipes, tab_insights = st.tabs(["Täna", "Lisa toit", "Kalender", "Retseptid", "Ülevaade"])

with tab_today:
    if st.session_state.pop("last_added_message", None):
        st.success("Toit on kohe tänases logis.")
    today_entries = entries_for(TODAY)
    displayed_today_entries = grouped_log_entries(today_entries)
    t = totals(TODAY)
    goal = st.session_state.goals["kcal"]
    remaining = max(0, goal - int(t["kcal"]))
    percent = min(100, int(t["kcal"] / goal * 100))
    st.markdown(f'<div class="goal-card"><div class="goal-ring" style="--percent:{percent}%"><span>{percent}%</span></div><div class="goal-copy"><div class="metric-label">PÄEVA EESMÄRK</div><div class="metric-value">{int(t["kcal"]):,} <span style="font-size:.85rem;color:#78857d;font-weight:500">/ {goal:,} kcal</span></div><div class="metric-note">{remaining:,} kcal alles · {len(today_entries)} toidukirjet</div></div></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="streak-card">🔥 <b>{streak_count()} päeva järjest</b> · oled oma logimisega heas rütmis</div>', unsafe_allow_html=True)
    st.write("")
    c1, c2, c3 = st.columns(3)
    macro_goal_values = iter((st.session_state.goals["protein"], st.session_state.goals["carbs"], st.session_state.goals["fat"]))
    for col, label, value, goal_value in [(c1, "Valk", t["protein"], 140), (c2, "Süsivesikud", t["carbs"], 250), (c3, "Rasv", t["fat"], 70)]:
        with col:
            goal_value = next(macro_goal_values)
            st.markdown(f'<div class="metric-card"><div class="metric-label">{label.upper()}</div><div class="metric-value">{int(value)}g</div><div class="metric-note">/{goal_value}g</div></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title"><h2>Tänane logi</h2><span class="section-hint">{TODAY.strftime("%d. %b")}</span></div>', unsafe_allow_html=True)
    if not today_entries:
        st.info("Sinu päev on tühi. Lisa esimene toit allpool.")
    for i, item in enumerate(displayed_today_entries):
        is_recipe = item.get("meal") == "Retsept"
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
with tab_add:
    st.markdown("## Lisa toit")
    add_mode = st.radio("Vali viis", ["Otsi toitu", "Sisesta ise"], horizontal=True, label_visibility="collapsed")
    if add_mode == "Otsi toitu":
        query = st.text_input("Otsi toodet", placeholder="nt kohuke, rukkileib, skyr…", key="food_search_query")
        filtered = [p for p in all_products() if not query or query.lower() in (p["name"] + " " + p["brand"]).lower()]
        for idx, product in enumerate(filtered[:15]):
            st.markdown(f'**{product["name"]}**  \n<span style="color:#718078;font-size:.8rem">{product["brand"]} · {product["portion"]} · {product["kcal"]} kcal</span>  \n<span style="color:#287a56;font-size:.75rem;font-weight:600">Valk {product["protein"]}g · Süsivesikud {product["carbs"]}g · Rasv {product["fat"]}g</span>', unsafe_allow_html=True)
            with st.container(key=f"product-actions-{idx}", horizontal=True, width="stretch", horizontal_alignment="distribute", gap="small", vertical_alignment="center"):
                if st.button("Lisa", type="primary", key=f"add_{idx}_{product['name']}"):
                    add_entry(product, day=TODAY)
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
                inline_meal = st.selectbox("Toidukord", ["Hommikusöök", "Lõuna", "Õhtusöök", "Vahepala"])
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
                    add_entry(new_product, inline_meal, TODAY)
                    st.session_state.inline_create_food = ""
                    st.rerun()
    else:
        with st.form("manual_food"):
            name = st.text_input("Toidu nimi", placeholder="nt õhtusöök")
            meal = st.selectbox("Toidukord", ["Hommikusöök", "Lõuna", "Õhtusöök", "Vahepala"])
            nutrition_basis = st.selectbox("Toiteväärtus käib", ["100 g", "100 ml", "1 tk", "1 portsjon"], help="Märgi, mille kohta pakendil või sinu andmetes kalorid ja makrod käivad.")
            c1, c2 = st.columns(2)
            with c1:
                kcal = st.number_input("Kalorid", min_value=0, value=300)
                protein = st.number_input("Valk (g)", min_value=0, value=20)
            with c2:
                carbs = st.number_input("Süsivesikud (g)", min_value=0, value=30)
                fat = st.number_input("Rasv (g)", min_value=0, value=10)
            save_product = st.checkbox("Salvesta see toit toodete alla järgmiseks korraks", value=True)
            if st.form_submit_button("Lisa logisse", type="primary", use_container_width=True) and name:
                new_product = {"name": name, "brand": "Minu toit", "kcal": kcal, "protein": protein, "carbs": carbs, "fat": fat, "portion": nutrition_basis}
                if save_product:
                    save_custom_product(new_product)
                add_entry(new_product, meal, TODAY)
                st.rerun()

with tab_calendar:
    st.markdown("## Kalender")
    selected_day = st.date_input("Vali päev", value=TODAY, min_value=TODAY - timedelta(days=365), max_value=TODAY, format="DD.MM.YYYY", key="calendar_day")
    st.session_state.active_date = selected_day
    selected_entries = entries_for(selected_day)
    selected_totals = totals(selected_day)
    st.markdown(f'<div class="goal-card"><div class="goal-copy"><div class="metric-label">{selected_day.strftime("%d. %B %Y").upper()}</div><div class="metric-value">{int(selected_totals["kcal"]):,} kcal</div><div class="metric-note">{len(selected_entries)} toidukirjet · {int(selected_totals["protein"])}g valku</div></div></div>', unsafe_allow_html=True)
    st.markdown("### Selle päeva toit")
    if not selected_entries:
        st.info("Sellel päeval pole veel toite logitud.")
    for index, item in enumerate(selected_entries):
        left, right = st.columns([6, 1])
        with left:
            st.markdown(f'<div class="food-row"><div><div class="pill">{item.get("meal", "Toit")}</div><div class="food-name">{item["name"]}</div><div class="food-meta">{item.get("time", "")}</div></div><div class="food-kcal">{int(item["kcal"])} kcal</div></div>', unsafe_allow_html=True)
        with right:
            if st.button("×", key=f"remove_calendar_{selected_day}_{index}", help="Eemalda see toit"):
                remove_entry(index, selected_day)
                st.rerun()
    logged_days = sorted(st.session_state.daily_logs.keys(), reverse=True)

with tab_recipes:
    st.markdown("## Retseptid")
    if st.session_state.pop("recipe_saved_message", None):
        st.success("Uus retsept on kohe nimekirjas.")
    recipe_query = st.text_input("Otsi retsepti", placeholder="nt kana, hommikusöök…", key="recipe_query")
    visible_recipes = [r for r in all_recipes() if not recipe_query or recipe_query.lower() in (r.get("name", "") + " " + r.get("ingredients", "")).lower()]
    for index, recipe in enumerate(visible_recipes):
        with st.expander(f'{recipe["name"]} · {recipe["kcal"]} kcal', expanded=False):
            st.markdown(f'<div class="recipe-macros"><span class="recipe-macro">{int(recipe["kcal"])} kcal</span><span class="recipe-macro">Valk {int(recipe["protein"])} g</span><span class="recipe-macro">Süsivesikud {int(recipe["carbs"])} g</span><span class="recipe-macro">Rasv {int(recipe["fat"])} g</span></div>', unsafe_allow_html=True)
            recipe_ingredients = recipe.get("ingredients_data", [])
            if recipe_ingredients:
                st.markdown('<div class="ingredient-header"><span>Toode</span><span>Kaal</span><span></span></div>', unsafe_allow_html=True)
                for ingredient in recipe_ingredients:
                    read_product_col, read_weight_col, _ = st.columns([4, 1.5, .8])
                    with read_product_col:
                        st.write(ingredient["name"])
                    with read_weight_col:
                        st.write(f'{ingredient["grams"]} g')
            else:
                st.write("")
            with st.container(key=f"recipe-actions-{index}", horizontal=True, width="stretch", horizontal_alignment="distribute", gap="small", vertical_alignment="center"):
                with st.popover("✎", help="Muuda retsepti"):
                    edit_key = f"recipe_edit_data_{index}"
                    if edit_key not in st.session_state:
                        st.session_state[edit_key] = json.loads(json.dumps(recipe))
                    edit_data = st.session_state[edit_key]
                    edited_ingredients_data = edit_data.setdefault("ingredients_data", [])
                    edit_name = st.text_input("Retsepti nimi", value=edit_data["name"], key=f"recipe_name_{index}")
                    st.markdown("**Koostisosad**")
                    recipe_products = all_products()
                    recipe_labels = [f'{product["name"]} · {product["brand"]}' for product in recipe_products]
                    st.markdown('<div class="ingredient-header"><span>Toode</span><span>Kaal</span><span></span></div>', unsafe_allow_html=True)
                    for ingredient_index, ingredient in enumerate(edited_ingredients_data):
                        product_col, grams_col, remove_col = st.columns([4, 1.5, .8])
                        with product_col:
                            current_label = next((label for label in recipe_labels if label.startswith(f'{ingredient["name"]} ·')), recipe_labels[0] if recipe_labels else "")
                            selected_label = st.selectbox("Toode", recipe_labels, index=recipe_labels.index(current_label) if current_label in recipe_labels else 0, key=f"recipe_product_{index}_{ingredient_index}", label_visibility="collapsed") if recipe_labels else ""
                            if selected_label:
                                ingredient["name"] = selected_label.rsplit(" · ", 1)[0]
                        with grams_col:
                            ingredient["grams"] = st.number_input("Kaal (g)", min_value=1, value=int(ingredient.get("grams", 100)), step=5, key=f"recipe_grams_{index}_{ingredient_index}", label_visibility="collapsed")
                        with remove_col:
                            if st.button("×", key=f"remove_recipe_row_{index}_{ingredient_index}", help="Eemalda rida"):
                                edited_ingredients_data.pop(ingredient_index)
                                st.rerun()
                    if st.button("＋ Lisa toode", key=f"add_recipe_row_{index}", use_container_width=True):
                        if recipe_products:
                            edited_ingredients_data.append({"name": recipe_products[0]["name"], "grams": 100})
                            st.rerun()
                    auto_totals = calculate_recipe_ingredients(edited_ingredients_data)
                    st.info(f'Kokku: {int(auto_totals["kcal"])} kcal · {int(auto_totals["protein"])}g valku · {int(auto_totals["carbs"])}g süsivesikuid · {int(auto_totals["fat"])}g rasva')
                    edit_ingredients = " · ".join(f'{item["name"]} ({item["grams"]} g)' for item in edited_ingredients_data)
                    if st.button("Salvesta retsept", type="primary", use_container_width=True, key=f"save_recipe_{index}"):
                        if not edited_ingredients_data:
                            st.warning("Retseptil peab olema vähemalt üks toode.")
                        else:
                            normalized_ingredients = [{"name": item["name"], "grams": item["grams"]} for item in edited_ingredients_data]
                            save_custom_recipe({"name": edit_name.strip(), "tag": "", "kcal": int(auto_totals["kcal"]), "protein": int(auto_totals["protein"]), "carbs": int(auto_totals["carbs"]), "fat": int(auto_totals["fat"]), "time": "", "ingredients": edit_ingredients, "ingredients_data": normalized_ingredients})
                            del st.session_state[edit_key]
                            st.rerun()
                if st.button("🗑", key=f"delete_recipe_{index}", help="Kustuta retsept"):
                    delete_custom_recipe(recipe["name"])
                    st.rerun()
            if st.button("Lisa tänasesse", key=f"recipe_add_{index}", use_container_width=True):
                add_entry(recipe, "Retsept", TODAY)
                st.rerun()

    st.markdown("### Lisa uus retsept")
    new_name = st.text_input("Retsepti nimi", placeholder="nt minu õhtusöök", key="new_recipe_name")
    recipe_products = all_products()
    if recipe_products:
        recipe_labels = [f'{p["name"]} · {p["brand"]}' for p in recipe_products]
        ingredient_col, grams_col, add_col = st.columns([4, 2, 1])
        with ingredient_col:
            selected_ingredient_label = st.selectbox("Toode", recipe_labels, key="recipe_ingredient_product")
        with grams_col:
            ingredient_grams = st.number_input("Grammid", min_value=1, value=100, step=5, key="recipe_ingredient_grams")
        with add_col:
            st.write("")
            if st.button("Lisa", key="recipe_add_ingredient"):
                selected_product = recipe_products[recipe_labels.index(selected_ingredient_label)]
                existing_ingredient = next((item for item in st.session_state.recipe_builder if item["name"] == selected_product["name"]), None)
                if existing_ingredient:
                    existing_ingredient["grams"] += ingredient_grams
                else:
                    st.session_state.recipe_builder.append({"name": selected_product["name"], "grams": ingredient_grams})
                st.rerun()

    if st.session_state.recipe_builder:
        st.markdown("**Retsepti koostisosad**")
        st.markdown('<div class="ingredient-header"><span>Toode</span><span>Kaal</span><span></span></div>', unsafe_allow_html=True)
        for ingredient_index, ingredient in enumerate(st.session_state.recipe_builder):
            ingredient_product = next((p for p in recipe_products if p["name"] == ingredient["name"]), None)
            ingredient_kcal = calculate_recipe_ingredients([ingredient])["kcal"]
            row_product, row_weight, row_remove = st.columns([4, 2, 1])
            with row_product:
                st.write(ingredient["name"])
            with row_weight:
                st.write(f'{ingredient["grams"]} g · {int(ingredient_kcal)} kcal')
            with row_remove:
                if st.button("×", key=f"remove_recipe_ingredient_{ingredient_index}"):
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
            normalized_ingredients = [{"name": item["name"], "grams": item["grams"]} for item in st.session_state.recipe_builder]
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

