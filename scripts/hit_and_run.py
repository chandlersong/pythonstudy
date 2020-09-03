import argparse

from scripts import SparkSubmit, SPARK_DEPLOY_MODE_CLIENT, get_kubernetes_address


def create_command_parser() -> argparse.Namespace:
    result = argparse.ArgumentParser(description='manual to this script')
    result.add_argument('--workspace', type=str, default=None)
    result.add_argument('--app', type=str, default="simple_app")
    result.add_argument('--deploy_mode', type=str, default=SPARK_DEPLOY_MODE_CLIENT)
    result.add_argument('--executor_number', type=int, default=3)
    result.add_argument('--master', type=str, default=("k8s://" + get_kubernetes_address()))
    return result.parse_args()


if __name__ == '__main__':
    args = create_command_parser()
    app = SparkSubmit(workspace=args.workspace,
                      name=args.app,
                      deploy_mode=args.deploy_mode,
                      executor_num=args.executor_number,
                      master=args.master)
    result = app.execute()
