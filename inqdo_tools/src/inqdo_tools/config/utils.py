import json


def delete_config_rule(config_rules: list, event: str) -> list:
    new_config_rules = config_rules

    for i in range(len(new_config_rules)):
        if new_config_rules[i]["Name"] == event["Name"]:
            new_config_rules[i]
            del new_config_rules[i]
            break

    return new_config_rules


def update_config_rules(config_rules: list, event: str, enabled: bool) -> list:
    new_config_rules = config_rules
    # Remove the original from the array
    for i in range(len(new_config_rules)):
        if new_config_rules[i]["Name"] == event["Name"]:
            new_config_rules[i]
            del new_config_rules[i]
            break

    event["Enabled"] = enabled

    new_config_rules.append(event)

    return new_config_rules


def construct_managed_meta_data(event: dict) -> dict:
    meta_data = event.copy()
    # Delete all the meta data that is False
    for key, value in dict(meta_data).items():
        if not value:
            del meta_data[key]

    try:
        del meta_data["Name"]
    except KeyError:
        pass
    try:
        del meta_data["ExcludedAccounts"]
    except KeyError:
        pass
    try:
        del meta_data["Enabled"]
    except KeyError:
        pass

    params = meta_data.get("InputParameters")
    json_params = json.dumps(params)

    meta_data["InputParameters"] = json_params

    return meta_data
