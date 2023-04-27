import json
from datetime import datetime
from operator import itemgetter
import pytz
from web3 import Web3

from django.shortcuts import redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from eventhost.forms import loginForm, signupForm, eventrequestForm, TicketForm, requestManagementForm
from access.models import Event, web3User, SignUpRequest, EventRequest
from immutableTicketing.settings import TRUFFLE_PATH, WEB3_ADDRESS, LOGIN_REDIRECT_URL



class loginView(FormView):
    template_name = 'eventhost/index.html'
    success_url = reverse_lazy('dashboard')
    #next_page = reverse_lazy('dashboard')
    #authentication_form = loginForm
    form_class = loginForm
    
    
    def form_valid(self, form):
            print("form valid")
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
            # A backend authenticated the credentials
                try:
                    web3user = web3User.objects.get(user = user)
                except:
                    messages.error(self.request, 'Access Denied')
                    self.success_url = reverse_lazy('eventhostlogin')
                    return super(loginView, self).form_valid(form)    
                else:    
                    if web3user.is_event_host == True or web3user.is_GEA == True:
                        login(self.request, user)
                        print('After login')
                        #redirect_to = login_redirect(self.request.GET.get(REDIRECT_FIELD_NAME), user)
                        #return HttpResponseRedirect(redirect_to)
                        return super(loginView, self).form_valid(form)
                    else: #add another else for GEA to access GEA page
                        messages.error(self.request, 'Access Denied')
                        self.success_url = reverse_lazy('eventhostlogin')
                        return super(loginView, self).form_valid(form)
            else:
            # No backend authenticated the credentials
                messages.error(self.request, 'Incorrect Credentials')
                self.success_url = reverse_lazy('eventhostlogin')
                return super(loginView, self).form_valid(form)
            

class signUp(FormView):
    template_name = 'eventhost/signup.html'
    success_url = reverse_lazy('eventhostlogin')
    form_class = signupForm
    
    def form_valid(self, form):
        if (form.cleaned_data['password1'] == form.cleaned_data['password2']):# errors for form: password does not match
            userCondition = True
            for user in User.objects.all():
                if user.username == form.cleaned_data['companyName']:
                    userCondition = False #check is username already exists
            if(userCondition):         
                sign = SignUpRequest(companyName=form.cleaned_data['companyName'],
                                    companyEmail=form.cleaned_data['companyEmail'],
                                    password1=form.cleaned_data['password1'],
                                    password2=form.cleaned_data['password2'],
                                    wallet_address=form.cleaned_data['walletAddress'],)
                try: # errors for saving: company name, email, or wallet already exists 
                    sign.save()
                except:
                    messages.error(self.request, 'Company has already requested account')
                    self.success_url = reverse_lazy('eventhostsignup')
                    return super(signUp, self).form_valid(form)
                else:
                    messages.success(self.request, 'Company has succefully requested account')
                    self.success_url = reverse_lazy('eventhostlogin')
                    return super(signUp, self).form_valid(form)
            else:
                messages.error(self.request, 'User already exists')
                self.success_url = reverse_lazy('eventhostsignup')
                return super(signUp, self).form_valid(form)     
        else:
            messages.error(self.request, 'Password does not match')
            self.success_url = reverse_lazy('eventhostsignup')
            return super(signUp, self).form_valid(form)             
    
