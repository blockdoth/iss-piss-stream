{
  inputs.nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  outputs =
    inputs:
    let
      system = "x86_64-linux";
      pkgs = inputs.nixpkgs.legacyPackages.${system};
      local = inputs.self.packages.${system};
    in
    {
      packages.${system} = {
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
          libraries = [ local.lightstreamer-client-lib ];
          doCheck = false;
        } (builtins.readFile ./main.py);
        
        iss-piss-graph = pkgs.writers.writePython3Bin "iss-piss-stream" {
          libraries = [ pkgs.python3Packages.matplotlib];
          doCheck = false;
        } (builtins.readFile ./graph.py);

        default = local.iss-piss-stream;
      };

      devShell.x86_64-linux = pkgs.mkShell {
        packages = with pkgs; [
          local.lightstreamer-client-lib
          python3Packages.prometheus-client
          python3Packages.matplotlib
          python3
        ];
      };
    };
}
