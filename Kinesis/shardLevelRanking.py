import json
import subprocess
import sys

def getMetrics(shard_list):

    metric_dict = {}

    for shard in shard_list:
        #cmd2 = 'aws cloudwatch get-metric-statistics --namespace AWS/Kinesis --metric-name IncomingRecords --start-time 2019-03-19T22:52:00 --end-time 2019-03-20T22:52:00 --period 60 --statistic Sum --dimensions Name=StreamName,Value='+stream_name+' Name=ShardId,Value='+shard
        cmd2 = 'aws cloudwatch get-metric-statistics --namespace AWS/Kinesis --metric-name '+metric_name+' --start-time '+start_time+' --end-time '+end_time+' --period 60 --statistic Sum --dimensions Name=StreamName,Value='+stream_name+' Name=ShardId,Value='+shard

        temp_list2 = cmd2.split()

        out = subprocess.Popen(temp_list2, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout, stderr = out.communicate()

        my_json = stdout.decode('utf8')
        data = json.loads(my_json)

        if len(data["Datapoints"]) == 0:
            continue

        # print(data["Datapoints"])

        temp_list3 = []
        for i in data["Datapoints"]:
            temp_list3.append(i["Sum"])
            metric_dict[shard] = sum(temp_list3)

        # print(metric_dict)

    final_result = sorted(metric_dict, key=metric_dict.__getitem__,reverse=True)

    print("Printing the order of shards in desc order for metric",metric_name)
    counter = 1
    for i in final_result:
        print(str(counter)+".",i)
        counter = counter + 1
    print('\n')

def getShards():

    # get the list of shard Id's
    cmd1 = "aws kinesis list-shards --stream-name " + stream_name

    temp_list1 = cmd1.split()

    out = subprocess.Popen(temp_list1, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, stderr = out.communicate()

    msg = stdout.decode('utf8')
    # print(msg)

    if "error" in msg.split():
        sys.exit(msg);

    data = json.loads(msg)
    # print(data)

    data_list = data["Shards"]

    shard_list = []
    for shard in data_list:
        shard_list.append(shard["ShardId"])

    # print(shard_list)
    print("Getting the shard list..\n")
    getMetrics(shard_list)


while 1:
    print("Enter Stream name:", end='')
    stream_name = input()

    # valid Metrics are ['IncomingBytes','IncomingRecords','IteratorAgeMilliseconds','OutgoingBytes','OutgoingRecords','ReadProvisionedThroughputExceeded','WriteProvisionedThroughputExceeded']
    print("Enter a metric name:", end='')
    metric_name = input()

    # date format YYYY-MM-DDThh:mm:ss
    print("Enter the start time:", end='')
    start_time = input()

    print("Enter the end time:", end='')
    end_time = input()

    getShards()

    print("Check for other shard metrics? y/n:")
    user_inp = input()

    if user_inp == 'y' or user_inp == 'Y':
        continue
    else:
        sys.exit("Exiting..")