class dashboard(LoginRequiredMixin, TemplateView):
    template_name = 'eventhost/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        #retrieve a list of events under the same event host address
        web3user = web3User.objects.get(user = user)
        if(web3user.is_event_host == True):
            condition = True #display request page
            eventlist = []
            eventinfo = {} 
            #if eventhost does not have events
            eventinfo['event'] = '-'
            eventinfo['contract'] = None
            eventlist.append(eventinfo)
            if(len(web3user.event_set.all()) != 0):
                for event in web3user.event_set.all():
                    eventinfo = {}
                    contract = EventHost.w3.eth.contract(address= event.address, abi= EventHost.ABI, bytecode = EventHost.Bytecode)
                    eventinfo['event'] = contract.functions.name().call()
                    eventinfo['contract'] = event.address
                    eventlist.append(eventinfo)
        else:
            condition = False
            eventlist = []
            eventinfo = {} 
            #if there are no events registered
            eventinfo['event'] = '-'
            eventinfo['contract'] = None
            eventlist.append(eventinfo)
            if(len(Event.objects.all()) != 0):
                for event in Event.objects.all():
                    eventinfo = {}
                    contract = EventHost.w3.eth.contract(address= event.address, abi= EventHost.ABI, bytecode = EventHost.Bytecode)
                    eventinfo['event'] = contract.functions.name().call()
                    eventinfo['contract'] = event.address
                    eventlist.append(eventinfo)                                
        context = {
            'eventlist':eventlist,
            'condition': condition,
        }
        return context  
    
    def post(self, request, *args, **kwargs):
        selected_contract = request.POST.get('contract')
        if(selected_contract != "None"):
            contract = EventHost.w3.eth.contract(address= selected_contract, abi= EventHost.ABI, bytecode = EventHost.Bytecode)
            ticketsListed = contract.functions._tokenIdCounter().call()
            geaTickets = 0 #tickets under GEA that did not change ownership
            tickets_relisted = 0 #tickets under GEA that changed ownership
            gateTickets = 0
            tickets = []
            for user in web3User.objects.all():
                if(user.is_GEA == True):
                    geaUser = user
            for x in range(ticketsListed): # loops through the tickets
                if contract.functions.ticketIndexToOwner(x).call() == geaUser.wallet_address:
                    geaTickets = geaTickets + 1
                else:
                    #if ticket not under gea and has been relisted 
                    if (contract.functions._allTickets(x).call()[1] == True): # for sale == True
                        tickets_relisted = tickets_relisted + 1
                if contract.functions.ticketIndexToOwner(x).call() == geaUser.wallet_address:
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
  
class tickets(LoginRequiredMixin, TemplateView):
    template_name = 'eventhost/ticket-record.html'      

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contract_address = self.kwargs.get('contract', None)
        id = self.kwargs.get('id', None)
        # define your local time zone
        local_tz = pytz.timezone('Etc/GMT-3')
        
        # get the contract instance
        contract = EventHost.w3.eth.contract(address=contract_address, abi=EventHost.ABI)
        # retrieve ticket information
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

        # get the event filter object
        buyEvent_filter = contract.events.BuyEvent.create_filter(fromBlock=0)

        # get the logs for the event
        buylogs = EventHost.w3.eth.get_filter_logs(buyEvent_filter.filter_id)

        # loop through the logs and print the data
        for log in buylogs:
            decoded_log = contract.events.BuyEvent().process_log(log)
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
     
class requests(LoginRequiredMixin, FormView):
    template_name = 'eventhost/requests.html'
    success_url = reverse_lazy('requests')
    form_class = eventrequestForm
    
    def form_valid(self, form):
        requestEventNameCondition = True
        for event in Event.objects.all():
            contract = EventHost.w3.eth.contract(address= event.address, abi= EventHost.ABI, bytecode = EventHost.Bytecode)
            if(contract.functions.name().call() == form.cleaned_data['eventName']):
                        requestEventNameCondition = False
        if(requestEventNameCondition):                 
            eventRequest = EventRequest(event_host= web3User.objects.get(user = self.request.user),
                                eventName=form.cleaned_data['eventName'],
                                eventSymbol=form.cleaned_data['eventSymbol'],
                                eventLocation=form.cleaned_data['eventLocation'],
                                eventType=form.cleaned_data['eventType'],
                                eventStartDate=form.cleaned_data['eventStartDate'],
                                eventEndDate=form.cleaned_data['eventEndDate'],)
            try: # errors for saving: already exist 
                eventRequest.save()
            except:
                messages.error(self.request, 'Event name already requested')
                self.success_url = reverse_lazy('requests')
                return super(requests, self).form_valid(form)
            else:
                messages.success(self.request, 'Company has succefully requested event')
                self.success_url = reverse_lazy('requests')
                return super(requests, self).form_valid(form)
        else:
            messages.error(self.request, 'Event already exist')
            self.success_url = reverse_lazy('requests')
            return super(requests, self).form_valid(form)    
        
