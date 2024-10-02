{ pkgs, ... }: {
    channel = "stable-23.11";

    packages = [
        pkgs.openssh
        pkgs.python3
    ];
}