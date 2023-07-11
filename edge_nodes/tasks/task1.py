import time 

def readFileWithDelay():
    fileDir = "/home/syslab/workspace_la/edge_nodes/tasks/reading_data.txt"
    fileReading = open(fileDir, 'r')
    lines = fileReading.readlines()
    for line in lines:
        time.sleep(5)
        print(line)
    fileReading.close()

readFileWithDelay()
