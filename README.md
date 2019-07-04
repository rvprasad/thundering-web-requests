# Thundering Web Requests

Implementations of a simple web service and client using different programming languages and technologies.  The purpose of the implementations is to explore the support for web service in different technologies and see how well they handle  thundering web requests.

The web service (`http://127.0.0.1:1234/random`) generates as collection of random numbers as strings.  By default, the service generates a collection of 10 random numbers between 0 to 999,999, both inclusive.  The number of random numbers can be controlled via `num` query parameter, e.g., `http://127.0.0.1:1234/random?num=5`.

The client is a CLI program used to simulate a thundering herd by concurrently (as permitted by the system) issuing *n* HTTP GET requests to a URL.  Both the URL and *n* are specified via the command line.


## Web Client Technologies

1.  [HTTPoison]() ([Elixir](http://www.elixir-lang.org/) v1.8.2)
2.  [Erlang](http://www.erlang.org/) v22.0.1
3.  [Go](https://golang.org/) v1.12.6
4.  [Vert.x](http://vertx.io) v3.7.1 ([Kotlin](http://kotlinlang.org) v1.3.40)


## Web Service Technologies

1.  [Actix-Web](https://actix.rs/) v1.0.0 ([Rust](http://rust-lang.org) v1.35.0)
2.  [Cowboy](http://ninenines.eu) v2.6.3 ([Erlang](http://erlang.org) v22.0.1)
3.  [Cyclone](http://cyclone.io) v1.2 + [Twisted](http://twistedmatrix.com/trac/) v19.2.0 ([Python](http://python.org) v2.7.16)
4.  [Flask](http://flask.pocoo.org) v1.0.3 + [Gunicorn](http://gunicorn.org/) v19.9.0 ([Python](http://python.org) v3.7.3)
5.  [Kemal](http://kemalcr.com) v0.25.2 ([Crystal](http://crystal-lang.org/) v0.28.0)
6.  [Ktor](http://ktor.io) v1.2.2 ([Kotlin](http://kotlinlang.org) v1.3.40)
7.  [Go](https://golang.org/) v1.12.6
8.  [Micronaut](http://micronaut.io) 1.1.3 ([Kotlin](http://kotlinlang.org) v1.3.40)

9.  [NodeJS](http://nodejs.org) v10.16 (JavaScript)
10.  [NodeJS](http://nodejs.org) v10.16 + [Express](http://expressjs.com) v4.17.1 (JavaScript)
11. [Phoenix](https://phoenixframework.orgt) v1.4.0 ([Elixir](http://www.elixir-lang.org/) v1.8.2)
12. [Ratpack](http://ratpack.io) v1.6.1 ([Kotlin](http://kotlinlang.org) v1.3.40)
13. [Tornado](http://www.tornadoweb.org) v6.0.2 ([Python](http://python.org) v3.7.3)
14. [Trot](https://github.com/hexedpackets/trot) v0.7.0 ([Elixir](http://www.elixir-lang.org/) v1.8.2)
15. [Vert.x](http://vertx.io) v3.7.1 ([Kotlin](http://kotlinlang.org) v1.3.40)
16. [Yaws](http://yaws.hyber.org/) v2.0.6 ([Erlang](http://erlang.org) v22.0.1)


## Notes

The implementations was created for a very specific purpose -- experimentation.  So, they are intentionally light on use of good software engineering practices.  Specifically,
-   there are no automated tests.  Servers were manually tested using `curl` and `ab`.  Clients were tested against the servers with debug print statements.
-   minimal error checking is done in conjunction with internal logic.
-   *n* provided as part of the URL is assumed to be a valid positive integer and is not checked for validity.

That said, suggestions to improve other aspects of the implementations are welcome.  Also, implementations covering other HTTP-based microservice-related operations as well as other languages/technologies are welcome.


## Attribution

Copyright (c) 2019, Venkatesh-Prasad Ranganath

Licensed under [BSD 3-clause "New" or "Revised" License](https://choosealicense.com/licenses/bsd-3-clause/)

**Authors:** Venkatesh-Prasad Ranganath
