defmodule PhoenixElixirWeb.Router do
  use PhoenixElixirWeb, :router

  pipeline :api do
    plug :accepts, ["json"]
  end

  scope "/", PhoenixElixirWeb do
    pipe_through :api
    get "/random", RandomController, :show
  end
end
