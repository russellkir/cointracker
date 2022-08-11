# cointracker

## Setup

    source ./setup.sh

## Usage
API examples below

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