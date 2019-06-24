defmodule HttpoisonElixir.MixProject do
  use Mix.Project

  def project do
    [
      app: :httpoison_elixir,
      version: "0.1.0",
      elixir: "~> 1.8",
      escript: [main_module: Client],
      start_permanent: Mix.env() == :dev,
      deps: deps()
    ]
  end

  # Run "mix help compile.app" to learn about applications.
  def application do
    [application: [:httpoison_elixir]]
    [extra_applications: [:logger]]
  end

  # Run "mix help deps" to learn about dependencies.
  def deps do
    [{:httpoison, "~> 1.5.1"}]
  end
end
