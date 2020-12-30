import os
import csv
import requests
from datetime import datetime
import json
from dotenv import load_dotenv

load_dotenv()

# Enter your TikTok-scraper folder here, for example: "C:/Users/myname/Desktop/Homework/TikTok":
rootFolder = "" or os.getenv("folder")

folders = []
csvFiles = []
sessionLog = {}

now = datetime.strftime(datetime.now(), "%d-%m-%Y")

running = True
while running:
   csvFiles = []
   sessionLog = {}
   os.system("cls")
   def write_json(data, user):
      with open('logs.json') as json_file:
         data = json.load(json_file)

      if now in data.keys():
         if user in data[now].keys():
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
         print(f"{i} | {subFolders[i]}")

   userChoice = input("\nSelect a user: ")
   while userChoice.isnumeric() == False:
      print("Please enter a number.")
      userChoice = input("Select a user: ")
      
   userChoice = subFolders[int(userChoice)]

   csvFiles.append(find_csv_folders(f"{rootFolder}/{userChoice}"))
   
   fileProgress = 0
   sessionLog[userChoice] = {}
   for file in csvFiles[0]:
      lineProgress = 0
      fileProgress += 1
      os.system("cls")
      completedFromCurrFile = 0
      
      # if file not in completedFiles:
      sessionLog[userChoice][file] = {}
      path = os.path.join(rootFolder, userChoice)
      with open(f"{path}/{file}", "r", encoding="utf8") as f:
         reader = csv.DictReader(f)
         data = list(reader)
         for line in data:
            lineProgress += 1
            print(f"File: {fileProgress}/{len(csvFiles[0])} | Completed: {lineProgress}/{len(data)}")
            endpoint = "https://tik.fail/api/geturl"
            body = {"url": line["webVideoUrl"]}
            response = requests.post(url = endpoint, data = body)
            print(f"Response: {response}")
            videoId = line['id']
            sessionLog[userChoice][file][videoId] = {}

            if response.status_code == 200:
               json_data = response.json()

               try:
                  sessionLog[userChoice][file][videoId].update({
                  'code': response.status_code,
                  'url': json_data["webpage"],
                  'direct': json_data["direct"],
                  'original': line['webVideoUrl']
                  })
                  completedFromCurrFile += 1
               except TypeError:
                  sessionLog[userChoice][file][videoId].update({
                  'status': 'Failed',
                  'response': json_data,
                  'original': line["webVideoUrl"]
               })
            else:
               print("Failed: See logs for details")
               sessionLog[userChoice][file][videoId].update({
                  'code': response.status_code,
                  'response': response,
                  'original': line["webVideoUrl"]
               })
            write_json(sessionLog, userChoice)
            if completedFromCurrFile == len(data):
               print("Done")
      # else:
      #    print(f"{file} completed")
   stop = input("Press enter to continue or 'X' to exit: ").lower()
   if stop == 'x':
      running = False