from google.cloud import firestore

db = firestore.Client()
music_ref = db.collection(u'musicCatalog')


class MusicCatalog(object):
    def __init__(self):
        pass

    def get_disc(self, disc_id, artist_id):
        disc = music_ref.document(artist_id).collection("DiscInfo").document(disc_id)
        return disc.get().to_dict()

    def post_disc(self, disc_id, artist_id, name, year, genre):
        try:
            ref = music_ref.document(artist_id).collection("DiscInfo").document(disc_id)
            ref.set({
                'name': name,
                'genre': genre,
                'year': year
            })
            return True
        except Exception:
            return False       

    def get_artist(self, artist_id):
        return music_ref.document(artist_id).get().to_dict()

    def post_artist(self, artist_id, name):
        try:
            ref = music_ref.document(artist_id)
            ref.set({
                'name': name
            })
            return True
        except Exception:
            return False
    
    def get_genre(self, genre):
        ref = []

        for artist in music_ref.get():
            discs = music_ref.document(artist.id).collection(u'DiscInfo').get()
            for disc in discs:
                if genre == disc.to_dict()['genre']:
                    ref.append(disc.to_dict())
        return ref