with import <nixpkgs> {};

let
  python-with-packages = python3.withPackages (ps: with ps; [
    psutil
    pillow
    matplotlib
    colorama
    pretty-errors
    pygame
    requests
    progressbar2
    plyer
    art
  ]);
in
pkgs.mkShell {
  buildInputs = [
    python-with-packages
    (python3.pkgs.buildPythonPackage rec {
      pname = "python_goto";
      version = "0.1.4";
      src = python3.pkgs.fetchPypi {
        inherit pname version;
        sha256 = "I4PCyy5SAaUuCWzMKrBRScUtk5gBCNBgcmHPPoJGRXU=";
      };
      prePatch = ''
        substituteInPlace setup.py --replace-warn 'C:\\Users\\NewUser\\Desktop\\github\\pygoto\\README.md' 'README.md'
      '';
      doCheck = false;
    })
    (python3.pkgs.buildPythonPackage rec {
      pname = "pymod";
      version = "0.2";
      src = python3.pkgs.fetchPypi {
        inherit pname version;
        sha256 = "0+gtXpOeTN6y56uNtNtHT1plJT4FkcVlb51Ec2lGcjw=";
      };
      doCheck = false;
    })
  ];
}
