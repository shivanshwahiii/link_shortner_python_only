import random
import string
import json
import os
from datetime import datetime

DATA_FILE = "urls.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_data(url_map):
    with open(DATA_FILE, "w") as f:
        json.dump(url_map, f, indent=2)

def generate_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def shorten(url_map, url, custom_code=None):
    # Check if URL already exists
    for code, data in url_map.items():
        if data["url"] == url:
            print(f"(Already shortened before)")
            return f"http://short.ly/{code}"

    code = custom_code if custom_code else generate_code()

    if code in url_map:
        print("That custom code is already taken. Try another.")
        return None

    url_map[code] = {
        "url": url,
        "clicks": 0,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    save_data(url_map)
    return f"http://short.ly/{code}"

def expand(url_map, short_url):
    code = short_url.strip().split("/")[-1]
    if code in url_map:
        url_map[code]["clicks"] += 1
        save_data(url_map)
        return url_map[code]["url"]
    return None

def show_stats(url_map):
    if not url_map:
        print("No URLs stored yet.")
        return
    print(f"\n{'Code':<10} {'Clicks':<8} {'Created':<22} URL")
    print("-" * 75)
    for code, data in url_map.items():
        print(f"{code:<10} {data['clicks']:<8} {data['created_at']:<22} {data['url']}")

def delete_url(url_map, short_url):
    code = short_url.strip().split("/")[-1]
    if code in url_map:
        del url_map[code]
        save_data(url_map)
        print(f"Deleted /{code}")
    else:
        print("Code not found.")

def search(url_map, keyword):
    results = [(c, d) for c, d in url_map.items() if keyword.lower() in d["url"].lower()]
    if not results:
        print("No matches found.")
    for code, data in results:
        print(f"  http://short.ly/{code}  ->  {data['url']}")

# --- CLI ---
url_map = load_data()

print("=== URL Shortener ===")
while True:
    print("\n1. Shorten URL")
    print("2. Expand URL")
    print("3. View all stats")
    print("4. Delete a URL")
    print("5. Search URLs")
    print("6. Quit")
    choice = input("\nChoose: ").strip()

    if choice == "1":
        url = input("Enter URL: ").strip()
        custom = input("Custom code? (leave blank for random): ").strip()
        result = shorten(url_map, url, custom or None)
        if result:
            print("Short URL:", result)

    elif choice == "2":
        short = input("Enter short URL or code: ").strip()
        original = expand(url_map, short)
        if original:
            print("Original URL:", original)
        else:
            print("URL not found.")

    elif choice == "3":
        show_stats(url_map)

    elif choice == "4":
        short = input("Enter short URL or code to delete: ").strip()
        delete_url(url_map, short)

    elif choice == "5":
        keyword = input("Search keyword: ").strip()
        search(url_map, keyword)

    elif choice == "6":
        print("Over and out...")
        break

    else:
        print("Invalid choice.")
