from concurrent.futures import ThreadPoolExecutor
from Logger import logging

import requests
import time
import os
import random
import json
import string


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
    
    
class Firstmail:
    def change_password(email: str, cpass: str, npass: str):
        while True:
            try:
                payload = {
                    "email": email,
                    "current_password": cpass,
                    "new_password": npass
                }
                
                resp = session.post("https://firstmail.ltd/api/v1/email/password/change/", json=payload)
                response = str(resp.json())
                
                if resp.status_code == 200 and resp.json()["success"]:
                    logging.success("Succesfully changed password.", email, resp.status_code)
                    return True, 'Completed'
                
                elif resp.status_code == 400:
                    if 'установлена двухфакторная аутентификация' in response:
                        logging.error("Email has 2FA.", email, resp.status_code)
                        return False, 'Email_has_2FA'
                    
                    elif 'установлен резервный email' in response:
                        logging.error("Reserve email set.", email, resp.status_code)
                        return False, 'Reserve_email_set'
                    
                    elif 'не менее 8 символов' in response:
                        logging.error("The password must consist of 8-20 characters. English + special characters", email, resp.status_code)
                        return False, None
                    
                    else:
                        logging.error(f"Unknown validation error: {response}", email, resp.status_code)
                        return False, None
                
                elif resp.status_code == 401:
                    if 'Недействительный API ключ' in response:
                        logging.error("Invalid ApiKey.", email, resp.status_code)
                        return False, None
                    
                    elif 'Неверный текущий пароль' in response:
                        logging.error("Password does not match.", email, resp.status_code)
                        return True, 'Password_does_not_match'
                    
                    else:
                        logging.error(f"Unknown error {response}", email, resp.status_code)
                        return True, 'Unknown_error'
                    
                elif resp.status_code == 404:
                    logging.error("Email not found.", email, resp.status_code)
                    return True, 'Email_not_found'
                    
                elif resp.status_code == 500:
                    logging.error("Internal server error.", email, resp.status_code)
                    return True, 'Internal_server_error'
                
                else:
                    logging.error(f"Unknown error {response}", email, resp.status_code)
                    return True, 'Unknown_error'
                
            except Exception as e:
                logging.error(f"Exception occured: {e}")
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

                    
