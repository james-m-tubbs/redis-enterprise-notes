#!/usr/bin/env python3

import redis
import sys

redis_hostname = "redis-11235.c10.us-east-1-4.ec2.cloud.redislabs.com"
redis_port = 11235

def test_connection(hostname, port, password):
    
    r = redis.StrictRedis(host=hostname, port=port, password=password, decode_responses=True)
    try:
        print("Attempting to connect to host={}, port={}".format(hostname, port))
        r.set("TEST_STRING", "TEST_VALUE")
        val = r.get("TEST_STRING")
        if val != "TEST_VALUE":
            print("\tConnection test failed")
            return False
        else:
            print("\tSuccessfully connected")
            return True
    except Exception as e:
        print("Failed to connect to the database: {}".format(str(e)))
        return False
    
def get_credentials(email, pwd):
    
    global redis_hostname, redis_port

    r = redis.StrictRedis(host=redis_hostname, port=redis_port, password=pwd, decode_responses=True)
    try:
        for db_type in ['rejson']:
            creds = r.hgetall(email + "_" + db_type)
            
            try:
                hostname = creds['hostname'].strip()
                port = creds['port'].strip()
                password = creds['password'].strip()
                
                if test_connection(hostname, port, password):
                    print("{} -> hostname: {} port: {}, password: {}\n".format(db_type, hostname, port, password))
                else:
                    return False
            except: 
                print("Unable to find that account, please check your registration email")
        
        return True
        
    except:
        print("Unable to connect, please check the password")
        return False

def get_user_input():
    "Return the email and password of the day"
    
    email = ""
    while len(email) == 0:
        email = input("Please enter your registration email: ")
    
    pwd = ""
    while len(pwd) == 0:
        pwd = input("Please enter the password from the instructor: ")

    print("")
    return (email, pwd)
    
    
def main():
    
    print("For this training you will need the ReJSON modules: \n")
    
    connected = False
    while not connected:
        email, pwd = get_user_input()
        connected = get_credentials(email, pwd)
        if connected is False:
            print("Was unable to retrieve your credentials - please contact instructor")    


if __name__ == '__main__':
    main() 
    sys.exit(0)
    
