import os, sys, time, json
from webwhatsapi import WhatsAPIDriver
from webwhatsapi.objects.message import Message, MediaMessage

print "Environment", os.environ
try:
   os.environ["SELENIUM"]
except KeyError:
   print "Please set the environment variable SELENIUM to Selenium URL"
   sys.exit(1)

##Save session on "/firefox_cache/localStorage.json".
##Create the directory "/firefox_cache", it's on .gitignore
##The "app" directory is internal to docker, it corresponds to the root of the project.
##The profile parameter requires a directory not a file.
profiledir=os.path.join(".","firefox_cache")
if not os.path.exists(profiledir): os.makedirs(profiledir)
driver = WhatsAPIDriver(profile=profiledir, client='remote', command_executor=os.environ["SELENIUM"])
print("Waiting for QR")
driver.wait_for_login()
print("Saving session")
driver.save_firefox_profile(remove_old=False)
print("Bot started")

while True:
    time.sleep(3)
    print 'Checking for more messages, status', driver.get_status()
    chats = driver.get_all_chats()
    print(chats)
