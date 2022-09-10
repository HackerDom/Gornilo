# Gornilo-Checker

Gornilo is a checker wrapper lib.

#### Features:
- no exit-code/chk-sys interface requirements
- object model
- built-in error handling
- asyncio support
- stdout redirect (print defaults for stderr)
- testing output


### Quick Start
#### Examples
* [Minimal working example](https://github.com/HackerDom/Gornilo/blob/master/gornilo/examples/checker.py) 
* [Checker for abstract service](https://github.com/HackerDom/Gornilo/blob/master/gornilo/examples/abstract_checker.py)

#### How to run locally: 
Start your service locally, then run checker against your service :)
```py checker.py TEST 0.0.0.0:8080```


### Tools and helpers
`requests_with_retries()` - wrapper for requests lib that retrys failed requests (:
 

### Concepts
#### Structure
Checker has similliar functionality to e2e tests. It has three most important methods:
* `CHECK` that service works correct.
* `PUT` flag to service
* `GET` flag from service, and check that falg is correct

If service has multiple flag types you must implement `PUT` and `GET` method for each type.

So for service with two flag types checker must implement next methods:
```
CHECK - check all service functionality

PUT_1 - put flag of firts type
GET_1 - check that service still has flag

PUT_2 - put flag of second type
GET_2 - check that service still has flag
```
Checker runs `CHECK` `PUT_i` `GET_i` sequence for each team seperatly.

#### Verdicts
Checker methods must complete with one of next verdicts:
* `OK` - method complete without problems
* `MUMBLE` - service response incorrect
* `DOWN` - failed connect to a service
* `CHECKER_ERROR` - exceptions in checker, or brocken checker logic

`GET` method has one more verdict
* `CORRUPT` - service has no flag or flag is incorrect

#### Flag Rate aka Vuln Rate
Flag rate is an option adjusting how many flags of this type, put in the service per round. In general various flag types are implements for various vulnarabilities, that vary in complexity. With __flag rate__ you can put more flag to difficult vuln and less to easy.

#### Flag id
Flag id - all data you need to get the flag, for example username+password. Passed from `PUT` to `GET` methods. 

#### Public flag Id
Public flag id is a feature simplifying service implementation. In most cases attacker must knows ids of entities of your service. So you need implement additional handler for listing, and check this handler in __CHECK__ method. Public flag id allows you to pass such ids with verdict, then attacker can list its from checksystem api.

### Example
Let's implement simple checker for abstract service
```python
@checker.define_check # every checker method should be wrapped with decorator checker.define_...
async def check_service(request: CheckRequest) -> Verdict:
    user = 'Bob'

    url = f"http://{request.hostname}/register/{user}" #request.hostname - address of checking team's service in host:port format

    response = requests_with_retries().post(url, data = "user")

    if response.status_code != 200: #if service response is unexpected, return mumble
        return Verdict.MUMBLE(f"response code {response.status_code}") #add reason to verdict, it will be shown to the checking team

    return Verdict.OK()
```

Next we need `PUT` + `GET` method pair, they should look like:
```python
#flag flag_id_description - hint for players, vuln_rate - flag rate
@checker.define_vuln(flag_id_description="flag_id is user", vuln_rate=1)
class FirstVuln(VulnChecker):

    #put flag method
    @staticmethod
    def put(request: PutRequest) -> Verdict:
        ...
        return Verdict.OK(...flag_id...)

    #get flag method
    @staticmethod
    def get(request: GetRequest) -> Verdict:
        ...
        return Verdict.Ok()
```

Implement some logic for clarity

```python
#flag flag_id_description - hint for players, vuln_rate - flag rate
@checker.define_vuln(flag_id_description="flag_id is user", vuln_rate=1)
class FirstVuln(VulnChecker):
    @staticmethod
    def put(request: PutRequest) -> Verdict:
        data = {
            "user": "Draco",
            "Password": "PureBl00d",
            "gringotts_pass_phrase": request.flag, #add flag
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
        if actual["gringotts_pass_phrase"] != request.flag: 
            return Verdict.CORRUPT(f"Expected falg {request.flag}, but actual {actual['secret']}")

        return Verdict.OK()
```

Full code can be found [here](https://github.com/HackerDom/Gornilo/blob/master/gornilo/examples/abstract_checker.py)
