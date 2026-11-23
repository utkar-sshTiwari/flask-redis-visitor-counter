{ pkgs ? import <nixpkgs> {} }:

let
  pythonEnv = pkgs.python3.withPackages (ps: with ps; [
    flask
    redis
    gunicorn
    requests
  ]);
in
pkgs.mkShell {
  name = "k8s-visitor-counter";

  buildInputs = with pkgs; [
    minikube
    kubectl
    docker-compose
    curl
    pythonEnv
  ];

  shellHook = ''
    export MINIKUBE_DRIVER=docker
    echo "Loaded minikube, kubectl, docker-compose, curl, and Python (flask, redis, gunicorn, requests)."
  '';
}
