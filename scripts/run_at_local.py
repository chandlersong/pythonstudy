import argparse
import subprocess

from scripts import MyWorkSpace


def create_command_parser() -> argparse.Namespace:
    result = argparse.ArgumentParser(description='manual to this script')
    result.add_argument('--workspace', type=str, default=None)
    result.add_argument('--app', type=str, default="simple_app")
    return result.parse_args()


if __name__ == '__main__':
    args = create_command_parser()
    workspace = MyWorkSpace(args.workspace)
    app_full_path = workspace.compose_app_name(args.app)
    commands = ["spark-submit",
                "--master",
                "local[3]",
                app_full_path]
    subprocess.run(commands, cwd=workspace.workspace)
