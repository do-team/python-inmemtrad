# /usr/bin/python
'''
 Purpose : Simple program to generate random product and it's price
 Format  : <prod1>-<price>-hash: customer
'''

import random
import redis
import time

POOL = redis.ConnectionPool(host='mycentos7', port=6379, db=0)

customers = ["AUX1", "BFG2", "CRE3", "DRS4", "EFI5", "FRA6", "GOR1", "AAR1"]
products = ["wood", "gold", "fish", "wine"]
variable_cycles = 100


def get_variable(variable_name):
    r = redis.Redis(connection_pool=POOL)
    response = r.get(variable_name)
    return response


def set_variable(variable_name, variable_value, variable_expire):
    r = redis.Redis(connection_pool=POOL)
    r.set(variable_name, variable_value, variable_expire)


def generate_orders(cycles=1, expire=1):
    for cycle in range(cycles):
        item, customer = randomize_values()
        print "Company " + str(customer) + " offers : " + str(item[0:4]) + " for " + str(item[5:10]) + " ( " + item + " )"
        set_variable(item, customer, expire)
    return


def randomize_values():
    item = str(random.choice(products)) + "-" + str(random.randint(1,1000))
    customer = str(random.choice(customers))
    return item, customer


def test_case_buy():
    item_test = (randomize_values())
    find_item = get_variable(item_test[0])
    my_uid = item_test[1]
    print "BUYER ID: " + my_uid + "   Looking for item : " + str(item_test[0])

    if find_item:
        print "There's offer for >>> " + str(item_test[0]) + " from : " +str(find_item)
    else:
        print "Nothing found, sorry"

if __name__ == '__main__':
    print('===============================================================')
    print('Generating orders for Redis')
    print('===============================================================')
    generate_orders(variable_cycles, expire=2)

    print('===============================================================')
    print('Time for tests')
    print('===============================================================')
    time.sleep(2)
    test_case_buy()


