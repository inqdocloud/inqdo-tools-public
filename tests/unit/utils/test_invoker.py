from inqdo_tools.invoker.client import Invoker


def _delegate_test_function(event, body, logger, context):
    return body["message"]


def test_invoker_with_event_bridge_event():
    event = {
        "version": "0",
        "id": "b53c98c6-2525-c5cb-e767-45348639035a",
        "detail-type": "test",
        "source": "invoke.test",
        "account": "503855582803",
        "time": "2021-10-27T07:02:56Z",
        "region": "eu-west-1",
        "resources": [],
        "detail": {
            "body": {
                "message": "invoked event bridge",
            }
        },
    }

    invoker = Invoker(
        event=event, context={}, file=__file__, delegate=_delegate_test_function
    ).lambda_handler()
    assert invoker == "invoked event bridge"
