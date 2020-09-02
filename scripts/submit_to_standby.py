import argparse
import os
import subprocess

from scripts import find_workspace

"""
FutureImprove:
1. it can receive argument in the script
    - workspace

"""


def _get_minikube_ip() -> str:
    minikube_ip = subprocess.Popen(["minikube", "ip"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
    outs, errs = minikube_ip.communicate(timeout=100)
    return outs[:len(outs) - 1]


class MyWorkSpace:

    def __init__(self, custom_workspace=None):
        if custom_workspace:
            self.workspace = custom_workspace
        else:
            self.workspace = find_workspace()

    def compose_app_name(self, app_name: str) -> str:
        return os.path.join(self.workspace, "sparkstudy", "apps", app_name + ".py")


def create_command_parser() -> argparse.Namespace:
    result = argparse.ArgumentParser(description='manual to this script')
    result.add_argument('--workspace', type=str, default=None)
    result.add_argument('--app', type=str, default="simple_app")
    minikube_ip = _get_minikube_ip()
    result.add_argument('--remote_server', type=str, default="spark://{}:{}".format(minikube_ip, 30083))
    return result.parse_args()


if __name__ == '__main__':
    args = create_command_parser()
    workspace = MyWorkSpace(args.workspace)
    app_full_path = workspace.compose_app_name(args.app)
    commands = ["spark-submit",
                "--master",
                args.remote_server,
                app_full_path]
    subprocess.run(commands, cwd=workspace.workspace)
