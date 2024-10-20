from typing import List

def calculate_equal_split(total: float, users: List[str]):
    share = total / len(users)
    return {user: share for user in users}