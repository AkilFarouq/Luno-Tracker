from Component.Component import Component

class Balances(Component):

    account_id = None
    asset = None
    balance = 0
    reserved = 0
    unconfirmed = 0
    url = None
    dir = None
    data = None

    def __init__(self, balance=None):
        super().__init__()
        if(balance != None):
            self.account_id = balance.get("account_id")
            self.asset = balance.get("asset")
            self.balance = balance.get("balance")
            self.reserved = balance.get("reserved")
            self.unconfirmed = balance.get("unconfirmed")
        self.createBalObj()
    
    def balanceExist(self):
        if(
            float(self.balance) == 0 and
            float(self.reserved) == 0 and
            float(self.unconfirmed) == 0
           ): return False
        return True
    
    def printData(self):
        print(f"Account ID: {self.account_id}")
        print(f"Asset: {self.asset}")
        print(f"Available: {self.balance}")
        print(f"Reserved: {self.reserved}")
        print(f"Unconfirmed: {self.unconfirmed}")
        print("-" * 20)
    
    def buildBalanceData(self,rebuilData='N'):
        if self.data is None or rebuilData == 'Y':
            self.data =  {
                "Account":self.account_id,
                "Asset":self.asset,
                "Available":self.balance,
                "Reserved":self.reserved,
                "Unconfirmed":self.unconfirmed,
            }
        return self.data

    def createBalObj(self,overwrite='Y'):
        if(not self.balanceExist()): 
            return False
        else:
            filename=f"{self.asset}_{self.account_id}"
            self.dir=f"{self.getDataPath()}{filename}"
            filepath =f"{self.dir}/{filename}.json"

            self.createPath(self.dir)
            self.createJsonFile(filepath,self.buildBalanceData(),overwrite)
    
    def createJsonTransactions(self,transactions,overwrite='N'):
        transactions = transactions.get("transactions", [])
        for transaction in transactions:
            filepath = f"{self.dir}/{transaction.get("row_index")}.json"

            self.createJsonFile(filepath,transaction,overwrite)