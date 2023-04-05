// SPDX-License-Identifier: MIT
pragma solidity ^0.8.9;

import "./node_modules/@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "./node_modules/@openzeppelin/contracts/token/ERC721/extensions/ERC721Burnable.sol";
import "./node_modules/@openzeppelin/contracts/access/Ownable.sol";
import "./node_modules/@openzeppelin/contracts/access/AccessControl.sol";
import "./node_modules/@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "./node_modules/@openzeppelin/contracts/utils/Counters.sol";
import "./node_modules/@openzeppelin/contracts/utils/Strings.sol";

contract TicketNFT is ERC721, ERC721Burnable, ERC721URIStorage, Ownable, AccessControl {
    using Counters for Counters.Counter;
    mapping (uint256 => address) public ticketIndexToOwner;//Ticket index to owner
    // Can change minter to array. This will enable multiple accounts to mint
    bytes32 public constant MINTER_ROLE = keccak256("MINTER_ROLE");//Account who can mint
    bytes32 public constant VERIFIED_ACCOUNTS = keccak256("VERIFIED_ACCOUNTS");//Accounts that are verified(in our database)
    bytes32 public constant GEA_ACCOUNTS = keccak256("GEA_ACCOUNTS");//Accounts belonging to GEA
    Ticket[] public _allTickets;//Array that contains all tickets index is ticket ID
    //Common for all tickets
    string public _eventName;
    string public _eventLocation;
    string public _eventType;
    uint256 public _startDate;
    uint256 public _endDate;
    Counters.Counter public _tokenIdCounter;
    struct Ticket{// Specific to individual ticket
    uint256 _price;// Different categories may have different prices
    bool _forSale;// If true indicates that any verified account can buy the ticket
    uint256 _seatNumber;// Each ticket has a different seat number
    } 
    constructor(string memory name, string memory symbol,string memory eventLocation,string memory eventType,
     uint256 startDate, uint256 endDate) ERC721(name, symbol){
        _setupRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _eventLocation = eventLocation;
        _eventType = eventType;
        _startDate = startDate;
        _endDate = endDate;
    } 


    function safeMint(address to, string memory uri, uint256 price, uint256 seatNumber) public onlyRole(MINTER_ROLE) {
        require(hasRole(GEA_ACCOUNTS, to), "Cannot mint to account not owned by GEA");
        uint256 tokenId = _tokenIdCounter.current();
        _allTickets.push(Ticket(price,true,seatNumber));// Add new ticket to array of tickets(true because it is originally with GEA who want to sell immidiatly)
        _tokenIdCounter.increment();//Increment counter
        _safeMint(to, tokenId);// Mint ticket
        ticketIndexToOwner[tokenId] = to;
        _setTokenURI(tokenId, uri);// URI will hold metadata such as image
    }
    //Function to buy ticket
    function buy(
        uint256 tokenId,
        bytes memory data)public payable onlyRole(VERIFIED_ACCOUNTS){
            require(_allTickets[tokenId]._forSale == true,"Ticket not for sale");
            require(msg.value == _allTickets[tokenId]._price, "Incorrect price");
            super._safeTransfer(ownerOf(tokenId),msg.sender,tokenId, data);
            ticketIndexToOwner[tokenId] = msg.sender;//Ticket is now owned by sender
            _allTickets[tokenId]._forSale = false;//Ticket no longer for sale once transfered to new owner
        }
    //Function to either enable or disable sale of ticket
    function sale(bool option,uint256 tokenId) public {
        require(ticketIndexToOwner[tokenId]==msg.sender,"No ticket owner");
        _allTickets[tokenId]._forSale = option;
    }

    function safeTransferFrom(
        address from,
        address to,
        uint256 tokenId,
        bytes memory data
    ) public virtual override {
        require(false,"Cannot transfer, can only sell");
    }
    // Overrides reequired by solidity
     function _burn(uint256 tokenId) internal override(ERC721, ERC721URIStorage) {
        super._burn(tokenId);
    }

    function tokenURI(uint256 tokenId)
        public
        view
        override(ERC721, ERC721URIStorage)
        returns (string memory)
    {
        return super.tokenURI(tokenId);
    }
    function supportsInterface(bytes4 interfaceId)
        public
        view
        override(ERC721, AccessControl)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }
}