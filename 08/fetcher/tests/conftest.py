# content of conftest.py
"""Copyright 2022 by Artem Ustsov"""

import pytest
import pytest_asyncio
import json
import json_tools
from unittest.mock import Mock, patch

# pytest_plugins = []
# @pytest.mark.parametrize("param1, param2", [(param1, param2),
#                                             (param3, param4)]) - original test-suites
# with pytest.raises(ValueError): - error exception
#     assert function() -> raise error

# fixtures
# @pytest.fixture(autouse=True) -> auto execution
# def open_file():
# @pytest.mark.asyncio
