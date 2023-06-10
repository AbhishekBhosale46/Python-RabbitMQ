import pika
from datetime import date
from jugaad_data.nse import bhavcopy_save

# FUNCTION TO DOWNLOAD DATA FROM NSE 
def getCsv():
    fileName = bhavcopy_save(date(2023,5,29), ".")
    return fileName

# CONECTION TO RABBITMQ SERVER 
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost')
)
channel = connection.channel()

# DECLARING THE EXCHANGE (IN CASE OF PUB/SUB NO NEEDTO DECLARE QUEUE, QUEUE IS CREATED AUTOMATICALLY FOR THAT PARTICULAR SUBSCRIBER) 
channel.exchange_declare(exchange='logs', exchange_type='fanout')

# SAVE THE CSV 
fileName = getCsv()

# OPEN THE CSV TO READ THE DATA AND SEND IT OVER EXCHANGE 
with open(fileName, 'rb') as file:
    csv_data = file.read()

# SEND THE CSV DATA 
channel.basic_publish(exchange='logs', routing_key='', body=csv_data)
print("Bhavcopy csv sent")
connection.close()