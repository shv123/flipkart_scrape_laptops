import sys

iparg1 = sys.argv[1]
iparg2 = sys.argv[2]

import os
os.system("scrapy crawl flipkartbot -a iparg1=" + iparg1 + " -a iparg2=" + iparg2)