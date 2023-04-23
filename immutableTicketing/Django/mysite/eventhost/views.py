from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib import messages
from django.db import IntegrityError
from django.urls import reverse_lazy
from django.template import loader
from django.views.generic import TemplateView, FormView, View
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login
import pytz
from .forms import loginForm, signupForm
from .models import Event, web3User, SignUpRequest, EventRequest
from web3 import Web3
import json
from datetime import datetime
from operator import itemgetter
# Create your views here.
class loginView(FormView):
    template_name = 'eventhost/index.html'
    success_url = reverse_lazy('dashboard')
    form_class = loginForm
    def form_valid(self, form):
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
            # A backend authenticated the credentials
                try:
                    web3user = web3User.objects.get(user = user)
                except:
                    messages.error(self.request, 'Access Denied')
                    self.success_url = reverse_lazy('login')
                    return super(loginView, self).form_valid(form)    
                else:    
                    if web3user.is_event_host == True:
                        login(self.request, user)
                        return super(loginView, self).form_valid(form)
                    else: #add another else for GEA to access GEA page
                        messages.error(self.request, 'Access Denied')
                        self.success_url = reverse_lazy('login')
                        return super(loginView, self).form_valid(form)
            else:
            # No backend authenticated the credentials
                messages.error(self.request, 'Incorrect Credentials')
                self.success_url = reverse_lazy('login')
                return super(loginView, self).form_valid(form)
            

class signUp(FormView):
    template_name = 'eventhost/signup.html'
    success_url = reverse_lazy('login')
    form_class = signupForm
    
    def form_valid(self, form):
        if (form.cleaned_data['password1'] == form.cleaned_data['password2']):# errors for form: password does not match
            sign = SignUpRequest(companyName=form.cleaned_data['companyName'],
                                companyEmail=form.cleaned_data['companyEmail'],
                                password1=form.cleaned_data['password1'],
                                password2=form.cleaned_data['password2'],
                                wallet_address=form.cleaned_data['walletAddress'],)
            try: # errors for saving: company name, email, or wallet already exists 
                sign.save()
            except:
                messages.error(self.request, 'Company has already requested account')
                self.success_url = reverse_lazy('signup')
                return super(signUp, self).form_valid(form)
            else:
                self.success_url = reverse_lazy('login')
                return super(signUp, self).form_valid(form)
        else:
            messages.error(self.request, 'Password does not match')
            self.success_url = reverse_lazy('signup')
            return super(signUp, self).form_valid(form) 

    #def form_invalid(self, form):
    #    if (form.cleaned_data['wallet_address'] is None):
    #        messages.error(self.request, 'Did not connect Metamask')
    #        return super(signUp, self).form_invalid(form)      
              

#class signUp(View):
#    def get(self, request, *args, **kwargs):
#        context = {'form': signupForm()}
#        return render(request, 'eventhost/signup.html', context)
#
#    def post(self, request, *args, **kwargs):
#        form = signupForm(request.POST)
#        if form.is_valid():
#            book = form.save()
#            book.save()
#            return HttpResponseRedirect(reverse_lazy('login'))
#        return render(request, 'eventhost/signup.html', {'form': form})                
    
