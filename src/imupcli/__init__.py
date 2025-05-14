import os
import httpx
import json
import argparse

from time import sleep
from dotenv import load_dotenv, dotenv_values 

def main():
  parser = argparse.ArgumentParser(description="Upload files to Uni-Server")
  parser.add_argument("file_name", type=str, help="the name of the uploaded file")
  parser.add_argument("file_path", type=str, help="the path to your file")
  parser.add_argument("task_number", type=str, help="the number of the task to upload")
  args = parser.parse_args()
  
  upload_file(args.file_path, args.file_name, args.task_number)

def upload_file(file_loc, file_name, number):
  load_dotenv()
  
  login_url   = str(os.getenv("base_url")) + str(os.getenv("login_path"))
  submission_url = str(os.getenv("base_url")) + str(os.getenv("task_path")) +  str(number) + str(os.getenv("submission_path"))
  result_url =  str(os.getenv("base_url")) + str(os.getenv("task_path")) + str(number) + str(os.getenv("result_path"))
  
  data =  {
      "email": os.getenv("email_address"), #Login Email
      "plain_password": os.getenv("password") #Password
  }
  
  files = {
      "file_data": (
      file_name, #Uploaded File Name
      open(file_loc, "rb"),
      "application/x-zip-compressed"
    )
  }

  with httpx.Client(follow_redirects=True) as session:
  # login post
    r = session.post(login_url, json=data)
  
    if r.status_code == 200:
      print("Login Succesful")
      # file upload
      upload = session.post(submission_url, files=files)
  
      if upload.status_code == 200:
        print("uploaded Succesfull")
  
        collected_results = False
        counter = 0

        # check if tests finished and if so print result
        while not collected_results:
          result = session.get(result_url)
          data = json.loads(result.text)
  
          result_state = data['public_execution_state']
  
          if result_state == 2:
            results = data['public_test_log']
            collected_results = True
            print(results)
          else:
            print("Waiting for Results: ")
  
          if counter == 60:
            collected_results = True
            print("Error: WAITED TO LONG")
  
          sleep(2)
          counter += 1;
  
  
      else:
        print("Fehler bei Daten: ", upload.status_code)
    else:
      print("Login failed: ", r.status_code)


#upload_file("C:/Users/levid/Documents/sheet4-1.zip", "Abgabe4-1-LD-LP.zip", 20)

if __name__ == "__main__":
  main()
