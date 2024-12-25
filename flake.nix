{
  description = "A Nix flake for a pissy environment";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  };

  outputs =
    { self, nixpkgs }:
    let
      supportedSystems = [
        "x86_64-linux"
        "aarch64-linux"
        "x86_64-darwin"
        "aarch64-darwin"
      ];
      forEachSupportedSystem =
        f: nixpkgs.lib.genAttrs supportedSystems (system: f { pkgs = import nixpkgs { inherit system; }; });
    in
    {
      devShells = forEachSupportedSystem (
        { pkgs }:
        {
          default = pkgs.mkShell {
            shellHook = "
              python3 -m venv .venv
              source .venv/bin/activate
              pip install --upgrade pip
              pip install lightstreamer-client  
              npm install lightstreamer-client-node
          ";
            packages = with pkgs; [
              nodejs-18_x
              python3
              python3Packages.pip
            ];
          };
        }
      );
    };
}

