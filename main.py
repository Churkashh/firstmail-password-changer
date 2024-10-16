import requests
import time
import os
import random
import json
import string

from concurrent.futures import ThreadPoolExecutor
from Logger import logging


emails = open('./Input/Mails.txt', 'r').read().splitlines()
config = json.load(open('./config.json', 'r'))

session = requests.Session()
session.headers = {"X-API-KEY": config["Main"]["X-Api-Key"],"content-type": "application/json"}

def generate_password() -> str:
    return ''.join(random.choices(string.ascii_lowercase, k=8)) + ''.join(random.choices(string.ascii_uppercase, k=1)) + '!' + ''.join(random.choices(string.digits, k=4))


def format_line(line: str):
    parts = line.split(":") if ":" in line else line.split("|") if "|" in line else None
    
    if not parts or len(parts) <= 1 or len(parts) >= 4:
        raise logging.error(f"Incorrect email format.", line)
    
    return parts[0], parts[1]
    
    
class Firstmail():
    def change_password(email: str, cpass: str, npass: str):
        while True:
            try:
                payload = {
                    "username": email,
                    "cpassword": cpass,
                    "npassword": npass
                }
                
                resp = session.post("https://api.firstmail.ltd/v1/mail/change/password", json=payload)
                response = resp.text
                
                if resp.status_code == 200:
                    if "Password was updated" in response:
                        logging.success("Succesfully changed password.", email, resp.status_code)
                        return True, 'Completed'
                    
                    elif "The password was changed less than a day ago" in response:
                        logging.error("The password was changed less than a day ago.", email, resp.status_code)
                        return True, 'Password_was_changed_less_than_a_day_ago'
                    
                    elif "wrongPassword" in response:
                        logging.error("Password does not match.", email, resp.status_code)
                        return True, 'Password_does_not_match'
                    
                    elif "Required username and cpassword and npassword" in response:
                        logging.error("Required username and cpassword and npassword (probably some of config values are missing).", email, resp.status_code)
                        return False, None
                    
                    elif "The password must consist of 8-20 characters" in response:
                        logging.error("The password must consist of 8-20 characters, English. language + special characters", email, resp.status_code)
                        return False, None

                    else:
                        logging.error(f"Unknown error {resp.text}", email, resp.status_code)
                        return True, 'Unknown_error'
                
                elif resp.status_code == 403:
                    if "IP missmatch" in response:
                        logging.error("ApiKey IP missmatch.", email, resp.status_code)
                        return False, None
                    
                    elif "Api rate limit reached" in response:
                        logging.ratelimit("Resource has been ratelimited. Sleeping for 30 seconds...", email, resp.status_code)
                        time.sleep(30)
                        continue
                    
                    elif "Api user not found" in response:
                        logging.error("Invalid ApiKey.", email, resp.status_code)
                        return False, None
                    
                elif resp.status_code == 500:
                    logging.error("Internal server error.", email, resp.status_code)
                    return True, 'Internal_server_error'
                
                else:
                    logging.error(f"Unknown error {resp.text}", email, resp.status_code)
                    return True, 'Unknown_error'
                
            except Exception as e:
                print(e)
                time.sleep(1)
            
            
def thread(line: str):
    email, cpass = format_line(line)
    if config["Password"]["Generate_password"] == True:
        npass = generate_password()
    
    else:
        npass = config["Password"]["new_password"]
    
    result, file = Firstmail.change_password(email, cpass, npass)
    if result:
        if not os.path.exists(f'./Output/{file}.txt'):
            with open(f'./Output/{file}.txt', 'a') as file:
                file.write(f"{email}:{npass}\n")
                
        else:
            with open(f'./Output/{file}.txt', 'a') as file:
                file.write(f"{email}:{npass}\n")


with ThreadPoolExecutor(max_workers=config["Main"]["Threads"]) as executor:
    for email in emails:
        executor.submit(thread, email)

                    
