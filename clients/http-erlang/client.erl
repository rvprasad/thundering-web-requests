% escript client.erl http://127.0.0.1:1234/random?num=5 30

-module(client).
-export([main/1]).

-import(httpc, [request/1]).

dispatch_request(Url, Parent) ->
  Start = erlang:monotonic_time(millisecond),
  {Status, Value} = httpc:request(Url),
  Elapsed_Time = erlang:monotonic_time(millisecond) - Start,
  case Status of
    ok ->
      io:format("~pms OK~n", [Elapsed_Time]),
      Parent ! succ;
    error ->
      io:format("~pms REQ_ERR ~p~n", [Elapsed_Time, element(1, Value)]),
      Parent ! fail
  end.

wait_on_children(0, NumOfSucc, NumOfFail) ->
  io:format("Success: ~p~n", [NumOfSucc]),
  io:format("Failure: ~p~n", [NumOfFail]);
wait_on_children(Num, NumOfSucc, NumOfFail) ->
  receive
    succ -> wait_on_children(Num - 1, NumOfSucc + 1, NumOfFail);
    fail -> wait_on_children(Num - 1, NumOfSucc, NumOfFail + 1)
  end.

main(Args) ->
  inets:start(),
  Url = lists:nth(1, Args),
  Num = list_to_integer(lists:nth(2, Args)),
  Parent = self(),
  [spawn(fun() -> dispatch_request(Url, Parent) end) || _ <- lists:seq(1, Num)],
  wait_on_children(Num, 0, 0).
