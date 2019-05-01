import boto3
import psycopg2 # install using:  pip install psycopg2-binary

client = boto3.client('s3')

# specify the date in the prefix below, example: if you want all manifests of 19th April set prefix below as:  "errors/manifests/2019/04/19"
response = client.list_objects(Bucket='UserEventsRawData', Prefix="errors/manifests/2019/04/18") # get all manifests of 18th April
x = response["Contents"]

new_list = []
for i in x:
    new_list.append("s3://yourbucketname/" + i["Key"])
    print("s3://yourbucketname/" + i["Key"])

# print(new_list)
try:
    # enter your details below
    conn = psycopg2.connect(database = "your-database-name", user = "user-name", password = "your-password", host = "xx.xx.us-east-1.redshift.amazonaws.com", port = "5439")

except:
    print("Connection to Database failed to establish")

cur = conn.cursor()
try:

    for url in new_list:

        # you may change the COPY command as required
        print("COPY yourbucketname FROM "+ url +" iam_role 'arn:aws:iam::xxxx:role/xxx' MANIFEST maxerror 1000 FILLRECORD TRUNCATECOLUMNS ACCEPTINVCHARS;")
        cur.execute(("COPY yourbucketname FROM "+ url +" iam_role 'arn:aws:iam::xxxx:role/xxx' MANIFEST maxerror 1000 FILLRECORD TRUNCATECOLUMNS ACCEPTINVCHARS;"))
        conn.commit()

except:
    print("Did not work")

conn.commit()
conn.close()
cur.close()
