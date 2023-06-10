import pika, json
from kiteconnect import KiteConnect

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare('user_exchange', exchange_type='direct')

channel.queue_declare(queue='request_queue')
channel.queue_declare(queue='response_queue')

channel.queue_bind(exchange='user_exchange', queue='request_queue', routing_key='request_key')
channel.queue_bind(exchange='user_exchange', queue='response_queue', routing_key='response_key')

def request_callback(ch, method, properties, body):
    message = json.loads(body)
    option = message['option']

    kite = KiteConnect(api_key="API_KEY")
    kite.set_access_token("ACCESS_TOKEN")

    if option=='profile':
        profile = kite.profile()
        response_message = {
            'option': 'profile',
            'name': profile['user_name'],
            'userid': profile['user_id']
        }
    elif option=='margin':
        margin = kite.margins()
        response_message = {
            'option': 'margin',
            'net': margin['equity']['net'],
            'cash': margin['equity']['available']['cash']
        }
    elif option=='ltp':
        ticker = message['ticker']
        response_message = {
            'option': 'ltp',
            'ltp': kite.ltp(ticker)
        }
    elif option=='ohlc':
        ticker = message['ticker']
        response_message = {
            'option': 'ohlc',
            'ohlc': kite.ohlc(ticker)
        }
    elif option=='holdings':
        holdings = kite.holdings()
        response_message = {
            'option': 'holdings',
            'holdings': holdings
        }
    else:
        response_message = {
            'message': 'Invalid option'
        }

    channel.basic_publish(exchange='user_exchange', routing_key='response_key', body=json.dumps(response_message))
    print('Response sent back to queue')

channel.basic_consume(queue='request_queue', on_message_callback=request_callback, auto_ack=True)
print('Waiting for request...')
channel.start_consuming()
