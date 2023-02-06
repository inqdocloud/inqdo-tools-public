from inqdo_tools.ssm.client import ParameterStore


# GET SPECIFIC STORE KEY
def test_get_key(ssm_client, ssm_create_parameter):

    # initialize parameter store
    store = ParameterStore(prefix="/root")

    # test getting parameter value
    assert store.get(name="key1") == "value1"
    assert "key1" in store
    assert store["key1"] == "value1"

    # test keys method
    assert "key1" in store.keys()


# REFRESH STORE
def test_refresh_store(ssm_client, ssm_create_parameter):

    # initialize parameter store
    store = ParameterStore(prefix="/root")

    # test refreshing parameters
    store.refresh()
    assert store.get(name="key1") == "value1"
