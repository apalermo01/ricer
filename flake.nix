# https://github.com/dtgoitia/nix-python/blob/main/flake.nix
{
  description = "Python development environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    nixpkgs-python.url = "github:cachix/nixpkgs-python";
  };

  outputs =
    {
      self,
      nixpkgs,
      nixpkgs-python,
    }:
    let
      system = "x86_64-linux";
      pythonVersion = "3.11";

      pkgs = import nixpkgs { inherit system; };
      python = nixpkgs-python.packages.${system}.${pythonVersion};
      # inherit (pkgs) lib stdenv;
    in
    {
      devShells.${system}.default = pkgs.mkShell {
        buildInputs = [
          python
          python.pkgs.pip
          python.pkgs.setuptools
          python.pkgs.wheel
          python.pkgs.virtualenv
          pkgs.zlib
          pkgs.gcc
        ];
        # NIX_LD_LLIBRARY_PATH = lib.makeLibraryPath [
        #   stdenv.cc.cc
        # ];
        # NIX_LD = builtins.readFile "${stdenv.cc}/nix-support/dynamic-linker";
        # packages = [
        #   myPython
        # ];
        shellHook = ''
          echo "RUNNING SHELL HOOK"
          export LD_LIBRARY_PATH="${pkgs.gcc.cc.lib}/lib:$LD_LIBRARY_PATH"
          python --version
          zsh
        '';
      };
    };
}
