import os
from scraper_extract import main
from upload_to_s3 import upload_csv_s3

if __name__ == "__main__":

    file = main.main()

    upload_csv_s3(file)

    os.remove(file)