import subprocess
import sys

def install_package(package_name: str) -> None:
    subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])

def uninstall_package(package_name: str) -> None:
    subprocess.check_call([sys.executable, "-m", "pip", "uninstall", "-y", package_name])

def list_installed_packages() -> None:
    subprocess.check_call([sys.executable, "-m", "pip", "list"])

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Simple Package Manager")
    parser.add_argument("command", choices=["install", "uninstall", "list"], help="Command to execute")
    parser.add_argument("package", nargs="?", help="Package name for install/uninstall")

    args = parser.parse_args()

    if args.command == "install" and args.package:
        install_package(args.package)
    elif args.command == "uninstall" and args.package:
        uninstall_package(args.package)
    elif args.command == "list":
        list_installed_packages()
    else:
        parser.print_help()

