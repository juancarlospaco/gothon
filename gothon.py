#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Gothon.

Gothon runs GO Code from Python using IPC RPC JSON (non-HTTP) & subprocess."""


import json
import os
import signal
import socket
import subprocess

from glob import iglob
from itertools import count
from pathlib import Path
from shutil import which
from time import sleep
from uuid import uuid4


__version__ = "1.0.0"
__all__ = ("Gothon", )


PYTHON_MODULE_GO_TEMPLATE = """
package main

import (
	"log"
	"net"
	"net/rpc"
	"net/rpc/jsonrpc"
	"os"
)

// Define Functions here.
type Echo int

func (h *Echo) Echo(arg *string, reply *string) error {
	log.Println("received: ", *arg)
	*reply = *arg
	return nil
}

func main() {
	// Register Functions on the RPC here.
	hello := new(Echo)
	rpc.Register(hello)

	listener, errors := net.Listen("unix", os.Args[1])
	defer listener.Close()

	if errors != nil {
		log.Fatal(errors)
	}

	log.Print("Listening for RPC-JSON connections: ", listener.Addr())

	for {
		log.Print("Waiting for RPC-JSON connections...")
		conection, errors := listener.Accept()

		if errors != nil {
			log.Printf("Accept error: %s", conection)
			continue
		}

		log.Printf("Connection started: %v", conection.RemoteAddr())
		go jsonrpc.ServeConn(conection)
	}
}
"""


class RPCJSONClient(object):

    """RPC JSON Client (non-HTTP)."""

    __slots__ = ("socket_file", "_id", "socket")

    def __init__(self, socket_file):
        self.socket_file = socket_file
        self._id = count()
        self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.socket.connect(self.socket_file)

    def call(self, name, *params):
        """RPC IPC Call to a Go function, return results or raise error."""
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

        response, _id = json_response.get, mssg.get('id')
        if response('id') != _id:
            raise Exception(f"Expected ID={_id},received ID={response('id')}.")
        elif response('error') is not None:
            raise Exception(f"{self.__class__.__name__}: {response('error')}.")
        print(f"Received: {response('result')}")
        return response('result')

    def __exit__(self, *args, **kwargs):
        self.socket.close()


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
        """Run Go code using 'go run' passing the Unix Socket as argument. """
        self.proces = subprocess.Popen(  # stackoverflow.com/a/4791612
            f"{self.go} run {self.go_file} {self.socket_file}",
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            shell=True, preexec_fn=os.setpgrp)

    def start(self) -> RPCJSONClient:
        """Start the RPC IPC Python Client side."""
        self.rpc = RPCJSONClient(self.socket_file)
        sleep(self.startup_delay)
        return self.rpc

    @staticmethod
    def clean():
        """Simple helper function to clean stale unused Unix Socket files."""
        for file2clean in iglob("/tmp/gothon-*.sock"):
            print(f"Deleted old stale unused Unix Socket file: {file2clean}")
            Path(file2clean).unlink()

    @staticmethod
    def template():
        """Helper function to print a Go code Template to start hacking into."""
        print(PYTHON_MODULE_GO_TEMPLATE)

    def __exit__(self, *args, **kwargs):
        self.rpc.socket.close()
        self.proces.kill()
        os.killpg(os.getpgid(self.proces.pid), signal.SIGTERM)
