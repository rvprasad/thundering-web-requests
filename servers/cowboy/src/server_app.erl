-module(server_app).
-behaviour(application).

-export([start/2]).
-export([stop/1]).

start(_Type, _Args) ->
	Dispatch = cowboy_router:compile([
		{'_', [
			{"/random", random_handler, []}
		]}
	]),
	{ok, _} = cowboy:start_clear(my_http_listener,
		[{ip, {0, 0, 0, 0}}, {port, 1234}],
		#{env => #{dispatch => Dispatch}}
	),
	server_sup:start_link().

stop(_State) ->
	ok.
