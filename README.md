# s3-dedupe

This is a Python script to remove duplicate files from a given AWS S3 bucket.  It determines a file to be a duplicate by it's etag and it's file size.  This is done to insure that any collisions that may occur with an etag are accounted for.  Obviously, this method does not take into account file names.  For instance, if "file1.txt" and "file2.txt" have the same etag and size, the code will consider them duplicates and delete the latter (alphabetical order) of the two.  The code also looks across an entire bucket.  It does not work, in its current form, on a specific folder.

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
