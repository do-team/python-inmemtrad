# /usr/bin/python
'''
 Purpose : Simple program to generate random product and it's price
 Format  : <prod1>-<price>-hash: customer
'''

import argparse
import random
import redis

POOL = redis.ConnectionPool(host='mycentos7', port=6379, db=0)

# List of few customer id's for free, rest will be added for small fee.. You know the drill, right
customers = ["AUX1", "BFG2", "CRE3", "DRS4", "EFI5", "FRA6", "GOR1", "AAR1"]
products = ["wood", "gold", "fish", "wine"]

# Look into DB for selling bid
def get_variable(variable_name):
    r = redis.Redis(connection_pool=POOL)

    response = r.lrange(variable_name,0,-1)
    if response is not None:
        r.lpop(variable_name)
        print "Listing " + str(variable_name) + " : " + str(response)
    else:
        print "Response: " + str(response)
    return response


def set_variable(variable_name, variable_value, variable_expire):
    r = redis.Redis(connection_pool=POOL)
    print "Variable name: " + variable_name +  " val: " + variable_value
    try:
        r.lpush(variable_name, variable_value)
    except redis.exceptions.ResponseError as exc:
        print "Failed with " + str(exc)
#    else:
#        r.set(variable_name, variable_value, variable_expire)


# Let's have some engine generating orders,
# P.S. After 10 hours, i can say that manually it's fuking boring :)
def generate_orders(cycles=1, expire=1):
    for cycle in range(cycles):
        item, customer = randomize_values()
        print "Company " + str(customer) + " offers : " + str(item[0:4]) + " for " + str(item[5:10]) + " ( " + item + " )"
        set_variable(item, customer, expire)
    return


# Throw me some random items offered by customers
def randomize_values():
    item = str(random.choice(products)) + "-" + str(random.randint(1,3))
    customer = str(random.choice(customers))
    return item, customer


# Let say we have a deal
def make_a_deal():
    return


# Simplest test case
def test_case_buy():
    item_test = (randomize_values())    # Generate random cust with demand
    buy_id = item_test[1]               # Customer name
    item_id = item_test[0]              # Customer item

    print "BUYER ID: " + buy_id + "   Looking for item : " + str(item_id) + "\n"
    find_item = get_variable(item_id)   # Determine if item already exist

    # When exist, we can arrange a deal
    if find_item:
        print "There's offer for >>> " + str(item_id) + " from : " + str(find_item)
        print "Buying !!  Company " + str(buy_id) + " buying " + str(item_id) + " from : " + str(find_item[0])
    # Otherwise just wipe an eye
    else:
        print "Nothing found, sorry. No deal today."

    print "----------------------------------------- *** ---------------------------------------------------- "

if __name__ == '__main__':
    # Let's describe purpose of utility & add some mandatory & optional arguments
    ap = argparse.ArgumentParser(description='Utility generating buy/sell orders based on parameter. Default=Sell orders',
                                 prog='InMemoryAlgoTrader')

    ap.add_argument("-r", "--role", action="store",default="sell",
                    help="Are you buying or selling? Let's state 'BUY/SELL' and your dream and it will come true immediatelly!")

    ap.add_argument("-c", "--cycles", action="store", default=1000, help="How long should I run? Just state number of cycles")
    ap.add_argument("-v", "--version", action="version", version="%(prog)s 1.0", help="Display script version, nothing really new.")
    ap.add_argument("-l", "--verbosity_level", action="store_true", help="Enables output verbosity")

    args = ap.parse_args()
    my_role = args.role
    cycles = args.cycles
    print "My role is now : " + my_role

    verbose = args.verbosity_level

    if my_role == "buy":
        print('===============================================================')
        print('Generating orders for Redis')
        print('===============================================================')
        generate_orders(cycles)

    if my_role == "sell":
        print('===============================================================')
        print('Time for tests')
        print('===============================================================')

        for i in range(200):
            test_case_buy()


