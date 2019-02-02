import sys

sys.path.append("/Users/szagar/ZTS/Dropbox/Business/ats/Code/lib")

from db_query import connectDB,nextPrototypeId
from prototype_tools import getPrototypeSetup
from prototype_tools import generatePrototypeCode,generateJclCode

dbh = connectDB()
proto_id = nextPrototypeId(dbh)
print(f"proto_id={proto_id}")
proto_id = 2
print(f"proto_id={proto_id}")
setup = getPrototypeSetup(dbh,proto_id)

out = generatePrototypeCode(dbh,setup)
#print(out)

#pprint(setup)
out = generateJclCode(dbh,setup)
#print(out)

