# /usr/bin/python
'''
 Purpose : Simple program to generate random product and it's price
 Format  : <prod1>-<price>-hash: customer
'''


import argparse
import os
import random
import redis

POOL = redis.ConnectionPool(host='mycentos7', port=6379, db=0)

# List of few customer id's for free, rest will be added for small fee.. You know the drill, right
customers = ["AUX1", "BFG2", "CRE3", "DRS4", "EFI5", "FRA6", "GOR1", "AAR1"]
products = ["wood", "gold", "fish", "wine"]
orders   = ["buy", "sell"]


# Look into DB for selling/buying offers
def get_variable(variable_name, variable_value):
    r = redis.Redis(connection_pool=POOL)

    # Lets see if there's key
    response = r.lrange(variable_name,0,-1)

    # If there is, remove it from left
    # otherwise add from right
    if not response:
        print "Listing " + str(variable_name) + " : " + str(response)
        r.lpop(variable_name)
    else:
        print "Response: " + str(response)
        r.rpush(variable_name, variable_value)

    print "List of customers for " + str(variable_name) + " " + str(r.lrange(variable_name,0,-1))
    return response


# Create variable in Redis database
# Key is composed from item_name + price_value + order_type, eg. gold-200-buy/sell
def set_variable(variable_name, variable_value, variable_type):
    r = redis.Redis(connection_pool=POOL)
    variable_name = variable_name + "-" + variable_type
    response = r.lrange(variable_name,0,-1)

    if not response:
        r.lpush(variable_name, variable_value)
        print r.lrange(variable_name,0,-1)
    else:
        get_variable(variable_name,variable_value)
    #except redis.exceptions.ResponseError as exc:
    #    print "Failed with " + str(exc)


# Let's have some engine generating pseudo-random orders
def generate_orders(cycles=1):
    for cycle in range(int(cycles)):
        item, customer, instruct = randomize_values()
        print "Company " + str(customer) + " offers : " + str(item[0:4]) + " for $" + str(item[5:9]) + " ( " + item + " )"
        set_variable(item, customer, instruct)
    return


# Throw me some random items offered by customers
def randomize_values():
    item = str(random.choice(products)) + "-" + random.randint(10,30).__format__('{:04d}'.format(4))
    customer = str(random.choice(customers))
    instruction = str(random.choice(orders))
    return item, customer, instruction


# Let say we have a deal
def make_a_deal():
    return


# Simplest test case
def test_case_buy():
    item_test = (randomize_values())    # Generate random cust with demand
    buy_id = item_test[1]               # Customer name
    item_id = item_test[0]              # Customer item

    print "BUYER ID: " + buy_id + "   Looking for item : " + str(item_id) + "\n"

    # Determine if item already exist
    find_item = get_variable(item_id, buy_id)

    # When exist, we can arrange a deal
    if find_item:
        # print "There's offer for >>> " + str(item_id) + " from : " + str(find_item)
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

    ap.add_argument("-c", "--cycles", type=int, action="store", default=100, help="How long should I run? Just state number of cycles")
    ap.add_argument("-v", "--version", action="version", version="%(prog)s 1.0", help="Display script version, nothing really new.")
    ap.add_argument("-l", "--verbosity_level", action="store_true", help="Enables output verbosity")

    args = ap.parse_args()
    my_role = args.role
    cycles = args.cycles
    print "My role is now : " + my_role

#    print "Reading environment variable " + os.environ("IMTCONNECT")


    verbose = args.verbosity_level

    if my_role == "sell":
        print('===============================================================')
        print('Generating orders for Redis')
        print('===============================================================')
        generate_orders(cycles)

    if my_role == "buy":
        print('===============================================================')
        print('Time for tests')
        print('===============================================================')

        for i in range(cycles):
            test_case_buy()
