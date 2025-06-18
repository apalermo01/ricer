with import <nixpkgs> {};
with pkgs.python3Packages;

buildPythonPackage rec {
  name = "ricer";
  src = ./src;
  propagatedBuildInputs = [ pytest numpy pkgs.libsndfile ];
}
