import csv
import os
from datetime import datetime

INPUT_PRICE_PER_M = 0.30
OUTPUT_PRICE_PER_M = 2.50


class TokenTracker:
    def __init__(self, transcript_name="transcript"):
        self.transcript_name = transcript_name
        self.calls = []

    def add(self, step, input_tokens, output_tokens):
        cost = (input_tokens * INPUT_PRICE_PER_M + output_tokens * OUTPUT_PRICE_PER_M) / 1_000_000
        self.calls.append({
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "transcript": self.transcript_name,
            "step": step,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "cost_usd": round(cost, 6),
        })
        print(f"  [tokens] {step}: in={input_tokens} out={output_tokens} cost=${cost:.5f}")

    def summary(self):
        return {
            "calls": len(self.calls),
            "input_tokens": sum(c["input_tokens"] for c in self.calls),
            "output_tokens": sum(c["output_tokens"] for c in self.calls),
            "estimated_cost_usd": round(sum(c["cost_usd"] for c in self.calls), 6),
        }
    

    def save(self, path="logs/token_log.csv"):

        if not self.calls:
            return
        
        os.makedirs(os.path.dirname(path), exist_ok=True)
        new_file = not os.path.exists(path)
        with open(path, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(self.calls[0].keys()))
            if new_file:
                writer.writeheader()
            writer.writerows(self.calls)