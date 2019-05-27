# Thundering Web Herd

Implementations of clients and web services to measure performance of different technologies that can enable web services.

The web service generates as collection of random numbers as strings, i.e., `http://127.0.0.1:1234/random`.  By default, it generates a collection of 10 random numbers between 0 to 999,999, both inclusive.  The number of random numbers provided can be changed via `num` arguments, i.e., `http://127.0.0.1:1234/random?num=5`.

The client is a CLI program that simulates a thundering herd by issuing *n* concurrent HTTP GET requests to a URL.  Both the URL and *n* are specified via the command line.


## Client Technologies

1.  [Go](https://golang.org/) v1.12.5
2.  [Erlang](http://www.erlang.org/) v22.0.1


## Server Technologies

1.  [Cowboy](http://ninenines.eu) v2.6.3 ([Erlang](http://erlang.org) v22.0.1)
2.  [Cyclone](http://cyclone.io) v1.2 ([Python](http://python.org) v2.7.16)
3.  [Flask](http://flask.pocoo.org) v1.0.3 + [Gunicorn](http://gunicorn.org/) v19.9.0 ([Python](http://python.org) v3.7.3)
4.  [Iron](http://ironframework.io) v0.6.0 ([Rust](http://rust-lang.org) v1.35.0)
5.  [Ktor](http://ktor.io) v1.2 ([Kotlin](http://kotlinlang.org) v1.3.31)
6.  [NodeJS](http://nodejs.org) v10.15.3 (JavaScript)
7.  [Ratpack](http://ratpack.io) v1.6.1 ([Kotlin](http://kotlinlang.org) v1.3.31)
8.  [Tornado](http://www.tornadoweb.org) v6.0.2 ([Python](http://python.org) v3.7.3)
9.  [Vert.x](http://vertx.io) v3.7.0 ([Kotlin](http://kotlinlang.org) v1.3.31)


## Attribution

Copyright (c) 2019, Venkatesh-Prasad Ranganath

Licensed under [BSD 3-clause "New" or "Revised" License](https://choosealicense.com/licenses/bsd-3-clause/)

**Authors:** Venkatesh-Prasad Ranganath
