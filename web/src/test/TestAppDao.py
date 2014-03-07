#=======================
#### file: test.py ####
#=======================

import sys
import os
import nose
from nose import with_setup
c_path = os.getcwd()
base_path = c_path[:c_path.rfind("src")]
sys.path.append(base_path)

from src.dao import AppDao




def setup_func():
    "set up test fixtures"

def teardown_func():
    "tear down test fixtures"

@with_setup(setup_func, teardown_func)
def TestShouldBeImplemented():
	the_target_result = "Specific result should be outputed using below method"
	if AppDao.some_method_should_be_implemented_in_the_future(the_input_paras) == the_target_result:
		assert True
	else:
		assert False


if __name__ == "__main__":
	TestQuery()