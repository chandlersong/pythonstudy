import argparse
import subprocess

from scripts import MyWorkSpace
from sparkstudy.deploy.kubernetes_tools import get_minikube_ip

"""
FutureImprove:
1. it can receive argument in the script
    - workspace

"""


def create_command_parser() -> argparse.Namespace:
    result = argparse.ArgumentParser(description='manual to this script')
    result.add_argument('--workspace', type=str, default=None)
    result.add_argument('--app', type=str, default="simple_app")
    minikube_ip = get_minikube_ip()
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
