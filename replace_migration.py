import os
import sys
import shutil
import json
import datetime

OLD = "billingconsole.amazonaws.com"
NEW = "freetier.amazonaws.com"

IGNORED_FILES = {
    ".git",
    "search_billingconsole.py",
    "report.json",
    "report_replacements.json"
    "replace_migration.py"
}

REPORT = {
    "timestamp": "",
    "replacements": []
}

def ask(prompt):
    while True:
        ans = input(prompt + " (y/n): ").lower().strip()
        if ans in ("y", "yes"):
            return True
        if ans in ("n", "no"):
            return False
        print("Please answer y or n.")

def save_report():
    REPORT["timestamp"] = datetime.datetime.utcnow().isoformat() + "Z"

    with open("report_replacements.json", "w", encoding="utf-8") as f:
        json.dump(REPORT, f, indent=4)

    print("\n📄 report_replacements.json generated.\n")

def process_file(path):
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
    except:
        return

    modified = False
    file_changes = []

    for i, line in enumerate(lines):
        if OLD in line:
            print("\n File:", path)
            print(f"  Line {i+1}: {line.strip()}")

            if ask(f"Replace '{OLD}' with '{NEW}' ?"):
                new_line = line.replace(OLD, NEW)
                file_changes.append({
                    "file": path,
                    "line_number": i + 1,
                    "old_line": line.strip(),
                    "new_line": new_line.strip(),
                    "status": "accepted"
    
                })
                lines[i] = new_line
                modified = True
            else:
                file_changes.append({
                    "file": path,
                    "line_number": i + 1,
                    "old_line": line.strip(),
                    "new_line": line.strip(),
                    "status": "rejected"
                })

    if file_changes:
        REPORT["replacements"].extend(file_changes)

    if modified:
        backup_path = path + ".backup_before_replacement"
        shutil.copy2(path, backup_path)
        print(f"   Backup saved: {backup_path}")

        with open(path, "w", encoding="utf-8", errors="ignore") as f:
            f.writelines(lines)

        print(f"   Updated file: {path}")

def scan_repo(base="."):

    for root, dirs, files in os.walk(base):

        if ".git" in root:
            continue

        for filename in files:

            if filename in IGNORED_FILES:
                continue

            process_file(os.path.join(root, filename))


if __name__ == "__main__":
    print("\n=== CloudTrail Interactive Replacer ===")
    print(f"Replacing '{OLD}' → '{NEW}'\n")

    scan_repo(".")
    save_report()

    print("\n Replacement process completed.\n")

