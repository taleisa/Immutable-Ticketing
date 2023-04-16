from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView
from django.views import View
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from access.models import Event

class homePage(LoginRequiredMixin, TemplateView):
    template_name = 'marketplace/marketplacePage.html'
    login_url = reverse_lazy("login")

class eventPage(LoginRequiredMixin, TemplateView):
    template_name = 'marketplace/eventPage.html'
    login_url = reverse_lazy("events")
    
class ownedTickets(LoginRequiredMixin,TemplateView):
    template_name  = 'marketplace/myTicket.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User(self.request.user.web3User.wallet_address) 
        # all_tickets = [ticket1,ticket2]
        all_tickets = user.retrieveAllTickets()
        context["tickets"] = all_tickets
        return context
    
    
    
class listTicket(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        ticket_address = args['address']
        ###################################################
        ####Invoke transaction to list ticket on blockchain
        ###################################################
        return HttpResponseRedirect('myTickets')
    
    
from web3 import Web3
# from dbms import DBMS
# from eventhost import EventHost
import json
class User:
    # connecting the blockchain network in ganache
    w3 = Web3(Web3.HTTPProvider('HTTP://127.0.0.1:7545'))
    #retrieving the generated ABI and Byte code from the 
    truffleFile = json.load(open('marketplace/static/marketplace/TicketNFT.json')) # truffle generated file
    ABI = truffleFile['abi'] # ABI generated in the file
    Bytecode = truffleFile['bytecode'] # metadata generated in the file

    def __init__(self, user_address):
        self.user_address = user_address

    def retrieveAllTickets(self):
        # retrieve tickets under the same address
        # tickets array contains an array of tickets each contatins the attributes of the ticket
        # contract_addressess = DBMS.getAllcontracts()
        events = Event.objects.all()
        # Each ticket is a dictionary, list contains all tickets
        tickets = []
        for event in events: # iterate through the contract instances
            # contract instance
            contract = User.w3.eth.contract(address= event.wallet_address, abi= User.ABI, bytecode = User.Bytecode)
            # number of tickets in the entire contract (each event)
            ticket_counter = contract.functions._tokenIdCounter().call()
            for x in range(ticket_counter): # loops through the
                if contract.functions.ticketIndexToOwner(x).call().casefold() == self.user_address:
                    ticket = {}
                    ticket['name'] = contract.functions.name().call()
                    ticket['location'] = contract.functions._eventLocation().call()
                    ticket['eventType'] = contract.functions._eventType().call()
                    ticket['startDate'] = contract.functions._startDate().call()
                    ticket['endDate'] = contract.functions._endDate().call()
                    ticket['tokenURI'] = contract.functions.tokenURI(x).call()
                    ticket['price'] = contract.functions._allTickets(x).call()[0]  
                    ticket['onSale'] = contract.functions._allTickets(x).call()[1]
                    ticket['seatNumber'] =  contract.functions._allTickets(x).call()[2]                   
                    tickets.append(ticket)                    
        return tickets
    # def retrieveSpecificTickets(self, event_name):
    #     # retrieve tickets under the same address
    #     # tickets array contains an array of tickets each contatins the attributes of the ticket
    #     contract_address = DBMS.getSpecificContract(event_name)
    #     tickets = []
    #     # contract instance
    #     contract = User.w3.eth.contract(address= contract_address, abi= User.ABI, bytecode = User.Bytecode)
    #     # number of tickets in the entire contract (each event)
    #     ticket_counter = contract.functions._tokenIdCounter().call()
    #     for x in range(ticket_counter): # loops through the
    #         if contract.functions.ticketIndexToOwner(x).call() == self.user_address:
    #             #event name, location, type, start date, end date, uri, ticket price, for sale, seat number
    #             tickets.append([contract.functions.name().call(),
    #             contract.functions._eventLocation().call(),contract.functions._eventType().call(),
    #             contract.functions._startDate().call(),contract.functions._endDate().call(),
    #             contract.functions.tokenURI(x).call(),contract.functions._allTickets(x).call()[0],
    #             contract.functions._allTickets(x).call()[1],contract.functions._allTickets(x).call()[2]])
    #     return tickets    


    # def buyTicket(self, event_name):
    #     # assumes event_name is unique
    #     #create contract instance of the event the user wants to buy
    #     temp_contract = User.w3.eth.contract(DBMS.getSpecificContract(event_name), abi= User.ABI, bytecode = User.Bytecode)
    #     #grant customer verified accounts role if customer exists in database (assumes customer exists)
    #     event_host = EventHost(DBMS.getEventHostAddress(event_name))
    #     #event_host.grantCustomerRole(self.user_address, temp_contract)
    #     #retrieve the ticket index
    #     ticket_index = 0
    #     gea = User(EventHost.GEA)
    #     for x in gea.retrieveSpecificTickets(event_name):
    #         if x[0] == event_name:
    #             ticket_index = x[1]
    #             print(ticket_index)
    #             #call the buy function to excute transaction
    #             #my_contract.functions.my_function().buildTransaction()
    #             #Eth.sign_transaction(transaction)
    #             #Eth.send_raw_transaction(raw_transaction)
    #             #temp_contract.functions.buy().transact({"from": EventHost.GEA})
    #     #send the transaction to metamask to confirm the transaction
        

                

    # #def resellTicket():
    # #def availableTickets(): #retrieve tickets available to buy

