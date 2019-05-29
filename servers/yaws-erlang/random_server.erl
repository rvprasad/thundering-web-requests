-module(random_server).

-export([out/1]).

get_random() -> rand:uniform(999999).

random_generator(0, List) -> List;
random_generator(N, List) -> random_generator(N - 1, List ++ [get_random()]).

to_string(X) -> io_lib:format("\"~6..0B\"", [X]).

out(Req) ->
  Start = erlang:monotonic_time(microsecond),
  Num = case yaws_api:queryvar(Req, "num") of
    {ok, Val} -> list_to_integer(Val);
    _ -> 10
  end,
  RandomNums = random_generator(Num, []),
  Reply = "[" ++ string:join(lists:map(fun to_string/1, RandomNums), ",")
    ++ "]",
  Elapsed_Time = (erlang:monotonic_time(microsecond) - Start) / 1000,
	io:fwrite("~pms~n", [Elapsed_Time]),
	{html, Reply}.
