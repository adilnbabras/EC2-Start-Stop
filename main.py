import boto3 #pip3 install boto3
import time


G = '\033[92m'  # green
Y = '\033[93m'  # yellow
B = '\033[94m'  # blue
R = '\033[91m'  # red
W = '\033[0m'   # white

global INST_IDs
INST_IDs = ["{Instance-Id}"]           # created ec2 instance ID
AWSSecretKey = "{Your-secret-Key}"         # Amazon console secret key
AWSAccessKeyId = "{Key-Id}"       # Amazon console access key
mon_ips = ['{ip-one}','ip-two'] # IP addresses to takeover

# connect to ec2 service with provided keys
ecc2 = boto3.client(
    'ec2',
    aws_access_key_id=AWSAccessKeyId,
    aws_secret_access_key=AWSSecretKey,
    region_name='eu-west-1'
)


# extract PublicIp with instance ID
def get_ip(ec2):
    ips = []
    response = ec2.describe_instances(InstanceIds=INST_IDs)
    for inst in response['Reservations']:
        for i in inst['Instances']:
            for ii in i['NetworkInterfaces']:
                ips.append(ii['Association']['PublicIp'])
    return ips


# stop ec2 with instance ID
def stop_ec2(ec2):
    response = ec2.stop_instances(InstanceIds=INST_IDs, Hibernate=False, Force=True)
    #print(response)
    print("---------------")
    print(Y + "Stopping Service" + W)
    time.sleep(60)
    print(R + "Service Stopped" + W)
    print("---------------")

def start_ec2(ec2):
    response = ec2.start_instances(InstanceIds=INST_IDs)
    #print(response)
    print("---------------")
    print(Y + "Starting Service" + W)
    time.sleep(60)
    print(G + "Service Started" + W)
    print("---------------")


if __name__ == "__main__":
    found = False
    
    # start and stop ec2 instance until we acquire IP 
    while not found:
        start_ec2(ecc2)
        ip = get_ip(ecc2)[0]
        print(Y + f"Current Instance IP is {G}{ip} "+ W)
        for i in mon_ips:
            if ip == i:
                found = True
                print(G + f"Matched: {Y}{i} {G}= {Y}{ip}"+ W)
                break
            else:
                print(R + f"Not Matched: {Y}{i} {R}!= {Y}{ip}" + W)

        if not found:
            print(G + "-- Trying Again --" + W)
            time.sleep(3)
            stop_ec2(ecc2)
