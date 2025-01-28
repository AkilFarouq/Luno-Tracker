from luno_python.client import Client
from bootstrap import *
    

def main():
    client = Client(api_key_id=API_KEY, api_key_secret=API_SECRET)
    try:
        response = client.get_balances()
        
        balobjs = []
        for balance in response.get("balance", []):
            BALOBJ = COMP.loadComponent('Balances',balance)
            if(BALOBJ.balanceExist()): balobjs.append(BALOBJ.getComp())
        
        TRANSOBJ = COMP.loadComponent('Transactions')
        for balobj in balobjs:
            resp = TRANSOBJ.getTransactions(balobj.account_id)
            balobj.createJsonTransactions(resp)

    except Exception as e:
        print("An error occurred:")
        print(e)

if __name__ == '__main__':
    main()