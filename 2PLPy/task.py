from enum import Enum
from lock import Lock, LockType

#Define TaskType
class TaskType(Enum):
    READ = 1
    WRITE = 2
    COMMIT = 3
    WAIT = 4

#Define each task contained in the task list of a transaction
class Task:
    def __init__(self, records, task_type, transaction_id=None, record_id=None, value_to_set=None) -> None:
        self.records = records
        self.task_type = task_type
        self.record_id = record_id
        self.transaction_id = transaction_id
        self.value_to_set = value_to_set

        # This boolean value is used to resolve when this task can't acquire lock because another transaction is holding it. 
        self.completed = False

    #Function to acquire Read/Shared Lock, if task can't acquire new Lock, this task will add to last index in list be execute later
    def _read(self):
        try:
            self.records.set_lock(
                self.record_id, LockType.SHARED, self.transaction_id)
            value = self.records.get_value(
                self.record_id) or self.record_id
            self.completed = True
            return value, value
        except Exception as e:
            self.completed = False
            raise e
        

    #Function to acquire Write/Exclusive Lock, similar to above, this task will be execute later if can't acquire Lock.
    def _write(self):
        try:
            self.records.set_lock(
                self.record_id, LockType.EXCLUSIVE, self.transaction_id)
            old_value = self.records.get_value(
                self.record_id) or self.record_id
            self.records.set_value(self.record_id, self.value_to_set)
            self.completed = True
            return old_value, self.value_to_set
        except Exception as e:
            self.completed = False
            raise e

    # Release Locks on Item that are being held by Transaction, allowing other Transaction to acquire new Lock. 
    def _commit(self):
        self.records.release_lock(self.transaction_id)
        self.completed = True
        
        return None, None

    #Start acquire new or release holding locks 
    def execute(self):
        if self.task_type == TaskType.READ:
            return self._read()
        elif self.task_type == TaskType.WRITE:
            return self._write()
        elif self.task_type == TaskType.COMMIT:
            return self._commit()
        else:
            raise Exception('Invalid task type')
