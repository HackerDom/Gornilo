from gornilo import CheckRequest, Verdict, PutRequest, GetRequest, NewChecker, VulnChecker
from gornilo.http_clients import requests_with_retries

checker = NewChecker()

from logging import getLogger
print = getLogger().info


@checker.define_check
async def check_service(request: CheckRequest) -> Verdict:
    ...  # your code
    requests_with_retries().get(f"http://{request.hostname}")
    print("Another log")
    return Verdict.OK()


@checker.define_vuln("flag_id is an email")
class XSSChecker(VulnChecker):
    @staticmethod
    def put(request: PutRequest) -> Verdict:
        return Verdict.OK_WITH_FLAG_ID("email", "next_id")

    @staticmethod
    def get(request: GetRequest) -> Verdict:
        return Verdict.OK()


@checker.define_vuln("flag_id is something else in xml")
class XMLChecker(VulnChecker):
    @staticmethod
    def put(request: PutRequest) -> Verdict:
        return Verdict.OK_WITH_FLAG_ID("email", "next_id")

    @staticmethod
    def get(request: GetRequest) -> Verdict:
        return Verdict.OK()


if __name__ == '__main__':
    checker.run()
