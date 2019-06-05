cd packages
echo 'packaging function'
zip  -q -r9 ../function.zip .
cd ..

zip -g function.zip lambda_function.py
echo 'uploading function'
aws lambda update-function-code --function-name s3tordsstorestream --zip-file fileb://function.zip