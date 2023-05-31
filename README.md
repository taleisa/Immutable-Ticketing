# Immutable-Ticketing

The immutable ticketing system is our capstone project at Alfaisal university.

The goal of the system is to eliminate the black market of tickets.This goal can be acheived using blockchain technology. Tickets are NFT's meaning they can neither be forged nor sold to more than one person.
This system is built using the etheruem public blockchain


How to install and run the project:

 - Use pip or pipenv to install django , web3 and any other neccessary packages.
 - install ganache
 - open ganache ,create a new workspace , and add a new truffle project(choose the truffleconfig.js file found at immutableTicketing/immutableTicketing/truffle)
 - install metamask as a browser extension
 - after launching ganache a list of accounts will be displayed
 - click the key icon and copy the private key
 - click on metamask extension and add the ganache blockchain you just launched as a network
 - add accounts in the metamask extension by using private keys from the ganache blockchain
 - Find the manage.py file
 - run python manage.py makemigrations
 - run python manage.py migrate
 - run manage.py createsuperuser(This will be the GEA account)
 - run python manage.py runserver
