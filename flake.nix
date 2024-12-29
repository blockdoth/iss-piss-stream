{
  inputs.nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  outputs =
    inputs:
    let
      system = "x86_64-linux";
      pkgs = inputs.nixpkgs.legacyPackages.${system};
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
        
        xkcd-script = pkgs.stdenvNoCC.mkDerivation {
          pname = "xkcd script";
          version = "1.0";
          dontUnpack = true;
          src = pkgs.fetchurl {
            url = "https://raw.githubusercontent.com/ipython/xkcd-font/master/xkcd-script/font/xkcd-script.ttf";
            hash = "sha256-m43yVeJlYzWmoLtcQ965QaE8PcT4Wmv/xvCI3IQWM6w=";
          };
          installPhase = ''       
            install -Dm755 $src $out/share/fonts/truetype/'xkcd Script'
          '';
        };

        iss-piss-stream = pkgs.writers.writePython3Bin "iss-piss-stream" {
          libraries = [ inputs.self.packages.${system}.lightstreamer-client-lib ];
          doCheck = false;
        } (builtins.readFile ./main.py);
        
        iss-piss-graph = pkgs.writers.writePython3Bin "iss-piss-stream" {
          libraries = [ pkgs.python3Packages.matplotlib pkgs.xkcd-script];
          doCheck = false;
        } (builtins.readFile ./graph.py);

        default = inputs.self.packages.${system}.iss-piss-stream;
      };

      devShell.x86_64-linux = pkgs.mkShell {
        packages = with pkgs; [
          inputs.self.packages.${system}.lightstreamer-client-lib
          inputs.self.packages.${system}.xkcd-script
          python3Packages.matplotlib
          python3
        ];
      };
    };
}
