from datetime import datetime

from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, FormView
from django.views import View
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from access.models import Event
from .forms import listForm


class homePage(LoginRequiredMixin, TemplateView):
    template_name = "marketplace/marketplacePage.html"
    login_url = reverse_lazy("login")


class eventPage(LoginRequiredMixin, TemplateView):
    template_name = "marketplace/eventPage.html"
    login_url = reverse_lazy("events")


class ownedTickets(LoginRequiredMixin, FormView):
    template_name = "marketplace/myTicket.html"
    form_class = listForm

    def form_valid(self, form):
        print("here")
        contract_address = form.cleaned_data["contract_address"]
        ticket_index = form.cleaned_data["ticket_index"]
        user = User(self.request.user.web3User.wallet_address)
        transaction_variables = user.listTicket(ticket_index, contract_address)
        for variable in transaction_variables:
            variable = str(variable)
        return render(
            self.request,
            "marketplace/myTicket.html",
            {"form": form, "transaction_variable": transaction_variables},
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User(self.request.user.web3User.wallet_address)
        # all_tickets = [ticket1,ticket2]
        all_tickets = user.retrieveAllTickets()
        context["tickets"] = all_tickets
        return context


from web3 import Web3

# from dbms import DBMS
# from eventhost import EventHost
import json


class User:
    # connecting the blockchain network in ganache
    w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
    # retrieving the generated ABI and Byte code from the
    truffleFile = json.load(
        open("marketplace/static/marketplace/TicketNFT.json")
    )  # truffle generated file
    ABI = truffleFile["abi"]  # ABI generated in the file
    Bytecode = truffleFile["bytecode"]  # metadata generated in the file

    def __init__(self, user_address):
        self.user_address = Web3.to_checksum_address(user_address)

    def listTicket(self, ticket_index, contract_addrress):
        # Contract the the ticket belongs to

        return tx_dict

    def retrieveAllTickets(self):
        # Dictionary to change from numbers of month to name of month
        dates = {
            "01": "Jan",
            "02": "Feb",
            "03": "Mar",
            "04": "Apr",
            "05": "May",
            "06": "Jun",
            "07": "Jul",
            "08": "Aug",
            "09": "Sep",
            "10": "Oct",
            "11": "Nov",
            "12": "Dec",
        }
        # retrieve tickets under the same address
        # tickets array contains an array of tickets each contatins the attributes of the ticket
        # contract_addressess = DBMS.getAllcontracts()
        events = Event.objects.all()
        # Each ticket is a dictionary, list contains all tickets
        tickets = []
        for event in events:  # iterate through the contract instances
            # contract instance
            contract = User.w3.eth.contract(
                address=event.address, abi=User.ABI, bytecode=User.Bytecode
            )
            # number of tickets in the entire contract (each event)
            ticket_counter = contract.functions._tokenIdCounter().call()
            for x in range(ticket_counter):  # loops through the
                if contract.functions.ticketIndexToOwner(x).call() == self.user_address:
                    ticket = {}
                    ticket["name"] = contract.functions.name().call()
                    ticket["location"] = contract.functions._eventLocation().call()
                    ticket["event_type"] = contract.functions._eventType().call()
                    ticket["start_date_hour"] = datetime.utcfromtimestamp(
                        contract.functions._startDate().call()
                    ).strftime("%H:%M:%S")
                    ticket["end_date_hour"] = datetime.utcfromtimestamp(
                        contract.functions._endDate().call()
                    ).strftime("%H:%M:%S")
                    ticket["start_date_day"] = datetime.utcfromtimestamp(
                        contract.functions._startDate().call()
                    ).strftime("%d")
                    ticket["end_date_day"] = datetime.utcfromtimestamp(
                        contract.functions._endDate().call()
                    ).strftime("%d")
                    ticket["start_date_month"] = dates[
                        datetime.utcfromtimestamp(
                            contract.functions._startDate().call()
                        ).strftime("%m")
                    ]
                    ticket["end_date_month"] = dates[
                        datetime.utcfromtimestamp(
                            contract.functions._endDate().call()
                        ).strftime("%m")
                    ]
                    ticket["start_date"] = datetime.utcfromtimestamp(
                        contract.functions._startDate().call()
                    ).strftime("%Y-%m-%d %H:%M:%S")
                    ticket["end_date"] = datetime.utcfromtimestamp(
                        contract.functions._endDate().call()
                    ).strftime("%Y-%m-%d %H:%M:%S")
                    ticket["token_URI"] = contract.functions.tokenURI(x).call()
                    ticket["price"] = contract.functions._allTickets(x).call()[0]
                    ticket["on_sale"] = contract.functions._allTickets(x).call()[1]
                    ticket["seat_number"] = contract.functions._allTickets(x).call()[2]
                    ticket["contract_address"] = event.address
                    ticket["ticket_index"] = x
                    ticket["abi"] = User.ABI
                    contract = User.w3.eth.contract(
                        address=event.address, abi=User.ABI, bytecode=User.Bytecode
                    )
                    tx_dict = contract.functions.sale(
                        not ticket["on_sale"] , x
                    ).build_transaction(
                        {
                            "from": self.user_address,
                            "nonce": User.w3.eth.get_transaction_count(
                                self.user_address
                            ),
                        }
                    )
                    ticket = {**ticket,**tx_dict}
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
