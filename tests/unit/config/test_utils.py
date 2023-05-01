from inqdo_tools.config.utils import (
    construct_managed_meta_data,
    delete_config_rule,
    update_config_rules,
)


def test_delete_config_rule():
    config_rule = {"Name": "TestRule"}

    config_rules = []
    config_rules.append(config_rule)

    event: str
    event = {"Name": "TestRule"}  # type: ignore

    result = delete_config_rule(config_rules=config_rules, event=event)

    assert len(result) == 0


def test_update_config_rules():
    config_rule = {"Name": "TestRule"}
    config_rules = []
    config_rules.append(config_rule)
    event: str
    event = {"Name": "TestRule"}  # type: ignore

    result = update_config_rules(config_rules=config_rules, event=event, enabled=True)

    assert len(result) == 1


def test_construct_managed_meta_data_fullevent():
    event = {
        "Name": "",
        "ExcludedAccounts": "Test",
        "Enabled": True,
        "InputParameters": {"Test": "Test"},
    }

    result = construct_managed_meta_data(event=event)

    assert result == {"InputParameters": '{"Test": "Test"}'}


def test_construct_managed_meta_data_missing_excluded_accounts():
    event = {"Name": "", "Enabled": True, "InputParameters": {"Test": "Test"}}
    result = construct_managed_meta_data(event=event)

    assert result == {"InputParameters": '{"Test": "Test"}'}


def test_construct_managed_meta_data_missing_enabled():
    event = {
        "Name": "",
        "ExcludedAccounts": "Test",
        "InputParameters": {"Test": "Test"},
    }

    result = construct_managed_meta_data(event=event)

    assert result == {"InputParameters": '{"Test": "Test"}'}
