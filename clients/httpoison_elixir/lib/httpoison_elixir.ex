defmodule Client do
  require HTTPoison
  require HTTPoison.Response
  def dispatch_request(url, parent) do
    start = :erlang.monotonic_time(:microsecond)
    result = HTTPoison.get(url)
    elapsed_time =
      (:erlang.monotonic_time(:microsecond) - start) / 1000

    case result do
      {:ok, %HTTPoison.Response{status_code: 200}} ->
            msg = :io_lib.format("~pms OK", [elapsed_time])
            send(parent, {"succ", msg})
      {:ok, %HTTPoison.Response{status_code: s}} ->
            msg = :io_lib.format("~pms REQ_ERR ~p", [elapsed_time, s])
            send(parent, {"fail", msg})
      {:error, %HTTPoison.Error{reason: s}} ->
        msg = :io_lib.format("~pms REQ_ERR ~p", [elapsed_time, s])
        send(parent, {"fail", msg})
    end
  end

  def wait_on_children(num, num_of_succ, num_of_fail) do
    case num do
      0 ->
        :io.format("Success: ~p~n", [num_of_succ])
        :io.format("Failure: ~p~n", [num_of_fail])

      _ ->
        receive do
          {'EXIT', child_pid, {error_code, _}} ->
            :io.format("Child ~p crashed ~p~n", [child_pid, error_code])
            wait_on_children(num - 1, num_of_succ, num_of_fail)

          {verdict, msg} ->
            :io.format("~s~n", [msg])
            case verdict do
              "succ" -> wait_on_children(num - 1, num_of_succ + 1,
                                         num_of_fail)
              "fail" -> wait_on_children(num - 1, num_of_succ,
                                         num_of_fail + 1)
            end
        end
    end
  end

  def process(args) do
    [url, arg2] = args
    num = String.to_integer(arg2)
    parent = self()
    Process.flag(:trap_exit, true)
    for _ <- 1..num do
      spawn_link(fn -> dispatch_request(url, parent) end)
    end
    wait_on_children(num, 0, 0)
  end

  def main(args) do
    process(args)
  end
end
