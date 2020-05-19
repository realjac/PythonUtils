#!/usr/bin/python3
# _*_ coding:UTF-8 _*_

import functools
import random
import time

import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry


class Request(requests.Session):
    """Request"""

    def __init__(self, max_retries=5, delay_time=1):
        """
        :param proxies: proxy agent
        :param try_time: retry count
        :param timeout: timeout
        """
        # 可以在发生重试时使用回调函数，进行如打日志的操作
        # s.get(url, callback=retry_callback, callback_params=[url])
        # max_retries为网络错误重试次数,使用Retry对象可根据复杂条件重试.如果是response内容解析错误为逻辑问题。
        adapter = HTTPAdapter(max_retries=Retry(total=5, status_forcelist=[500, 502, 503, 504], status=2),
                              pool_maxsize=self.max_workers)
        self.max_retries = max_retries
        self.delay_time = delay_time
        self.max_workers = 20
        super(Request, self).__init__()
        self.mount("http://", adapter)
        self.mount("https://", adapter)

    def __del__(self):
        self.close()

    @staticmethod
    def _retry(max_retries=5, delay_time=1):
        """
        request retry decorator
        :param delay_times:
        :return:
        """
        def wrapper(func):
            @functools.wraps(func)
            def _wrapper(*args, **kwargs):
                _err = None
                for i in range(max_retries):
                    try:
                        _err = None
                        return func(*args, **kwargs)
                    except Exception as e:
                        _err = e
                        if delay_time > 0:
                            time.sleep(delay_time)

                if _err:
                    raise _err

            return _wrapper

        return wrapper

    def proxy(self):
        """
        get proxy
        If there are other agents, change the functimaven_vulDBon here.
        :return: return a ip：http://12.23.88.23:2345
        """
        if not self.proxies:
            one_proxy = None
        elif isinstance(self.proxies, list):
            one_proxy = random.choice(self.proxies)
        else:
            one_proxy = None
        # if one_proxy == None:
        # logging.info("self ip")
        return one_proxy

    @_retry(max_retries=5, delay_time=1)
    def request(self, method, url, response_status="500",
                params=None, data=None, headers=None, cookies=None, files=None,
                auth=None, timeout=None, allow_redirects=True, proxies=None,
                hooks=None, stream=None, verify=None, cert=None, json=None):
        # request(self, method, url,
        #         params=None, data=None, headers=None, cookies=None, files=None,
        #         auth=None, timeout=None, allow_redirects=True, proxies=None,
        #         hooks=None, stream=None, verify=None, cert=None, json=None):
        _err = None
        for try_time in range(self.max_retries):
            try:
                one_proxy_ = self.proxy()
                one_proxy = one_proxy_
                if one_proxy is None:
                    pass
                else:
                    # logging.info("ip-->%s" % one_proxy)
                    one_proxy = {
                        "http" :"%s" %
                                one_proxy,
                        "https":"%s" %
                                one_proxy
                    }
                response = super(Request, self).request(
                        method,
                        url,
                        params=params,
                        data=data,
                        headers=headers,
                        cookies=cookies,
                        files=files,
                        auth=auth,
                        timeout=timeout,
                        allow_redirects=allow_redirects,
                        proxies=one_proxy,
                        hooks=hooks,
                        stream=stream,
                        verify=verify,
                        cert=cert,
                        json=json)
                if str(response.status_code) > response_status:
                    continue
                response.proxy = one_proxy_
                return response
            except Exception as e:
                _err = e
                time.sleep(self.delay_time)
            if _err:
                raise _err
