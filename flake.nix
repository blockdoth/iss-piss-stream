{
  inputs.nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  outputs = inputs:
    let
      system = "x86_64-linux";
      pkgs = inputs.nixpkgs.legacyPackages.${system};
      lightstreamer-client-lib = pkgs.python3Packages.buildPythonPackage rec {
        pname = "lightstreamer_client_lib";
        version = "2.2.0";
        propagatedBuildInputs = with pkgs.python3Packages; [ aiohttp jsonpatch ];
        src = pkgs.fetchPypi {
          inherit pname version;
          sha256 = "7306e42707ebc40144879854e0aa568383f37e1e006e5430f96455867761a73c";
        };
      };
    in
    {
      packages.${system} = {
        iss-piss-stream = pkgs.writers.writePython3Bin "iss-piss-stream"{ 
          libraries = [ lightstreamer-client-lib ]; 
          doCheck = false;
          }
          (builtins.readFile ./main.py);
      };

    
      devShell.x86_64-linux = pkgs.mkShell {
        packages = with pkgs; [
          lightstreamer-client-lib 
          python3
          python3Packages.matplotlib
        ];      
      };
    };
}

