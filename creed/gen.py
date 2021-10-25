import random
import string

lower = string.ascii_letters
num = string.digits
sym = string.punctuation

all_1 = lower+num+sym

temp = random.sample(all_1,70)
password = ("").join(temp)
print(password)
