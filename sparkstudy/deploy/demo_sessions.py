from pyspark import SparkConf
from pyspark.sql import SparkSession

from sparkstudy.deploy.kubernetes_tools import get_kubernetes_address

DEAULT_ACCOUNT = "spark"

DEFAULT_IMAGES = "chandlersong/spark:0.0.1"
SPARK_DEPLOY_MODE_CLIENT = "client"
SPARK_DEPLOY_MODE_CLUSTER = "cluster"


class DemoSQLSessionFactory:
    def __init__(self, deploy_mode=SPARK_DEPLOY_MODE_CLIENT, name="simple_app", remote=False,
                 image=DEFAULT_IMAGES,
                 account=DEAULT_ACCOUNT, executor_num=3, master=None):
        self._deploy_mode = deploy_mode
        self._name = name
        self._image = image
        self._account = account
        self._executor_num = executor_num
        if master is None and remote:
            self._master = "k8s://" + get_kubernetes_address()
        elif master is None and not remote:
            self._master = "local[{}]".format(self._executor_num)
        else:
            self._master = master

        self._remote = remote
        self._extra_conf = {}

    def build_session(self) -> SparkSession:
        conf = SparkConf(). \
            setMaster(self._master). \
            setAppName(self._name)

        if self._remote:
            conf.set("spark.submit.deployMode", self._deploy_mode). \
                set("spark.executor.instances", str(self._executor_num)). \
                set("spark.kubernetes.authenticate.driver.serviceAccountName", self._account). \
                set("spark.kubernetes.container.image", self._image). \
                set("spark.kubernetes.pyspark.pythonVersion", "3")

        for conf_key in self._extra_conf:
            conf.set(key=conf_key, value=self._extra_conf[conf_key])

        return SparkSession.builder.config(conf=conf).getOrCreate()

    def add_config(self, key: str, value: str) -> None:
        self._extra_conf[key] = value
