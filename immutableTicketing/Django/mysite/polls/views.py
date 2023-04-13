from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
from web3 import Web3
from django.template import loader

def load_template(request):
    #get ABI
    truffleFile = json.load(open('/Users/Faisal/desktop/capstone/Immutable-Ticketing/truffle/build/contracts/TicketNFT.json')) # truffle generated file
    abi = truffleFile['abi'] # ABI generated in the file

    #Get contract address
    contract_address = "0xDFf43e81a80BdB91EF10d8316b29701d0813A2D6"

    return render(request, 'buy_ticket.html', {"contract_address": contract_address , "contract_abi": abi})

def send_transaction(request, account):
    #get ABI
    truffleFile = json.load(open('/Users/Faisal/desktop/capstone/Immutable-Ticketing/truffle/build/contracts/TicketNFT.json')) # truffle generated file
    abi = truffleFile['abi'] # ABI generated in the file
    Bytecode = truffleFile['bytecode'] # metadata generated in the file

    #Get contract address
    contract_address = "0xDFf43e81a80BdB91EF10d8316b29701d0813A2D6" #example address

    
    # assumes event_name is unique
    #create contract instance of the event the user wants to buy
    w3 = Web3(Web3.HTTPProvider('HTTP://127.0.0.1:7545'))
    temp_contract = w3.eth.contract(contract_address, abi= abi, bytecode = Bytecode)

    #grant customer verified accounts role if customer exists in database (assumes customer exists)

    #event_host = EventHost(DBMS.getEventHostAddress(event_name))
    #event_host.grantCustomerRole(account, temp_contract)

    #retrieve the ticket index
    #arr = self.retrieveTicketInfo(event_name)
    ticket_index = 3 #arr[0]
    ticket_price = 500000000000000 #arr[1]

    #call the buy function to excute transaction
    tx_dict = temp_contract.functions.buy(
        ticket_index, temp_contract.encodeABI(fn_name="buy", args= [ticket_index, account])
                                              ).build_transaction({"from": account,
                                                                    'value': ticket_price,
                                                                    'nonce': w3.eth.get_transaction_count(account)}) # {'nonce': User.w3.eth.get_transaction_count(self.user_address)} specifies nonce
    print(tx_dict)
        #key = "0x58514bd1f6170c2978b8f5e4aedc9dccf63da236710f9e0e94b7e8296b79c7f4" #for testing purposes only
        #signed_txn = User.w3.eth.account.sign_transaction(tx_dict,key)
        #print(User.w3.eth.send_raw_transaction(signed_txn.rawTransaction))
        #temp_contract.functions.buy().transact({"from": EventHost.GEA})
        #send the transaction to metamask to confirm the transaction
    return render(request, 'buy_ticket.html', {"contract_address": contract_address , "contract_abi": abi, "tx_dict": tx_dict})