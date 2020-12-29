import os
import csv
import requests
from datetime import datetime
import json
from dotenv import load_dotenv

load_dotenv()

rootFolder = os.getenv("folder")

# outputFile = open("logs.json", "a+", encoding="utf8")
prevCompletedFile = open("completed.txt", "r", encoding="utf8")
completedFiles = []
for completedFile in prevCompletedFile:
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
         data = json.load(json_file)

      if now in data.keys():
         if user in data[now].keys():
            print("User found in now")
            data[now].update(sessionLog)
         else:
            data[now].update(sessionLog)
      else:
         data[now] = sessionLog
      
      with open('logs.json', 'w') as json_file:
         json.dump(data, json_file, indent=4)

   def find_csv_folders( path_to_dir, suffix=".csv" ):
      folders = os.listdir(path_to_dir)
      return [ filename for filename in folders if filename.endswith( suffix ) ] or ""

   subFolders = os.listdir(rootFolder)

   for i in range(len(subFolders)):
      currFolder = os.path.join(rootFolder, subFolders[i])
      if os.path.isdir(currFolder):
         print(f"{i}. {subFolders[i]}")

   userChoice = input("Select a user: ")
   userChoice = subFolders[int(userChoice)]

   print(userChoice)
   csvFiles.append(find_csv_folders(f"{rootFolder}/{userChoice}"))
   print(csvFiles)

   # for name in folders:
   sessionLog[userChoice] = {}
   for file in csvFiles[0]:
      if file not in completedFiles:
         sessionLog[userChoice][file] = {}
         # sessionLog[f"{userChoice}"].append(file)
         print(f"{file} not completed yet")
         path = os.path.join(rootFolder, userChoice)
         with open(f"{path}/{file}", "r", encoding="utf8") as f:
            reader = csv.DictReader(f)
            data = list(reader)
            for line in data:
            # for line in data[:5]:
               print(line["webVideoUrl"])
               endpoint = "https://tik.fail/api/geturl"
               body = {"url": line["webVideoUrl"]}
               response = requests.post(url = endpoint, data = body)
               print(f"Text: {response}")

               # print(response)
               videoId = line['id']
               sessionLog[userChoice][file][videoId] = {}
               
               if response.status_code == 200:
                  json_data = response.json()
                  print(f"Data: {json_data}")
                  # print(f"Webpage: {json_data['webpage']}")
                  # sessionLog[userChoice][file].append(line['id'])
                  sessionLog[userChoice][file][videoId].update({
                     'code': response.status_code,
                     'url': json_data["webpage"],
                     'direct': json_data["direct"],
                     'original': line['webVideoUrl']
                  })
               else:
                  sessionLog[userChoice][file][videoId].update({
                     'code': response.status_code,
                     'original': line["webVideoUrl"]
                  })
      else:
         print(f"{file} completed")
         

   write_json(sessionLog, userChoice)

   stop = input("Press enter to continue or 'X' to exit: ").lower()
   if stop == 'x':
      running = False

# json.dump(sessionLog, outputFile)
print(len(csvFiles))
# outputFile.close()
prevCompletedFile.close()