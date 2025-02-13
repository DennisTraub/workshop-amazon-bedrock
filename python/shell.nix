with import <nixpkgs> {};
mkShell {
  buildInputs = [
    pkgs.uv
  ];

  LD_LIBRARY_PATH = "${pkgs.stdenv.cc.cc.lib}/lib/";

  shellHook = ''
    uv sync
  '';
}
