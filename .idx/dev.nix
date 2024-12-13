# To learn more about how to use Nix to configure your environment
# see: https://developers.google.com/idx/guides/customize-idx-env
{ pkgs, ... }: {
  # Which nixpkgs channel to use.
  channel = "stable-24.05"; # or "unstable"

  # Use https://search.nixos.org/packages to find packages
  packages = [
    pkgs.python312
  ];

env = {
    UV_HOME = "$HOME/.local/bin:$PATH";
  };

  idx = {

    extensions = [
      "ms-toolsai.jupyter"
      "ms-python.python"
    ];

    workspace = {
      onCreate = {
        create-venv = ''
        curl -LsSf https://astral.sh/uv/install.sh | sh
        uv sync --reinstall
        source .venv/bin/activate
        '';
      };
    };
  };
}
