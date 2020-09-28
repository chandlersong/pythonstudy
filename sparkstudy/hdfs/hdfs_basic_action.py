import unittest

from hdfs import Client, InsecureClient
import pandas as pd
from sparkstudy.deploy.kubernetes_tools import get_minikube_ip


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        host = get_minikube_ip()
        self._client = InsecureClient(url="http://{}:30084/".format(host), user="root")

    def test_upload_file(self):
        client_list = self._client.list(hdfs_path="/", status=True)
        for item in client_list:
            print("item is {}".format(item))

        liste_hello = ['hello1', 'hello2']
        liste_world = ['world1', 'world2']
        df = pd.DataFrame(data={'hello': liste_hello, 'world': liste_world})

        with self._client.write('/helloworld.csv', encoding='utf-8', overwrite=True) as writer:
            df.to_csv(writer)
            self._client.set_permission('/helloworld.csv', '755')

        self._client.delete('/helloworld.csv')


if __name__ == '__main__':
    unittest.main()
