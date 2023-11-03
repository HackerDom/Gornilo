import sys

from gornilo import CheckRequest, Verdict, PutRequest, GetRequest, NewChecker, VulnChecker
from gornilo.http_clients import requests_with_retries

checker = NewChecker()


@checker.define_check
async def check_service(request: CheckRequest) -> Verdict:
    ...  # your code
    requests_with_retries().get(f"http://{request.hostname}")
    return Verdict.OK()


@checker.define_vuln("flag_id is an email")
class XSSChecker(VulnChecker):
    @staticmethod
    def put(request: PutRequest) -> Verdict:
        return Verdict.OK_WITH_FLAG_ID("email1", "next_id1")

    @staticmethod
    def get(request: GetRequest) -> Verdict:
        return Verdict.OK()


@checker.define_vuln("flag_id is something else in xml")
class XMLChecker(VulnChecker):
    @staticmethod
    def put(request: PutRequest) -> Verdict:
        return Verdict.OK_WITH_FLAG_ID("email2", "next_id2")

    @staticmethod
    def get(request: GetRequest) -> Verdict:
        return Verdict.OK()


if __name__ == '__main__':
    checker.run()
