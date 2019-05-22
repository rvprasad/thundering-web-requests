% escript client.erl http://127.0.0.1:1234/random?num=5 30

-module(client).
-export([main/1]).

-import(httpc, [request/1]).

dispatch_request(Url, Parent) ->
  Start = erlang:monotonic_time(millisecond),
  {Status, _} = httpc:request(Url),
  Suffix =
    case Status of
      ok -> 'OK';
      error -> 'ERR'
    end,
  io:format("~pms ~s~n",
    [(erlang:monotonic_time(millisecond) - Start), Suffix]),
  Parent ! done.

wait_on_children(0) -> return;
wait_on_children(Num) ->
  receive
    done -> wait_on_children(Num - 1)
  end.

main(Args) ->
  inets:start(),
  Url = lists:nth(1, Args),
  Num = list_to_integer(lists:nth(2, Args)),
  Parent = self(),
  [spawn(fun() -> dispatch_request(Url, Parent) end) || _ <- lists:seq(1, Num)],
  wait_on_children(Num).
