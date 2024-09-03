import boto3
import concurrent.futures
import logging

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
        'ap-northeast-3'
    ]

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(delete_clusters_in_region, regions)

if __name__ == "__main__":
    main()