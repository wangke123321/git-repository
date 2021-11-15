import os
from jianlian.config.class_config import FileConfig

project_path = os.path.realpath(__file__)
l1 = os.path.split(project_path)[0]
l2 = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
test_case_path = os.path.split(os.path.split(os.path.split(os.path.realpath(__file__))[0])[0])[0]

# print(test_case_path)
# print(project_path)
# print(l1)
# print(l2)
# print(test_case_path)

project_tx = os.path.join(test_case_path, 'jianlian', 'tixian_class', 'tx_data.csv')
project_sm_tx = os.path.join(test_case_path, 'jianlian', 'tixian_class', 'scandeal_data.csv')
project_tx_url = os.path.join(test_case_path, 'jianlian', 'class_config')


