from google.cloud import pubsub_v1

project_id = "esercizio1a"
sub_name = "subSacTest"

subscriber = pubsub_v1.SubscriberClient()
sub_path = subscriber.subscription_path(project_id,sub_name)

def callback(message):
    print(f"{message}")
    message.ack()

sub_pull = subscriber.subscribe(sub_path,callback=callback)

try:
    sub_pull.result(timeout=10)
except:
    sub_pull.cancel()
    