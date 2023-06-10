import pika, json
import pandas as pd

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='user_exchange', exchange_type='direct')

channel.queue_declare(queue='request_queue')
channel.queue_declare(queue='response_queue')

channel.queue_bind(exchange='user_exchange', queue='request_queue', routing_key='request_key')
channel.queue_bind(exchange='user_exchange', queue='response_queue', routing_key='response_key')

def response_callback(ch, method, properties, body):
    response = json.loads(body)
    option = response['option']
    if option=='holdings':
        print('Data frame : ')
        holdings = response['holdings'][0]
        df = pd.DataFrame.from_dict(holdings, orient='index').T
        print(df)
    else:
        print('Received response : ')
        print(response)
    print()


def main():

    print()
    print('1] Get user profile')
    print('2] Get margin')
    print('3] Get LTP')
    print('4] OHLC Values')
    print('5] Holdings')
    print()
    choice = int(input("Enter your choice : "))

    if choice == 1:
        message = {
            'option': 'profile'
        }
    elif choice == 2:
        message = {
            'option': 'margin'
        }
    elif choice == 3:
        ticker = str(input('Enter stock ticker : '))
        message = {
            'option': 'ltp',
            'ticker': ticker,
        }
    elif choice==4:
        ticker = str(input('Enter stock ticker : '))
        message = {
            'option': 'ohlc',
            'ticker': ticker,
        }
    elif choice==5:
        message = {
            'option': 'holdings'
        }
    else:
        print('Invalid option')

    channel.basic_publish(exchange='user_exchange', routing_key='request_key', body=json.dumps(message))
    print("\nRequest sent\n")
    channel.basic_consume(queue='response_queue', on_message_callback=response_callback, auto_ack=True)

    channel.start_consuming()
    print('Stopped consuming')


if __name__ == '__main__':
    main()
    
    



