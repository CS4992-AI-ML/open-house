import sagemaker
import boto3

import numpy as np  # For performing matrix operations and numerical processing
import pandas as pd  # For manipulating tabular data
from time import gmtime, strftime
import os
from sagemaker import get_execution_role

region = "ap-southeast-2"
smclient = boto3.Session().client("sagemaker")

## test code to interact with sagemaker once deployed