class eventRequestManegement(LoginRequiredMixin, FormView):
    template_name = "eventhost/eventRequestManagement.html"
    success_url = reverse_lazy('eventRequestManegement')
    form_class = requestManagementForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = requestManagementForm()
        eventRequestList = []
        if(len(EventRequest.objects.all()) != 0):
            for event in EventRequest.objects.all():
                eventRequestInfo = {}
                eventRequestInfo['requestId'] = event.id
                eventRequestInfo['eventName'] = event.eventName
                eventRequestInfo['eventSymbol'] = event.eventSymbol
                eventRequestInfo['eventLocation'] = event.eventLocation
                eventRequestInfo['eventStartDate'] = event.eventStartDate
                eventRequestInfo['eventEndDate'] = event.eventEndDate
                eventRequestInfo['eventType'] = event.eventType
                eventRequestInfo['eventHostWallet'] = event.event_host.wallet_address
                eventRequestList.append(eventRequestInfo)                             
        context = {
            'form': form,
            'eventRequestList': eventRequestList,
        }
        return context  

    def form_valid(self, form):
        if(form.cleaned_data['status'] == 'Accept'):
            request = EventRequest.objects.get(id = form.cleaned_data['requestId'])
            #retrieve GEA address and create eventhost object with it
            for user in web3User.objects.all():
                if(user.is_GEA == True):
                    geaUser = user
            gea = EventHost(geaUser.wallet_address)
            # define your local time zone
            local_tz = pytz.timezone('Etc/GMT-3')

            # Make the datetime object timezone-naive
            naive_eventStartDate = request.eventStartDate.replace(tzinfo=None)
            naive_eventEndDate = request.eventEndDate.replace(tzinfo=None)

            # Convert the date to UTC time
            startDate_utc_time = local_tz.localize(naive_eventStartDate).astimezone(pytz.utc)
            endDate_utc_time = local_tz.localize(naive_eventEndDate).astimezone(pytz.utc)

            # Convert the UTC time to a Linux timestamp
            startDate_unix_timestamp = int(startDate_utc_time.timestamp())
            endDate_unix_timestamp = int(endDate_utc_time.timestamp())
            try:
                #deploy event
                contract = gea.deployNFT(geaUser.wallet_address, request.eventName, request.eventSymbol, 
                                         request.eventLocation, request.eventType, startDate_unix_timestamp, 
                                         endDate_unix_timestamp)
            except:
                #handle error
                messages.error(self.request, 'Error occured in deploying event')
                return super().form_valid(form)
            else:
                #handle success
                #create entry in event
                try:
                    event = Event(event_host = request.event_host, address = contract)
                except:
                    messages.error(self.request, 'Error occured in inserting event into database') 
                    return super().form_valid(form)
                else:
                    event.save()
                    name = request.eventName
                    # Create and send the email
                    subject = 'New Event Created'
                    message = str(name) + ' has been successfully created.'
                    from_email = 'ImmutableTicketing@gmail.com'
                    recipient_list = [request.event_host.user.email]
                    email = EmailMessage(subject, message, from_email, recipient_list)
                    email.send()
                    request.delete()        
                    messages.success(self.request, str(name) + ' Event Successfully Created')       
                    return super().form_valid(form)
        else:
            #delete request
            request = EventRequest.objects.get(id = form.cleaned_data['requestId'])
            name = request.eventName
            request.delete()        
            messages.success(self.request, str(name) + ' Event Successfully Deleted') 
            return super().form_valid(form)
    
