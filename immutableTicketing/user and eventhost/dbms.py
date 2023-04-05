import sqlite3

class DBMS:
    con = sqlite3.connect("user and eventhost/ImmutabelTicketing.db")
    cur = con.cursor()

    # Database methods
    @staticmethod
    def getAllevents():
        #returns all events in the database
        results = []
        for row in DBMS.cur.execute("SELECT * FROM event"):
            results.append(row)
        return results
    @staticmethod    
    def getEvents(deployer_address):
        #returns all events deployed by the specific event host address
        results = []
        for row in DBMS.cur.execute("SELECT * FROM event WHERE event_host_address ='"+deployer_address+"'"):
            results.append(row)
        return results
    @staticmethod    
    def getAllcontracts():
        #returns all contract addresses in the database
        results = []
        for row in DBMS.cur.execute("SELECT contract_address FROM event"):
            results.append(row)
        return results    
    @staticmethod    
    def getContracts(deployer_address): # check if needed
        #returns all contracts deployed by the specific event host address
        results = []
        for row in DBMS.cur.execute("SELECT contract_address FROM event WHERE event_host_address ='"+deployer_address+"'"):
            results.append(row)
        return results  
    @staticmethod     
    def getSpecificContract(event_name):
        results = []
        for row in DBMS.cur.execute("SELECT contract_address FROM event WHERE event_name ='"+event_name+"'"):
            results.append(row)
        return results[0][0] 
    @staticmethod     
    def getEventHostAddress(event_name):
        results = []
        for row in DBMS.cur.execute("SELECT event_host_address FROM event WHERE event_name ='"+event_name+"'"):
            results.append(row)
        return results[0][0]     


    @staticmethod    
    def insertValues(event_name, event_symbol, event_location, event_type, event_start_date, event_end_date, event_host_address, contractAddress):
        query = """INSERT INTO event VALUES(?,?,?,?,?,?,?,?)"""
        DBMS.cur.execute(query, [event_name,event_symbol,event_location,event_type,str(event_start_date),str(event_end_date),event_host_address,contractAddress])
        DBMS.con.commit()
  