#!/usr/bin/python
# -*- coding: utf8 -*-

from __future__ import print_function

import unittest

from stormer import Requester


class TestClient(unittest.TestCase):
    def test_get_server(self):
        # init Requester instance
        requester = Requester(
            server_url="https://www.baidu.com",
            # redis_url="redis://127.0.0.1:6379/0",
            # timeout=30,  # in seconds
            # headers={"Content-Type": "text/html;charset=utf8"},
            encoding='utf8'
        )

        # open debug
        requester.set_debugging()

        # register request function
        requester.register(
            action="get",
            func="bd_index",
            uri="/"
        )

        # execute function
        rlt = requester.bd_index()
        # print(rlt.data)
        print(rlt.resp)

        self.assertEqual(rlt.status_code, 200)


if __name__ == '__main__':
    unittest.main()
