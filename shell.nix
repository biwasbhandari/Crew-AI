{ pkgs ? import <nixpkgs> {} }:

let
  pythonPackages = pkgs.python310Packages; # Use Python 3.10 packages
  python = pkgs.python310;
in pkgs.mkShell {
  buildInputs = with pkgs; [
    python
    pythonPackages.pip
    pythonPackages.virtualenv
    gcc
    stdenv.cc.cc.lib
    zlib
    glib
    ffmpeg
  ];

  shellHook = ''
    export LD_LIBRARY_PATH=${pkgs.stdenv.cc.cc.lib}/lib:${pkgs.zlib}/lib:$LD_LIBRARY_PATH
  '';
}