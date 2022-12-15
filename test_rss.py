import feedparser
from azqueuemanager_rss import RSSTransform
from azqueuemanager import QueueManager
from azqueuemanager.queue import QueueClient

url = "https://pythoncommunitynews.com/python-community-news-archive.xml"

queue_client = QueueClient.from_connection_string("rss-test")

QueueManager = QueueManager(
    queue=queue_client,
    input_transformer=RSSTransform(rss_in=url, time_interval="-7d"),
)

QueueManager.queue_messages()  # this will send the data to the queue``

print(QueueManager.list_messages())  # this will print a preview of the data that will be sent to the queue