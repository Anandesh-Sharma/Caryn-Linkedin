from linkedin import Linkedin
from config import username, password, message

# get a session
session = Linkedin.login(username, password)

# send messages
try:
    session.send_message(message)
except:
    import traceback

    print(traceback.print_exc())
