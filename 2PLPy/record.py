from lock import Lock, LockType

#This class make record of locks when execute Transaction -> Task
class Record:
    def __init__(self, record_id, value=None) -> None:
        self.record_id = record_id
        self.value = value
        self.lock = None


class Records:
    def __init__(self) -> None:
        self.records = {}

    # Return RecordID
    def get_record(self, record_id):
        if record_id not in self.records:
            self.records[record_id] = Record(record_id)
        return self.records[record_id]

    #Generate a list of lock that are currently being held by the transactions at that execution.
    def generate_lock_table(self):
        lock_table = {}
        for record in self.records:
            if self.records[record].lock:
                lock_table[record] = self.records[record].lock
        pretty_lock_table = ""
        for x in lock_table.keys():
            pretty_lock_table += ("{} ({})  ".format(lock_table.get(x),x))


        return pretty_lock_table
    
    
    #Return the value get from input
    def get_value(self, record_id):
        return self.get_record(record_id).value

#Use for write task, set old value to the new value. 
    def set_value(self, record_id, value):
        self.get_record(record_id).value = value

    #Set appropriate lock to item in task from the task list in Transaction transaction_id 
    def set_lock(self, record_id, lock_type, transaction_id):
        if lock_type == LockType.SHARED:
            self.set_lock_shared(record_id, transaction_id)
        elif lock_type == LockType.EXCLUSIVE:
            self.set_lock_exclusive(record_id, transaction_id)
        else:
            raise Exception('Invalid lock type')

    #Set Shared Lock for Read task if no Exclusive Lock already made on that record by another transaction or no lock existed on that record from any transactions.
    def set_lock_shared(self, record_id, transaction_id):
        curr_lock = self.get_lock(record_id)
        if not curr_lock:
            self._set_lock(record_id, Lock(LockType.SHARED, transaction_id))
        elif curr_lock.lock_type == LockType.SHARED or (curr_lock.lock_type == LockType.EXCLUSIVE and curr_lock.transaction_id == transaction_id):
            return
        else:
            raise Exception(
                'Cannot set lock shared on record with exclusive lock')

    #Set Exclusive Lock for Write Task if no other lock already made on that record by another transaction. 
    #If there's already a Read Lock on that record, update it to Exlusive Lock
    def set_lock_exclusive(self, record_id, transaction_id):
        curr_lock = self.get_lock(record_id)
        if not curr_lock or curr_lock.lock_type == LockType.SHARED:
            self._set_lock(record_id, Lock(LockType.EXCLUSIVE, transaction_id))
        elif curr_lock.lock_type == LockType.EXCLUSIVE:
            return


    def _set_lock(self, record_id, lock):
        self.get_record(record_id).lock = lock

    def get_lock(self, record_id):
        return self.get_record(record_id).lock

    #Release lock holding on record (Set type to None)
    def release_lock(self, transaction_id):
        for record in self.records:
            if self.records[record].lock and self.records[record].lock.transaction_id == transaction_id:
                self.records[record].lock = None

