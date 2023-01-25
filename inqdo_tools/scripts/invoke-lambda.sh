#!/bin/bash

EVENTS['9000']='{
   "body":"{\"instances\":\"i-05e38a3f917e9d21d\",\"arn\":\"arn:aws:iam::056907270820:role/inQdoCloudPortalRole\",\"region\":\"eu-west-1\",\"account_alias\":\"portal-tst-1\",\"account_id\":\"056907270820\"}",
}'

curl -XPOST "http://localhost:{$1}/2015-03-31/functions/function/invocations" -d "${EVENTS[$1]}"
