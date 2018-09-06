class Pitch:

    all_pitches = []

    def __init__(self,title,pitch):
        # self.movie_id = movie_id
        self.title = title
        # self.imageurl = imageurl
        self.pitch = pitch


    def save_pitch(self):
        Pitch.all_pitches.append(self)


    @classmethod
    def clear_pitch(cls):
        Pitch.all_pitches.clear()