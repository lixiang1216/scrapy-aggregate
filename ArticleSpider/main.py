from scrapy.cmdline import execute

import sys
import os
#获取父级
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy","crawl","jobbole"])
