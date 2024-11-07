# To learn more about how to use Nix to configure your environment
# see: https://developers.google.com/idx/guides/customize-idx-env
{ pkgs, ... }: {
  # Which nixpkgs channel to use.
  channel = "stable-24.05"; # or "unstable"

  # Use https://search.nixos.org/packages to find packages
  packages = [
    pkgs.poetry
    pkgs.python311
    pkgs.python311Packages.pip
  ];

  # Sets environment variables in the workspace
  env = { };
  idx = {
    # Search for the extensions you want on https://open-vsx.org/ and use "publisher.id"
    extensions = [
      "ms-toolsai.jupyter"
      "ms-python.python"
    ];

    # Enable previews
    previews = {
      # enable = false;
      # previews = {
      # web = {
      #   # Example: run "npm run dev" with PORT set to IDX's defined port for previews,
      #   # and show it in IDX's web preview panel
      #   command = ["npm" "run" "dev"];
      #   manager = "web";
      #   env = {
      #     # Environment variables to set for your server
      #     PORT = "$PORT";
      #   };
      # };
      # };
    };

    # Workspace lifecycle hooks
    workspace = {
      # Runs when a workspace is first created with this `dev.nix` file
      onCreate = {
        create-venv = ''
          python -m venv .venv
          source .venv/bin/activate
          poetry  install
        '';
        # Open editors for the following files by default, if they exist:
        default.openFiles = [ ];
      };
      # To run something each time the workspace is (re)started, use the `onStart` hook
    };
    # Runs when the workspace is (re)started
    # onStart = {
    # Example: start a background task to watch and re-build backend code
    # watch-backend = "npm run watch-backend";
    # };
  };
}
