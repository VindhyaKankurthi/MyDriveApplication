from flask import Blueprint, render_template, request, session

import time
import boto3
from S3.s3Bucket import create_bucket
from S3.s3Bucket import uploadToS3
from werkzeug.utils import secure_filename
from botocore.exceptions import ClientError

# create an instance of dynamobd
dynamodb = boto3.resource('dynamodb')

s3 = boto3.client('s3')

from boto3.dynamodb.conditions import Key, Attr
auth = Blueprint('auth', __name__)

#defining login route
@auth.route('/login')
def login():
    return render_template("loginPage.html")

#performing email and password check
@auth.route('/loginCheck', methods=['GET', 'POST'])
def check():
    print('login')
    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']
        print("entered password.."+password)

        #querying details of a specific user with Email ID
        table = dynamodb.Table('usersdata')
        response = table.query(
            KeyConditionExpression=Key('email').eq(email)
        )
        items = response['Items']
        print(items)
        
        print(items[0]['password1'])
        if password == items[0]['password1']:
            bucketname = items[0]['bucketname']
            session["bucketname"] = bucketname
            return render_template("fileUploadtoS3.html")

        return render_template("homePage.html")
    
#defining logout route
@auth.route('/logout')
def logout():
    return render_template("homePage.html")

#defining signup route
@auth.route('/sign-up', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        password1 = request.form['password1']
    
        # creating a bucket name for a user
        bucketname = firstName + str(round(time.time() * 1000))
        print("bucketname"+bucketname)
        create_bucket(bucketname)

        # name of the table to be created
        table = dynamodb.Table('usersdata')

        table.put_item(
            Item={
        'email' : email,
        'firstName' : firstName,
        'lastName' : lastName,
        'password1' : password1,
        'bucketname': bucketname
         }
        )
   
        print("success!!")
        return render_template('loginPage.html')

    return render_template('signupPage.html')
       

@auth.route('/uploadFile', methods=['POST'])
def upload():
    if "bucketname" in session:
        bucketname = session["bucketname"]
        print("my bucket"+bucketname)
        img = request.files['file']
        if img:
             filename = secure_filename(img.filename)
             print(filename)
             img.save(filename)
             uploadToS3(filename, bucketname)
        
    return render_template('fileUploadtoS3.html')
   

#view Files
@auth.route('/viewFiles', methods=['POST'])
def viewfile():
    keys = []
    if "bucketname" in session:
        bucketname = session["bucketname"]
        print('bucketname'+bucketname)
        response = s3.list_objects_v2(Bucket=bucketname)
        print(response)
        for obj in response['Contents']:
         keys.append(obj['Key'])
    return keys


#downloading the files from S3
@auth.route('/downloadfiles', methods=['GET', 'POST'])
def downloadfile():
    
        return 'download successful!'