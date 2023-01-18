import boto3
from botocore.exceptions import  NoCredentialsError

def s3_client():
    try:
        s3 = boto3.client("s3")
        return s3
    except NoCredentialsError as e:
        raise (e)


def upload_csv_s3(path_to_file):
    """
    Upload both CSV files to the S3 bucket
    """
    s3 = s3_client()
    
    s3.upload_file(
        Filename= f"{path_to_file}",
        Bucket="cheapper",
        Key= f"{path_to_file}",
    )