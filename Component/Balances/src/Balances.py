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
    
    def getBalances(self):
        """Return all balances for this account"""
        if(self.Client == None):
            self.getClient()
        return self.Client.get_balances()
    
    def init_balance(self, balance):
        self.account_id = balance.get("account_id")
        self.asset = balance.get("asset")
        self.balance = balance.get("balance")
        self.reserved = balance.get("reserved")
        self.unconfirmed = balance.get("unconfirmed")
        

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
    
    def loadJsonData(self):
        if self.asset == 'MYR': return
        filedir = self.dir
        transFiles = self.get_filtered_files(filedir)
        transData = {
            "id":self.account_id,
            "currency":self.asset,
            "transactions": []
        }
        for file in transFiles:
            with open(f"{self.dir}/{file}", 'r') as filedata:
                data = self.json.load(filedata)
            
            if "balance_delta"  not in data: continue
            trade = 'N'
            value = data["balance_delta"]
            bal_before = data["balance"]
            bal_after = bal_before + value
            price = 0
            if data['description'] == 'Trading fee':
                transtype = "FEE"
                trade = 'Y'
            else:
                if value > 0:
                    transtype = "BOUGHT"
                else: transtype = "SOLD"
                
                if "detail_fields" in data:
                    trade = 'Y'
            app_val = "0"
            if "Price" in data["details"]: 
                app_val = data["details"]["Price"]
                pattern = r"([\d,]+\.\d+)"
            elif "Approximate value" in data["details"]: 
                app_val = data["details"]["Approximate value"]
                pattern = r"\(([\d,]+)"
                
            match = self.re.search(pattern, app_val)
            if match:
                app_val = match.group(1)
                price = float(app_val.replace(",", ""))

            trans = {
                "id":data["row_index"],
                "type":transtype,
                "value":value,
                "price":price,
                "trade":trade,
                "balance_before":bal_before,
                "balance_after":bal_after,
                "description":""
            }
            transData["transactions"].append(trans)
        # print(transData)
        self.createJsonFile(f"{self.dir}/compile.json",transData,'Y')

    def get_filtered_files(self,directory):
        # Get the last folder name in the given path
        dir_name = self.Path(directory).name

        # Get all files in the specified directory
        files = [
            f for f in self.os.listdir(directory) 
            if self.os.path.isfile(self.os.path.join(directory, f)) and self.Path(f).stem != dir_name
        ]

        return files