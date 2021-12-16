{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.hugo
    pkgs.sshfs

    # keep this line if you use bash
    pkgs.bashInteractive
  ];
}
