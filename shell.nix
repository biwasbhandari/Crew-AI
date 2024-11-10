{ pkgs ? import <nixpkgs> {} }:

let
  pythonPackages = pkgs.python310Packages;
  python = pkgs.python310;
in pkgs.mkShell {
  buildInputs = with pkgs; [
    python
    pythonPackages.pip
    pythonPackages.poetry-core    # Access poetry-core through pythonPackages
    poetry                        # Full Poetry CLI is a top-level package
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