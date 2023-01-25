"""
Events client
=============
"""

from inqdo_tools.utils.get_client import Client
from inqdo_tools.utils.json import Json


class EventsClient(object):
    """This object helps to respond to state changes.

    :param body: Expects a :class:`body` argument which will be
        send to the EventBridge.
    :type body: dict

    :param source: Expects a :class:`source` argument which will be
        the source of the event.
    :type source: str

    :param detail_type: Expects :class:`detail_type` argument, this should be a
        free-form string used to decide what fields to expect in the event detail.

    :type detail_type: str,

    :param bus_name: Expects a :class:`bus_name` argument, this will be
        the name or ARN of the event bus to receive the event.

    :rtype: dict
    """

    def __init__(
        self,
        detail_type: str,
        bus_name: str,
    ):
        """Constructor method"""

        self.detail_type = detail_type
        self.bus_name = bus_name
        self.client = Client(service="events").service

    def put_events(self, source: str, body: dict):
        self.client.put_events(
            Entries=[
                {
                    "Source": source,
                    "DetailType": self.detail_type,
                    "Detail": Json.compact({"body": body}),
                    "EventBusName": self.bus_name,
                }
            ]
        )
