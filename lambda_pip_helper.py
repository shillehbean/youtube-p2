import os
import subprocess
import boto3
import zipfile

def lambda_handler(event, context):
    # Initial setup: package name(s) and S3 bucket details
    try:
        packages = ['pyjwt']
        bucket_name = 'your-bucket-name'
        object_key = 'python_package_pyjwt.zip'

        # Target directory for package installation
        package_dir = '/tmp/python/lib/python3.12/site-packages/'
        os.makedirs(package_dir, exist_ok=True)

        # Install the package(s) using pip
        for package in packages:
            subprocess.run(['pip', 'install', package, '--target', package_dir], check=True)

        # Create a zip archive of the installed package(s)
        with zipfile.ZipFile('/tmp/python_package.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk('/tmp/python'):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, '/tmp'))
        
        # Upload the zip file to S3
        s3_client = boto3.client('s3')
        s3_client.upload_file('python_package.zip', bucket_name, object_key)

        return {
            'statusCode': 200,
            'body': f'Successfully installed, zipped, and uploaded package to s3://{bucket_name}/{object_key}'
        }

    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': 'An error occurred during the process.'
        }
