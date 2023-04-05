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

def send_transaction(request):
    #load template
    template = loader.get_template('polls/send_transaction.html')
    
    # Connect to an Ethereum node using a provider (e.g., Infura)
    infura_url = 'https://mainnet.infura.io/v3/YOUR-INFURA-PROJECT-ID'
    web3 = Web3(Web3.HTTPProvider(infura_url))

    # Load the contract ABI and address
    with open('contract_abi.json') as f:
        contract_abi = json.load(f)
    contract_address = 'YOUR-CONTRACT-ADDRESS'

    # Get the user's account address from Metamask
    account = request.POST['account']

    # Get the recipient and amount from the user
    recipient = request.POST['recipient']
    amount = request.POST['amount']

    # Create a contract instance using the ABI and address
    contract = web3.eth.contract(address=contract_address, abi=contract_abi)

    # Encode the contract function call data
    data = contract.functions.transfer(recipient, amount).buildTransaction()['data']

    # Build the transaction object
    txn = {
        'to': contract_address,
        'data': data,
        'gas': 200000,
        'gasPrice': web3.eth.gas_price,
        'nonce': web3.eth.getTransactionCount(account),
    }

    # Sign the transaction using Metamask
    signed_txn = web3.eth.account.sign_transaction(txn, private_key=None)

    # Send the signed transaction to the Ethereum network
    txn_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
    txn_receipt = web3.eth.waitForTransactionReceipt(txn_hash)

    # Return the transaction receipt
    return JsonResponse({'status': 'success', 'txn_receipt': txn_receipt})
