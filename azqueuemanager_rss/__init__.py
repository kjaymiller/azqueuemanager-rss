from datetime import datetime
import dateparser
import feedparser
from time import mktime

from azqueuemanager.extension import ExtensionBaseClass, _parser_filter 


# Replease MYEXTENSION with the name of your extension
def get_current_interval(interval):
    """Default datetime filter method"""
    return dateparser.parse(interval)


def to_datetime(time_struct):
    """Validate time interval"""
    return datetime.fromtimestamp(mktime(time_struct))



class RSSTransform(ExtensionBaseClass):
    """This class transforms json data into a format that can be used by the queue."""

    def __init__(
        self,
        rss_in: any,
        time_interval: str='-24h',
        parser_filter: _parser_filter=None
        
    ):

        # currently only the `parser filter` kwarg is required
        # for more information on the parser filter, see - github.com/kjaymiller/azqueuemanager/blob/main/azqueuemanager/extension.py
        super().__init__()

        # The REQUIRED_ARG is likely something that can determine how to ingest the data.
        # You can rename this to whatever you want and have as many as needed
        self.rss_in = rss_in

        if time_interval[0] != '-':
            self.time_interval = "-" + time_interval

        else:
            self.time_interval = time_interval

        if parser_filter:
            self.parser_filter=parser_filter
        else:
            self.parser_filter=lambda x: to_datetime(x['published_parsed']) > get_current_interval(self.time_interval)

    def transform_in(self):
        """This method transforms the data into a format that can be used by the queue."""
        feed = feedparser.parse(self.rss_in)

        for item in filter(self.parser_filter, feed.entries):
            yield item
    
    def transform_preview(self, data: str):
        """
        This method assists with creating previews.
        This is shouldn't send data to a response but provide a preview of the data that will be sent to the queue.
        """
        raise NotImplementedError('transform_preview not implemented')

    def transform_out(self, data: list[str]):
        """This method transform the data passed. If there is an output step it should be done here."""
        raise NotImplementedError('transform_out not implemented')