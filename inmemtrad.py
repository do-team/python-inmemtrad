# /usr/bin/python
'''
 Purpose : Simple program to generate random product and it's price
 Format  : <prod>-<price>-<order_type>: customer_list
'''


import argparse
import random
import redis
import time

POOL = redis.ConnectionPool(host='mycentos7', port=6379, db=0)
#POOL = redis.ConnectionPool(host='35.156.118.89', port=6379, db=0)

# List of few customer id's for free, rest will be added for small bribe.. You know the drill, right
customers = ["AUX1", "BFG2", "CRE3", "DRS4", "EFI5", "FRA6", "GOR1", "AAR1"]
products = ["wood", "gold", "fish", "wine"]
orders = ["buy", "sell"]


# Look into DB for selling/buying offers
def get_variable(variable_name):
    r = redis.Redis(connection_pool=POOL)
    response = r.lrange(variable_name,0,-1)
    return response


def remove_variable(variable_name):
    r = redis.Redis(connection_pool=POOL)
    response = r.lpop(variable_name)
    return response


# Create variable in Redis database
# Key is composed from item_name + price_value + order_type, eg. gold-200-buy/sell
def set_variable(variable_name, variable_value):
    r = redis.Redis(connection_pool=POOL)
    response = r.rpush(variable_name, variable_value)
    return response


# Let's have some engine generating pseudo-random orders
def generate_orders():
    item, customer, instruct = randomize_values()
    return item, customer, instruct


# Throw me some random items offered by customers
def randomize_values():
    item = str(random.choice(products))
    price = random.randint(1,99)
    customer = str(random.choice(customers))
    instruction = str(random.choice(orders))
    item = item + "-" + str(price)
    return item, customer, instruction


# Let say we have a deal
def make_a_deal():
    return


# Simplest test case
def test_case():
    test_item, test_customer, test_instruction = generate_orders()
    print "CustomerID : " + test_customer + " wants to " + test_instruction + " " + str(test_item)

    if test_instruction == "buy":
        find_item = get_variable(test_item+"-sell")
    else:
        find_item = get_variable(test_item+"-buy")

    if find_item:
        print "TRADE DETECTED! " + str(test_customer) + " just traded " + str(test_item) + \
              ", best offer by: " + str(find_item) + ". Removing from orderbook. \n"
        remove_variable(find_item)
        print get_variable(test_item+"-"+test_instruction)                      # DEBUG info

    else:
        print "New order inserted! " + test_item + "-" + test_instruction + " " + test_customer + "\n"
        set_variable(test_item + "-" + test_instruction, test_customer)
        print get_variable(test_item+"-"+test_instruction)                      # DEBUG info
    print "----------------------------------------- *** ---------------------------------------------------- "


if __name__ == '__main__':
    # Let's describe purpose of utility & add some mandatory & optional arguments
    ap = argparse.ArgumentParser(description='Utility generating buy/sell orders based on parameter. Default=Selling orders',
                                 prog='InMemoryAlgoTrader')

    ap.add_argument("-r", "--role", action="store",default="sell", help="Welcome master. Are you buying or selling today?")
    ap.add_argument("-e", "--env", action="store", default="mycentos7", help="Where is your REDIS DB residing?")
    ap.add_argument("-c", "--cycles", type=int, action="store", default=100000, help="How long should I run? Just state number of cycles")
    ap.add_argument("-v", "--version", action="version", version="%(prog)s 1.0", help="Display script version, nothing really new.")
    ap.add_argument("-l", "--verbosity_level", action="store_true", help="Enables output verbosity")

    args = ap.parse_args()
    my_role = args.role
    cycles = args.cycles

    verbose = args.verbosity_level

    start_time = time.time()

    for cycle in range(int(cycles)):
        test_case()

    print("--- %s seconds ---" % (time.time() - start_time))