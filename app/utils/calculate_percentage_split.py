from typing import Dict

def calculate_percentage_split(total: float, percentages: Dict[str, float]):
    if sum(percentages.values()) != 100:
        return -1
    return {user: total * (percent / 100) for user, percent in percentages.items()}
