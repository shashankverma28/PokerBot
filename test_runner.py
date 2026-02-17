import subprocess
import datetime
import os
from collections import Counter

BOT_COMMAND = ["python", "bot.py"]
OUTPUT_FILE = "test_results.txt"


def timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def classify_action(output_line):
    """Classify bot action for statistics"""
    if output_line.startswith("RAISE"):
        return "RAISE"
    if output_line.startswith("CALL"):
        return "CALL"
    if output_line.startswith("CHECK"):
        return "CHECK"
    if output_line.startswith("FOLD"):
        return "FOLD"
    return "OTHER"


def run_test_case(name, input_data, repeats):

    stats = Counter()

    with open(OUTPUT_FILE, "a", encoding="utf-8") as f:

        f.write("\n" + "=" * 80 + "\n")
        f.write(f"TEST CASE: {name}\n")
        f.write(f"REPEATS: {repeats}\n")
        f.write(f"TIME: {timestamp()}\n")
        f.write("=" * 80 + "\n")

        for i in range(repeats):

            process = subprocess.Popen(
                BOT_COMMAND,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            out, err = process.communicate(input_data)

            action = out.strip()
            action_type = classify_action(action)
            stats[action_type] += 1

            f.write(f"\n--- RUN {i+1} ---\n")

            f.write("\nINPUT:\n")
            f.write(input_data.strip() + "\n")

            f.write("\nOUTPUT:\n")
            f.write(action + "\n")

            if err.strip():
                f.write("\nDEBUG:\n")
                f.write(err.strip() + "\n")

        # ----- Summary -----
        f.write("\n--- SUMMARY ---\n")

        total = sum(stats.values())

        for key in ["RAISE", "CALL", "CHECK", "FOLD", "OTHER"]:
            count = stats.get(key, 0)
            pct = (count / total * 100) if total > 0 else 0
            f.write(f"{key}: {count} ({pct:.1f}%)\n")

        f.write("\n")

    print(f"Completed: {name}")


def main():

    # Clear old results
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)

    tests = [

        # Strong hand
        ("Strong Hand Raise",
         """NEWGAME botA botB 200 2 1000 10.0
NEWHAND 1 1 Ah Kd 200 200 10.0
GETACTION 20 3 Qh Jh Tc 0 3 FOLD CALL:10 RAISE:10:50 10.0
""", 10),

        # Cheap call
        ("Cheap Call Weak",
         """NEWGAME botA botB 200 2 1000 10.0
NEWHAND 2 1 7c 2d 200 200 10.0
GETACTION 100 3 Ah Kh Qh 0 2 CALL:5 FOLD 10.0
""", 10),

        # Expensive call
        ("Expensive Call Weak",
         """NEWGAME botA botB 200 2 1000 10.0
NEWHAND 3 1 7c 2d 200 200 10.0
GETACTION 100 3 Ah Kh Qh 0 2 CALL:80 FOLD 10.0
""", 10),

        # Medium hand
        ("Medium Strength",
         """NEWGAME botA botB 200 2 1000 10.0
NEWHAND 4 1 9h 9d 200 200 10.0
GETACTION 50 3 Ah 7c 2s 0 3 CALL:10 FOLD RAISE:10:60 10.0
""", 10),

        # Check free
        ("Free Check",
         """NEWGAME botA botB 200 2 1000 10.0
NEWHAND 5 1 5h 6d 200 200 10.0
GETACTION 30 3 Ah Kd Qs 0 2 CHECK FOLD 10.0
""", 10),

        # No raise available
        ("No Raise Available",
         """NEWGAME botA botB 200 2 1000 10.0
NEWHAND 6 1 Ah Ad 200 200 10.0
GETACTION 40 3 2c 7d 9h 0 2 CALL:10 FOLD 10.0
""", 10),

        # Bluff scenario
        ("Bluff Opportunity",
         """NEWGAME botA botB 200 2 1000 10.0
NEWHAND 7 1 2c 7d 200 200 10.0
GETACTION 30 3 Ah Kd Qs 0 3 FOLD CALL:10 RAISE:10:40 10.0
""", 20),

        # Opponent folds a lot
        ("Opponent Fold Heavy",
         """NEWGAME botA botB 200 2 1000 10.0
NEWHAND 8 1 4c 8d 200 200 10.0
GETACTION 40 3 Ah Kh Qh 3 FOLD FOLD FOLD 3 FOLD CALL:10 RAISE:10:50 10.0
""", 20),

        # Opponent aggressive
        ("Opponent Aggressive",
         """NEWGAME botA botB 200 2 1000 10.0
NEWHAND 9 1 4c 8d 200 200 10.0
GETACTION 40 3 Ah Kh Qh 3 RAISE:20 RAISE:30 RAISE:40 3 FOLD CALL:20 RAISE:20:60 10.0
""", 20),

        # Preflop strong
        ("Preflop Strong",
         """NEWGAME botA botB 200 2 1000 10.0
NEWHAND 10 1 Ah Ad 200 200 10.0
GETACTION 10 0 0 3 FOLD CALL:2 RAISE:4:20 10.0
""", 15),

        # Preflop weak
        ("Preflop Weak",
         """NEWGAME botA botB 200 2 1000 10.0
NEWHAND 11 1 2c 7d 200 200 10.0
GETACTION 10 0 0 2 CALL:2 FOLD 10.0
""", 15),

        # Large pot
        ("Large Pot",
         """NEWGAME botA botB 200 2 1000 10.0
NEWHAND 12 1 Kh Qh 200 200 10.0
GETACTION 300 3 Ah Jh Tc 0 3 FOLD CALL:50 RAISE:50:200 10.0
""", 10),

        # Raise clamp
        ("Raise Clamp",
         """NEWGAME botA botB 200 2 1000 10.0
NEWHAND 13 1 Ah Kd 200 200 10.0
GETACTION 10 3 Qh Jh Tc 0 3 FOLD CALL:5 RAISE:5:12 10.0
""", 10),

        # River full board
        ("River Full Board",
         """NEWGAME botA botB 200 2 1000 10.0
NEWHAND 14 1 Ah Kd 200 200 10.0
GETACTION 100 5 Qh Jh Tc 2d 9s 0 3 FOLD CALL:20 RAISE:20:80 10.0
""", 10),

        # Only fold
        ("Only Fold Legal",
         """NEWGAME botA botB 200 2 1000 10.0
NEWHAND 15 1 Ah Kd 200 200 10.0
GETACTION 50 3 Qh Jh Tc 0 1 FOLD 10.0
""", 5),

        # Only check
        ("Only Check Legal",
         """NEWGAME botA botB 200 2 1000 10.0
NEWHAND 16 1 Ah Kd 200 200 10.0
GETACTION 50 3 Qh Jh Tc 0 1 CHECK 10.0
""", 5),

    ]

    for name, data, reps in tests:
        run_test_case(name, data, reps)

    print("\nAll tests completed.")
    print(f"Results saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
