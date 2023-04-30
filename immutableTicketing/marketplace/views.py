from datetime import datetime
import json

from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, FormView
from django.views import View
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from access.models import Event, Gate
from immutableTicketing.settings import TRUFFLE_PATH, WEB3_ADDRESS
from .forms import listForm
from django.contrib import messages
from web3 import Web3


class homePage(LoginRequiredMixin, TemplateView):
    template_name = "marketplace/homePage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = QueryBC()
        context["tickets"] = query.retrieveAllTickets(self.request)
        context["events"] = query.retreiveAllEvents()
        return context

class marketplace(LoginRequiredMixin, TemplateView):
    template_name = "marketplace/marketplacePage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = QueryBC()
        try:# Check if parameter has been passed through url
            contract_address = kwargs['contract_address']
        except:# If no parameters have beem passed throughg the url pass the entire page
            context["tickets"] = query.retrieveAllTickets(self.request)
        else:# If parameters were passed through url query tickets belonging to that contract(event)
            context["tickets"] = query.retreiveEventTickets(self.request, contract_address)

        context["events"] = query.retreiveAllEvents()
        return context


class eventPage(LoginRequiredMixin, TemplateView):
    template_name = "marketplace/eventPage.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contract_address = kwargs['contract_address']
        context["event"] = QueryBC().retreiveSingleEvent(self.request, contract_address)
        return context
    
class eventTickets(LoginRequiredMixin,TemplateView):
    template_name = 'marketplace/checkoutPage.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contract_address = kwargs['contract_address']
        context["tickets"] = QueryBC().retreiveEventTickets(self.request, contract_address)
        return context
    

class ownedTickets(LoginRequiredMixin, TemplateView):
    template_name = "marketplace/myTicket.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User(self.request.user.web3User.wallet_address)
        all_tickets = user.retrieveAllTickets(self.request)
        context["tickets"] = all_tickets
        return context


class singleTicket(LoginRequiredMixin, TemplateView):
    template_name = "marketplace/marketPlaceTicketPage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contract_address = kwargs["contract_address"]
        ticket_index = kwargs["ticket_index"]
        context["ticket"] = QueryBC().retrieveSingleTicket(
            self.request,
            contract_address,
            ticket_index,
            self.request.user.web3User.wallet_address,
        )
        return context





