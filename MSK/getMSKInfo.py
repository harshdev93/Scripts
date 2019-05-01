# Prerequisites:
# Upgrade botocore and boto3 to the latest version as older version do not support kafka
# pip install botocore --upgrade
# pip install boto3 --upgrade

import boto3

client = boto3.client('kafka')

listCluster_response = client.list_clusters()

cluster_list = listCluster_response["ClusterInfoList"]
print("Total number of MSK clusters:", len(cluster_list), "\n")
# print(listCluster_response["ClusterInfoList"][0]["ClusterArn"])

i = 0
for cluster in cluster_list:
    print("Details on MSK cluster:", i)
    print("clusterArn:", cluster["ClusterArn"], '\n')

    clusterArn = cluster["ClusterArn"]

    describeCluster_response = client.describe_cluster(ClusterArn=clusterArn)
    print("ClusterInfo", describeCluster_response["ClusterInfo"], '\n')
    print("ZookeeperConnectString:", describeCluster_response["ClusterInfo"]["ZookeeperConnectString"], '\n')

    bootstrap_brokers = client.get_bootstrap_brokers(ClusterArn=clusterArn)
    print("Bootstrap Brokers:", bootstrap_brokers["BootstrapBrokerString"])
    i = i + 1



