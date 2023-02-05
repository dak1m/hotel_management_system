import time

from django.test import TestCase

# Create your tests here.
print((time.mktime(time.strptime('2022-01-04', '%Y-%m-%d')) - time.mktime(time.strptime('2022-01-03', '%Y-%m-%d')))/3600/24)