-module(random_handler).
-behavior(cowboy_handler).

-export([init/2]).

get_random() -> rand:uniform(999999).

random_generator(0, List) -> List;
random_generator(N, List) -> random_generator(N - 1, List ++ [get_random()]).

to_string(X) -> io_lib:format("~6..0B", [X]).

init(Request=#{method := <<"GET">>}, State) ->
  Start = erlang:monotonic_time(microsecond),
	#{num := Num} = cowboy_req:match_qs([{num, int, 10}], Request),
  RandomNums = random_generator(Num, []),
  Ret = "[" ++ string:join(lists:map(fun to_string/1, RandomNums), ",") ++ "]",
  Reply = cowboy_req:reply(200,
    #{<<"content-type">> => <<"text/plain">>}, Ret, Request),
  Elapsed_Time = (erlang:monotonic_time(microsecond) - Start) / 1000,
	io:fwrite("~pms~n", [Elapsed_Time]),
	{ok, Reply, State}.
