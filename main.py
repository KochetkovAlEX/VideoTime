import random
from datetime import datetime

print(datetime.now().time())

seconds = str(datetime.now().time())[9:]
print(seconds, seconds[3:])

print()