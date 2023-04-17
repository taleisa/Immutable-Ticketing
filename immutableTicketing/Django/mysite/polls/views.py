from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
import json
from web3 import Web3
from django.template import loader
from django.views.generic import TemplateView, FormView, View
from .forms import buyForm
from .models import Event, web3User
from web3 import Web3
import json

class buyForm(FormView):
    form_class = buyForm
    template_name = "buy_ticket.html"
    #success_url = "/success/"

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        #return super().form_valid(form)
        buyer = User(Web3.to_checksum_address(form.data["wallet_address"]))
        tx_dict = buyer.createTxDict(form.data["event_name"])
        gas = str(tx_dict["gas"])
        maxFeePerGas = str(tx_dict["maxFeePerGas"])
        maxPriorityFeePerGas = str(tx_dict["maxPriorityFeePerGas"])
        chainId = str(tx_dict["chainId"])
        from_ = str(tx_dict["from"])
        value = str(hex(tx_dict["value"]))
        nonce = str(tx_dict["nonce"])
        to = str(tx_dict["to"])
        data = str(tx_dict["data"])
        return render(self.request, "buy_ticket.html", {"form": form,
                                                        'gas': gas,
                                                        'maxFeePerGas': maxFeePerGas,
                                                        'maxPriorityFeePerGas': maxPriorityFeePerGas,
                                                        'chainId': chainId,
                                                        'from_': from_,
                                                        'value': value,
                                                        'nonce': nonce,
                                                        'to': to,
                                                        'data': data,})
    

class success(TemplateView):
    template_name = "success.html"

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

    #retrieve alltickets and retrieve specific tickets methods should be entered here

    #should be static?
    def retrieveTicketInfo(self, event):
        # retrieve ticketID and price form available tickets
        # tickets array contains an array of tickets each contatins the attributes of the ticket
        ticketInfo = {}
        # contract instance
        contract = User.w3.eth.contract(address= event.contract_address, abi= User.ABI, bytecode = User.Bytecode)
        # number of tickets in the entire contract (each event)
        ticket_counter = contract.functions._tokenIdCounter().call()
        for x in range(ticket_counter): # loops through the tickets
            if contract.functions.ticketIndexToOwner(x).call() == User.GEA:
                ticketInfo['index'] = x
                ticketInfo['price'] = contract.functions._allTickets(x).call()[0]
                break # retrieve the ticketId and price of the first available ticket
        return ticketInfo    

    def testing(self, event_name):
        event = Event.objects.get(id='1')
        return event.event_host.wallet_address
            
    def createTxDict(self, event_name):
        # assumes event_name is unique
        #create contract instance of the event the user wants to buy
        events = Event.objects.all()
        for e in events: # iterate through the contract instances
            if (User.w3.eth.contract(address= e.contract_address, abi= User.ABI, bytecode = User.Bytecode).functions.name().call() == event_name):
                event = Event.objects.get(contract_address=e.contract_address)
        temp_contract = User.w3.eth.contract(event.contract_address, abi= User.ABI, bytecode = User.Bytecode)
        #grant customer verified accounts role if customer exists in database (assumes customer exists) 
        event_host = EventHost(Web3.to_checksum_address(event.event_host.wallet_address))
        event_host.grantCustomerRole(self.user_address, temp_contract)
        #retrieve the ticket index
        arr = self.retrieveTicketInfo(event)
        ticket_index = arr['index']
        ticket_price = arr['price']
        #call the buy function to excute transaction
        tx_dict = temp_contract.functions.buy(
            ticket_index, temp_contract.encodeABI(fn_name="buy", args= [ticket_index, self.user_address])
                                              ).build_transaction({"from": self.user_address,
                                                                    'value': ticket_price,
                                                                    'nonce': User.w3.eth.get_transaction_count(self.user_address)}) # {'nonce': User.w3.eth.get_transaction_count(self.user_address)} specifies nonce
        return tx_dict
        #key = "0x58514bd1f6170c2978b8f5e4aedc9dccf63da236710f9e0e94b7e8296b79c7f4" #for testing purposes only
        #signed_txn = User.w3.eth.account.sign_transaction(tx_dict,key)
        #print(User.w3.eth.send_raw_transaction(signed_txn.rawTransaction))
        #temp_contract.functions.buy().transact({"from": EventHost.GEA})
        #send the transaction to metamask to confirm the transaction
        
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
        #if tx_receipt.status == 1: # check if the transaction is successfull
            #DBMS.insertValues(event_name,event_symbol,event_location,event_type,str(event_start_date),str(event_end_date),self.event_host_address,tx_receipt.contractAddress)
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