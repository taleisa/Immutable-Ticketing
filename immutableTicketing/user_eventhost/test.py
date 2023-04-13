from web3 import Web3
from eventhost import EventHost
import json

# Defining the address of the GEA and the minter
GEA = "0x1cd482155343F078647F504B81d07871e27d4484"      # Account[3] address GEA
minter = "0x8Fe530263775D54Ae23149ebF8Ad60c133DDFF38"      # Account[4] address minter

def grantMinterRole(minter_add, deployer_add, contract):  
    # Send transaction
    send_tx = contract.functions.grantRole(Web3.solidity_keccak(["bytes32"],[str.encode("MINTER_ROLE")]) ,minter_add).transact({"from": deployer_add})

    # Wait for transaction receipt
    tx_receipt = w3.eth.wait_for_transaction_receipt(send_tx)
    return tx_receipt # Optional

def grantGEARole(GEA_add, deployer_add, contract):
    # Send transaction
    send_tx = contract.functions.grantRole(Web3.solidity_keccak(["bytes32"],[str.encode("GEA_ACCOUNTS")]) ,GEA_add).transact({"from": deployer_add})

    # Wait for transaction receipt
    tx_receipt = w3.eth.wait_for_transaction_receipt(send_tx)
    return tx_receipt # Optional    

def grantCustomerRole(cust_add, deployer_add, contract):
    # Send transaction
    send_tx = contract.functions.grantRole(Web3.solidity_keccak(["bytes32"],[str.encode("VERIFIED_ACCOUNTS")]) ,cust_add).transact({"from": deployer_add})

    # Wait for transaction receipt
    tx_receipt = w3.eth.wait_for_transaction_receipt(send_tx)
    return tx_receipt # Optional   

def deployNFT(abi, bytecode, event_name, event_symbol, event_location, event_type, event_start_date, event_end_date, event_host_address): # event_host address is the address of the event host deploying the ticket
    contract = w3.eth.contract(abi=abi, bytecode=bytecode)
    tx_hash = contract.constructor(event_name,event_symbol,event_location,event_type, event_start_date ,event_end_date).transact({"from": event_host_address})
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    #call method to save information in databse
    temp_contract = w3.eth.contract(tx_receipt.contractAddress, abi= ABI, bytecode = Bytecode)
    #grant roles for the NFT instance
    grantMinterRole(minter, event_host_address, temp_contract)
    grantGEARole(GEA, event_host_address, temp_contract) 
    return temp_contract    

def mintTicket(nft_contract, ticket_URI, ticket_price, ticket_seat_number, minter):
    #create nft_contract by querying the database and retreiving the contract address
    nft_contract.functions.safeMint(GEA,ticket_URI,ticket_price,ticket_seat_number).transact({"from": minter})    

def retrieveTickets(contract_addressess, owner_address): # event contract address
    # retrieve tickets under the same address
    # tickets array contains an array of tickets each contatins the attributes of the ticket
    tickets = []
    for y in contract_addressess: # iterate through the contract instances
        # contract instance
        contract = w3.eth.contract(address= y, abi= ABI, bytecode = Bytecode)
        # number of tickets in the entire contract (each event)
        ticket_counter = contract.functions._tokenIdCounter().call()
        for x in range(ticket_counter): # loops through the
            if contract.functions.ticketIndexToOwner(x).call() == owner_address:
                #event name, location, type, start date, end date, uri, ticket price, for sale, seat number
                tickets.append([contract.functions.name().call(),
                contract.functions._eventLocation().call(),contract.functions._eventType().call(),
                contract.functions._startDate().call(),contract.functions._endDate().call(),
                contract.functions.tokenURI(x).call(),contract.functions._allTickets(x).call()[0],
                contract.functions._allTickets(x).call()[1],contract.functions._allTickets(x).call()[2]])
    return tickets 


w3 = Web3(Web3.HTTPProvider('HTTP://127.0.0.1:7545'))

NFT_token_addr = "0x38a2A4f07Ebf04A94F978035bAbfEbf3C88Cb309"    # Event 0 version v1.0
NFT_token_addr_2 = "0xf72f8C7c61c493305594D2b4378014ba3637dFeD"  # Event 1 version v1.0
NFT_token_addr_3 = "0x8242883d369EB1944DFC4658fF5beC4a406Ca71e" # Test 1 version v1.0
NFT_token_addr_4 = "0x539c9e3892240AEEc1d60cB79bD16b731ed2B834" # Event 2 version v1.1
NFT_token_addr_5 = "0xA7003eAB97BCEA0D429fB6D8E8059A7D1CC48E00" # Event 3 version v1.2

