import os
import httpx
import json

from time import sleep
from dotenv import load_dotenv, dotenv_values 

load_dotenv()

login_url   = str(os.getenv("base_url")) + str(os.getenv("login_path"))
submission_url = str(os.getenv("base_url")) + str(os.getenv("task_path")) + str(os.getenv("task_nr")) + str(os.getenv("submission_path"))
result_url =  str(os.getenv("base_url")) + str(os.getenv("task_path")) + str(os.getenv("task_nr")) + str(os.getenv("result_path"))

file_loc = os.getenv("file_path")
file_name = "Submission.zip"

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



