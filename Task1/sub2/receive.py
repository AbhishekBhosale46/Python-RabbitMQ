import pika

# CONECTION TO RABBITMQ SERVER 
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost')
)
channel = connection.channel()

# DECLARING THE EXCHANGE
channel.exchange_declare(exchange='logs', exchange_type='fanout')

# DECLARING THE QUEUE (THE QUEUE NAME IS GENERATED AUTOMATICALLY, USE result.method.queue TO GET IT)
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue
channel.queue_bind(exchange='logs', queue=queue_name)

print("Waiting for data ...")

# PROCESSING THE RECEIVED BODY AND WRITING IT TO A FILE
def callback(ch, method, properties, body):
    with open('received_file.csv', 'wb') as file:
        file.write(body)
    print("Csv received")

channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True
)
channel.start_consuming()