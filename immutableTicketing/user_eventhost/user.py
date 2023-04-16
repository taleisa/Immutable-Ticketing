from web3 import Web3
from dbms import DBMS
from eventhost import EventHost
import json
class User:
    # connecting the blockchain network in ganache
    w3 = Web3(Web3.HTTPProvider('HTTP://127.0.0.1:7545'))
    #retrieving the generated ABI and Byte code from the 
    truffleFile = json.load(open('/Users/Faisal/desktop/capstone/Immutable-Ticketing/truffle/build/contracts/TicketNFT.json')) # truffle generated file
    ABI = truffleFile['abi'] # ABI generated in the file
    Bytecode = truffleFile['bytecode'] # metadata generated in the file

    GEA = "0x11D5575b8EE64B048b46dDc7942176444e3D8b70"

    def __init__(self, user_address):
        self.user_address = user_address

    def retrieveAllTickets(self):
        # retrieve tickets under the same address
        # tickets array contains an array of tickets each contatins the attributes of the ticket
        contract_addressess = DBMS.getAllcontracts()
        tickets = []
        for y in contract_addressess: # iterate through the contract instances
            # contract instance
            contract = User.w3.eth.contract(address= y[0], abi= User.ABI, bytecode = User.Bytecode)
            # number of tickets in the entire contract (each event)
            ticket_counter = contract.functions._tokenIdCounter().call()
            for x in range(ticket_counter): # loops through the
                if contract.functions.ticketIndexToOwner(x).call() == self.user_address:
                    #event name, location, type, start date, end date, uri, ticket price, for sale, seat number
                    tickets.append([contract.functions.name().call(),
                    contract.functions._eventLocation().call(),contract.functions._eventType().call(),
                    contract.functions._startDate().call(),contract.functions._endDate().call(),
                    contract.functions.tokenURI(x).call(),contract.functions._allTickets(x).call()[0],
                    contract.functions._allTickets(x).call()[1],contract.functions._allTickets(x).call()[2]])
        return tickets
    def retrieveSpecificTickets(self, event_name):
        # retrieve tickets under the same address
        # tickets array contains an array of tickets each contatins the attributes of the ticket
        contract_address = DBMS.getSpecificContract(event_name)
        tickets = []
        # contract instance
        contract = User.w3.eth.contract(address= contract_address, abi= User.ABI, bytecode = User.Bytecode)
        # number of tickets in the entire contract (each event)
        ticket_counter = contract.functions._tokenIdCounter().call()
        for x in range(ticket_counter): # loops through the tickets
            if contract.functions.ticketIndexToOwner(x).call() == self.user_address:
                #event name, location, type, start date, end date, uri, ticket price, for sale, seat number
                tickets.append([contract.functions.name().call(),
                contract.functions._eventLocation().call(),contract.functions._eventType().call(),
                contract.functions._startDate().call(),contract.functions._endDate().call(),
                contract.functions.tokenURI(x).call(),contract.functions._allTickets(x).call()[0],
                contract.functions._allTickets(x).call()[1],contract.functions._allTickets(x).call()[2]])
        return tickets
    #should be static?
    def retrieveTicketInfo(self, event_name):
        # retrieve ticketID and price form available tickets
        # tickets array contains an array of tickets each contatins the attributes of the ticket
        contract_address = DBMS.getSpecificContract(event_name)
        ticketInfo = []
        # contract instance
        contract = User.w3.eth.contract(address= contract_address, abi= User.ABI, bytecode = User.Bytecode)
        # number of tickets in the entire contract (each event)
        ticket_counter = contract.functions._tokenIdCounter().call()
        for x in range(ticket_counter): # loops through the tickets
            if contract.functions.ticketIndexToOwner(x).call() == User.GEA:
                ticketInfo.append(x)
                ticketInfo.append(contract.functions._allTickets(x).call()[0])
                break # retrieve the ticketId and price of the first available ticket
        return ticketInfo    


    def buyTicket(self, event_name):
        # assumes event_name is unique
        #create contract instance of the event the user wants to buy
        temp_contract = User.w3.eth.contract(DBMS.getSpecificContract(event_name), abi= User.ABI, bytecode = User.Bytecode)
        #grant customer verified accounts role if customer exists in database (assumes customer exists)
        event_host = EventHost(DBMS.getEventHostAddress(event_name))
        event_host.grantCustomerRole(self.user_address, temp_contract)
        #retrieve the ticket index
        arr = self.retrieveTicketInfo(event_name)
        ticket_index = arr[0]
        ticket_price = arr[1]
        #call the buy function to excute transaction
        tx_dict = temp_contract.functions.buy(
            ticket_index, temp_contract.encodeABI(fn_name="buy", args= [ticket_index, self.user_address])
                                              ).build_transaction({"from": self.user_address,
                                                                    'value': ticket_price,
                                                                    'nonce': User.w3.eth.get_transaction_count(self.user_address)}) # {'nonce': User.w3.eth.get_transaction_count(self.user_address)} specifies nonce
        print(tx_dict)
        #key = "0x58514bd1f6170c2978b8f5e4aedc9dccf63da236710f9e0e94b7e8296b79c7f4" #for testing purposes only
        #signed_txn = User.w3.eth.account.sign_transaction(tx_dict,key)
        #print(User.w3.eth.send_raw_transaction(signed_txn.rawTransaction))
        #temp_contract.functions.buy().transact({"from": EventHost.GEA})
        #send the transaction to metamask to confirm the transaction
        
                 

                

    #def resellTicket():
    #def availableTickets(): #retrieve tickets available to buy
