import os
import re
import subprocess

DEAULT_ACCOUNT = "spark"

DEFAULT_IMAGES = "chandlersong/spark:0.0.1"
SPARK_DEPLOY_MODE_CLIENT = "client"
SPARK_DEPLOY_MODE_CLUSTER = "cluster"


def find_workspace():
    result = os.path.abspath(os.path.dirname(__file__))
    while result != "/":
        result = os.path.abspath(os.path.dirname(result))
        if os.path.exists(os.path.join(result, "setup.py")):
            return result
    return None


def _compose_app_name(workspace: str, app_name: str) -> str:
    return os.path.join(workspace, "sparkstudy", "apps", app_name + ".py")


class MyWorkSpace:

    def __init__(self, custom_workspace=None):
        if custom_workspace:
            self.workspace = custom_workspace
        else:
            self.workspace = find_workspace()

    def compose_app_name(self, app_name: str) -> str:
        return _compose_app_name(self.workspace, app_name)


def get_kubernetes_address():
    minikube_ip = subprocess.Popen(["kubectl", "cluster-info"], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   encoding="utf-8")
    outs, errs = minikube_ip.communicate(timeout=100)
    pattern = r'(http|https):\/\/([\w.]+\/?)\:\d{0,4}'
    item = re.search(pattern, outs, 0)

    if item:
        return str(item.group())
    return None


class SparkSubmit:

    def __init__(self, deploy_mode=SPARK_DEPLOY_MODE_CLIENT, name="simple_app", workspace=None,
                 image=DEFAULT_IMAGES,
                 account=DEAULT_ACCOUNT, executor_num=3, master=None):
        self._deploy_mode = deploy_mode
        self._name = name
        self._image = image
        self._account = account
        self._executor_num = executor_num

        if workspace is None:
            self._workspace = find_workspace()
        else:
            self._workspace = workspace

        if master is None:
            self._master = "k8s://" + get_kubernetes_address()
        else:
            self._master = master

        self._extra_conf = {}

    def execute(self):
        command = ["spark-submit"]

        def compose_conf_literal(key: str, value: str):
            nonlocal command
            command.append("--conf")
            command.append("{}={}".format(key, value))

        command.append("--master")
        command.append(self._master)
        command.append("--deploy-mode")
        command.append(self._deploy_mode)
        command.append("--name")
        command.append(self._name)
        compose_conf_literal("spark.executor.instances", str(self._executor_num))
        compose_conf_literal("spark.kubernetes.authenticate.driver.serviceAccountName", self._account)
        compose_conf_literal("spark.kubernetes.container.image", self._image)
        compose_conf_literal("spark.kubernetes.pyspark.pythonVersion", "3")
        for key in self._extra_conf:
            compose_conf_literal(key, self._extra_conf[key])

        command.append(self.python_file_path)
        return subprocess.run(command,
                              encoding="utf-8", cwd=self._workspace)

    def add_config(self, key: str, value: str) -> None:
        self._extra_conf[key] = value

    @property
    def python_file_path(self) -> str:
        return _compose_app_name(self._workspace, self._name)
