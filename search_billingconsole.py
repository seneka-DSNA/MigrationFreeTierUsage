import os
import sys
import json
import datetime

KEYWORDS = [
    "billingconsole.amazonaws.com",
    "freetier.amazonaws.com",
    "GetFreeTierUsage"
]

IGNORED_FILES = {
    ".git",
    "search_billingconsole.py",
    "report.json",
    "report_replacements.json"
    "replace_migration.py"
}

REPORT = {
    "timestamp": "",
    "matches": []
}

def scan_repo(base="."):
    for root, dirs, files in os.walk(base):

        # Skip .git folder entirely
        if ".git" in root:
            continue

        for filename in files:

            # Skip ignored files
            if filename in IGNORED_FILES:
                continue

            path = os.path.join(root, filename)

            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    lines = f.readlines()
            except:
                continue

            for i, line in enumerate(lines, start=1):
                for kw in KEYWORDS:
                    if kw in line:
                        REPORT["matches"].append({
                            "file": path,
                            "line_number": i,
                            "keyword": kw,
                            "content": line.strip()
                        })

def save_report():
    REPORT["timestamp"] = datetime.datetime.utcnow().isoformat() + "Z"

    with open("report.json", "w", encoding="utf-8") as f:
        json.dump(REPORT, f, indent=4)

    print("\n📄 report.json generated.")

def print_results():
    if not REPORT["matches"]:
        print("No matches found.")
        return

    print("\n=== MATCHES FOUND ===\n")

    for entry in REPORT["matches"]:
        print(f"📌 File: {entry['file']}")
        print(f"  Line {entry['line_number']} | Keyword: {entry['keyword']}")
        print(f"    → {entry['content']}\n")


if __name__ == "__main__":
    print("\n=== CloudTrail Scanner ===\n")
    scan_repo(".")
    print_results()
    save_report()
    print("\n✅ Scan complete.\n")

