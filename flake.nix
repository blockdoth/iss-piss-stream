{
  inputs.nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";

  outputs = { self, nixpkgs, ... } @ inputs:
    let
      forAllSystems = f: nixpkgs.lib.genAttrs nixpkgs.lib.systems.flakeExposed f;
    in
    {
      packages = forAllSystems (system:
        let
          pkgs = import nixpkgs { inherit system; };
        in
        {
          lightstreamer-client-lib = pkgs.python3Packages.buildPythonPackage rec {
            pname = "lightstreamer_client_lib";
            version = "2.2.0";
            propagatedBuildInputs = with pkgs.python3Packages; [
              aiohttp
              jsonpatch
            ];
            src = pkgs.fetchPypi {
              inherit pname version;
              sha256 = "7306e42707ebc40144879854e0aa568383f37e1e006e5430f96455867761a73c";
            };
          };

          iss-piss-stream = pkgs.writers.writePython3Bin "iss-piss-stream" {
            libraries = [ self.packages.${system}.lightstreamer-client-lib ];
            doCheck = false;
          } (builtins.readFile ./logger.py);

          iss-piss-graph = pkgs.writers.writePython3Bin "iss-piss-graph" {
            libraries = [ pkgs.python3Packages.matplotlib ];
            doCheck = false;
          } (builtins.readFile ./graph.py);

          default = self.packages.${system}.iss-piss-stream;
        });

      apps = forAllSystems (system:
        {
          default = {
            type = "app";
            program = "${self.packages.${system}.default}/bin/iss-piss-stream";
          };
          graph = {
            type = "app";
            program = "${self.packages.${system}.iss-piss-graph}/bin/iss-piss-graph";
          };
        });

      devShells = forAllSystems (system:
        let
          pkgs = import nixpkgs { inherit system; };
        in
        pkgs.mkShell {
          packages = with pkgs; [
            self.packages.${system}.lightstreamer-client-lib
            python3Packages.prometheus-client
            python3Packages.matplotlib
            python3Packages.fastapi
            python3
          ];
        });
    };
}

