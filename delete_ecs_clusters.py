import boto3
import concurrent.futures
import logging
import sys
import time  

# Delete Clusters (add regions)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def delete_service(ecs_client, cluster, service):
    try:
        ecs_client.update_service(cluster=cluster, service=service, desiredCount=0)
        ecs_client.delete_service(cluster=cluster, service=service)
        logger.info(f"Deleted service {service} in cluster {cluster}")
    except Exception as e:
        logger.error(f"Error deleting service {service} in cluster {cluster}: {str(e)}")

def delete_cluster(ecs_client, cluster):
    try:
        # Delete services
        services = ecs_client.list_services(cluster=cluster)['serviceArns']
        for service in services:
            delete_service(ecs_client, cluster, service)

        # Deregister container instances
        instances = ecs_client.list_container_instances(cluster=cluster)['containerInstanceArns']
        if instances:
            ecs_client.deregister_container_instance(cluster=cluster, containerInstance=instances[0], force=True)

        # Delete the cluster
        ecs_client.delete_cluster(cluster=cluster)
        logger.info(f"Deleted cluster {cluster}")
    except Exception as e:
        logger.error(f"Error deleting cluster {cluster}: {str(e)}")

def delete_clusters_in_region(region):
    ecs_client = boto3.client('ecs', region_name=region)
    try:
        clusters = ecs_client.list_clusters()['clusterArns']
        logger.info(f"Found {len(clusters)} clusters in region {region}")
        for cluster in clusters:
            delete_cluster(ecs_client, cluster)
    except Exception as e:
        logger.error(f"Error processing region {region}: {str(e)}")

def main():
    regions = [
        'ap-northeast-3','ap-northeast-3', 'us-east-1', 'us-east-2', 'us-west-1', 'us-west-2',
        'ap-south-1', 'ap-northeast-2', 'ap-southeast-1', 'ap-southeast-2',
        'ap-northeast-1', 'ca-central-1', 'eu-central-1', 'eu-west-1',
        'eu-west-2', 'eu-west-3', 'eu-north-1', 'sa-east-1',
        'ap-east-1', 'me-south-1', 'af-south-1'
    ]

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(delete_clusters_in_region, regions)

if __name__ == "__main__":
    main() 





# Delete task definitions (add regions) ==> for avtive tasks



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def delete_service(ecs_client, cluster, service):
    try:
        ecs_client.update_service(cluster=cluster, service=service, desiredCount=0)
        ecs_client.delete_service(cluster=cluster, service=service)
        logger.info(f"Deleted service {service} in cluster {cluster}")
    except Exception as e:
        logger.error(f"Error deleting service {service} in cluster {cluster}: {str(e)}")

def delete_cluster(ecs_client, cluster):
    try:
        # Delete services
        services = ecs_client.list_services(cluster=cluster)['serviceArns']
        for service in services:
            delete_service(ecs_client, cluster, service)

        # Deregister container instances
        instances = ecs_client.list_container_instances(cluster=cluster)['containerInstanceArns']
        if instances:
            ecs_client.deregister_container_instance(cluster=cluster, containerInstance=instances[0], force=True)

        # Delete the cluster
        ecs_client.delete_cluster(cluster=cluster)
        logger.info(f"Deleted cluster {cluster}")
    except Exception as e:
        logger.error(f"Error deleting cluster {cluster}: {str(e)}")

def delete_clusters_in_region(region):
    ecs_client = boto3.client('ecs', region_name=region)
    try:
        clusters = ecs_client.list_clusters()['clusterArns']
        logger.info(f"Found {len(clusters)} clusters in region {region}")
        for cluster in clusters:
            delete_cluster(ecs_client, cluster)
    except Exception as e:
        logger.error(f"Error processing region {region}: {str(e)}")

def main():
    regions = [
        'ap-northeast-3', 'us-east-1', 'us-east-2', 'us-west-1', 'us-west-2',
        'ap-south-1', 'ap-northeast-2', 'ap-southeast-1', 'ap-southeast-2',
        'ap-northeast-1', 'ca-central-1', 'eu-central-1', 'eu-west-1',
        'eu-west-2', 'eu-west-3', 'eu-north-1', 'sa-east-1',
        'ap-east-1', 'me-south-1', 'af-south-1'
    ]

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(delete_clusters_in_region, regions)

if __name__ == "__main__":
    main()






