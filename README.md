# cointracker

## Setup

    source ./setup.sh

## Run application

Run the following command in one terminal after running setup script at least once

    flask --app coin_tracker.py --debug run
    
## Usage
API examples below.  Make sure application is running.

### Get members
    Example: curl localhost:5000/get_members

input: None
output: list of members 

### Add member
    Example: curl localhost:5000/add_member --header "Content-Type: application/json" --request POST --data '{"member":"Russell"}'
    
input: {"member": member name}
output: operation status

### Add coin
    Example: curl localhost:5000/add_coin --header "Content-Type: application/json" --request POST --data '{"member":"Russell", "coin":{"blockchain":"bitcoin","address":"3E8ociqZa9mZUSwGdSmAEMAoAxBK3FNDcd"}}'

    Example: curl localhost:5000/add_coin --header "Content-Type: application/json" --request POST --data '{"member":"Russell", "coin":{"blockchain":"bitcoin","address":"bc1q0sg9rdst255gtldsmcf8rk0764avqy2h2ksqs5"}}'

input: {"member": member name, "coin": {"blockchain": chain name, "address": coin address}}
output: operation status

### Update coin
    Example update: curl localhost:5000/update_coin --header "Content-Type: application/json" --request POST --data '{"member":"Russell", "coin":{"blockchain":"bitcoin","old_address":"3E8ociqZa9mZUSwGdSmAEMAoAxBK3FNDcd","new_address":"3E8ociqZa9mZUSwGdSmAEMAoAxBK3FNDcd3"}}'

input: {"member": member name, "coin": {"blockchain": chain name, "old address": original coin address, "new address": new address with which to update}}
output: operation status

### Delete coin
    curl localhost:5000/update_coin --header "Content-Type: application/json" --request DELETE --data '{"member":"Russell", "coin":{"blockchain":"bitcoin","address":"3E8ociqZa9mZUSwGdSmAEMAoAxBK3FNDcd"}}'

input: {"member": member name, "coin": {"blockchain": chain name, "address": coin address}}
output: operation status

### Get wallet
    Example: curl localhost:5000/get_wallet --header "Content-Type: application/json" --request GET --data '{"member":"Russell"}'

input: {"member": member name}
output: list of coins in member wallet

### Sync coin transactions
    Example: curl localhost:5000/sync_coin_transactions --header "Content-Type: application/json" --request POST --data '{"member":"Russell","coin":{"address":"bc1q0sg9rdst255gtldsmcf8rk0764avqy2h2ksqs5"}}'

input: {"member": member name, "coin": { "address": coin address}} 
output: operation status

### Get coin transactions
    Example: curl localhost:5000/get_coin_transactions --header "Content-Type: application/json" --request POST --data '{"member":"Russell","coin":{"address":"bc1q0sg9rdst255gtldsmcf8rk0764avqy2h2ksqs5"}}'

input: {"member": member name, "coin": { "address": coin address}} 
output: list of transactions

### Get coin balance
    Example: curl localhost:5000/get_coin_balance --header "Content-Type: application/json" --request POST --data '{"member":"Russell","coin":{"address":"bc1q0sg9rdst255gtldsmcf8rk0764avqy2h2ksqs5"}}'

input: {"member": member name, "coin": { "address": coin address}} 
output: balance in BTC