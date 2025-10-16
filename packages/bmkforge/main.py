#!/usr/bin/env python3
import os, time, platform, json, urllib.request

# ────────────────────────────────────────────────
# BMKForge - Hardhat Edition
# Pure Python Benchmark CLI
# By Yixuan (2025)
# ────────────────────────────────────────────────

BMK_REPO = "https://raw.githubusercontent.com/YixuanXuDev/BMKForgeBenchmarks/main/"
BENCH_DIR = "benchmarks"
RESULT_DIR = "results"
RESULT_FILE = os.path.join(RESULT_DIR, "leaderboard.json")

# ────────────────────────────────────────────────
# Utility Functions
# ────────────────────────────────────────────────
def setup_environment():
    """Create folders if missing."""
    for d in [BENCH_DIR, RESULT_DIR]:
        if not os.path.exists(d):
            os.makedirs(d)
    if not os.path.exists(RESULT_FILE):
        with open(RESULT_FILE, "w") as f:
            json.dump([], f)

def color(text, code):
    """ANSI color helper."""
    return f"\033[{code}m{text}\033[0m"

def header():
    """Display header banner."""
    print(color("█▄▄ ▄▀█ █▀▄ █▄░█ █▄▀ █▀▀ █▀█ █▀▀", "95"))
    print(color("█▄█ █▀█ █▄▀ █░▀█ █░█ ██▄ █▀▄ █▄█", "95"))
    print(color("      Forge your performance.\n", "90"))

# ────────────────────────────────────────────────
# Core Logic
# ────────────────────────────────────────────────
def get_hardware_info():
    """Get basic system information."""
    return {
        "CPU": platform.processor() or "Unknown CPU",
        "OS": platform.system() + " " + platform.release(),
        "Arch": platform.machine(),
    }

def download_bmk(name):
    """Download a .bmk file from GitHub."""
    url = BMK_REPO + name
    path = os.path.join(BENCH_DIR, name)
    print(f"[BMKForge] Downloading {name}...")
    try:
        urllib.request.urlretrieve(url, path)
        print(color(f"[BMKForge] Download complete: {path}\n", "92"))
    except Exception as e:
        print(color(f"[Error] Failed to download: {e}", "91"))

def run_benchmark(file_path):
    """Run the benchmark test."""
    if not os.path.exists(file_path):
        print(color("[Error] File not found.", "91"))
        return

    size_gb = os.path.getsize(file_path) / (1024**3)
    print(color(f"[BMKForge] Running benchmark on {os.path.basename(file_path)}", "94"))
    print(f"File size: {size_gb:.2f} GB\n")

    start = time.time()
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            data = f.read()
    except Exception:
        with open(file_path, "rb") as f:
            data = f.read()
    end = time.time()

    elapsed = end - start
    throughput = (size_gb * 1024) / elapsed  # MB/s
    info = get_hardware_info()
    score, rank = calculate_rank(size_gb, elapsed)

    result = {
        "CPU": info["CPU"],
        "OS": info["OS"],
        "File": os.path.basename(file_path),
        "SizeGB": round(size_gb, 2),
        "TimeS": round(elapsed, 2),
        "SpeedMBs": round(throughput, 2),
        "Score": score,
        "Rank": rank,
    }

    print("\n──────────────────────────────")
    print(color(f"🏆 Rank: {rank}", "93"))
    print(f"Score: {score}")
    print(f"Load Time: {elapsed:.2f}s | Speed: {throughput:.2f} MB/s")
    print("──────────────────────────────\n")

    save_result(result)

def calculate_rank(size_gb, elapsed):
    """Score and rank calculation."""
    score = int((size_gb / elapsed) * 100)
    if score > 8000:
        rank = "S+"
    elif score > 6000:
        rank = "S"
    elif score > 4000:
        rank = "A"
    elif score > 2000:
        rank = "B"
    elif score > 1000:
        rank = "C"
    else:
        rank = "D"
    return score, rank

def save_result(result):
    """Save results to leaderboard."""
    with open(RESULT_FILE, "r+") as f:
        data = json.load(f)
        data.append(result)
        f.seek(0)
        json.dump(data, f, indent=2)
    print(color("[BMKForge] Result saved to leaderboard.\n", "92"))

def show_leaderboard():
    """Display past benchmark results."""
    if not os.path.exists(RESULT_FILE):
        print(color("No results found.\n", "93"))
        return

    with open(RESULT_FILE, "r") as f:
        results = json.load(f)

    if not results:
        print(color("No results yet.\n", "93"))
        return

    print(color("─── Leaderboard ────────────────────────", "96"))
    for r in results[-10:][::-1]:  # show latest 10
        print(f"{r['CPU']} | {r['File']} | {r['Rank']} | {r['Score']} pts")
    print(color("────────────────────────────────────────\n", "96"))

# ────────────────────────────────────────────────
# Main CLI Loop
# ────────────────────────────────────────────────
def main():
    setup_environment()
    header()

    while True:
        cmd = input(color("> ", "96")).strip().split()
        if not cmd:
            continue

        if cmd[0] == "exit":
            print(color("Goodbye, Operator.\n", "90"))
            break
        elif cmd[0] == "get":
            if len(cmd) < 2:
                print("Usage: get [filename.bmk]\n")
            else:
                download_bmk(cmd[1])
        elif cmd[0] == "run":
            if len(cmd) < 2:
                print("Usage: run [path/to/file.bmk]\n")
            else:
                run_benchmark(cmd[1])
        elif cmd[0] == "info":
            print(json.dumps(get_hardware_info(), indent=2), "\n")
        elif cmd[0] == "leaderboard":
            show_leaderboard()
        elif cmd[0] == "help":
            print("""
Commands:
  get [file.bmk]       Download benchmark file
  run [file.bmk]       Run benchmark
  info                 Show hardware info
  leaderboard          Show saved results
  exit                 Quit BMKForge
""")
        else:
            print(color("[Error] Unknown command. Type 'help' for options.\n", "91"))

# ────────────────────────────────────────────────
if __name__ == "__main__":
    main()
