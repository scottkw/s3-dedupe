import argparse, boto3, sys

class S3DeDupe:

    def __init__(self):

        '''
        Method:       __init__
        Visibility:   private
        Purpose:      Initialize object with class vars
        Parameters:   self - the current instance of the class
        Returns:      nothing
        '''

        # Show banner
        self.__print_banner()

        # Set up command line argument parsing
        self.ap = argparse.ArgumentParser()
        self.__create_arguments()
        self.args = vars(self.ap.parse_args())

        # If no arguments are passed, display the help message
        if len(sys.argv)==1:
            self.ap.print_help(sys.stderr)
            sys.exit(1)

        self.s3_bucket = self.args["bucket_name"]
        self.dupe_count = 0
        self.unique_count = 0
        self.etag_size = []

    def __print_banner(self):

        '''
        Method:       __print_banner
        Visibility:   private
        Purpose:      Prints the title banner for the CLI
        Parameters:   none
        Returns:      nothing
        '''

        # Print banner
        print()
        print("S3 Dedupe")
        print("Written by Ken Scott")
        print("MIT License 2022, EightAByte Industries")
        print("https://www.eightabyte.com")
        print()

    def __create_arguments(self):

        '''
        Method:       __create_arguments
        Visibility:   private
        Purpose:      Sets up all the CLI arguments and their configurations
        Parameters:   none
        Returns:      nothing
        '''

        self.ap.add_argument('-b', '--bucket', type=str, metavar='bucket_name', dest='bucket_name', required=True, default='', help='The name of the S3 bucket to be deduped.')
        self.ap.add_argument('-v', '--verbose', default=False, action="store_true", help='Determines if each file processed is written to stdout.')
        self.ap.add_argument('-d', '--delete', default=False, action="store_true", help='Delete the duplicate files.')

    def dedupe_bucket(self):

        '''
        Method:       dedupe_bucket
        Visibility:   public
        Purpose:      Dedupe the bucket
        Parameters:   none
        Returns:      nothing
        '''

        s3_client = boto3.client('s3')
        paginator = s3_client.get_paginator('list_objects_v2')

        response_iterator = paginator.paginate(Bucket=self.s3_bucket)

        file_counter = 'Unique files = {}; Duped files = {}; Total = {}'
    
        for page in response_iterator:
            for key in page['Contents']:
                s3_resp = s3_client.head_object(Bucket=self.s3_bucket, Key=key['Key'])

                file_key = key['Key']
                file_etag = s3_resp['ETag'].replace('"', '')
                file_size = str(s3_resp['ContentLength'])
                
                file_data = 'File: ' + file_key + ' | ' + 'ETag: ' + file_etag + ' | ' + 'ContentLength: ' + file_size

                unique_id = file_etag + '.' + file_size
                
                if unique_id in self.etag_size:
                    self.dupe_count = self.dupe_count + 1 
                    file_state = 'DUPE'

                    if self.args["delete"]:
                        s3_client.delete_object(Bucket=self.s3_bucket, Key=key['Key'])
                        file_state = 'DUPE DELETED'
                else:
                    self.unique_count = self.unique_count + 1
                    file_state = 'UNIQUE'
                    self.etag_size.append(unique_id)

                if self.args["verbose"]:
                    print(file_state + ' = ' + file_data)
                else:
                    print(file_counter.format(self.unique_count, self.dupe_count, (self.unique_count + self.dupe_count)), end='\r')

    def main(self):

        '''
        Method:       main
        Visibility:   public
        Purpose:      The main controlling function of the application
        Parameters:   none
        Returns:      nothing
        '''

        # If a search string was provided, perform the search
        if self.args["bucket_name"]:
            self.dedupe_bucket()

            if self.args["verbose"]:
                print()
                print('Unique files: ' + str(self.unique_count))
                print('Duped files: ' + str(self.dupe_count))
                print('=====')
                print('Total files: ' + str(self.dupe_count + self.unique_count))
                print()

        print()
        
if __name__ == '__main__':
  s3_dedupe = S3DeDupe()
  s3_dedupe.main()