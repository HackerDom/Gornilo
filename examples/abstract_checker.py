#!/usr/bin/env python3
from gornilo import CheckRequest, Verdict, Checker, PutRequest, GetRequest, VulnChecker
from gornilo.http_clients import requests_with_retries
import json

checker = Checker()

@checker.define_check # every checker method should be wrapped with decorator checker.define_...
async def check_service(request: CheckRequest) -> Verdict:
    user = 'Bob'

    url = f"http://{request.hostname}/register/{user}" #request.hostname - address of checking team's service in host:port format

    response = requests_with_retries().post(url, data = "user")

    if response.status_code != 200: #if service response is unexpected, return mumble
        return Verdict.MUMBLE(f"response code {response.status_code}") #add reason to verdict, it will be shown to the checking team

    return Verdict.OK()


#flag flag_id_description - hint for players, vuln_rate - flag rate
@checker.define_vuln(flag_id_description="flag_id is user", vuln_rate=1)
class FirstVuln(VulnChecker):
    @staticmethod
    def put(request: PutRequest) -> Verdict:
        data = {
            "user": "Draco",
            "Password": "PureBl00d",
            "secret": request.flag, #add flag
            "guilty_secret": "loves Hermion and A/D ctf" #some functional data
        }

        url = f"http://{request.hostname}/secrets/{data['user']}"

        response = requests_with_retries().post(url, data = json.dumps(data))

        if response.status_code != 200:
            return Verdict.MUMBLE(f"response code {response.status_code}")
        
        # set public_flag_id, and flag_id
        return Verdict.OK_WITH_FLAG_ID(data["user"] ,json.dumps(data))  

    @staticmethod
    def get(request: GetRequest) -> Verdict:
        #get flag id
        expected = json.loads(request.flag_id) 

        #get flag
        user = expected["user"]
        url = f"http://{request.hostname}/secrets/{user}/"
        response = requests_with_retries().post(url, data=expected["password"])
        actual = json.loads(response.content)

        #check flag
        if actual["secret"] != request.flag: 
            return Verdict.CORRUPT(f"Expected falg {request.flag}, but actual {actual['secret']}")

        return Verdict.OK()


if __name__ == '__main__':
    checker.run()