class signUpRequestManegement(LoginRequiredMixin, FormView):
    template_name = "eventhost/signUpRequestManagement.html"
    success_url = reverse_lazy('signUpRequestManegement')
    form_class = requestManagementForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = requestManagementForm()
        signupRequestList = []
        if(len(SignUpRequest.objects.all()) != 0):
            for request in SignUpRequest.objects.all():
                signupRequestInfo = {}
                signupRequestInfo['requestId'] = request.id
                signupRequestInfo['companyName'] = request.companyName
                signupRequestInfo['companyEmail'] = request.companyEmail
                signupRequestInfo['wallet_address'] = request.wallet_address
                signupRequestList.append(signupRequestInfo)                                
        context = {
            'form': form,
            'signupRequestList': signupRequestList,
        }
        return context
    
    def form_valid(self, form):
        if(form.cleaned_data['status'] == 'Accept'):
            request = SignUpRequest.objects.get(id = form.cleaned_data['requestId'])
            try:
                user = User.objects.create_user(
                    username=request.companyName,
                    email=request.companyEmail,
                    password=request.password1
                )
            except:
                messages.error(self.request, 'Error occured in creating User Account')
                return super().form_valid(form)
            else:
                try:
                    web3User.objects.create(user = user, wallet_address = request.wallet_address ,is_event_host =  True, is_GEA =  False)
                except:
                    messages.error(self.request, 'Error occured in creating Web3User Account')
                    return super().form_valid(form)
                else:
                    name = request.companyName
                    # Create and send the email
                    subject = 'New Account Created'
                    message = 'Your Event Host Account has been successfully created.'
                    from_email = 'ImmutableTicketing@gmail.com'
                    recipient_list = [request.companyEmail]
                    email = EmailMessage(subject, message, from_email, recipient_list)
                    email.send()
                    request.delete()        
                    messages.success(self.request, str(name) + ' Account Successfully Created')       
                    return super().form_valid(form)
        else:
            request = SignUpRequest.objects.get(id = form.cleaned_data['requestId'])
            name = request.companyName
            request.delete()        
            messages.success(self.request, str(name) + ' Request Successfully Deleted') 
            return super().form_valid(form)               

class TicketRequest(LoginRequiredMixin, FormView):
    template_name = 'eventhost/ticketRequest.html'
    success_url = reverse_lazy('ticketrequest')
    form_class = TicketForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = TicketForm()
        user = self.request.user
        #retrieve a list of events under the same event host address
        web3user = web3User.objects.get(user = user)
        eventlist = []
        eventinfo = {} 
        #if eventhost does not have events
        eventinfo['event'] = '-'
        eventinfo['contract'] = None
        eventlist.append(eventinfo)
        if(len(web3user.event_set.all()) != 0):
            for event in web3user.event_set.all():
                eventinfo = {}
                contract = EventHost.w3.eth.contract(address= event.address, abi= EventHost.ABI, bytecode = EventHost.Bytecode)
                eventinfo['event'] = contract.functions.name().call()
                eventinfo['contract'] = event.address
                eventlist.append(eventinfo)                                
        context = {
            "form": form,
            'eventlist':eventlist,
        }
        return context
    
    def form_valid(self, form):
        #retrieve GEA address and create eventhost object with it
        for user in web3User.objects.all():
            if(user.is_GEA == True):
                geaUser = user
        gea = EventHost(geaUser.wallet_address)
        #create contract instance
        contract = EventHost.w3.eth.contract(address= form.cleaned_data['contractAddress'], abi= EventHost.ABI, bytecode = EventHost.Bytecode)
        seat_number = form.cleaned_data['seatNumberStart']
        price = EventHost.w3.to_wei(form.cleaned_data['price'], 'ether')
        #then mint the tickets based on the input from the form
        try:
            for _ in range(form.cleaned_data['quantity']):
                gea.mintTicket(contract, form.cleaned_data['uri'], price, seat_number, form.cleaned_data['name'], geaUser.wallet_address)
                seat_number = seat_number + 1
        except:
            messages.error(self.request, 'Error occured in minting Ticket')
            return super(TicketRequest, self).form_valid(form)
        else:            
            messages.success(self.request, 'Tickets Successfully Minted')
            return super(TicketRequest, self).form_valid(form)  

