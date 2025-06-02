from pydantic import BaseModel
from typing import Dict, List
import os

class DenominationCombination(BaseModel):
    denomination: int
    count: int

class AmountCombinations(BaseModel):
    amount: int
    combinations: List[Dict[int, int]]

class DenominationResponse(BaseModel):
    results: List[AmountCombinations]

class DenominationRoutine:
    def __init__(self):
        self.denominations = [100, 50, 10]
        self.test_amounts = [30, 50, 60, 80, 140, 230, 370, 610, 980]

    def find_combinations(self, amount):
        def backtrack(remaining, start_idx, current_combo):
            if remaining == 0:
                result = {}
                for d in self.denominations:
                    if current_combo.count(d) > 0:
                        result[d] = current_combo.count(d)
                combinations.append(result)
                return
            
            for i in range(start_idx, len(self.denominations)):
                if remaining >= self.denominations[i]:
                    current_combo.append(self.denominations[i])
                    backtrack(remaining - self.denominations[i], i, current_combo)
                    current_combo.pop()
        
        combinations = []
        backtrack(amount, 0, [])
        return combinations

    def format_combination(self, combo):
        parts = []
        for denom, count in sorted(combo.items()):
            parts.append(f"{count} x {denom} EUR")
        return " + ".join(parts)

    def run(self):
        os.makedirs('outputs', exist_ok=True)
        file_path = 'outputs/denomination_routine_run.txt'
        
        with open(file_path, 'w') as f:
            for amount in self.test_amounts:
                f.write(f"\nPossible combinations for {amount} EUR:\n")
                
                combinations = self.find_combinations(amount)
                
                if not combinations:
                    f.write("No possible combinations\n")
                else:
                    for combo in combinations:
                        f.write(f"- {self.format_combination(combo)}\n")
        
        print(f"Execution successful. Results written to {file_path}")

if __name__ == "__main__":
    routine = DenominationRoutine()
    routine.run()