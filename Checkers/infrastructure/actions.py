import inspect
from .verdict import Verdict


INFO, CHECK, PUT, GET = "INFO", "CHECK", "PUT", "GET"


class Register:
    INFO: str = None
    __multiple_actions = frozenset((PUT, GET))
    __actions_handlers = {
        CHECK: None,
        PUT: {},
        GET: {},
    }

    @staticmethod
    def __check_function(func):
        func_annotations: dict = dict(inspect.getmembers(func))["__annotations__"]
        if func_annotations.get("return") != Verdict:
            raise TypeError(f"Checker function should return {Verdict} object!")
        # todo check args for ip / flag / flag_id / vuln_id

    @classmethod
    def __register_action(cls, action_name: str, action: callable, action_period: int = None):
        if action_name in cls.__multiple_actions:
            if action_period is None:
                raise ValueError("Period should not be None for multiple actions!")
            cls.__actions_handlers[action_name][action_period] = action
        else:
            if action_name in cls.__actions_handlers:
                if cls.__actions_handlers[action_name] is not None:
                    raise ValueError("Action has been already registered!")
                cls.__actions_handlers[action_name] = action
            else:
                raise ValueError("Incorrect action name!")

    @staticmethod
    def check(func: callable) -> callable:
        Register.__check_function(func)
        Register.__register_action(CHECK, func)
        return func

    @staticmethod
    def put(vuln_num: int) -> callable:
        def wrapper(func: callable):
            Register.__check_function(func)
            Register.__register_action(PUT, func, vuln_num)
            return func
        return wrapper

    @staticmethod
    def get(vuln_num: int) -> callable:
        def wrapper(func: callable):
            Register.__check_function(func)
            Register.__register_action(GET, func, vuln_num)
            return func
        return wrapper


