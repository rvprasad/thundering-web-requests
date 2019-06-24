defmodule PhoenixElixirWeb.RandomController do
  use PhoenixElixirWeb, :controller

  def show(conn, _params) do
    start_time = :erlang.monotonic_time(:microsecond)
    tmp1 = conn.query_params["num"]
    num = if tmp1 == nil, do: 10, else: String.to_integer(tmp1)
    nums = for _ <- 1..num, do: :rand.uniform(999999)
    render conn, "show.json", %{nums: nums, start_time: start_time}
  end
end
