# Thundering Web Requests

Implementations of simple web services and clients using different programming languages and technologies.  The purpose of the implementations is to see how different web serving technologies fare in the face of thundering web requests.

The web service generates as collection of random numbers as strings -- `http://127.0.0.1:1234/random`.  By default, the service generates a collection of 10 random numbers between 0 to 999,999, both inclusive.  The number of random numbers can be controlled via `num` query parameter, i.e., `http://127.0.0.1:1234/random?num=5`.

The client is a CLI program used to simulate a thundering herd by concurrently (as permitted by the system) issuing *n* HTTP GET requests to a URL.  Both the URL and *n* are specified via the command line.


## Client Technologies

1.  [Erlang](http://www.erlang.org/) v22.0.1
2.  [Go](https://golang.org/) v1.12.5
3.  [Vert.x](http://vertx.io) v3.7.0 ([Kotlin](http://kotlinlang.org) v1.3.31)


## Server Technologies

1.  [Actix](https://actix.rs/) v0.7 ([Rust](http://rust-lang.org) v1.35.0)
2.  [Cowboy](http://ninenines.eu) v2.6.3 ([Erlang](http://erlang.org) v22.0.1)
3.  [Cyclone](http://cyclone.io) v1.2 + [Twisted](http://twistedmatrix.com/trac/) v19.2.0 ([PyPy](http://pypy.org) v2.7.13)
4.  [Flask](http://flask.pocoo.org) v1.0.3 + [Gunicorn](http://gunicorn.org/) v19.9.0 ([Python](http://python.org) v3.7.3)
5.  [Kemal](http://kemalcr.com) v0.25.2 ([Crystal](http://crystal-lang.org/) v0.28.0)
6.  [Ktor](http://ktor.io) v1.2 ([Kotlin](http://kotlinlang.org) v1.3.31)
7.  [Go](https://golang.org/) v1.12.5
8.  [NodeJS](http://nodejs.org) v10.15.3 (JavaScript)
9.  [NodeJS](http://nodejs.org) v10.15.3 + [Express](http://expressjs.com) v4.17.1 (JavaScript)
10. [Ratpack](http://ratpack.io) v1.6.1 ([Kotlin](http://kotlinlang.org) v1.3.31)
11. [Tornado](http://www.tornadoweb.org) v6.0.2 ([Python](http://python.org) v3.7.3)
12. [Vert.x](http://vertx.io) v3.7.0 ([Kotlin](http://kotlinlang.org) v1.3.31)
13. [Yaws](http://yaws.hyber.org/) v2.0.6 ([Erlang](http://erlang.org) v22.0.1)


## Notes

The implementations was created for a very specific purpose.  So, they are intentionally light on use of good software engineering practices.  Specifically,
- there are no automated tests.  `curl` and `ab` were used to manually test the servers and the clients were tested against the servers with debug print statements.
- minimal error checking is done in conjunction with internal logic.
- user-input are not checked for errors.

That said, suggestions to improve other aspects of the implementations are welcome.  Also, implementations covering other HTTP-based microservice-related operations as well as other languages/technologies are welcome.


## Attribution

Copyright (c) 2019, Venkatesh-Prasad Ranganath

Licensed under [BSD 3-clause "New" or "Revised" License](https://choosealicense.com/licenses/bsd-3-clause/)

**Authors:** Venkatesh-Prasad Ranganath
