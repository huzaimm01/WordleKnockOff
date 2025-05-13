import random
import datetime
from core.data import load_json, save_json
from config import NUM_DAILY_PUZZLES

def generate_daily_seed():
    today = datetime.date.today().isoformat()
    return today

def get_daily_words():
    regular = open("assets/words.txt").read().splitlines()
    fun = open("assets/funwords.txt").read().splitlines()
    today = generate_daily_seed()

    saved = load_json("data/puzzles.json")
    if today in saved:
        return saved[today]

    chosen = random.sample(regular, NUM_DAILY_PUZZLES - 1)
    chosen.append(random.choice(fun))
    random.shuffle(chosen)

    saved[today] = chosen
    save_json("data/puzzles.json", saved)
    return chosen
