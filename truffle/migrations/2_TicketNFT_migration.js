// 2_TicketNFT_migration.js

const Migrations = artifacts.require("TicketNFT");

module.exports = function (deployer) {
  deployer.deploy(Migrations, "Event 9", "E9", "Home", "Testing",1676332800,1676678400);
};