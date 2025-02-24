from celery import shared_task
import redis

from .exchange import buy_from_exchange
from .models import Order

redis_client = redis.StrictRedis(host="localhost", port=6379, db=0, decode_responses=True)

@shared_task
def fulfill_order(order_id, crypto_name, amount):
    print(f"Processing order {order_id} for {amount} {crypto_name}")

    try:
        crypt_pending_orders_key = f"crypto_pending_orders:{{{crypto_name}}}"
        crypt_orders_sum_key = f"crypto_orders_sum:{{{crypto_name}}}"

        min_amount = get_min_amount(crypto_name)

        lua_script = """
            local total_amount = redis.call('INCRBY', KEYS[1], ARGV[1])
            if total_amount > tonumber(ARGV[3]) then
                local orders = redis.call('SMEMBERS', KEYS[2])
                redis.call('DEL', KEYS[2])
                redis.call('SET', KEYS[1], 0)
                return {total_amount, orders}
            else
                redis.call('SADD', KEYS[2], ARGV[2])
                return {total_amount, {}}
            end 
        """

        total_amount, orders = redis_client.eval(lua_script, 2, 
                                                crypt_orders_sum_key, 
                                                crypt_pending_orders_key, 
                                                amount, 
                                                str(order_id), 
                                                min_amount)

        if total_amount > min_amount:
            buy_from_exchange(crypto_name, total_amount)

            if orders is None:
                orders = []
            orders.append(order_id)

            for order_id in orders:
                order = Order.objects.get(id=order_id)
                order.status = 1
                order.save()
                
    except Exception as e:
        print(f"Error processing order {order_id}: {str(e)}")

min_crypto_amount = {
    "ABAN": 10
}

def get_min_amount(crypto_name):
    min_amount = min_crypto_amount.get(crypto_name)
    return min_amount