# Gothon

Python 3 modules written on pure Go. No CFFI, no CTypes, no CGo, no PyBindGen, just import `*.go` files from Python.

Open Repo access to anyone who want to contribute, just contact me.
It works using IPC RPC. Inspired by Cythons `pyximport`.

**This is a Work In Progress.**


# Why

Things that Ive tried and didnt work (2018, Linux):

- https://blog.filippo.io/building-python-modules-with-go-1-5/ (Go 1.5 only)
- https://github.com/go-python/gopy/issues/83 (Python 2 only)
- https://github.com/go-python/gopy/blob/master/gen.go#L81 (Python 2 only)
- https://github.com/sbinet/go-python (Python 2 only)
- https://dustymabe.com/2016/09/13/sharing-a-go-library-to-python-using-cffi/ (Compiler Errors on embebed obfuscated C)
- http://pybindgen.readthedocs.io/en/latest/tutorial/#supported-python-versions (Compiler Errors on obfuscated C)
- https://hackernoon.com/extending-python-3-in-go-78f3a69552ac (All of the above)
- Other solutions call Python from Go, the reverse of Gothon.
- Others I dont remember the links.


# Use

```python
$ ls
gothon.py  python_module.go

$ python
Python 3.6.4 (default, Jan  5 2018, 02:35:40)

>>> import gothon
>>> unemployed = gothon.Gothon()
>>> worker = unemployed.start()
>>> worker.call("Echo.Echo", "Hello from Python to Go")
'Hello from Python to Go'
>>>
```


# Documentation

<details>
    <summary><b>gothon.py</b></summary>

**Description:**
Gothon runs GO Code from Python using IPC RPC JSON (non-HTTP) and subprocess.
Unix Socket are used because from benchmarks it performs 3x faster than TCP/UDP Sockets.

**Arguments:**
- `go_file` A GO file to compile and run as a python module, string type, defaults to `python_module.go`, required.
- `startup_delay` A startup delay, after running the go file but before returning the RPC client to Python, float type, defaults to `0.1`, optional.

**Keyword Arguments:** None.

**Returns:** `gothon.RPCJSONClient()` an custom IPC RPC.

**Base Class:** `object`.

**Type:** `object`.

**Source Code file:** https://github.com/juancarlospaco/gothon/blob/master/gothon.py

| State              | OS          | Description |
| ------------------ |:-----------:| -----------:|
| :white_check_mark: | **Linux**   | Works Ok    |
| :white_check_mark: | **Os X**    | Works Ok    |

**Usage Example:**

```python
>>> import gothon
>>> unemployed = gothon.Gothon()
>>> worker = unemployed.start()
>>> worker.call("Echo.Echo", "Hello from Python to Go")
'Hello from Python to Go'
>>> worker.stop()
>>>
```

</details>

<details>
    <summary><b>python_module.go</b></summary>

**Description:** GO source code with functions that must be registered on an IPC RPC.
This file is pure Go source, check Go Documentation for more info.

**Arguments:** None.

**Keyword Arguments:** None from Python.

**Returns:** None from Python.

**Base Class:** None from Python.

**Type:** None from Python.

**Source Code file:** https://github.com/juancarlospaco/gothon/blob/master/python_module.go

**Usage Example:** None from Python. Can NOT be used directly from Python or from itself.

</details>


# Requisites

- [Python 3.6+](https://python.org)
- [Go 1.10+](https://golang.org)


### Contributors

- **Please Star this Repo on Github !**, it helps to show up faster on searchs.
- [Help](https://help.github.com/articles/using-pull-requests) and more [Help](https://help.github.com/articles/fork-a-repo) and Interactive Quick [Git Tutorial](https://try.github.io).
- English is the primary default spoken language, unless explicitly stated otherwise *(eg. Dont send Translation Pull Request)*
- Pull Requests for working passing unittests welcomed.


### Licence

- BSD.


### Ethics and Humanism Policy

- Religions is not allowed. Contributing means you agree with the COC.
