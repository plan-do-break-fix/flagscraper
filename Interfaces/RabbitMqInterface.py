from os import environ
import pika


class RabbitMqInterface:

    def __init__(self):
        self.host = environ["Q_HOST"]
        self.user = environ["Q_LOGIN"]
        self.password = environ["Q_PASSWD"]

    def enqueue(self, message, qname) -> bool:
        try:
            self.channel.basic_publish(
                exchange="",
                routing_key=qname,
                body=message
            )
            return True
        except pika.exception.StreamLostError:
            self.connect()
            self.enqueue(message, qname)

    def dequeue(self, qname) -> str:
        self.connect()
        method, header, body = self.channel.basic_get(queue=qname)
        if not body:
            self.connection.close
            return False
        else:
            self.channel.basic_ack(delivery_tag=method.delivery_tag)
            self.connection.close
            return body.decode()
        

    def connect(self) -> True:
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=self.host,
                credentials=pika.credentials.PlainCredentials(
                    self.user,
                    self.pswd
                )
            )
        )
        self.channel = self.connection.channel()
        return True



