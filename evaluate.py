import os
import time
from rouge_score import rouge_scorer

from src.ingestion import normalize_transcript
from src.pipeline import process_transcript

NUM_SAMPLES = 5


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def main():
    scorer = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=True)
    rows = []

    for i in range(1, NUM_SAMPLES + 1):
        name = f"meeting{i}.txt"
        text = normalize_transcript(read(f"samples/{name}"))
        reference = read(f"samples/expected/meeting{i}_summary.txt")

        result, usage = process_transcript(text, name)
        scores = scorer.score(reference, result.summary)
        rows.append((name, scores["rouge1"].fmeasure, scores["rouge2"].fmeasure,
                     scores["rougeL"].fmeasure, usage["estimated_cost_usd"]))
        time.sleep(5)      

    avg = [sum(r[k] for r in rows) / len(rows) for k in (1, 2, 3)]

    os.makedirs("docs", exist_ok=True)
    with open("docs/evaluation_report.md", "w", encoding="utf-8") as f:
        f.write("# Evaluation Report\n\n## ROUGE scores (F1)\n\n")
        f.write("| Transcript | ROUGE-1 | ROUGE-2 | ROUGE-L | Est. cost (USD) |\n")
        f.write("|---|---|---|---|---|\n")
        for name, r1, r2, rl, cost in rows:
            f.write(f"| {name} | {r1:.2f} | {r2:.2f} | {rl:.2f} | {cost} |\n")
        f.write(f"| **Average** | {avg[0]:.2f} | {avg[1]:.2f} | {avg[2]:.2f} | |\n\n")

        f.write("## Manual quality rubric (score each 1-5 by hand)\n\n")
        f.write("| Criteria | m1 | m2 | m3 | m4 | m5 |\n|---|---|---|---|---|---|\n")
        for criteria in ["Decisions correct", "Action owners and deadlines correct",
                         "Risks found", "No invented facts"]:
            f.write(f"| {criteria} |  |  |  |  |  |\n")

    print("Report saved to docs/evaluation_report.md")


if __name__ == "__main__":
    main()