class QueryBC:
    # connecting the blockchain network in ganache
    w3 = Web3(Web3.HTTPProvider(WEB3_ADDRESS))
    # retrieving the generated ABI and Byte code from the
    truffleFile = json.load(
        open(TRUFFLE_PATH)
    )  # truffle generated file
    ABI = truffleFile["abi"]  # ABI generated in the file
    Bytecode = truffleFile["bytecode"]  # metadata generated in the file
    dates = {# Dictionary to change from numbers of month to name of month
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
    # Retreieve all tickets that belong to all contracts in DB
    def retrieveAllTickets(self, request):

        events = Event.objects.all()
        # Each ticket is a dictionary, list contains all tickets
        tickets = []
        for event in events:  # iterate through the contract instances
            # contract instance
            contract = QueryBC.w3.eth.contract(
                address=event.address, abi=QueryBC.ABI, bytecode=QueryBC.Bytecode
            )
            # number of tickets in the entire contract (each event)
            try:
                ticket_counter = contract.functions._tokenIdCounter().call()
            except:
                messages.error(request, "Blockchain connection error")
                return None
            for index in range(ticket_counter):  # loops through the tickets
                # If ticket belongs to user do not add it
                if (
                    not contract.functions.ticketIndexToOwner(index).call()
                    == request.user.web3User.wallet_address
                ):
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
                    ticket["start_date_month"] = self.dates[
                        datetime.utcfromtimestamp(
                            contract.functions._startDate().call()
                        ).strftime("%m")
                    ]
                    ticket["end_date_month"] = self.dates[
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
                    ticket["token_URI"] = contract.functions.tokenURI(index).call()
                    ticket["price"] = QueryBC.w3.from_wei(contract.functions._allTickets(index).call()[0], 'ether')
                    ticket["on_sale"] = contract.functions._allTickets(index).call()[1]
                    ticket["seat_number"] = contract.functions._allTickets(index).call()[2]
                    ticket["contract_address"] = event.address
                    ticket["ticket_index"] = index
                    tickets.append(ticket)
        return tickets

    def retrieveSingleTicket(self, request, contract_address, ticket_index, user_address):

        # retrieve tickets under the same address
        # tickets array contains an array of tickets each contatins the attributes of the ticket
        # contract_addressess = DBMS.getAllcontracts()
        try:
            event = Event.objects.get(address=contract_address)
        except:
            messages.error(request, "Event does not exist")
            return None
        # Each ticket is a dictionary, list contains all tickets
        tickets = []
        # contract instance
        contract = User.w3.eth.contract(
            address=event.address, abi=User.ABI, bytecode=User.Bytecode
        )
        # number of tickets in the entire contract (each event)
        try:
            ticket_counter = contract.functions._tokenIdCounter().call()
        except:
            messages.error(request, "Blockchain connection error")
            return None

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
        ticket["start_date_month"] = self.dates[
            datetime.utcfromtimestamp(contract.functions._startDate().call()).strftime(
                "%m"
            )
        ]
        ticket["end_date_month"] = self.dates[
            datetime.utcfromtimestamp(contract.functions._endDate().call()).strftime(
                "%m"
            )
        ]
        ticket["start_date_year"] = datetime.utcfromtimestamp(
            contract.functions._startDate().call()
        ).strftime("%Y")
        ticket["end_date_year"] = datetime.utcfromtimestamp(
            contract.functions._endDate().call()
        ).strftime("%Y")
        ticket["start_date"] = datetime.utcfromtimestamp(
            contract.functions._startDate().call()
        ).strftime("%Y-%m-%d %H:%M:%S")
        ticket["end_date"] = datetime.utcfromtimestamp(
            contract.functions._endDate().call()
        ).strftime("%Y-%m-%d %H:%M:%S")
        ticket["token_URI"] = contract.functions.tokenURI(ticket_index).call()
        ticket["price"] = QueryBC.w3.from_wei(contract.functions._allTickets(ticket_index).call()[0], 'ether')
        ticket["on_sale"] = contract.functions._allTickets(ticket_index).call()[1]
        ticket["seat_number"] = contract.functions._allTickets(ticket_index).call()[2]
        ticket["contract_address"] = event.address
        ticket["ticket_index"] = ticket_index
        try:
            tx_dict = contract.functions.buy(
                ticket_index,
                contract.encodeABI(fn_name="buy", args=[ticket_index, user_address]),
            ).build_transaction(
                {
                    "from": user_address,
                    "value": hex(contract.functions._allTickets(ticket_index).call()[0]),
                    "nonce": QueryBC.w3.eth.get_transaction_count(user_address),
                }
            )
        except:
            messages.error(request, "Ticket not for sale/ You don't have the proper role")
            return None
        ticket = {**ticket, **tx_dict}
        return ticket

    def retreiveAllEvents(self):
        db_events = Event.objects.all()
        
        events = []
        for db_event in db_events:
            contract = User.w3.eth.contract(
            address=db_event.address, abi=User.ABI, bytecode=User.Bytecode
            )
            event = {}
            event["name"] = contract.functions.name().call()
            event["location"] = contract.functions._eventLocation().call()
            event["event_type"] = contract.functions._eventType().call()
            event["start_date_hour"] = datetime.utcfromtimestamp(
                contract.functions._startDate().call()
            ).strftime("%H:%M:%S")
            event["end_date_hour"] = datetime.utcfromtimestamp(
                contract.functions._endDate().call()
            ).strftime("%H:%M:%S")
            event["start_date_day"] = datetime.utcfromtimestamp(
                contract.functions._startDate().call()
            ).strftime("%d")
            event["end_date_day"] = datetime.utcfromtimestamp(
                contract.functions._endDate().call()
            ).strftime("%d")
            event["start_date_month"] = self.dates[
                datetime.utcfromtimestamp(contract.functions._startDate().call()).strftime(
                    "%m"
                )
            ]
            event["end_date_month"] = self.dates[
                datetime.utcfromtimestamp(contract.functions._endDate().call()).strftime(
                    "%m"
                )
            ]
            event["start_date_year"] = datetime.utcfromtimestamp(
                contract.functions._startDate().call()
            ).strftime("%Y")
            event["end_date_year"] = datetime.utcfromtimestamp(
                contract.functions._endDate().call()
            ).strftime("%Y")
            event["start_date"] = datetime.utcfromtimestamp(
                contract.functions._startDate().call()
            ).strftime("%Y-%m-%d %H:%M:%S")
            event["end_date"] = datetime.utcfromtimestamp(
                contract.functions._endDate().call()
            ).strftime("%Y-%m-%d %H:%M:%S")
            event["token_URI"] = contract.functions.tokenURI(0).call()
            event["contract_address"] = db_event.address
            events.append(event)
        return events

    def retreiveSingleEvent(self,request,contract_address):
        try:
            db_event = Event.objects.get(address=contract_address)
        except:
            messages.error(request, "Event does not exist")
            return None
        contract = User.w3.eth.contract(
        address=db_event.address, abi=User.ABI, bytecode=User.Bytecode
        )
        event = {}
        event["name"] = contract.functions.name().call()
        event["location"] = contract.functions._eventLocation().call()
        event["event_type"] = contract.functions._eventType().call()
        event["start_date_hour"] = datetime.utcfromtimestamp(
            contract.functions._startDate().call()
        ).strftime("%H:%M:%S")
        event["end_date_hour"] = datetime.utcfromtimestamp(
            contract.functions._endDate().call()
        ).strftime("%H:%M:%S")
        event["start_date_day"] = datetime.utcfromtimestamp(
            contract.functions._startDate().call()
        ).strftime("%d")
        event["end_date_day"] = datetime.utcfromtimestamp(
            contract.functions._endDate().call()
        ).strftime("%d")
        event["start_date_month"] = self.dates[
            datetime.utcfromtimestamp(contract.functions._startDate().call()).strftime(
                "%m"
            )
        ]
        event["end_date_month"] = self.dates[
            datetime.utcfromtimestamp(contract.functions._endDate().call()).strftime(
                "%m"
            )
        ]
        event["start_date_year"] = datetime.utcfromtimestamp(
            contract.functions._startDate().call()
        ).strftime("%Y")
        event["end_date_year"] = datetime.utcfromtimestamp(
            contract.functions._endDate().call()
        ).strftime("%Y")
        event["start_date"] = datetime.utcfromtimestamp(
            contract.functions._startDate().call()
        ).strftime("%Y-%m-%d %H:%M:%S")
        event["end_date"] = datetime.utcfromtimestamp(
            contract.functions._endDate().call()
        ).strftime("%Y-%m-%d %H:%M:%S")
        event["token_URI"] = contract.functions.tokenURI(0).call()
        event["contract_address"] = db_event.address
        return event

    def retreiveEventTickets(self,request,contract_address):
        
        try:
            db_event = Event.objects.get(address=contract_address)
        except:
            messages.error(request, "Event does not exist")
            return None
        # contract instance
        contract = QueryBC.w3.eth.contract(
            address=contract_address, abi=QueryBC.ABI, bytecode=QueryBC.Bytecode
        )
        try:
            ticket_counter = contract.functions._tokenIdCounter().call()
        except:
            messages.error(request, "Blockchain connection error")
            return None
        
        # Each ticket is a dictionary, list contains all tickets
        tickets = []
        for index in range(ticket_counter):  # loops through the tickets
                # If ticket belongs to user do not add it
                if (
                    not contract.functions.ticketIndexToOwner(index).call()
                    == request.user.web3User.wallet_address
                ):
            # number of tickets in the entire contract (each event)
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
                    ticket["start_date_month"] = self.dates[
                        datetime.utcfromtimestamp(
                            contract.functions._startDate().call()
                        ).strftime("%m")
                    ]
                    ticket["end_date_month"] = self.dates[
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
                    ticket["token_URI"] = contract.functions.tokenURI(index).call()
                    ticket["price"] = QueryBC.w3.from_wei(contract.functions._allTickets(index).call()[0], 'ether')
                    ticket["on_sale"] = contract.functions._allTickets(index).call()[1]
                    ticket["seat_number"] = contract.functions._allTickets(index).call()[2]
                    ticket["contract_address"] = contract_address
                    ticket["ticket_index"] = index
                    try:
                        tx_dict = contract.functions.buy(
                            index,
                            contract.encodeABI(fn_name="buy", args=[index, request.user.web3User.wallet_address]),
                        ).build_transaction(
                            {
                                "from": request.user.web3User.wallet_address,
                                "value": hex(contract.functions._allTickets(index).call()[0]),
                                "nonce": QueryBC.w3.eth.get_transaction_count(request.user.web3User.wallet_address),
                            }
                        )
                    except:
                        pass
                    else:
                        ticket = {**ticket, **tx_dict}
                        tickets.append(ticket)
        return tickets
        

class User:
    # connecting the blockchain network in ganache
    w3 = Web3(Web3.HTTPProvider(WEB3_ADDRESS))
    # retrieving the generated ABI and Byte code from the
    truffleFile = json.load(
        open(TRUFFLE_PATH)
    )  # truffle generated file
    ABI = truffleFile["abi"]  # ABI generated in the file
    Bytecode = truffleFile["bytecode"]  # metadata generated in the file

    def __init__(self, user_address):
        self.user_address = Web3.to_checksum_address(user_address)

    def listTicket(self, ticket_index, contract_addrress):
        # Contract the the ticket belongs to

        return tx_dict

    def retrieveAllTickets(self, request):
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

        events = Event.objects.all()
        try:
            gate = Gate.objects.first()
        except:
            messages.error(request, "No gates available")
            gate = False

        # Each ticket is a dictionary, list contains all tickets
        tickets = []
        for event in events:  # iterate through the contract instances
            # contract instance
            contract = User.w3.eth.contract(
                address=event.address, abi=User.ABI, bytecode=User.Bytecode
            )
            # number of tickets in the entire contract (each event)
            try:
                ticket_counter = contract.functions._tokenIdCounter().call()
            except:
                messages.error(request, "Blockchain connection error")
                return None
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
                    ticket["price"] = User.w3.from_wei(contract.functions._allTickets(x).call()[0], 'ether')
                    ticket["on_sale"] = contract.functions._allTickets(x).call()[1]
                    ticket["seat_number"] = contract.functions._allTickets(x).call()[2]
                    ticket["contract_address"] = event.address
                    ticket["ticket_index"] = x
                    ticket["abi"] = User.ABI
                    contract = User.w3.eth.contract(
                        address=event.address, abi=User.ABI, bytecode=User.Bytecode
                    )
                    tx_dict = contract.functions.sale(
                        not ticket["on_sale"], x
                    ).build_transaction(
                        {
                            "from": self.user_address,
                            "nonce": User.w3.eth.get_transaction_count(
                                self.user_address
                            ),
                        }
                    )
                    ticket = {**ticket, **tx_dict}
                    if not ticket["on_sale"] and gate:
                        tx_dict = contract.functions.useTicket(
                            gate.address, x,contract.encodeABI(fn_name="useTicket", args=[gate.address,x, self.user_address]),
                        ).build_transaction(
                            {
                                "from": self.user_address,
                                "nonce": User.w3.eth.get_transaction_count(
                                    self.user_address
                                ),
                            }
                        )
                        ticket["use_ticket_data"] = tx_dict["data"]
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
