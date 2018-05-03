# Gothon

Python 3 modules written on pure Go. No CFFI, no CTypes, no CGo, no PyBindGen, just import `*.go` files from Python.

##### I stoped this project, [I changed Go for NIM that uses Python syntax, is faster, smaller binaries, compiles to C and JS.](https://nim-lang.org)

It works using RPC. Inspired by [Cythons `pyximport`](http://cython.readthedocs.io/en/latest/src/tutorial/cython_tutorial.html?highlight=pyximport#pyximport-cython-compilation-for-developers) and [CPPImport](https://github.com/tbenthompson/cppimport#import-c-or-c-files-directly-from-python). Designed to speed up Python using Go. [![Build Status](https://travis-ci.org/juancarlospaco/gothon.svg?branch=master)](https://travis-ci.org/juancarlospaco/gothon)

Open Repo access to anyone who want to contribute, just contact me.

![screenshot](https://source.unsplash.com/FqkBXo2Nkq0/850x420 "Illustrative Photo by https://unsplash.com/@stickermule")


# Use

```python
$ ls
gothon.py  python_module.go

$ python
Python 3.6.4 (default, Jan  5 2018, 02:35:40)

>>> import gothon                   # Import & enable Gothon.
>>> gothon.import_hook()
>>> import python_module            # Import *.go files.
>>> repr(python_module)
'<Gothon object 140066220608272 from python_module.go>'
>>> python_module.__doc__
'Gothon runs GO Code from Python using IPC RPC JSON.'
>>> worker = python_module.start()
>>> worker.call("Echo.Echo", "Hello from Python to Go")
'Hello from Python to Go'
>>>
```
- [The Echo Function is written in Go.](https://github.com/juancarlospaco/gothon/blob/master/python_module.go#L14-L18)


# Install

```
pip install gothon
```
- No dependencies, it does not install any Python dependency nor Go dependency.
- Uninstall `pip uninstall gothon`


# Documentation

<details>
    <summary><b>gothon.Gothon()</b></summary>

**Description:**
Gothon runs GO Code from Python using IPC RPC JSON.

Delegates the Parse, Compile, Build and Cache to Go itself.

If you Upgrade your Go version you dont have to change anything on Gothon, it just works.

If you Upgrade your Python version you dont have to change anything on Gothon, it just works.

Unix Socket are used because from benchmarks it performs 3x faster than TCP/UDP Sockets.

This does not connect to the network, nor internet, nor use HTTP.

This project is oriented to Developers, NOT end-users.

This project can be used with Fades, FireJails, Docker, RKT.

This project assumes at least very basic knowledge of the Go programming language.

Its recommended to have 1 `*.go` file importable from Python for project or package,
the `*.go` file itself can import Go functions from other `*.go` files using Go way of importing stuff.

Feel free to contact us if you need help integrating it on your project.

**Arguments:**
- `go_file` A GO file to compile and run as a python module, `str` or `pathlib.Path` type, defaults to `python_module.go`, required.
- `startup_delay` A startup delay, after building the go file but before returning the IPC RPC to Python, float type, defaults to `0.1`, can be set to `0.0` too, can not be `None`, optional.

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
>>> from gothon import Gothon
>>> unemployed = Gothon()
>>> worker = unemployed.start()
>>> worker.call("Echo.Echo", "Hello from Python to Go")
'Hello from Python to Go'
>>> worker.stop()
>>>
```

**Helper Static Methods:**

- `gothon.Gothon().template()`

Prints to standard output a Go source code template to start hacking into,
with all bits and pieces to write a Python module using Go,
it has 1 "Echo" function that you can overwrite or delete,
this Go source code is ready to run as-is.

- `gothon.Gothon().clean()`

Clean up the Cache, uses `glob.iglob()` and `pathlib.Path().unlink()`, its very fast.

</details>


# Requisites

- [Python 3.6+](https://python.org)
- [Go 1.10+](https://golang.org)


##### Troubleshoot

<details>
    <summary>Not working</summary>

- Delete all `__pycache__` and `*.pyc`.
- Execute `go clean -x -cache` (Usually Go takes care of cleaning Cache automatically).
- Update your Go to the latest version.
</details>


# Why

Things that Ive tried and didnt work (2018, Linux):

- https://blog.filippo.io/building-python-modules-with-go-1-5/ (Go 1.5 only)
- https://github.com/go-python/gopy/issues/83 (Python 2 only)
- https://github.com/go-python/gopy/blob/master/gen.go#L81 (Python 2 only)
- https://github.com/sbinet/go-python (Python 2 only)
- https://dustymabe.com/2016/09/13/sharing-a-go-library-to-python-using-cffi/ (Compiler Errors on embebed obfuscated C)
- http://pybindgen.readthedocs.io/en/latest/tutorial/#supported-python-versions (Compiler Errors on obfuscated C)
- https://hackernoon.com/extending-python-3-in-go-78f3a69552ac (All of the above)
- https://medium.com/learning-the-go-programming-language/calling-go-functions-from-other-languages-4c7d8bcc69bf (Go 1.5 only)
- Other solutions call Python from Go, the reverse of Gothon.
- Others I dont remember the links. No [KISS](https://en.wikipedia.org/wiki/KISS_principle) solution. Both languages have simplicity but other solutions have error prone complexity, while this may not be ideal, I feel is better than manual C glue code or inlined C embebed CFFI hacks.


### Contributors

- **This project welcomes all Python and Go developers.**
- **Please Star this Repo on Github !**, it helps to show up faster on searchs.
- [Help](https://help.github.com/articles/using-pull-requests) and more [Help](https://help.github.com/articles/fork-a-repo) and Interactive Quick [Git Tutorial](https://try.github.io).
- English is the primary default spoken language, unless explicitly stated otherwise *(eg. Dont send Translation Pull Request)*
- Pull Requests for working passing unittests welcomed.


### Licence

- BSD.


### Ethics and Humanism Policy

- Religions is not allowed. Contributing means you agree with the COC.