class dashboard(LoginRequiredMixin, TemplateView):
    template_name = 'eventhost/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        #retrieve a list of events under the same event host address
        eventHost = web3User.objects.get(user = user)
        eventlist = []
        eventinfo = {} 
        #add if statement if eventhost does not have events add none to eventlist eventlist.append('none')
        eventinfo['event'] = '-'
        eventinfo['contract'] = None
        eventlist.append(eventinfo)
        if(len(eventHost.event_set.all()) != 0):
            for event in eventHost.event_set.all():
                eventinfo = {}
                contract = EventHost.w3.eth.contract(address= event.contract_address, abi= EventHost.ABI, bytecode = EventHost.Bytecode)
                eventinfo['event'] = contract.functions.name().call()
                eventinfo['contract'] = event.contract_address
                eventlist.append(eventinfo)
            #display info   eventlist[0]['contract'] 
        #else:
        #    eventinfo = {} 
        #    eventinfo['event'] = '-'
        #    eventinfo['contract'] = '-'
        #    eventlist.append(eventinfo)
            #display info for -                       
        context = {
            'eventlist':eventlist,
        }
        return context  
    
    def post(self, request, *args, **kwargs):
        #selected_event = request.POST.get('event')
        selected_contract = request.POST.get('contract')
        if(selected_contract != "None"):
            contract = EventHost.w3.eth.contract(address= selected_contract, abi= EventHost.ABI, bytecode = EventHost.Bytecode)
            ticketsListed = contract.functions._tokenIdCounter().call()
            geaTickets = 0 #tickets under GEA that did not change ownership
            tickets_relisted = 0 #tickets under GEA that changed ownership
            gateTickets = 0
            tickets = []
            for x in range(ticketsListed): # loops through the tickets
                if contract.functions.ticketIndexToOwner(x).call() == EventHost.GEA:
                    geaTickets = geaTickets + 1
                else:
                    #if ticket not under gea and has been relisted 
                    if (contract.functions._allTickets(x).call()[1] == True): # for sale == True
                        tickets_relisted = tickets_relisted + 1
                if contract.functions.ticketIndexToOwner(x).call() == EventHost.GATE:
                    gateTickets = gateTickets + 1
                     
                ticketInfo = {}
                ticketInfo['id'] = x
                ticketInfo['price'] = EventHost.w3.from_wei(contract.functions._allTickets(x).call()[0], 'ether')
                ticketInfo['owner'] = contract.functions.ticketIndexToOwner(x).call()
                ticketInfo['event'] = contract.functions.name().call()
                tickets.append(ticketInfo)        
            tickets_sold = ticketsListed - geaTickets 
            tickets_used = gateTickets #tickets under Gate
        else:
            ticketsListed = 'NA'
            tickets_sold = 'NA'
            tickets_relisted = 'NA'
            tickets_used = 'NA'  
            tickets = []         
        response_data = {
            'ticketsListed':ticketsListed,
            'ticketsSold':tickets_sold,
            'ticketsRelisted':tickets_relisted,
            'ticketsUsed':tickets_used,
            'tickets':tickets,
        }
        return JsonResponse(response_data)
  
