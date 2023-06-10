import pika

# CONNECTION WITH RABITMQ SERVER
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# DECLARING A QUEUE
channel.queue_declare(queue='hello')

# PUBLISH MESSAGES TO THE QUEUES
channel.basic_publish(exchange='', routing_key='hello', body='Hello World')
print("Message Sent")
connection.close()

