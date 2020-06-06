from google.cloud import firestore
from flask import request
import json
from google.cloud import pubsub_v1

db = firestore.Client(project='airports-project')
    
def http_visiting(request):
    if request.method == 'GET':
        return '', 200
    if request.method == 'POST':
        ref = request.get_json()
        if ref['page']:
            page = ref['page']
            try:  
                db.collection(u'visits').document(page).update({
                'counter': firestore.Increment(1)
            })            
            except Exception:
                db.collection(u'visits').document(page).set({
                    'counter': 1
                })
        return '', 200

def visiting_counting(data, context):
    """ Triggered by a change to a Firestore document.
    Args:
        data (dict): The event payload.
        context (google.cloud.functions.Context): Metadata for the event.
    """

    project_id = 'airports-project'
    topic = 'visits'

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic) #pylint: disable=no-member

    trigger_resource = context.resource
    page = json.dumps(trigger_resource.split('/')[-1])
    number = json.dumps(data["value"]["fields"]["counter"]["integerValue"]) #valore di counter dentro al db firestore

    publisher.publish(topic_path, f'number of visits of the page {page}'.encode('ascii'), number=number)

    print(f'published message on {topic} topic: page {page}, number {number}')
