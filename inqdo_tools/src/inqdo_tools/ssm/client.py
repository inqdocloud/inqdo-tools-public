import datetime
import os

if "DEBUG_INQDO_TOOLS" in os.environ.keys(): # pragma: no cover
    from utils.get_client import Client
else:
    from inqdo_tools.utils.get_client import Client


class SSMClient(object):
    """This creates the parent boto3 client to the SSM"""

    def __init__(self):
        self._client = Client(service="ssm").service


class ParameterStore(SSMClient):
    """Provide a dictionary-like interface to access AWS SSM Parameter Store

    : param prefix: Base path for the store (ie. /prod)
    : type prefix: str

    : param ttl: Cache the result up to X seconds
    : type ttl: number

    : rtype: dict
    """

    def __init__(self, prefix=None, ttl=None):
        super(ParameterStore, self).__init__()
        self._prefix = (prefix or "").rstrip("/") + "/"
        self._keys = None
        self._substores = {}
        self._ttl = ttl

    def get(self, name, **kwargs):
        """Fetch a certain parameter or all the children

        :param name: The name (key) of the parameter to fetch
        :type name: str

        :rtype: dict
        """
        assert name, "Name can not be empty"
        if self._keys is None:
            self.refresh()

        abs_key = "%s%s" % (self._prefix, name)
        if name not in self._keys:
            if "default" in kwargs:
                return kwargs["default"]

            raise KeyError(name)
        elif self._keys[name]["type"] == "prefix":
            if abs_key not in self._substores:
                store = self.__class__(prefix=abs_key, ttl=self._ttl)
                store._keys = self._keys[name]["children"]
                self._substores[abs_key] = store

            return self._substores[abs_key]
        else:
            return self._get_value(name, abs_key)

    def refresh(self):
        """Refresh the parameters"""
        self._keys = {}
        self._substores = {}

        paginator = self._client.get_paginator("describe_parameters")
        pager = paginator.paginate(
            ParameterFilters=[
                dict(Key="Path", Option="Recursive", Values=[self._prefix])
            ]
        )

        for page in pager:
            for p in page["Parameters"]:
                name = p["Name"]
                if name.startswith("/"):
                    paths = name[len(self._prefix) :].split("/")  # noqa
                else:
                    paths = name.split("/")
                self._update_keys(self._keys, paths)

    @classmethod
    def _update_keys(cls, keys, paths):
        name = paths[0]
        # this is a prefix
        if len(paths) > 1:
            if name not in keys:
                keys[name] = {"type": "prefix", "children": {}}
            if "children" in keys[name]:
                cls._update_keys(keys[name]["children"], paths[1:])
        else:
            keys[name] = {"type": "parameter", "expire": None}

    def keys(self):
        """List all parameters (ie. keys)

        :rtype: dict
        """
        if self._keys is None:
            self.refresh()

        return self._keys.keys()

    def _get_value(self, name, abs_key):
        entry = self._keys[name]

        # simple ttl
        if self._ttl is False or (
            entry["expire"] and entry["expire"] <= datetime.datetime.now()
        ):
            entry.pop("value", None)

        if "value" not in entry:
            parameter = self._client.get_parameter(Name=abs_key, WithDecryption=True)[
                "Parameter"
            ]
            value = parameter["Value"]
            if parameter["Type"] == "StringList":
                value = value.split(",")

            entry["value"] = value

            if self._ttl:
                entry["expire"] = datetime.datetime.now() + datetime.timedelta(
                    seconds=self._ttl
                )
            else:
                entry["expire"] = None

        return entry["value"]

    def __contains__(self, name):
        try:
            self.get(name)
            return True
        except Exception:
            return False

    def __getitem__(self, name):
        return self.get(name)

    def __setitem__(self, key, value):
        raise NotImplementedError()

    def __delitem__(self, name):
        raise NotImplementedError()

    def __repr__(self):
        return "ParameterStore[%s]" % self._prefix
