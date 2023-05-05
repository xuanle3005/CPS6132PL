from task import Task, TaskType
from transaction import Transaction
from record import Records


class Schedule:

    def __init__(self, transactions):
        self.transactions = transactions
        self.records = Records()
        self.timestamp = 0
        self.entrys = -1

    def round_robin(self):
        # Create new text file
        with open('locktable_output.txt', 'w') as file:
            file.write('Lock held in schedule: \n   No Lock\n')

        with open('system_log.txt', 'w') as file:
            file.write('')

        with open('schedule.txt', 'w') as file:
            file.write('')

        curr_lock_table = {}

        # Initiate Counter for TimeStamp
        cnt = 0
        # Remove and Execute the first transaction from the list, if the transaction cannot execute, add it back.
        while self.transactions:
            transaction = self.transactions.pop(0)
            cnt += transaction.execute(cnt)
        
            if not transaction.is_completed():
                self.transactions.append(transaction)
                
        # Update the state of locks that are stored in lock_table.txt 
            new_lock_table = self.records.generate_lock_table()
            if curr_lock_table != new_lock_table:
                with open('locktable_output.txt', 'a') as file:
                    if new_lock_table == "":
                        file.write("   No Lock")
                    else:
                        file.write("   " + str(new_lock_table) + '\n')
                curr_lock_table = new_lock_table



    #Send values of the Tasks read from input file to Task class
    def _parse_task(self, task_string, transaction_id):
        task_type = task_string[0]
        if task_type == 'C':
            return Task(self.records, TaskType.COMMIT, transaction_id=transaction_id)
        elif task_type == 'W':
            record_id, value = map(int, task_string[2:-1].split(','))
            return Task(self.records, TaskType.WRITE, transaction_id=transaction_id, record_id=record_id, value_to_set=value)
        elif task_type == 'R':
            return Task(self.records, TaskType.READ, transaction_id=transaction_id, record_id=int(task_string[2:-1]))
        else:
            raise Exception('Invalid task type')
        

    #Read given schedule from input.txt, send Transaction id and the list of Task it has into Transaction Class.
    def read_transactions(self):
        with open('input.txt', 'r') as file:
            for line in file.readlines():
                line = line.replace(' ', '').strip()
                if line:
                    transaction_id, tasks_string = line.split(':')
                    tasks = []
                    for task_string in tasks_string.split(';'):
                        tasks.append(self._parse_task(
                            task_string, transaction_id))
                    transaction = Transaction(tasks, transaction_id)
                    self.transactions.append(transaction)