class LogoutView(View):
    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('eventhostlogin')                
        
class EventHost:
    # connecting the blockchain network in ganache
    w3 = Web3(Web3.HTTPProvider(WEB3_ADDRESS))
    #retrieving the generated ABI and Byte code from the 
    truffleFile = json.load(open(TRUFFLE_PATH)) # truffle generated file
    ABI = truffleFile['abi'] # ABI generated in the file
    Bytecode = truffleFile['bytecode'] # metadata generated in the file

    def __init__(self, event_host_address):
        self.event_host_address = event_host_address

    def grantMinterRole(self, geaAddress,contract):  
        # Send transaction
        send_tx = contract.functions.grantRole(Web3.solidity_keccak(["bytes32"],[str.encode("MINTER_ROLE")]) ,geaAddress).transact({"from": self.event_host_address})
        # Wait for transaction receipt
        tx_receipt = EventHost.w3.eth.wait_for_transaction_receipt(send_tx)
        return tx_receipt # Optional

    def grantGEARole(self, geaAddress,contract):
        # Send transaction
        send_tx = contract.functions.grantRole(Web3.solidity_keccak(["bytes32"],[str.encode("GEA_ACCOUNTS")]) ,geaAddress).transact({"from": self.event_host_address})

        # Wait for transaction receipt
        tx_receipt = EventHost.w3.eth.wait_for_transaction_receipt(send_tx)
        return tx_receipt # Optional    

    def grantCustomerRole(self, cust_add, contract):
        # Send transaction
        send_tx = contract.functions.grantRole(Web3.solidity_keccak(["bytes32"],[str.encode("VERIFIED_ACCOUNTS")]) ,cust_add).transact({"from": self.event_host_address})

        # Wait for transaction receipt
        tx_receipt = EventHost.w3.eth.wait_for_transaction_receipt(send_tx)
        return tx_receipt # Optional   

    def deployNFT(self, geaAddress,event_name, event_symbol, event_location, event_type, event_start_date, event_end_date): # event_host address is the address of the event host deploying the ticket
        contract = EventHost.w3.eth.contract(abi=EventHost.ABI, bytecode=EventHost.Bytecode)
        tx_hash = contract.constructor(event_name,event_symbol,event_location,event_type, event_start_date ,event_end_date).transact({"from": self.event_host_address})
        tx_receipt = EventHost.w3.eth.wait_for_transaction_receipt(tx_hash)
        temp_contract = EventHost.w3.eth.contract(tx_receipt.contractAddress, abi= EventHost.ABI, bytecode = EventHost.Bytecode)
        #grant roles for the NFT instance
        self.grantGEARole(geaAddress,temp_contract)
        self.grantMinterRole(geaAddress,temp_contract)
        ################################################################
        ################################################################
        #########Only for convenience not how it should actually be
        ################################################################
        ################################################################
        users = web3User.objects.all()
        for user in users:
            self.grantCustomerRole(user.wallet_address, temp_contract)
        return tx_receipt.contractAddress    

    def mintTicket(self, nft_contract, ticket_URI, ticket_price, ticket_seat_number, ticket_class, geaAddress):
        #create nft_contract by querying the database and retreiving the contract address
        nft_contract.functions.safeMint(geaAddress,ticket_URI,ticket_price,ticket_seat_number, ticket_class).transact({"from": geaAddress})    
