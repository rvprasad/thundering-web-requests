% escript client.erl http://127.0.0.1:1234/random?num=5 30

-module(client).
-export([main/1]).

-import(httpc, [request/1]).

-mode(compile).

dispatch_request(Url, Parent) ->
  Start = erlang:monotonic_time(microsecond),
  {Status, Value} = httpc:request(get, {Url, []}, [{timeout, 60000}], []),
  Elapsed_Time = (erlang:monotonic_time(microsecond) - Start) / 1000,
  Msg = case Status of
    ok ->
      io_lib:format("~pms OK", [Elapsed_Time]);
    error ->
      io_lib:format("~pms REQ_ERR ~p", [Elapsed_Time, element(1, Value)])
  end,
  Parent ! {Status, Msg}.

wait_on_children(0, NumOfSucc, NumOfFail) ->
  io:format("Success: ~p~n", [NumOfSucc]),
  io:format("Failure: ~p~n", [NumOfFail]);
wait_on_children(Num, NumOfSucc, NumOfFail) ->
  receive
    {'EXIT', ChildPid, {ErrorCode, _}} ->
      io:format("Child ~p crashed ~p~n", [ChildPid, ErrorCode]),
      wait_on_children(Num - 1, NumOfSucc, NumOfFail);
    {Verdict, Msg} ->
      io:format("~s~n", [Msg]),
      case Verdict of
        ok -> wait_on_children(Num - 1, NumOfSucc + 1, NumOfFail);
        error -> wait_on_children(Num - 1, NumOfSucc, NumOfFail + 1)
      end
  end.

main(Args) ->
  inets:start(),
  Url = lists:nth(1, Args),
  Num = list_to_integer(lists:nth(2, Args)),
  Parent = self(),
  process_flag(trap_exit, true),
  [spawn_link(fun() -> dispatch_request(Url, Parent) end) ||
    _ <- lists:seq(1, Num)],
  wait_on_children(Num, 0, 0).
