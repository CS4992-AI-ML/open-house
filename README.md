# Welcome to Project Open House

## Team
- Diane
- Owen
- Luis
- Maggie
- Maddie
- Spencer

# _Dev Setup_

## Step 1: Installing Anaconda and Python
First install Anaconda and make sure you have Python 3.11.x

[Python](https://www.python.org/downloads/release/python-3110/)

[Anaconda](https://www.anaconda.com/download)
## Step 2: Installing Interpreter
```angular2html
PyCharm -> Settings -> Python Interpreter -> Add New Interpreter -> Add Local Interpreter -> 
Conda Environment -> Create new environment -> Set Python Version to 3.11 -> Click OK
```
## Step 3: Confirm Python Version 3.11.0
```angular2html
Make sure Python's Version is set to 3.11.0.
If not, double click the version -> Specify Version -> 3.11 -> Wait for install -> Reset IDE
```
![img.png](readme-imgs/img.png)

## Step 4: Test Interpreter is setup

```angular2html
python ./tests/test_version.py
```

### Result should be something similar to this
```angular2html
3.11.0 (main, Mar  1 2023, 12:33:14) [Clang 14.0.6 ]
```

## Step 5: Install Requirements
### Anytime you want to add a library make sure to add it to the .txt
```angular2html
pip install -r ./requirements.txt
```

## Step 6: Download Data
### Follow this [link](https://northeastern-my.sharepoint.com/:f:/r/personal/igortn_northeastern_edu/Documents/DoCs/UTS-Projects/Rental%20prediction?csf=1&web=1&e=IPnzKu) to access data.

In a git bash terminal run this to create a folder labeled `data` in `open-house` or just create the folder.

```angular2html
mkdir data
```

Download files labeled part 1-12. Add to the data folder.
Run data-imports.py. This will create `housing_data.csv`

## *Interacting with AWS*
Install [AWS CLI](https://aws.amazon.com/cli/) and install [boto3](https://pypi.org/project/boto3/) and login

Once you have done and logged in, run this:
```angular2html
python ./tests/test_boto3.py
```
The output should look something like this:
```angular2html
Existing buckets:
  silly-australia-bucket
```

To see the sample S3 JSON run this:
```angular2html
python ./tests/test_squid.py
```