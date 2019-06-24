defmodule Server do
  use Trot.Router

  get "/random" do
    start = :erlang.monotonic_time(:microsecond)
    tmp1 = conn.query_params["num"]
    num = if tmp1 == nil, do: 10, else: String.to_integer(tmp1)
    nums = for _ <- 1..num, do: :rand.uniform(999999)
    tmp2 = nums |> Enum.map(fn x ->
        "\"" <> String.pad_leading(Integer.to_string(x), 6, "0") <> "\""
      end) |> Enum.join(",")
    ret = "[" <> tmp2 <> "]"
    elapsed_time = (:erlang.monotonic_time(:microsecond) - start) / 1000
    IO.puts(:io_lib.format("~pms", [elapsed_time]))
    ret
  end

  import_routes Trot.NotFound
end
