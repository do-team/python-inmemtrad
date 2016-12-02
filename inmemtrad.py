# /usr/bin/python
'''
 Purpose : Generate random product and it's price
'''

import random
import redis

POOL = redis.ConnectionPool(host='mycentos7', port=6379, db=0)

customers = ["AUX1", "BFG2", "EFI3", "DRS4", "FRA5"]
products = ["wood", "gold", "stone", "food"]
variable_cycles = 500


def get_variable(variable_name):
    r = redis.Redis(connection_pool=POOL)
    response = r.get(variable_name)
    return response


def set_variable(variable_name, variable_value):
    r = redis.Redis(connection_pool=POOL)
    r.mset(variable_name, variable_value, 2, 1)


def generateOrders(cycles):
    for i in range(cycles):
        product = str(random.choice(customers)) + " " + str(random.choice(products))
        value   = str(random.randint(1,100))

        print "Generating random price for : " + str(i) + " " + product + " " + value
        set_variable(product, value)

if __name__ == '__main__':
    print('===============================================================')
    print('Generating orders for Redis')
    print('===============================================================')
    generateOrders(variable_cycles)
    print "Getting latest price for WOOD: " + str(get_variable('FRA5 wood'))