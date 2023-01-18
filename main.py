import os
import scraper_extract
from upload_to_s3 import upload_csv_s3

if __name__ == "__main__":

    file = scraper_extract.main()

    upload_csv_s3(file)

    os.remove(file)