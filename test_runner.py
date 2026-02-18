import subprocess
import datetime
import os
from collections import Counter

BOT_COMMAND = ["python", "bot.py"]
OUTPUT_FILE = "test_results.txt"


def timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def classify_action(output_line):
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

        f.write("\n--- SUMMARY ---\n")

        total = sum(stats.values())

        for key in ["RAISE", "CALL", "CHECK", "FOLD", "OTHER"]:
            count = stats.get(key, 0)
            pct = (count / total * 100) if total > 0 else 0
            f.write(f"{key}: {count} ({pct:.1f}%)\n")

        f.write("\n")

    print(f"Completed: {name}")


def main():

    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)

    tests = [

        # =========================================================
        # PREFLOISE PREFLOP — POSITION + RANGE VALIDATION
        # =========================================================

        ("Preflop Premium BTN",
        """NEWGAME botA botB 200 2 1000 10.0
    NEWHAND 1 1 Ah Ad 200 200 10.0
    GETACTION 10 0 0 3 FOLD CALL:2 RAISE:4:20 10.0
    """, 25),

        ("Preflop Premium BB",
        """NEWGAME botA botB 200 2 1000 10.0
    NEWHAND 2 0 Ah Ad 200 200 10.0
    GETACTION 10 0 0 3 FOLD CALL:2 RAISE:4:20 10.0
    """, 25),

        ("Preflop Medium BTN",
        """NEWGAME botA botB 200 2 1000 10.0
    NEWHAND 3 1 Kd Qd 200 200 10.0
    GETACTION 10 0 0 3 FOLD CALL:2 RAISE:4:20 10.0
    """, 30),

        ("Preflop Speculative BTN",
        """NEWGAME botA botB 200 2 1000 10.0
    NEWHAND 4 1 7h 6h 200 200 10.0
    GETACTION 10 0 0 3 FOLD CALL:2 RAISE:4:20 10.0
    """, 30),

        ("Preflop Trash BTN",
        """NEWGAME botA botB 200 2 1000 10.0
    NEWHAND 5 1 7c 2d 200 200 10.0
    GETACTION 10 0 0 2 CALL:2 FOLD 10.0
    """, 40),

        ("Preflop Trash BB",
        """NEWGAME botA botB 200 2 1000 10.0
    NEWHAND 6 0 7c 2d 200 200 10.0
    GETACTION 10 0 0 2 CALL:2 FOLD 10.0
    """, 40),

        # =========================================================
        # SPR EFFECT VALIDATION
        # =========================================================

        ("Low SPR Commit",
        """NEWGAME botA botB 200 2 1000 10.0
    NEWHAND 7 1 Kh Qh 60 60 10.0
    GETACTION 40 3 Ah Jh Tc 0 3 FOLD CALL:10 RAISE:10:200 10.0
    """, 25),

        ("High SPR Deep",
        """NEWGAME botA botB 200 2 1000 10.0
    NEWHAND 8 1 Kh Qh 500 500 10.0
    GETACTION 20 3 Ah Jh Tc 0 3 FOLD CALL:5 RAISE:10:200 10.0
    """, 25),

        # =========================================================
        # BOARD TEXTURE SIZING VALIDATION
        # =========================================================

        ("Dry Board Small Bet",
        """NEWGAME botA botB 200 2 1000 10.0
    NEWHAND 9 1 As Kd 200 200 10.0
    GETACTION 40 3 Ah 7d 2c 0 3 FOLD CALL:5 RAISE:10:200 10.0
    """, 30),

        ("Wet Board Large Bet",
        """NEWGAME botA botB 200 2 1000 10.0
    NEWHAND 10 1 Qh Qd 200 200 10.0
    GETACTION 40 3 Jh Tc 9h 0 3 FOLD CALL:5 RAISE:10:200 10.0
    """, 30),

        ("Paired Board",
        """NEWGAME botA botB 200 2 1000 10.0
    NEWHAND 11 1 Ah Kd 200 200 10.0
    GETACTION 40 3 Kc Kd 4h 0 3 FOLD CALL:5 RAISE:10:200 10.0
    """, 30),

        # =========================================================
        # BLUFF + SEMI-BLUFF
        # =========================================================

        ("Flush Draw Semi Bluff",
        """NEWGAME botA botB 200 2 1000 10.0
    NEWHAND 12 1 9h 8h 200 200 10.0
    GETACTION 30 3 Ah Kh 2c 0 3 FOLD CALL:5 RAISE:10:200 10.0
    """, 40),

        ("Open Ended Straight Draw",
        """NEWGAME botA botB 200 2 1000 10.0
    NEWHAND 13 1 9h 8d 200 200 10.0
    GETACTION 30 3 7c 6s 2h 0 3 FOLD CALL:5 RAISE:10:200 10.0
    """, 40),

        ("Pure Bluff Opportunity",
        """NEWGAME botA botB 200 2 1000 10.0
    NEWHAND 14 1 7c 2d 200 200 10.0
    GETACTION 30 3 Ah 7d 2c 0 3 FOLD CALL:5 RAISE:10:200 10.0
    """, 50),

        # =========================================================
        # POSITION EFFECT POSTFLOP
        # =========================================================

        ("In Position Aggression",
        """NEWGAME botA botB 200 2 1000 10.0
    NEWHAND 15 1 Ah Kh 200 200 10.0
    GETACTION 30 3 As 7d 2c 0 3 FOLD CALL:5 RAISE:10:200 10.0
    """, 30),

        ("Out Position Control",
        """NEWGAME botA botB 200 2 1000 10.0
    NEWHAND 16 0 Ah Kh 200 200 10.0
    GETACTION 30 3 As 7d 2c 0 3 FOLD CALL:5 RAISE:10:200 10.0
    """, 30),

        # =========================================================
        # EXTREME POT PRESSURE
        # =========================================================

        ("Huge Pot Pressure",
        """NEWGAME botA botB 200 2 1000 10.0
    NEWHAND 17 1 Ah Qh 200 200 10.0
    GETACTION 300 3 Ah Jh Tc 0 3 FOLD CALL:50 RAISE:50:400 10.0
    """, 25),

        # =========================================================
        # LEGAL EDGE CASES
        # =========================================================

        ("No Raise Available",
        """NEWGAME botA botB 200 2 1000 10.0
    NEWHAND 18 1 Ah Ad 200 200 10.0
    GETACTION 40 3 2c 7d 9h 0 2 CALL:10 FOLD 10.0
    """, 15),

        ("Only Check Legal",
        """NEWGAME botA botB 200 2 1000 10.0
    NEWHAND 19 1 Ah Kd 200 200 10.0
    GETACTION 50 3 Qh Jh Tc 0 1 CHECK 10.0
    """, 10),
    ]



    for name, data, reps in tests:
        run_test_case(name, data, reps)

    print("\nAll tests completed.")
    print(f"Results saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
