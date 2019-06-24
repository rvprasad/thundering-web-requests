defmodule PhoenixElixirWeb.RandomView do
  def render("show.json", %{nums: nums, start_time: start_time}) do
    ret = nums |> Enum.map(fn x ->
        String.pad_leading(Integer.to_string(x), 6, "0")
      end)
    elapsed_time = (:erlang.monotonic_time(:microsecond) - start_time) / 1000
    IO.puts(:io_lib.format("~pms", [elapsed_time]))
    ret
  end
end
