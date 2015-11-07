import os

f = os.popen('./curl.sh')
output = f.read()


print(output)
