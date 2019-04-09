from infrastructure.actions import Register
from infrastructure.verdict import Verdict


Register.INFO = "1:2"


@Register.check
def check_service() -> Verdict:
    return Verdict.OK()


@Register.put
def put_flag_into_the_service() -> Verdict:
    return Verdict.OK()


