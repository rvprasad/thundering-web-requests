-module(random_handler).
-behavior(cowboy_handler).

-export([init/2]).

get_random() -> rand:uniform(1000000).

random_generator(0, List) -> List;
random_generator(N, List) -> random_generator(N - 1, List ++ [get_random()]).

init(Req0=#{method := <<"GET">>}, State) ->
  Start = erlang:monotonic_time(microsecond),
	#{num := Num} = cowboy_req:match_qs([{num, int, 10}], Req0),
  Req = cowboy_req:reply(200,
    #{<<"content-type">> => <<"text/plain">>},
    io_lib:format("~p", [random_generator(Num, [])]),
    Req0),
  Elapsed_Time = (erlang:monotonic_time(microsecond) - Start) / 1000,
	io:format("~pms~n", [Elapsed_Time]),
	{ok, Req, State}.
