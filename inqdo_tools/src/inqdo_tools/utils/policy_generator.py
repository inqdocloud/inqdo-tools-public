from botocore.hooks import HierarchicalEmitter
from botocore.model import OperationModel


class PolicyGenerator:
    def __init__(self):
        self.actions = set()

    def record(self):
        HierarchicalEmitter.emit_until_response = self._event_wrapper(
            HierarchicalEmitter.emit_until_response
        )

    def generate(self):
        services = {}

        for action in list(self.actions):
            service = action.split(":")[0]

            if service in services:
                services[service].append(action)
            else:
                services[service] = [action]

        return services

    def _event_wrapper(self, method):
        def wrapper_method(*args, **kwargs):
            """
            The PolicyGenerator class is used to generate a policy for
            AWS services based on the actions that are recorded.

            It has the following methods:

            __init__: Initializes an empty set to store the actions

            record: Wraps the emit_until_response method of the HierarchicalEmitter class to record the actions

            generate: Organizes the recorded actions by AWS service and returns them as a dictionary

            _event_wrapper: A helper method that is used by the record method to find the
            OperationModel in the args and kwargs and adds the corresponding action to the set of recorded actions
            """
            model = kwargs.get("model")

            # If model isn't in kwargs, check for it in args
            if not model:
                try:
                    model = next(a for a in args if type(a) is OperationModel)
                except StopIteration:
                    pass  # No model found

            if model:
                action = "{}:{}".format(model.metadata["endpointPrefix"], model.name)

                self.actions.add(action)

            return method(*args, **kwargs)

        return wrapper_method
