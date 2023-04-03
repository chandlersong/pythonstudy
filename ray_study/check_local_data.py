import os.path

import ray

from ray_study.others import check_file_in_other


@ray.remote
def check_file(file_path_local):

    return check_file_in_other(file_path_local)


file_path = "a.txt"
ref = check_file.remote(file_path)
print(f"ray result {ray.get(ref)}")
print(f"local {os.path.exists(file_path)}")
