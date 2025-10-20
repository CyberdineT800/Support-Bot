import json
from datetime import datetime, timedelta
import os

STATS_FILE = "data/stats.json"

def load_stats():
    if not os.path.exists(STATS_FILE):
        stats = {
            "offer": {"daily": 0, "weekly": 0, "monthly": 0, "yearly": 0, "total": 0, "last_update": str(datetime.now().date())},
            "problem": {"daily": 0, "weekly": 0, "monthly": 0, "yearly": 0, "total": 0, "last_update": str(datetime.now().date())}
        }
        save_stats(stats)
    else:
        with open(STATS_FILE, "r") as file:
            stats = json.load(file)
    return stats

def save_stats(stats):
    with open(STATS_FILE, "w") as file:
        json.dump(stats, file, indent=4)

def reset_counters_if_needed(stats, key):
    last_update = datetime.strptime(stats[key]["last_update"], "%Y-%m-%d").date()
    now = datetime.now()
    today = now.date()
    start_of_week = today - timedelta(days=today.weekday())
    start_of_month = today.replace(day=1)
    start_of_year = today.replace(month=1, day=1)

    if last_update < today:
        stats[key]["daily"] = 0
        stats[key]["last_update"] = str(today)
    if last_update < start_of_week:
        stats[key]["weekly"] = 0
    if last_update < start_of_month:
        stats[key]["monthly"] = 0
    if last_update < start_of_year:
        stats[key]["yearly"] = 0

def update_stats(category):
    stats = load_stats()
    reset_counters_if_needed(stats, category)

    stats[category]["daily"] += 1
    stats[category]["weekly"] += 1
    stats[category]["monthly"] += 1
    stats[category]["yearly"] += 1
    stats[category]["total"] += 1

    save_stats(stats)

def get_stats():
    stats = load_stats()
    
    reset_counters_if_needed(stats, 'offer')
    reset_counters_if_needed(stats, 'problem')
    
    save_stats(stats)
    
    return stats

# update_stats("offer")  
# update_stats("problem")  

# current_stats = get_stats()
# print(json.dumps(current_stats, indent=4))
