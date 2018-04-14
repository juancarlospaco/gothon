#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Gothon.

Gothon runs GO Code from Python using IPC RPC JSON (non-HTTP) & subprocess."""


import json
import subprocess
import os
import signal

from itertools import count
from pathlib import Path
from shutil import which
from socket import create_connection as make_conect
from time import sleep


__all__ = ("Gothon", )


class RPCJSONClient(object):

    """RPC-JSON Client (non-HTTP)."""

    __slots__ = ("adres", "codec", "recv", "_soket", "_id", "_codec", "close")

    def __init__(self, adres=("127.0.0.1", 5090), codec=json, recv=4096):
        self._soket, self._id, self._codec = make_conect(adres), count(), codec
        self.close, self.recv = self.__exit__, recv

    def _message(self, name, *params):
        return {"id": next(self._id), "params": tuple(params), "method": name}

    def call(self, name, *params):
        request = self._message(name, *params)
        _id = request.get('id')
        self._soket.sendall(bytes(self._codec.dumps(request), "utf-8"))
        while True:
            try:
                response = self._codec.loads(self._soket.recv(self.recv)).get
            except Exception:
                sleep(0.1)
            else:
                break
        if response('id') != _id:
            raise Exception(f"Expected ID={_id},received ID={response('id')}.")
        if response('error') is not None:
            raise Exception(f"{self.__class__.__name__}: {response('error')}.")
        return response('result')

    def __exit__(self, *args, **kwargs):
        self._soket.close()
        del self._soket, self._id, self._codec, self.recv


class Gothon(object):

    """Gothon runs GO Code from Python using IPC RPC JSON (non-HTTP)."""

    __slots__ = ("go_file", "startup_delay", "go", "rpc", "proces",
                 "close", "stop", "kill")

    def __init__(self, go_file: str=Path(__file__).parent / "python_module.go",
                 startup_delay: float=0.1):
        self.go_file, self.startup_delay = Path(go_file), float(startup_delay)
        self.go, self.rpc, self.proces = which("go"), None, None
        self.close = self.stop = self.kill = self.terminate = self.__exit__
        if self.go and self.go_file.is_file():
            self._build()

    def _build(self):
        self.proces = subprocess.Popen(  # stackoverflow.com/a/4791612
            f"{self.go} run {self.go_file}", stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, shell=True, preexec_fn=os.setpgrp)

    def start(self):
        self.rpc = RPCJSONClient()
        sleep(self.startup_delay)
        return self.rpc

    def __exit__(self, *args, **kwargs):
        self.rpc._soket.close()
        self.proces.kill()
        os.killpg(os.getpgid(self.proces.pid), signal.SIGTERM)
