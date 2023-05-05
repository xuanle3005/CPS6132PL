from schedule import Schedule

schedule = Schedule([])
schedule.read_transactions()
schedule.round_robin()

with open('locktable_output.txt', 'r') as file:
    lockTable = file.read()
#Print all lock helds in lock table after executing each task
print(lockTable)

with open('system_log.txt', 'r') as file:
    systemLog = file.read()
print("System Log: \n " + systemLog)

with open('schedule.txt', 'r') as file:
    finalschedule = file.read()
print('Final Schedule: \n' + finalschedule)
