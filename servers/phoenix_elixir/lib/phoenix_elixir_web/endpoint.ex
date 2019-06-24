defmodule PhoenixElixirWeb.Endpoint do
  use Phoenix.Endpoint, otp_app: :phoenix_elixir

  plug Plug.Parsers,
    parsers: [:urlencoded, :multipart, :json],
    pass: ["*/*"],
    json_decoder: Phoenix.json_library()

  plug PhoenixElixirWeb.Router
end
