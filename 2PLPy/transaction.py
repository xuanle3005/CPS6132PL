from task import TaskType

#Define each Transaction from schedule provided in the input file. 
class Transaction:
    def __init__(self, tasks, transaction_id=None, timestamp=0) -> None:
        self.tasks = tasks
        self.transaction_id = transaction_id
        self.timestamp = timestamp
        self.previous_timestamp = -1

#Attempt to execute uncompleted task from the task list stored in this Transaction
    def execute(self, timestamp):
        self.timestamp = timestamp
        for task in self.tasks:
            if not task.completed:
                try:
                    old_value, new_value = task.execute()
                    #Add completed task to system log
                    with open('system_log.txt', 'a') as file:
                        file.write(self.generate_log_table(
                            task, old_value, new_value) + '\n')
                    with open('schedule.txt', 'a') as file:
                        file.write(self.generate_schedule(task, new_value) + " ")
                    #Set roll back point to the previous timestamp
                    self.previous_timestamp = self.timestamp
                    return 1
                except Exception as e:
                    return 0

#Generate log table after each successful task
    def generate_log_table(self, task, old_value, new_value):
        if task.task_type == TaskType.READ:
            return f"{TaskType.READ}, {self.timestamp}, {task.transaction_id}, {task.record_id}, {new_value}, {self.previous_timestamp}"
        elif task.task_type == TaskType.WRITE:
            return f"{TaskType.WRITE}, {self.timestamp}, {task.transaction_id}, {task.record_id}, {old_value}, {new_value}, {self.previous_timestamp}"
        elif task.task_type == TaskType.COMMIT:
            return f"{TaskType.COMMIT}, {self.timestamp}, {task.transaction_id}, {self.previous_timestamp}"
        
    def generate_schedule(self, task, new_value):
        if task.task_type == TaskType.READ:
            return f"{task.transaction_id}:R({task.record_id})"
        elif task.task_type == TaskType.WRITE:
            return f"{task.transaction_id}:W({task.record_id},{new_value})"
        elif task.task_type == TaskType.COMMIT:
            return f"{task.transaction_id}:C"        

#Find all completed tasks
    def is_completed(self):
        return all([task.completed for task in self.tasks])
