from django.shortcuts import render
from requests import get
from datetime import datetime



def main_page_view(request):
    context = {}
    return render(request, 'wallet/homepage.html', context)


address = "0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae"
ETHER_VALUE = 10 ** 18


def make_api_url(module, action, address, **kwargs):
    API_KEY = '1WYR1RVJPVI96EMSU3YCB43AH5MMYVU95E'
    BASE_URL = 'https://api.etherscan.io/api'

    url = BASE_URL + f"?module={module}&action={action}&address={address}&apikey={API_KEY}"

    for key, value in kwargs.items():
        url += f"&{key}={value}"
    return url


def get_account_balance(address):
    get_balance_url = make_api_url("account", "balance", address, tag="latest")
    response = get(get_balance_url)
    data = response.json()

    value = int(data["result"]) / ETHER_VALUE
    return value


def get_transactions(address):
    context = {}
    transactions_url = make_api_url("account", "txlist", address, startblock=0, endblock=99999999,
                                    page=1, offset=10, sort="asc")
    response = get(transactions_url)
    data = response.json()["result"]

    internal_tx_url = make_api_url("account", "txlistinternal", address, startblock=0, endblock=99999999,
                                   page=1, offset=10, sort="asc")
    response2 = get(internal_tx_url)
    data2 = response2.json()["result"]

    data.extend(data2)
    data.sort(key=lambda x: int(x["timeStamp"]))

    current_balance = 0
    balances = []
    times = []

    trans_num = 0
    for tx in data:
        to = tx["to"]
        from_address = tx["from"]
        value = int(tx["value"]) / ETHER_VALUE

        if "gasPrice" in tx:
            gas = int(tx["gasUsed"]) * int(tx['gasPrice']) / ETHER_VALUE
        else:
            gas = int(tx["gasUsed"]) / ETHER_VALUE

        time = datetime.fromtimestamp(int(tx["timeStamp"]))
        money_in = to.lower() == address.lower()

        if money_in:
            current_balance += value
        else:
            current_balance -= value + gas

        context[trans_num] = {
            "To": to,
            "From": from_address,
            "Current_Balance": current_balance,
            "Time": time
        }

        balances.append(current_balance)
        times.append(time)
        trans_num += 1
    return context

def transactions_page_view(request):
    context = get_transactions(address)
    for transaction_data in context.values():
        transaction_data['To'] = transaction_data.get('To')
        transaction_data['From'] = transaction_data.get('From')
        transaction_data['Current_Balance'] = transaction_data.get('Current_Balance')
        transaction_data['Time'] = transaction_data.get('Time')
    return render(request, 'wallet/transactions.html', {'context': context})





