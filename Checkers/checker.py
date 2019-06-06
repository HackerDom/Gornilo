from infrastructure.actions import Checker
from infrastructure.verdict import Verdict
from infrastructure.checker_request import CheckRequest, PutRequest, GetRequest


Checker.INFO = "1:2"  # means vulns distribution


@Checker.define_check
def check_service(request: CheckRequest) -> Verdict:
    ...  # your code

    return Verdict.OK()


@Checker.define_put(vuln_num=1)
def put_flag_into_the_service(request: PutRequest) -> Verdict:
    ...  # your code

    return Verdict.OK("my_new_flag_id")


@Checker.define_get(vuln_num=1)
def get_flag_from_the_service(request: GetRequest) -> Verdict:
    ...  # your code

    return Verdict.OK()


@Checker.define_put(vuln_num=2)
def put_flag_into_the_service(request: PutRequest) -> Verdict:
    ...  # your code

    return Verdict.MUMBLE("something bad with ur proto", "they are cheating!")


@Checker.define_get(vuln_num=2)
def get_flag_from_the_service(request: GetRequest) -> Verdict:
    ...  # your code

    return Verdict.CORRUPT("flag lost", "lol, they lost it")


if __name__ == '__main__':
    Checker.run()
