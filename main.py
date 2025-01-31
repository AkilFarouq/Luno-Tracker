from bootstrap import *

def main():
    try:
        bal_resp = COMP.loadComponent('Balances').getBalances()
        TRANSOBJ = COMP.loadComponent('Transactions')
        
        balobjs = []
        for balance in bal_resp.get("balance", []):
            balobj = COMP.loadComponent('Balances',balance)
            if(balobj.balanceExist()): 
                balobjs.append(balobj)
                trans_resp = TRANSOBJ.getTransactions(balobj.account_id)
                balobj.createJsonTransactions(trans_resp)
                balobj.loadJsonData()

    except Exception as e:
        print(f"An error occurred:{e}")

if __name__ == '__main__':
    main()