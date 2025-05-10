import os
import httpx
import json

from time import sleep
from dotenv import load_dotenv, dotenv_values 

load_dotenv()

login_url   = os.getenv("base_url") + os.getenv("login_path")
submission_url = os.getenv("base_url") + os.getenv("task_path") + os.getenv("task_nr") + os.getenv("submission_path")
result_url =  os.getenv("base_url") + os.getenv("task_path") + os.getenv("task_nr") + os.getenv("result_path")

file_loc = os.getenv("file_path")

#login headers
headers = {
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",
    "Connection": "keep-alive",
    "Content-Length": "78",
    "Content-Type": "application/json",
    "Host": "website.de",
    "Origin": "https://website.de",
    "Referer": "https://website.de/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 OPR/118.0.0.0",
    "sec-ch-ua": "\"Not(A:Brand\";v=\"99\", \"Opera GX\";v=\"118\", \"Chromium\";v=\"133\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
}

#post file headers
post_head = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",
    "Connection": "keep-alive",
    "Content-Length": "1582",
  #should hopefully be generated automatically /\ and \/
    "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundarypD4n0jzkQnrBPPN8",
    "Host": "website.de",
    "Origin": "https://website.de/",
    "Referer": "https://website.de/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 OPR/118.0.0.0",
    "sec-ch-ua": "\"Not(A:Brand\";v=\"99\", \"Opera GX\";v=\"118\", \"Chromium\";v=\"133\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
}

data =  {
    "email": os.getenv("email_address"), #Login Email
    "plain_password": os.getenv("password") #Password
}

files = {
    "file_data": (
    "", #Uploaded File Name
    open(file_loc, "rb"),
    "application/x-zip-compressed"
  )
}

with httpx.Client(follow_redirects=True) as session:
# login post
r = session.post(login_url, headers=headers, json=data)

  if r.status_code == 200:
    print("Login Succesful")

# file upload
    #course = session.get(c_url)
    upload = session.post(submission_url, headers=post_head, files=files)

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

        sleep(1)
        counter += 1;


    else:
      print("Fehler bei Daten: ", course.status_code)
  else:
    print("Login failed: ", r.status_code)



