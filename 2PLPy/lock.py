from enum import Enum

# Define LockType
class LockType(Enum):
    SHARED = 1
    EXCLUSIVE = 2


class Lock:
    def __init__(self, lock_type, transaction_id) -> None:
        self.lock_type = lock_type
        self.transaction_id = transaction_id

    def __repr__(self) -> str:
        if (self.lock_type == LockType.SHARED):
            return f"{self.transaction_id} - Shared Lock"
        else:
            return f"{self.transaction_id} - Exclusive Lock"

