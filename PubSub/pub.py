from google.cloud import pubsub_v1

project_id = "esercizio1a"
topic_name = "sacTest"

publisher = pubsub_v1.PublisherClient()
topic_path = f"projects/{project_id}/topics/{topic_name}"

resp = publisher.publish(topic_path, b'publish message with attributes', attr1='1',attr2 = '2')

print(resp.result())
print("Published message")