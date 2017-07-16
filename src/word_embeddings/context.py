import os
import sys
parent_path = os.path.join(os.path.dirname(__file__), os.pardir)
grandparent_path = os.path.join(parent_path, os.pardir)
sys.path.insert(0, os.path.abspath(grandparent_path))

import tml
