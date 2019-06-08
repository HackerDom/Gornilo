from Checker.src import Checker, Verdict, \
    CheckRequest, PutRequest, GetRequest


checker = Checker()


@checker.define_check
async def check_service(request: CheckRequest) -> Verdict:
    ...  # your code

    return Verdict.OK()


@checker.define_put(vuln_num=1, vuln_rate=2)
async def put_flag_into_the_service(request: PutRequest) -> Verdict:
    ...  # your code

    return Verdict.OK("my_new_flag_id")


@checker.define_get(vuln_num=1)
async def get_flag_from_the_service(request: GetRequest) -> Verdict:
    ...  # your code

    return Verdict.OK()


@checker.define_put(vuln_num=2, vuln_rate=1)
async def put_flag_into_the_service(request: PutRequest) -> Verdict:
    ...  # your code

    return Verdict.MUMBLE("something bad with ur proto", "they are cheating!")


@checker.define_get(vuln_num=2)
async def get_flag_from_the_service(request: GetRequest) -> Verdict:
    ...  # your code

    return Verdict.CORRUPT("flag lost", "lol, they lost it")


if __name__ == '__main__':
    checker.run()
