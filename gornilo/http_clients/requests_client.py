try:
    import requests
    from requests.adapters import HTTPAdapter, Retry

    USER_AGENT = lambda: "checker"


    def requests_with_retries(
        retries=3,
        backoff_factor=0.3,
        status_forcelist=(400, 404, 500, 502),
        session=None,
    ):
        session = session or requests.Session()
        retry = Retry(
            total=retries,
            read=retries,
            connect=retries,
            backoff_factor=backoff_factor,
            status_forcelist=status_forcelist,
        )
        adapter = HTTPAdapter(max_retries=retry)

        session.headers.update({"User-Agent": USER_AGENT()})
        session.mount('http://', adapter)
        return session

except ImportError:
    pass
