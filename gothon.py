#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Gothon.

Gothon runs GO Code from Python using IPC RPC JSON (non-HTTP) & subprocess."""


import json
import os
import signal
import socket
import subprocess

from itertools import count
from pathlib import Path
from shutil import which
from time import sleep
from uuid import uuid4


__all__ = ("Gothon", )


class RPCJSONClient(object):

    """RPC JSON Client (non-HTTP)."""

    __slots__ = ("socket_file", "_id", "socket")

    def __init__(self, socket_file, codec):
        self.socket_file = socket_file
        self._id = count()
        self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.socket.connect(self.socket_file)

    def call(self, name, *params):
        mssg = {"id": next(self._id), "params": tuple(params), "method": name}
        data = bytes(json.dumps(mssg, separators=(",", ":")), "utf-8")
        self.socket.sendall(data)
        print(f"Sent:     {data}")

        while True:
            try:
                json_response = json.loads(self.socket.recv(8192))
                if not json_response:
                    break
            except Exception:
                sleep(0.1)
            else:
                break

        response = json_response.get
        if response('id') != mssg.get('id'):
            raise Exception(f"Expected ID={_id},received ID={response('id')}.")
        elif response('error') is not None:
            raise Exception(f"{self.__class__.__name__}: {response('error')}.")
        print(f"Received: {response('result')}")
        return response('result')

    def __exit__(self, *args, **kwargs):
        self._soket.close()


class Gothon(object):

    """Gothon runs GO Code from Python using IPC RPC JSON (non-HTTP)."""

    __slots__ = ("go_file", "startup_delay", "go", "rpc", "proces",
                 "close", "stop", "kill", "terminate", "socket_file")

    def __init__(self, go_file: str=Path(__file__).parent / "python_module.go",
                 startup_delay: float=0.1):
        self.close = self.stop = self.kill = self.terminate = self.__exit__
        self.socket_file = f"/tmp/gothon-{uuid4().hex}.sock"
        self.startup_delay = float(startup_delay)
        self.go_file = Path(go_file)
        self.go = which("go")
        self.rpc, self.proces = None, None
        if self.go and self.go_file.is_file():
            self._build()
        print(f"PID: {self.proces.pid}, Socket: {self.socket_file}")

    def _build(self):
        self.proces = subprocess.Popen(  # stackoverflow.com/a/4791612
            f"{self.go} run {self.go_file} {self.socket_file}",
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            shell=True, preexec_fn=os.setpgrp)

    def start(self) -> RPCJSONClient:
        self.rpc = RPCJSONClient(self.socket_file)
        sleep(self.startup_delay)
        return self.rpc

    def __exit__(self, *args, **kwargs):
        self.rpc._soket.close()
        self.proces.kill()
        os.killpg(os.getpgid(self.proces.pid), signal.SIGTERM)
