from inqdo_tools.utils.common import (
    destruct_dict,
    dict_get,
    dict_get_forced,
    dict_set,
    lower_key_dict,
)


def test_dict_set():
    example_dict = {
        "results": {
            "movies": {
                "star_wars": {"darkside": {"members": {"anakin_skywalker": "level 5"}}}
            }
        }
    }

    dict_set(
        dictionary=example_dict,
        keys=["results", "movies", "star_wars", "darkside", "members"],
        value={"darth_vader": "lever 100"},
    )

    assert example_dict == {
        "results": {
            "movies": {
                "star_wars": {"darkside": {"members": {"darth_vader": "lever 100"}}}
            }
        }
    }


def test_lower_key_dict():
    example_dict = {"Movies": "abc"}

    lower_keys = lower_key_dict(d=example_dict)

    assert lower_keys == {"movies": "abc"}


def test_dict_get():
    example_dict = {"movies": {"rank": {"10": ["Star Wars", "Spiderman"]}}}

    result = dict_get(dictionary=example_dict, keys=["movies", "rank", "10"])
    result_with_default = dict_get(
        dictionary=example_dict, keys=["movies", "rank", "9"], default=["Batman"]
    )

    assert result == ["Star Wars", "Spiderman"]
    assert result_with_default == ["Batman"]


def test_dict_get_forced():
    example_dict = {"movIes": {"Rank": {"10": ["Star Wars", "Spiderman"]}}}

    result = dict_get_forced(dictionary=example_dict, keys=["movies", "rank", "10"])
    result_with_default = dict_get_forced(
        dictionary=example_dict, keys=["movies", "rank", "9"], default=["Batman"]
    )

    assert result == ["Star Wars", "Spiderman"]
    assert result_with_default == ["Batman"]


def test_destruct_dict():
    destructed_items = destruct_dict(
        dict_to_destruct={
            "keyword_argument_a": "a",
            "keyword_argument_b": "b",
            "keyword_argument_c": "c",
            "keyword_argument_d": "d",
        },
        keys=[
            "keyword_argument_a",
            "keyword_argument_b",
        ],
    )

    assert destructed_items == ("a", "b")
