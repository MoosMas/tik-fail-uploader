import os
import csv
import requests
from datetime import datetime
import json

# outputFile = open("logs.json", "a+", encoding="utf8")
compFilesFile = open("completed.txt", "r", encoding="utf8")
completedFiles = []
for completedFile in compFilesFile:
   completedFiles.append(completedFile)



folders = []
csvFiles = []
sessionLog = {}

# prevSessions = json.loads(outputFile)
now = datetime.strftime(datetime.now(), "%d-%m-%Y")

# def write_json(data, filename='logs.json'):
#    with open(filename, 'w') as o:
#       json.dump(data, o)
running = True
while running:
   csvFiles = []
   sessionLog = {}
   def write_json(data, user):
      with open('logs.json') as json_file:
         # Fixen dat er aan het logbestand kan worden toegevoegd
         data = json.load(json_file)

      if now in data.keys():
         if user in data[now].keys():
            print("User found in now")
            data[now].update = sessionLog
         else:
            data[now].update(sessionLog)
      else:
         data[now] = sessionLog
      
      with open('logs.json', 'w') as json_file:

         json.dump(data, json_file, indent=4)

   def find_csv_folders( path_to_dir, suffix=".csv" ):
      folders = os.listdir(path_to_dir)
      return [ filename for filename in folders if filename.endswith( suffix ) ] or ""

   rootFolder = ""
   subFolders = os.listdir(rootFolder)

   for i in range(len(subFolders)):
      currFolder = os.path.join(rootFolder, subFolders[i])
      if os.path.isdir(currFolder):
         print(f"{i}. {subFolders[i]}")

   choice = input("Select a user: ")
   choice = subFolders[int(choice)]

   print(choice)
   csvFiles.append(find_csv_folders(f"{rootFolder}/{choice}"))
   print(csvFiles)

   # for name in folders:
   sessionLog[choice] = []
   for file in csvFiles[0]:
      if file not in completedFiles:
         sessionLog[choice].append(file)
         # sessionLog[f"{choice}"].append(file)
         print(f"{file} not completed yet")
         path = os.path.join(rootFolder, choice)
         with open(f"{path}/{file}", "r", encoding="utf8") as f:
            reader = csv.DictReader(f)
            data = list(reader)
            # for line in data:
            for line in data[:5]:
               print(line["webVideoUrl"])
               endpoint = "https://tik.fail/api/geturl"
               body = {"url": line["webVideoUrl"]}
               r = requests.post(url = endpoint, data = body)

               response = r.text
               print(r.status_code)
               print(response)
               if r.status_code == 200:
                  sessionLog[-1].append(response)
      else:
         print(f"{file} completed")

   write_json(sessionLog, choice)

   stop = input("Press enter to continue or 'X' to exit: ").lower()
   if stop == 'x':
      running = False

# json.dump(sessionLog, outputFile)
print(len(csvFiles))
# outputFile.close()
compFilesFile.close()