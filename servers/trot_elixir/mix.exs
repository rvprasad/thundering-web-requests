defmodule HttpoisonElixir.MixProject do
  use Mix.Project

  def project do
    [
      app: :trot_elixir,
      version: "0.1.0",
      elixir: "~> 1.8",
      escript: [main_module: Server],
      start_permanent: Mix.env() == :prod,
      deps: deps()
    ]
  end

  # Run "mix help compile.app" to learn about applications.
  def application do
    [application: [:trot_elixir, :trot]]
  end

  # Run "mix help deps" to learn about dependencies.
  def deps do
    [
      {:trot, github: "hexedpackets/trot", tag: "v0.7.0"},
      {:plug_cowboy, "~> 1.0"}
    ]
  end
end