deployer = "0xDFf43e81a80BdB91EF10d8316b29701d0813A2D6"      # Account[0] address deployer (Event Host)
deployer_key = "0xf103df4a496a767da8e6aae2c4d0290bae572a52282f5c228223f14b94c4e1e6" # Account[0] private key deployer


truffleFile = json.load(open('/Users/Faisal/desktop/capstone/Immutable-Ticketing/truffle/build/contracts/TicketNFT.json')) # truffle generated file

ABI = truffleFile['abi'] # ABI generated in the file
Bytecode = truffleFile['bytecode'] # metadata generated in the file
nft_contract = w3.eth.contract(address= NFT_token_addr, abi= ABI, bytecode = Bytecode) # linking the nft address with nft Event 0
nft2_contract = w3.eth.contract(address= NFT_token_addr_2, abi= ABI, bytecode = Bytecode) # linking the nft address with nft Event 1
nft3_contract = w3.eth.contract(address= NFT_token_addr_3, abi= ABI, bytecode = Bytecode) # linking the nft address with nft Test 1
nft4_contract = w3.eth.contract(address= NFT_token_addr_4, abi= ABI, bytecode = Bytecode) # linking the nft address with nft Event 2
nft5_contract = w3.eth.contract(address= NFT_token_addr_5, abi= ABI, bytecode = Bytecode) # linking the nft address with nft Event 3

# Granting roles

#print(grantMinterRole(minter, deployer , nft5_contract))
#print(grantGEARole(GEA, deployer, nft5_contract))
#print(grantMinterRole(minter, deployer , nft2_contract))
#print(grantGEARole(GEA, deployer, nft2_contract))
#print(grantMinterRole(minter, deployer, nft3_contract))
#print(grantGEARole(GEA, deployer, nft3_contract))
# print(grantCustomerRole(cust1, deployer, nft_contract))
# print(grantCustomerRole(cust2, deployer, nft_contract))

# event host deploys ticket

#example = deployNFT(ABI, Bytecode, "Test 1", "T1", "Testing env", "Testing",1676332800,1676678400, deployer)
#print(example.functions.name().call())

#print(nft_contract.functions.hasRole(Web3.solidity_keccak(["bytes32"],[str.encode("MINTER_ROLE")]) ,minter).call())


# GEA mints tickets

# GEA has 4 minted tickets of Event 0, 1 minted ticket of Event 1, and 1 minted ticket of Test 1

#mintTicket(nft5_contract, "whfljkwef", 500000000000000000, 280, minter)
#mintTicket(nft5_contract, "whfljkwef", 500000000000000000, 281, minter)
#mintTicket(nft_contract, "whfljkwef", 500000000000000000, 261, minter)
#mintTicket(nft2_contract, "whfljkwef", 500000000000000000, 262, minter)
#mintTicket(nft3_contract, "whfljkwef", 500000000000000000, 263, minter)

#retrieving the tickets
#print(nft5_contract.functions.ticketIndexToOwner(0).call())
#print(nft5_contract.functions._allTickets(0).call()[2])
#print(nft5_contract.functions.balanceOf(GEA).call())

#adressess = [NFT_token_addr_5]
#print(len(retrieveTickets(adressess, GEA)))
#for x in retrieveTickets(adressess, GEA):
#    print("Event Name: "+ x[0] +"\nEvent Location: "+ x[1] +"\nEvent Type: " + x[2] +
#    "\nEvent Start Date: "+ str(x[3]) +"\nEvent End Date: "+ str(x[4]) +"\nTicket URI: "+ str(x[5]) +
#    "\nTicket Price: "+ str(x[6]) + "\nTicket Sale: "+ str(x[7]) +"\nTicket Seat Number: "+ str(x[8]))

#print(nft5_contract.functions._tokenIdCounter().call())


#main

#print(w3.eth.get_proof(GEA, [0], 31))

#print(nft_contract.all_functions())

#print(nft_contract.all_functions())
#print(nft_contract.events.myEvent().process_receipt("")[0]['args'])
#print(nft_contract._allTickets[0]._eventName)

# print(nft_contract.functions.name().call())
#print(Web3.solidity_keccak(["bytes32"],[str.encode("MINTER_ROLE")]))
#print(nft_contract.functions.balanceOf(GEA).call())
#print(nft2_contract.functions.balanceOf(GEA).call())
#print(nft3_contract.functions.balanceOf(GEA).call())
#print(nft4_contract.functions.balanceOf(GEA).call())


#testing
# w3.eth.account.create()
# print(w3.eth.accounts)
# print(nft_contract.functions.name().call())
# print(nft_contract.functions.name().call)
# name = nft_contract.functions.name().call()
# symbol = nft_contract.functions.symbol().call()
# nft_auctions = nft_contract.functions.balanceOf(minter).call()
# print(f"{name} [{symbol}] NFTs in Auctions: {nft_auctions}")


