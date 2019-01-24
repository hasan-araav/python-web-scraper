import re

string = 'http://jobs.bdjobs.com/jobdetails.asp?id=817747&fcatId=19&ln=3'

x = re.findall("^factId/\d", string)

print(x)