class tickets(TemplateView):
    template_name = 'eventhost/ticket-record.html'  
    # event_filter = w3.eth.filter({"address": contract_address})
    # for event in event_filter.get_new_entries():     

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contract_address = self.kwargs.get('contract', None)
        id = self.kwargs.get('id', None)
        # define your local time zone
        local_tz = pytz.timezone('Etc/GMT+3')
        
        # get the contract instance
        contract = EventHost.w3.eth.contract(address=contract_address, abi=EventHost.ABI)
        #ticket information context contract.functions._allTickets(x).call()[1] 
        utc_start_date = datetime.utcfromtimestamp(contract.functions._startDate().call())
        local_start_date = pytz.utc.localize(utc_start_date).astimezone(local_tz)       
        ticketStartDate = local_start_date.strftime('%Y/%m/%d %H:%M')
        utc_end_date = datetime.utcfromtimestamp(contract.functions._endDate().call())
        local_end_date = pytz.utc.localize(utc_end_date).astimezone(local_tz)
        ticketEndDate = local_end_date.strftime('%Y/%m/%d %H:%M')
        ticketLocation = contract.functions._eventLocation().call()
        ticketPrice = EventHost.w3.from_wei(contract.functions._allTickets(id).call()[0], 'ether') 
        ticketSale = contract.functions._allTickets(id).call()[1] 
        ticketSeat = contract.functions._allTickets(id).call()[2]
        ticketClass = contract.functions._allTickets(id).call()[3]
        ticketOwner = contract.functions.ticketIndexToOwner(id).call() 

        #tickets transaction table context
        events = []
        # get the event filter object
        mintEvent_filter = contract.events.MintEvent.create_filter(fromBlock=0)

        # get the logs for the event
        mintlogs = EventHost.w3.eth.get_filter_logs(mintEvent_filter.filter_id)

        # loop through the logs and print the data
        for log in mintlogs:
            decoded_log = contract.events.MintEvent().process_log(log)
            #print(decoded_log)
            tokenId = decoded_log['args']['tokenId']
            if(tokenId == id):
                eventinfo = {}
                eventinfo['event'] = "Minted"
                eventinfo['price'] = ""
                eventinfo['from'] = "Null"
                eventinfo['to'] = decoded_log['args']['_to']
                date = decoded_log['args']['date']
                utc_date = datetime.utcfromtimestamp(date)
                local_date = pytz.utc.localize(utc_date).astimezone(local_tz)
                eventinfo['date'] = local_date.strftime('%Y-%m-%d %H:%M:%S')
                events.append(eventinfo)
            #print(f"Token ID: {tokenId}, To: {to}, Date: {date_str}")

        # get the event filter object
        buyEvent_filter = contract.events.BuyEvent.create_filter(fromBlock=0)

        # get the logs for the event
        buylogs = EventHost.w3.eth.get_filter_logs(buyEvent_filter.filter_id)

        # loop through the logs and print the data
        for log in buylogs:
            decoded_log = contract.events.BuyEvent().process_log(log)
            #print(decoded_log)
            tokenId = decoded_log['args']['tokenId']
            if(tokenId == id):
                eventinfo = {}
                eventinfo['event'] = "Buy"
                eventinfo['price'] = str(EventHost.w3.from_wei(decoded_log['args']['price'], 'ether')) + " ETH" 
                eventinfo['from'] = decoded_log['args']['_from']
                eventinfo['to'] = decoded_log['args']['_to']
                date = decoded_log['args']['date']
                utc_date = datetime.utcfromtimestamp(date)
                local_date = pytz.utc.localize(utc_date).astimezone(local_tz)
                eventinfo['date'] = local_date.strftime('%Y-%m-%d %H:%M:%S')
                events.append(eventinfo)

        # get the event filter object
        useEvent_filter = contract.events.UseEvent.create_filter(fromBlock=0)

        # get the logs for the event
        uselogs = EventHost.w3.eth.get_filter_logs(useEvent_filter.filter_id)

        # loop through the logs and print the data
        for log in uselogs:
            decoded_log = contract.events.UseEvent().process_log(log)
            #print(decoded_log)
            tokenId = decoded_log['args']['tokenId']
            if(tokenId == id):
                eventinfo = {}
                eventinfo['event'] = "Use"
                eventinfo['price'] = ""
                eventinfo['from'] = decoded_log['args']['_from']
                eventinfo['to'] = decoded_log['args']['_to']
                date = decoded_log['args']['date']
                utc_date = datetime.utcfromtimestamp(date)
                local_date = pytz.utc.localize(utc_date).astimezone(local_tz)
                eventinfo['date'] = local_date.strftime('%Y-%m-%d %H:%M:%S')
                events.append(eventinfo)
        sorted_list = sorted(events, key=itemgetter('date'), reverse = True)             
        context = {
            'ticketId':id,
            'ticketStartDate':ticketStartDate,
            'ticketEndDate':ticketEndDate,
            'ticketPrice':ticketPrice,
            'ticketClass':ticketClass,
            'ticketSeat':ticketSeat,
            'ticketSale':ticketSale,
            'ticketLocation':ticketLocation,
            'ticketOwner':ticketOwner,
            'events':sorted_list,
        }
        return context  
     
class requests(TemplateView):
    template_name = 'eventhost/requests.html'


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
    GATE = "0x400fF5fC597483922a5Cb6Aa180241bE97595aF8"   # Account[9] address GATE
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
