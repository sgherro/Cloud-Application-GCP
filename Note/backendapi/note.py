from google.cloud import firestore

db = firestore.Client()
note_ref = db.collection(u'note')


class Note(object):
    def __init__(self):
        pass

    def get_note(self, owner_id, note_id):
        note = note_ref.document(owner_id).collection(u"Note").document(note_id)
        return note.get().to_dict()

    def post_note(self, owner_id, note_id, context):
        try:
            owner_ref = note_ref.document(owner_id)
            owner_ref.set({
                'id': note_id
            }) #senza questo perde di cosistenza
            ref = owner_ref.collection(u"Note").document(note_id)
            ref.set({
                'context': context, 
                'id': note_id
            })
        except Exception:
            return False

    def share_note(self, owner_id, recipient_id, note_id):
        note = note_ref.document(owner_id).collection(u"Note").document(note_id).get().to_dict()
        try:
            ref = note_ref.document(recipient_id).collection(u"Note").document(note_id)
            note_id = f'{note_id} (Shared)'
            ref.set({
                'id': note_id,
                'context': note['context']
            })
        except Exception:
            return False

    def check_note(self, owner_id):
        notes = note_ref.document(owner_id).collection(u'Note').get()
        for n in notes:
            if n.exists:
                return True
        return False

    def get_address(self, note_id):
        owners = note_ref.get()
        for owner in owners:
            notes = note_ref.document(owner.id).collection(u'Note').get()
            for n in notes:
                if n.id == note_id:
                    return owner.id, n.id
        return None

        