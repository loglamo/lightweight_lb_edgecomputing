# task: writing file with delay
import time

def writeFileWithDelay():
    fileDir = "/home/syslab/workspace_la/edge_nodes/tasks/writing_data.txt"
    fileWriting = open(fileDir, 'w')
    for i in range(1, 100):
        fileWriting.writelines("testing...")
        time.sleep(5)
        print("Already write line...")
    fileWriting.close()

writeFileWithDelay()
          
              


