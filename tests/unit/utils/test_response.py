from __future__ import absolute_import

from inqdo_tools.utils.json import Json
from inqdo_tools.utils.response import Response

standard_headers = {
    "Access-Control-Allow-Origin": "*",
    "Content-Type": "application/json",
}

ok_body = {
    "Success": "Successfull request",
}


# SUCCESSFULL RESPONSE
def test_successfull_response():
    ok_response = {
        "statusCode": 200,
        "headers": standard_headers,
        "body": Json.compact(ok_body),
    }
    assert Response(body=ok_body).ok() == ok_response


# UNSUCCESSFULL RESPONSE
def test_unsuccessfull_response():
    error_body = {
        "Error": "An unknown error occured, check the CloudWatch logs.",
    }
    error_response = {
        "statusCode": 400,
        "headers": standard_headers,
        "body": Json.compact(error_body),
    }
    assert Response(body=error_body).error() == error_response


# UNAUTHORIZED RESPONSE
def test_unauthorized_response():
    unauthorized_body = {
        "Error": "Unauthorized",
    }
    unauthorized_response = {
        "statusCode": 401,
        "headers": standard_headers,
        "body": Json.compact(unauthorized_body),
    }
    assert Response(body=unauthorized_body).unauthorized() == unauthorized_response


# FORBIDDEN RESPONSE
def test_forbidden_response():
    forbidden_body = {
        "Error": "Forbidden",
    }
    forbidden_response = {
        "statusCode": 403,
        "headers": standard_headers,
        "body": Json.compact(forbidden_body),
    }
    assert Response(body=forbidden_body).forbidden() == forbidden_response


# NOT FOUND RESPONSE
def test_not_found_response():
    empty_body = {
        "Error": "Not Found",
    }
    empty_response = {
        "statusCode": 404,
        "headers": standard_headers,
        "body": Json.compact(empty_body),
    }
    assert Response(body=empty_body).not_found() == empty_response


# CONFLICT RESPONSE
def test_conflict_response():
    conflict_body = {
        "conflict": "conflict request",
    }
    conflict_response = {
        "statusCode": 409,
        "headers": standard_headers,
        "body": Json.compact(conflict_body),
    }

    assert Response(body=conflict_body).conflict() == conflict_response


# UNPROCESSABLE ENTITY RESPONSE
def test_unprocessable_entity_response():
    unprocessable_entity_body = {
        "unprocessable_entity": "unprocessable_entity request",
    }
    unprocessable_entity_response = {
        "statusCode": 422,
        "headers": standard_headers,
        "body": Json.compact(unprocessable_entity_body),
    }

    assert (
        Response(body=unprocessable_entity_body).unprocessable_entity()
        == unprocessable_entity_response
    )


# INTERNAL SERVER ERROR
def test_internal_server_error():
    internal_server_error_body = {
        "internal_server_error": "internal_server_error request",
    }
    internal_server_error_response = {
        "statusCode": 500,
        "headers": standard_headers,
        "body": Json.compact(internal_server_error_body),
    }

    assert (
        Response(body=internal_server_error_body).internal_server_error()
        == internal_server_error_response
    )


# NOT IMPLEMENTED ERROR
def test_not_implemented():
    not_implemented_body = {
        "not_implemented": "not_implemented request",
    }
    not_implemented_response = {
        "statusCode": 501,
        "headers": standard_headers,
        "body": Json.compact(not_implemented_body),
    }

    assert (
        Response(body=not_implemented_body).not_implemented()
        == not_implemented_response
    )


# SERVICE UNAVAILABLE
def test_service_unavailable():
    service_unavailable_body = {
        "service_unavailable": "service_unavailable request",
    }
    service_unavailable_response = {
        "statusCode": 503,
        "headers": standard_headers,
        "body": Json.compact(service_unavailable_body),
    }

    assert (
        Response(body=service_unavailable_body).service_unavailable()
        == service_unavailable_response
    )


def test_extra_response():
    # ============================
    # Extra tests
    # ============================

    # Test string body error
    ok_string_body = "String"
    ok_string_response = {
        "statusCode": 200,
        "headers": standard_headers,
        "body": ok_string_body,
    }
    assert Response(body=ok_string_body).ok() != ok_string_response

    # Test adding extra headers
    ok_extra_headers = {"foo": "bar", "fizz": "bizz"}
    ok_response_extra_headers = {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json",
            "foo": "bar",
            "fizz": "bizz",
        },
        "body": Json.compact(ok_body),
    }

    assert (
        Response(body=ok_body, headers=ok_extra_headers).ok()
        == ok_response_extra_headers
    )

    # Test different content type
    ok_content_type = "xml"
    ok_response_content_type = {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "text/xml",
        },
        "body": Json.compact(ok_body),
    }

    assert (
        Response(body=ok_body, content_type=ok_content_type).ok()
        == ok_response_content_type
    )

    # Test both arguments together
    ok_response_content_type_extra_headers = {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "text/xml",
            "foo": "bar",
            "fizz": "bizz",
        },
        "body": Json.compact(ok_body),
    }

    assert (
        Response(
            body=ok_body, headers=ok_extra_headers, content_type=ok_content_type
        ).ok()
        == ok_response_content_type_extra_headers
    )
