import time
from google.cloud import pubsub_v1

"""Publisher"""
def publish_messages(project, topic_name):
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project, topic_name)

    data = u'Message number {}'.format("10215028733130789")
    data = data.encode('utf-8')
    publisher.publish(topic_path, data=data)

    """for n in range(1, 10):
        data = u'Message number {}'.format(n)
        data = data.encode('utf-8')
        publisher.publish(topic_path, data=data)"""

    print('Published messages')

"""Subscriber"""
def receive_messages(project, subscription_name):
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project, subscription_name)
    
    def callback(message):
        print('Received message: {}'.format(message))
        message.ack()

    subscriber.subscribe(subscription_path, callback=callback)
    print('Listening for messages on {}'.format(subscription_path))
    while True:
        time.sleep(60)

if __name__ == '__main__':
    receive_messages("nytint-stg", "fbworld")
    publish_messages("nytint-stg", "fbworld")
