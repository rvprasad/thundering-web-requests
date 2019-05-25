-module(random_handler).
-behavior(cowboy_handler).

-export([init/2]).

get_random() -> rand:uniform(1000000).

random_generator(0, List) -> List;
random_generator(N, List) -> random_generator(N - 1, List ++ [get_random()]).

init(Request=#{method := <<"GET">>}, State) ->
  Start = erlang:monotonic_time(microsecond),
	#{num := Num} = cowboy_req:match_qs([{num, int, 10}], Request),
  Reply = cowboy_req:reply(200,
    #{<<"content-type">> => <<"text/plain">>},
    io_lib:format("~p", [random_generator(Num, [])]),
    Request),
  Elapsed_Time = (erlang:monotonic_time(microsecond) - Start) / 1000,
	io:format("~pms~n", [Elapsed_Time]),
	{ok, Reply, State}.
