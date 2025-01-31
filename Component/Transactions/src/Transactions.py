from Component.Component import Component

class Transactions(Component):
    def __init__(self):
        super().__init__()
        self.url = f"{self.getEnv("API_URL")}{self.getEnv("API_TRANS_URL")}"
        # self.getClient()
    
    def getTransactions(self,account_id):
        # try:
        #     response = self.Client.list_transactions(account_id,100,0)
        #     print(response['transactions'])
        # except Exception as e:
        #     print("An error occurred:")
        #     print(e)
        #     return False
        url = self.getAccountUrl(account_id)

        response = self.sendRequest(url)

        if response.status_code == 200:
            return response.json()#.get("transactions", [])
        else:
            print(f"Error fetching transactions for account ID {account_id}: {response.status_code}, {response.text}")
            return False
    
    def getAccountUrl(self,account_id):
        return self.url.replace("{account_id}", account_id)
    
    def sendRequest(self,url=None):
        if url == None: return False
        
        requests = self.requests
        auth = self.HTTPBasicAuth(self.getEnv("API_KEY"), self.getEnv("API_SECRET"))
        params = {
            "min_row": 1, 
            "max_row": 100
        }

        return requests.get(url, auth=auth, params=params)

            