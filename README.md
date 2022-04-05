# s3-dedupe

Script to remove duplicate files from a given AWS S3 bucket.

## Usage

```
usage: s3_dedupe.py [-h] -b bucket_name [-v] [-d]

optional arguments:
  -h, --help            show this help message and exit
  -b bucket_name, --bucket bucket_name
        The name of the S3 bucket to be deduped.
  -v, --verbose         Determines if each file processed is written to stdout.
  -d, --delete          Delete the duplicate files.
  ```