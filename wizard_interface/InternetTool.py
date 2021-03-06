# coding=utf-8
'''
Created on Mar 31, 2016

@author: yangjie
'''
import http.cookiejar
import json
import logging
import socket
import urllib.request


class HTTPOpener():

    def __init__(self, logger: logging.Logger, enable_cookie: bool=False):
        self.logger = logger
        self.cookie_jar = http.cookiejar.CookieJar()
        self.logger.debug(
            "create HTTPTool:\n\t|enable cookie: %s" % enable_cookie)
        self.opener = self._get_opener(enable_cookie)

    def get_cookie(self):
        return self.cookie_jar

    def _get_opener(self, enable_cookie):
        if enable_cookie:
            pro = urllib.request.HTTPCookieProcessor(self.cookie_jar)
            opener = urllib.request.build_opener(pro)
        else:
            opener = urllib.request.build_opener()
        return opener

    def _data_body_dumps(self, data_raw, encoding, json_type):
        try:
            self.logger.info("start dump body data: %s" % data_raw)
            if data_raw is None:
                self.logger.debug("dump body data: None")
                data_send = data_raw
            elif isinstance(data_raw, str):
                self.logger.debug("dump body data: str")
                data_send = data_raw.encode(encoding)
            elif isinstance(data_raw, dict):
                if json_type:
                    self.logger.debug("dump body data: dict json")
                    data_send = json.dumps(data_raw).encode(encoding)
                else:
                    self.logger.debug("dump body data: dict unjson")
                    data_send = urllib.parse.urlencode(
                        data_raw).encode(encoding)
            else:
                self.logger.error("http request error: unknown type of data")
                return
            self.logger.info("dump body data success: %s" % data_send)
            return data_send
        except Exception as error:
            self.logger.error(error)

    def _data_url_dumps(self, data_raw, encoding, json_type):
        try:
            self.logger.info("start url dump data: %s" % data_raw)
            if data_raw is None:
                self.logger.debug("dump url data: None")
                data_send = data_raw
            elif isinstance(data_raw, str):
                self.logger.debug("dump url data: str")
                data_send = data_raw
            elif isinstance(data_raw, dict):
                if json_type:
                    self.logger.debug("dump url data: dict json")
                    data_send = json.dumps(data_raw).encode(encoding)
                else:
                    self.logger.debug("dump url data: dict unjson")
                    data_send = urllib.parse.urlencode(
                        data_raw)
            else:
                self.logger.error("http request error: unknown type of data")
                return
            self.logger.info("dump url data success: %s" % data_send)
            return data_send
        except Exception as error:
            self.logger.error(error)

    def request_url(self,
                    url_str,
                    data_raw_url=None,
                    data_raw_body=None,
                    encoding="utf-8",
                    method="GET",
                    timeout=5,
                    json_type: bool=False,
                    header: dict={}):
        try:
            self.logger.info("http request start: \
                \n\t|url: %s\
                \n\t|data url: %s\
                \n\t|data body: %s\
                \n\t|encoding: %s\
                \n\t|method: %s\
                \n\t|timeout: %s\
                \n\t|json_type:%s" % (url_str,
                                      data_raw_url,
                                      data_raw_body,
                                      encoding,
                                      method,
                                      timeout,
                                      json_type))
            socket.setdefaulttimeout(timeout)
            if data_raw_body is not None:
                data_send = self._data_body_dumps(
                    data_raw_body, encoding, json_type)
            else:
                data_send = data_raw_body
            if data_raw_url is not None:
                data_url = self._data_url_dumps(
                    data_raw_url, encoding, json_type)
                url_str = url_str + "?" + data_url
            else:
                pass
            if json_type:
                header = {"Content-Type": "application/json"}
            else:
                header = {}
            req = urllib.request.Request(
                url_str, data=data_send, method=method, headers=header)
            self.logger.debug("request body data: %s" % data_send)
            self.logger.debug("request url: %s" % url_str)
            op = self.opener.open(req, timeout=timeout)
            self.logger.info("http request success: \
                        \n\t|url: %s\
                        \n\t|data url: %s\
                        \n\t|data body: %s\
                        \n\t|encoding: %s\
                        \n\t|method: %s\
                        \n\t|timeout: %s\
                        \n\t|json_type:%s\
                        \n\t|http_code:%s" % (url_str,
                                              data_raw_url,
                                              data_raw_body,
                                              encoding,
                                              method,
                                              timeout,
                                              json_type,
                                              op.code))
            return op
        except Exception as error:
            self.logger.error(error)

    def GET(self,
            url_str,
            data_raw_url=None,
            data_raw_body=None,
            encoding="utf-8",
            timeout=5,
            json_type=False,
            header={}):
        res = self.request_url(url_str=url_str,
                               data_raw_url=data_raw_url,
                               data_raw_body=data_raw_body,
                               encoding=encoding,
                               method="GET",
                               timeout=timeout,
                               json_type=json_type,
                               header=header)
        return res

    def POST(self,
             url_str,
             data_raw_url=None,
             data_raw_body=None,
             encoding="utf-8",
             timeout=5,
             json_type=False,
             header={}):
        res = self.request_url(url_str=url_str,
                               data_raw_url=data_raw_url,
                               data_raw_body=data_raw_body,
                               encoding=encoding,
                               method="POST",
                               timeout=timeout,
                               json_type=json_type,
                               header=header)
        return res

    def DELETE(self,
               url_str,
               data_raw_url=None,
               data_raw_body=None,
               encoding="utf-8",
               timeout=5,
               json_type=False,
               header={}):
        res = self.request_url(url_str=url_str,
                               data_raw_url=data_raw_url,
                               data_raw_body=data_raw_body,
                               encoding=encoding,
                               method="DELETE",
                               timeout=timeout,
                               json_type=json_type,
                               header=header)
        return res

    def PATCH(self,
              url_str,
              data_raw_url=None,
              data_raw_body=None,
              encoding="utf-8",
              timeout=5,
              json_type=False,
              header={}):
        res = self.request_url(url_str=url_str,
                               data_raw_url=data_raw_url,
                               data_raw_body=data_raw_body,
                               encoding=encoding,
                               method="PATCH",
                               timeout=timeout,
                               json_type=json_type,
                               header=header)
        return res

    def PUT(self,
            url_str,
            data_raw_url=None,
            data_raw_body=None,
            encoding="utf-8",
            timeout=5,
            json_type=False,
            header={}):
        res = self.request_url(url_str=url_str,
                               data_raw_url=data_raw_url,
                               data_raw_body=data_raw_body,
                               encoding=encoding,
                               method="PUT",
                               timeout=timeout,
                               json_type=json_type,
                               header=header)
        return res
