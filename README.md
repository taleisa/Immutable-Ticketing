# Immutable-Ticketing

The immutable ticketing system is our capstone project at Alfaisal university.

The goal of the system is to eliminate the black market of tickets.This goal can be acheived using blockchain technology. Tickets are NFT's meaning they can neither be forged nor sold to more than one person.
This system is built using the etheruem public blockchain


How to install and run the project:

 - Use pip or pipenv to install the following packages:
 aiohttp==3.8.4
aiosignal==1.3.1
asgiref==3.7.1
asn1crypto==1.5.1
async-timeout==4.0.2
attrs==23.1.0
base58==2.1.1
bitarray==2.7.3
black==23.3.0
cached-property==1.5.2
certifi==2022.12.7
cffi==1.15.1
charset-normalizer==3.1.0
click==8.1.3
coincurve==18.0.0
colorama==0.4.6
cssbeautifier==1.14.7
cytoolz==0.12.1
Django==4.2.1
django-web3-auth==0.1.6
djlint==1.25.0
EditorConfig==0.12.3
et-xmlfile==1.1.0
eth-abi==4.0.0
eth-account==0.8.0
eth-hash==0.5.1
eth-keyfile==0.6.1
eth-keys==0.4.0
eth-rlp==0.3.0
eth-typing==3.3.0
eth-utils==2.1.0
ethereum==2.3.2
frozenlist==1.3.3
future==0.18.3
hexbytes==0.3.0
html-tag-names==0.1.2
html-void-elements==0.1.0
idna==3.4
ipfshttpclient==0.8.0a2
jsbeautifier==1.14.7
jsonschema==4.17.3
lru-dict==1.1.8
multiaddr==0.0.9
multidict==6.0.4
mypy-extensions==1.0.0
regex==2023.3.23
repoze.lru==0.7
requests==2.29.0
rlp==3.0.0
six==1.16.0
sqlparse==0.4.4
tomli==2.0.1
toolz==0.12.0
tqdm==4.65.0
typing_extensions==4.6.2
tzdata==2023.3
urllib3==1.26.15
varint==1.0.2
web3==6.2.0
websockets==11.0.2
yarl==1.9.2
 - install ganache v2.7
 - open ganache ,create a new workspace , and add a new truffle project(choose the truffleconfig.js file found at immutableTicketing/immutableTicketing/truffle)
 - install metamask as a browser extension
 - after launching ganache a list of accounts will be displayed(Refer to the following link for the  next 3 steps: https://www.geeksforgeeks.org/how-to-set-up-ganche-with-metamask/ excluding Steps to Deploy the Smart Contract and all that comes after )
 - click the key icon and copy the private key
 - click on metamask extension and add the ganache blockchain you just launched as a network new RPC URL: HTTP://127.0.0.1:7545, with the chain id as 1337. If the address and port number are different on ganache change them to the previous example
 - add minimum two accounts in the metamask extension by using private keys from the ganache blockchain(One for the user and one for the eventhost)
 - Find the manage.py file
 - run python manage.py makemigrations
 - run python manage.py migrate
 - run manage.py createsuperuser(This will be the GEA account)
 - run python manage.py runserver
 - In the terminal you will find the address of the website
 - Visit the website and you will be directed to the main page
 - Click on "Not a customer? Eventhost portal" and request an account
 - Then login in as the super user to accept the account request and logout
 - Login with the newly accepted account(Eventhost) to request an event and log back in as the GEA(superuser) to accept the event proposal
 - Log in again with the event host account to mint the tickets(At this stage the tickets are on the market)
 - In the url visit /admin, which will direct you to the admin page(Example: 127.0.0.1:8000/admin/)
 - Login with the super user you created and add a new user then logout
 - Navigate back to the main login page(The normal URL example: 127.0.0.1:8000) and click on login with nafath and enter the credentials of the new user you just added in the admin page
 - click on connect with metamask(if it does not popup click the extension) and choose the account you imported for the customer(Not the one used to signup the eventhost) and click login. This will tie the metamask account to this user
 - Click on connect to metamask again and login
