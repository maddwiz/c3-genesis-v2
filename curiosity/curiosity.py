"""
C.3 Curiosity Layer (v1)
-----------------------
This module manages C.3’s curiosity queue.
It tracks unanswered questions, uncertain inputs,
and “frontier areas” where C.3 wants to explore more.

This is a simple, safe starter version:
- Adds items to curiosity queue
- Lets you pop the highest-priority item
- Generates a frontier report (“what C.3 is unsure about”)
"""

from dataclasses import dataclass, field
from typing import List, Optional
import time
import uuid


@dataclass
class CuriosityItem:
    id: str
    question: str
    source: str
    timestamp: float
    uncertainty: float  # 0.0–1.0
    notes: Optional[str] = None


class CuriosityLayer:
    def __init__(self):
        self.queue: List[CuriosityItem] = []

    def add_item(self, question: str, source: str = "system", uncertainty: float = 0.5, notes: str = None):
        """
        Add a curiosity question / unknown / frontier signal.
        """
        item = CuriosityItem(
            id=str(uuid.uuid4()),
            question=question,
            source=source,
            timestamp=time.time(),
            uncertainty=max(0.0, min(1.0, uncertainty)),
            notes=notes
        )
        self.queue.append(item)
        return item

    def pop_highest_uncertainty(self) -> Optional[CuriosityItem]:
        """
        Return the item with the highest uncertainty.
        """
        if not self.queue:
            return None
        self.queue.sort(key=lambda x: x.uncertainty, reverse=True)
        return self.queue.pop(0)

    def frontier_report(self):
        """
        Return a summary of the current frontier.
        """
        if not self.queue:
            return {
                "count": 0,
                "message": "No open curiosity items."
            }
        highest = max(self.queue, key=lambda x: x.uncertainty)
        return {
            "count": len(self.queue),
            "highest_uncertainty_question": highest.question,
            "highest_uncertainty_score": highest.uncertainty,
            "examples": [item.question for item in self.queue[:5]],
        }


# If run directly: simple local test
if __name__ == "__main__":
    c = CuriosityLayer()
    c.add_item("What is the smallest MVP for C3?", "user", 0.9)
    c.add_item("How to optimize reconciliation?", "system", 0.6)
    print(c.frontier_report())
