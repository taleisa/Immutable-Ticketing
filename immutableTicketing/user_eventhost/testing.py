from web3 import Web3
from eventhost import EventHost
from dbms import DBMS
from user import User

w3 = Web3(Web3.HTTPProvider('HTTP://127.0.0.1:7545'))
deployer = "0xDFf43e81a80BdB91EF10d8316b29701d0813A2D6"      # Account[0] address deployer (Event Host)
deployer_key = "0xf103df4a496a767da8e6aae2c4d0290bae572a52282f5c228223f14b94c4e1e6" # Account[0] private key deployer  
deployer_2 = "0x8Fc72b1857803359A62f1408F01faA1952a65E59"      # Account[5] address deployer (Event Host 2)
GEA = "0x1cd482155343F078647F504B81d07871e27d4484"      # Account[3] address GEA

cust1 = "0x15FCf919E5Ed3d5964c3e5cD85EEFce14670AE98"      # Account[1] address customer 1
cust2 = "0xE701AC6f4b0cc12DCF33361e79edF2cEB01A6767"      # Account[2] address customer 2

#minting tickets
#EventHost3 = EventHost("0xDFf43e81a80BdB91EF10d8316b29701d0813A2D6")
#temp_contract = w3.eth.contract(DBMS.getSpecificContract("Event 3"), abi= User.ABI, bytecode = User.Bytecode)
#EventHost3.grantMinterRole(temp_contract)
#gea_e = EventHost(GEA)
#gea_e.mintTicket(temp_contract, "whfljkwef", 500000000000000, 291)
# price in hex 1C6BF52634000

#retrieving ticket information under gea (minted tickets)

gea = User(GEA)
#for x in gea.retrieveAllTickets():
#    print("Event Name: "+ x[0] +"\nEvent Location: "+ x[1] +"\nEvent Type: " + x[2] +
#    "\nEvent Start Date: "+ str(x[3]) +"\nEvent End Date: "+ str(x[4]) +"\nTicket URI: "+ str(x[5]) +
#    "\nTicket Price: "+ str(x[6]) + "\nTicket Sale: "+ str(x[7]) +"\nTicket Seat Number: "+ str(x[8]))
#user buys ticket
# available tickets are under Event 3 (281,290 under gea \\ 280 under customer 2)
customer2 = User(cust2)
#customer2.buyTicket("Event 3")
#for x in customer2.retrieveAllTickets():
#    print("Event Name: "+ x[0] +"\nEvent Location: "+ x[1] +"\nEvent Type: " + x[2] +
#    "\nEvent Start Date: "+ str(x[3]) +"\nEvent End Date: "+ str(x[4]) +"\nTicket URI: "+ str(x[5]) +
#    "\nTicket Price: "+ str(x[6]) + "\nTicket Sale: "+ str(x[7]) +"\nTicket Seat Number: "+ str(x[8]))


customer1 = User(cust1)
#customer1.buyTicket("Event 3")
for x in customer1.retrieveAllTickets():
    print("Event Name: "+ x[0] +"\nEvent Location: "+ x[1] +"\nEvent Type: " + x[2] +
    "\nEvent Start Date: "+ str(x[3]) +"\nEvent End Date: "+ str(x[4]) +"\nTicket URI: "+ str(x[5]) +
    "\nTicket Price: "+ str(x[6]) + "\nTicket Sale: "+ str(x[7]) +"\nTicket Seat Number: "+ str(x[8]))

# event host 2 deploys ticket

#eventhost2 = EventHost("0x8Fc72b1857803359A62f1408F01faA1952a65E59")
#example = eventhost2.deployNFT("Event 6", "E6", "Home", "Rest",1676332800,1676678400)
#print(example.functions.name().call())

#print(DBMS.getAllevents())

#print(w3.eth.get_balance('0x8Fc72b1857803359A62f1408F01faA1952a65E59'))
#print(w3.eth.get_storage_at(GEA, 0))

