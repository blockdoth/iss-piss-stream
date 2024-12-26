{
  description = "A Nix flake for a custom Python environment with lightstreamer-client-lib";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  };

  outputs =
    { self, nixpkgs }:
    let
      system = "x86_64-linux";    
      pkgs = import nixpkgs { inherit system; };

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
      pythonEnv = pkgs.python3.withPackages(ps: [ 
        lightstreamer-client-lib 
        pkgs.python3Packages.matplotlib
      ]);

      project-space-piss = pkgs.stdenv.mkDerivation {
        pname = "project-space-piss";
        version = "1.0.0";     
        meta.mainProgram = "project-space-piss";
        buildInputs = [ pythonEnv ];
        dontUnpack = true;  
        installPhase = ''
          install -Dm755 ${./main.py} $out/bin/project-space-piss
        '';
      };  
    in
    {  
      apps.x86_64-linux.default = {
        type = "app";
        program = "${pkgs.lib.getExe project-space-piss}";
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
