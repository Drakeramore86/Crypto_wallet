from django.shortcuts import render
from requests import get
from datetime import datetime
from .forms import AddressForm
from users.models import Profile, FavoriteAddress
from django.contrib import messages

ETHER_VALUE = 10 ** 18

def make_api_url(module, action, address, **kwargs):
    API_KEY = '1WYR1RVJPVI96EMSU3YCB43AH5MMYVU95E'
    BASE_URL = 'https://api.etherscan.io/api'
    url = BASE_URL + f"?module={module}&action={action}&address={address}&apikey={API_KEY}"
    for key, value in kwargs.items():
        url += f"&{key}={value}"
    return url

def get_transactions(address):
    transactions_url = make_api_url("account", "txlist", address, startblock=0, endblock=99999999, page=1, offset=10, sort="asc")
    response = get(transactions_url)
    data = response.json()["result"]
    internal_tx_url = make_api_url("account", "txlistinternal", address, startblock=0, endblock=99999999, page=1, offset=10, sort="asc")
    response2 = get(internal_tx_url)
    data2 = response2.json()["result"]
    data.extend(data2)
    data.sort(key=lambda x: int(x["timeStamp"]))
    current_balance = 0
    context = {}
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
        trans_num += 1
    return context

def search_address(request):
    form = AddressForm()
    context = {'form': form}
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.cleaned_data['address']
            transactions = get_transactions(address)
            context['address'] = address
            context['transactions'] = transactions
            if request.user.is_authenticated and 'save_address' in request.POST:
                profile = Profile.objects.get(user=request.user)
                # Check if the user already has 10 addresses
                if profile.favorite_addresses.count() < 10:
                    favorite_address, created = FavoriteAddress.objects.get_or_create(profile=profile, address=address)
                    if created:
                        messages.success(request, 'Address saved to your profile.')
                    else:
                        messages.info(request, 'Address already in your favorites.')
                else:
                    messages.error(request, 'You can only save up to 10 favorite addresses.')
    return render(request, 'wallet/search_address.html', context)

def main_page_view(request):
    context = {}
    return render(request, 'wallet/homepage.html', context)
