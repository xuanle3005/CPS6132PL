# CPS6132PL
This program will read a textfile schedule input in the form 
    T<id>: W(<Record_ID>, <Value>) ; R(<Record_ID>)  ; C 
where each new line is a new transaction. 

To run the program, 
1. Feed the input into input.txt 
2. In terminal, type "python3 main.py" 

The outputs will be add into the 3 text file: 
    locktable_output.txt, which in each line will show all lock on record that are being held in the schedule.
    system_log.txt, which display successfully executed task in execution order, where:

        In case of a Write task, store the following information:
            - Timestamp; can be a simple counter starting from 0 and incremented by 1 for each log entry
            - The Transaction Id
            - The Record Id
            - The old value stored in that record
            - The new value stored in that record
            - The timestamp of the previous log entry for this transaction (to be used for Roll-back)

        In case of a Read task, store the following information:
            - Timestamp; can be a simple counter starting from 0 and incremented by 1 for each log entry
            - The Transaction Id
            - The Record Id
            - The value read from that record
            - The timestamp of the previous log entry for this transaction (to be used for Roll-back)

        In case of a Commit, store the following information:
            - Timestamp; can be a simple counter starting from 0 and incremented by 1 for each log entry
            - The Transaction Id
            - The timestamp of the previous log entry for this transaction (to be used for Roll-back)
        
    schedule.txt, show the final schedule.