# Delete task definitions (add regions) ==> for inavtive tasks // this is the first solution




logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def delete_task_definition(ecs_client, task_definition_arn):
    try:
        # Deregister the task definition
        ecs_client.deregister_task_definition(taskDefinition=task_definition_arn)
        logger.info(f"Deregistered inactive task definition {task_definition_arn}")
    except Exception as e:
        logger.error(f"Error deregistering inactive task definition {task_definition_arn}: {str(e)}")

def delete_task_definitions_in_region(region):
    ecs_client = boto3.client('ecs', region_name=region)
    try:
        # List only inactive task definitions
        paginator = ecs_client.get_paginator('list_task_definitions')
        inactive_count = 0
        for page in paginator.paginate(status='INACTIVE'):
            for task_definition_arn in page['taskDefinitionArns']:
                delete_task_definition(ecs_client, task_definition_arn)
                inactive_count += 1
        logger.info(f"Processed {inactive_count} inactive task definitions in region {region}")
    except Exception as e:
        logger.error(f"Error processing region {region}: {str(e)}")

def main():
    regions = [
        'ap-northeast-3', 'us-east-1', 'us-east-2', 'us-west-1', 'us-west-2',
        'ap-south-1', 'ap-northeast-2', 'ap-southeast-1', 'ap-southeast-2',
        'ap-northeast-1', 'ca-central-1', 'eu-central-1', 'eu-west-1',
        'eu-west-2', 'eu-west-3', 'eu-north-1', 'sa-east-1',
        'ap-east-1', 'me-south-1', 'af-south-1'
    ]

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(delete_task_definitions_in_region, regions)

if __name__ == "__main__":
    main()



# Delete task definitions (add regions) ==> for inavtive tasks // this is the second solution
# I found this solution here ==>https://github.com/dannysteenman/aws-toolbox/blob/main/ecs/ecs_delete_inactive_task_definitions.py


def get_inactive_task_definition_arns(region):
    client = boto3.client("ecs", region_name=region)
    arns = []
    paginator = client.get_paginator("list_task_definitions")
    for page in paginator.paginate(status="INACTIVE"):
        arns.extend(page.get("taskDefinitionArns", []))
    return arns


def delete_task_definition(region, arn):
    client = boto3.client("ecs", region_name=region)
    max_retries = 5
    backoff = 1  # Initial backoff time in seconds
    for attempt in range(1, max_retries + 1):
        try:
            client.delete_task_definitions(taskDefinitions=[arn])
            print(f"Deleted task definition {arn}")
            break  # Break the loop if deletion was successful
        except client.exceptions.ClientException as e:
            if "Throttling" in str(e):  # Check for throttling in the error message
                print(f"Throttling exception when deleting {arn}: {e}, retrying in {backoff} seconds...")
                time.sleep(backoff)
                backoff *= 2  # Exponential backoff
            else:
                print(f"Client exception when deleting task definition {arn}: {e}")
                break  # Break the loop for other client exceptions
        except client.exceptions.ServerException as e:
            if "Throttling" in str(e):  # Check for throttling in the error message
                print(f"Throttling exception when deleting {arn}: {e}, retrying in {backoff} seconds...")
                time.sleep(backoff)
                backoff *= 2  # Exponential backoff
            else:
                print(f"Server exception when deleting task definition {arn}: {e}")
                break  # Break the loop for other server exceptions
        except Exception as e:
            print(f"Unexpected error deleting task definition {arn}: {e}")
            break  # Break the loop for any other unexpected errors


def delete_inactive_task_definitions_in_region(region):
    try:
        arns = get_inactive_task_definition_arns(region)
        if not arns:
            print(f"No inactive task definitions found in region {region}")
        else:
            for arn in arns:
                delete_task_definition(region, arn)
    except Exception as e:
        print(f"Error accessing region {region}: {e}")


def delete_inactive_task_definitions_in_all_regions():
    ecs_regions = boto3.session.Session().get_available_regions("ecs")
    for region in ecs_regions:
        delete_inactive_task_definitions_in_region(region)


if __name__ == "__main__":
    if len(sys.argv) > 2:
        print("Usage: python script.py [region]")
        sys.exit(1)
    elif len(sys.argv) == 2:
        region = sys.argv[1]
        delete_inactive_task_definitions_in_region(region)
    else:
        delete_inactive_task_definitions_in_all_regions()
