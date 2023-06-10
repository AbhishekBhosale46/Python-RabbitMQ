import pika, sys, os

def main():

    # CONNECTION WITH RABITMQ SERVER
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    # DECLARING A QUEUE
    channel.queue_declare(queue='hello')

    # CALLBACK FUNCTION (EXECUTED WHEN MESSAGES ARE RECEIVED)
    def callback(ch, method, properties, body):
        print(" Received %r" %body)

    # RECEIVE MESSAGES FROM QUEUE
    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)
    print("Waiting for messages to appear, press CTRL+C to exit")
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)



