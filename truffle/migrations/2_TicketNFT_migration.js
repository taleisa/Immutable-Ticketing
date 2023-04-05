// 2_TicketNFT_migration.js

const Migrations = artifacts.require("TicketNFT");

module.exports = function (deployer) {
  deployer.deploy(Migrations, "Event 3", "E3", "Boulevard", "Stand-up comedy",1676332800,1676678400);
};