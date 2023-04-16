from web3 import Web3
from dbms import DBMS
import json
class EventHost:
    # Defining the address of the GEA and the minter
    GEA = "0x11D5575b8EE64B048b46dDc7942176444e3D8b70"      # Account[3] address GEA
    # connecting the blockchain network in ganache
    w3 = Web3(Web3.HTTPProvider('HTTP://127.0.0.1:7545'))
    #retrieving the generated ABI and Byte code from the 
    truffleFile = json.load(open('/Users/Faisal/desktop/capstone/Immutable-Ticketing/truffle/build/contracts/TicketNFT.json')) # truffle generated file
    ABI = truffleFile['abi'] # ABI generated in the file
    Bytecode = truffleFile['bytecode'] # metadata generated in the file

    def __init__(self, event_host_address):
        self.event_host_address = event_host_address

    def grantMinterRole(self, contract):  
        # Send transaction
        send_tx = contract.functions.grantRole(Web3.solidity_keccak(["bytes32"],[str.encode("MINTER_ROLE")]) ,EventHost.GEA).transact({"from": self.event_host_address})

        # Wait for transaction receipt
        tx_receipt = EventHost.w3.eth.wait_for_transaction_receipt(send_tx)
        return tx_receipt # Optional

    def grantGEARole(self, contract):
        # Send transaction
        send_tx = contract.functions.grantRole(Web3.solidity_keccak(["bytes32"],[str.encode("GEA_ACCOUNTS")]) ,EventHost.GEA).transact({"from": self.event_host_address})

        # Wait for transaction receipt
        tx_receipt = EventHost.w3.eth.wait_for_transaction_receipt(send_tx)
        return tx_receipt # Optional    

    def grantCustomerRole(self, cust_add, contract):
        # Send transaction
        send_tx = contract.functions.grantRole(Web3.solidity_keccak(["bytes32"],[str.encode("VERIFIED_ACCOUNTS")]) ,cust_add).transact({"from": self.event_host_address})

        # Wait for transaction receipt
        tx_receipt = EventHost.w3.eth.wait_for_transaction_receipt(send_tx)
        return tx_receipt # Optional   

    def deployNFT(self, event_name, event_symbol, event_location, event_type, event_start_date, event_end_date): # event_host address is the address of the event host deploying the ticket
        contract = EventHost.w3.eth.contract(abi=EventHost.ABI, bytecode=EventHost.Bytecode)
        tx_hash = contract.constructor(event_name,event_symbol,event_location,event_type, event_start_date ,event_end_date).transact({"from": self.event_host_address})
        tx_receipt = EventHost.w3.eth.wait_for_transaction_receipt(tx_hash)
        # Insert values into the event table
        if tx_receipt.status == 1: # check if the transaction is successfull
            DBMS.insertValues(event_name,event_symbol,event_location,event_type,str(event_start_date),str(event_end_date),self.event_host_address,tx_receipt.contractAddress)
        temp_contract = EventHost.w3.eth.contract(tx_receipt.contractAddress, abi= EventHost.ABI, bytecode = EventHost.Bytecode)
        #grant roles for the NFT instance
        self.grantGEARole(temp_contract)
        self.grantMinterRole(temp_contract) 
        # if possible include the minting here or in the main method
        # self.mintTicket(tempcontract, other information)
        return temp_contract    

    def mintTicket(self, nft_contract, ticket_URI, ticket_price, ticket_seat_number):
        #create nft_contract by querying the database and retreiving the contract address
        nft_contract.functions.safeMint(EventHost.GEA,ticket_URI,ticket_price,ticket_seat_number).transact({"from": EventHost.GEA})    

