# Thundering Web Herd

Implementations of clients and web services to measure performance of different technologies that can enable web services.

The web service generates as collection of random numbers, i.e., `http://127.0.0.1:1234/random`.  By default, it generates a collection of 10 random numbers between 0 to 1e6, both inclusive.  The number of random numbers provided can be changed via `num` arguments, i.e., `http://127.0.0.1:1234/random?num=5`.

The client is a CLI program that simulates a thundering herd by issuing `n` concurrent HTTP GET requests to a URL.  Both the URL and n are specified via the command line.


## Client Technologies

1.  Go v1.12.5
2.  Erlang 22.0.1

## Server Technologies

1.  Cowboy v2.0 (Erlang)
2.  Cyclone v1.2 (Python v2.7.16)
3.  Ktor v1.2 (Kotlin)
4.  NodeJS v10.15.3 (JavaScript)
5.  Ratpack v1.6.1 (Kotlin)
6.  Tornado v6.0.2 (Python3)
7.  Vert.x v3.7.0 (Kotlin)


## Attribution

Copyright (c) 2019, Venkatesh-Prasad Ranganath

Licensed under [BSD 3-clause "New" or "Revised" License](https://choosealicense.com/licenses/bsd-3-clause/)

**Authors:** Venkatesh-Prasad Ranganath
