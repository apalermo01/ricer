# https://github.com/dtgoitia/nix-python/blob/main/flake.nix
{
  description = "Python development environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    # nixpkgs-python.url = "github:cachix/nixpkgs-python";
  };

  outputs =
    {
      self,
      nixpkgs,
      # nixpkgs-python,
    }:
    let
      system = "x86_64-linux";

      pkgs = import nixpkgs { inherit system; };
    in
    {
      devShells.${system}.default = pkgs.mkShell {
        buildInputs = [
          pkgs.zlib
          pkgs.gcc

          (pkgs.python311.withPackages(
            ps: with ps; [
              pip
              setuptools
              wheel
              pydantic
              pytest
              numpy
              matplotlib
              toml
              pyyaml
              isort
              black
              jinja2
            ]
          ))
        ];
      };
    };
}
