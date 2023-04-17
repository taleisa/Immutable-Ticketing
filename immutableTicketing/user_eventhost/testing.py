from web3 import Web3
from eventhost import EventHost
from dbms import DBMS
from user import User

w3 = Web3(Web3.HTTPProvider('HTTP://127.0.0.1:7545'))
deployer = "0xb7e673a25dd38ecf608aE41d48B18c24ddeAb2fd"      # Account[0] address deployer (Event Host)
#deployer_key = "0xf103df4a496a767da8e6aae2c4d0290bae572a52282f5c228223f14b94c4e1e6" # Account[0] private key deployer  
deployer_2 = "0x015Ef7a2Cc0805012216307d20EEf121a082680f"      # Account[5] address deployer (Event Host 2)
GEA = "0x11D5575b8EE64B048b46dDc7942176444e3D8b70"      # Account[3] address GEA

cust1 = "0x79F61a835acb55212915Dd05B546517BEBb2F97D"      # Account[1] address customer 1
cust2 = "0x37Fa79B8af77776E684D01A42d77aCc51AcBCa93"      # Account[2] address customer 2

value = hex(500000000000000)
print(value)

# Define the contract and transaction hash
contract_address = "0x15382Add19aD7DB6D6bD96cf774dafE94A0Fb731"

#tx_hash = '0xbcc048f25b41bf491273ebd36b6e776af9ffecd64ff90b60ed58ad08461a27e6'
#tx_receipt = w3.eth.get_transaction_receipt(tx_hash)
#temp_contract = EventHost.w3.eth.contract('0x15382Add19aD7DB6D6bD96cf774dafE94A0Fb731', abi= EventHost.ABI, bytecode = EventHost.Bytecode)
#processed_logs = temp_contract.events.ValueLogged().process_receipt(tx_receipt)
#print(processed_logs)


#new blockchain code
#eventhost1 = EventHost(deployer)
#DBMS.insertValues("Event 9", "E9", "Home", "Testing",str(1676332800),str(1676678400),eventhost1.event_host_address,'0x15382Add19aD7DB6D6bD96cf774dafE94A0Fb731')
#temp_contract = EventHost.w3.eth.contract('0x15382Add19aD7DB6D6bD96cf774dafE94A0Fb731', abi= EventHost.ABI, bytecode = EventHost.Bytecode)
#grant roles for the NFT instance
#eventhost1.grantGEARole(temp_contract)
#eventhost1.grantMinterRole(temp_contract)

#gea_e = EventHost(GEA)
#gea_e.mintTicket(temp_contract, "whfljkwef", 500000000000000, 502)


#minting tickets
#EventHost3 = EventHost("0xDFf43e81a80BdB91EF10d8316b29701d0813A2D6")
#temp_contract = w3.eth.contract(DBMS.getSpecificContract("Event 3"), abi= User.ABI, bytecode = User.Bytecode)
#EventHost3.grantMinterRole(temp_contract)
#gea_e = EventHost(GEA)
#gea_e.mintTicket(temp_contract, "whfljkwef", 500000000000000, 291)
# price in hex 1C6BF52634000

#retrieving ticket information under gea (minted tickets)

#gea = User(GEA)
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
#customer1.buyTicket("Event 9")
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

