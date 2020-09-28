import re
import subprocess


def get_kubernetes_address() -> str:
    minikube_ip = subprocess.Popen(["kubectl", "cluster-info"], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   encoding="utf-8")
    outs, errs = minikube_ip.communicate(timeout=100)
    pattern = r'(http|https):\/\/([\w.]+\/?)\:\d{0,4}'
    item = re.search(pattern, outs, 0)

    if item:
        return str(item.group())
    return None


def get_minikube_ip() -> str:
    minikube_ip = subprocess.Popen(["minikube", "ip"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
    outs, errs = minikube_ip.communicate(timeout=100)
    return outs[:len(outs) - 1]
