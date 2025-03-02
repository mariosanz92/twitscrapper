from ..config import db


class UserOperations(db.EmbeddedDocument):
    mentions = db.BooleanField(default=False)
    followers = db.BooleanField(default=False)
    following = db.BooleanField(default=False)
    lists = db.BooleanField(default=False)
    profession = db.BooleanField(default=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mentions = False
        self.followers = False
        self.following = False
        self.lists = False
        self.profession = False

    def has(self, operation):
        return getattr(self, operation)

    def mark(self, operation):
        setattr(self, operation, True)

    def unmark(self, operation):
        setattr(self, operation, False)

class User(db.Document):
    id = db.IntField(db_field='id', primary_key=True)
    name = db.StringField()
    handle = db.StringField()
    followers = db.IntField()
    following = db.IntField()
    tweets = db.IntField()
    profile_pic = db.StringField()
    description = db.StringField()
    location = db.StringField()
    created_at = db.DateTimeField()
    url = db.StringField()
    verified = db.BooleanField()
    profession = db.StringField()

    follower_list = db.ListField(db.IntField(), default=list)

    operations = db.EmbeddedDocumentField(UserOperations)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.operations = UserOperations()
        self.follower_list = []

    def __str__(self):
        return "@{}".format(self.name)

    def add_follower(self, user_id):
        self.mark('followers')
        self.follower_list.append(user_id)

    def add(self, field, value):
        setattr(self, field, value)

    def has(self, operation):
        return self.operations.has(operation)

    def mark(self, operation):
        return self.operations.mark(operation)

    def unmark(self, operation):
        return self.operations.unmark(operation)

    @staticmethod
    def from_json(json):
        metrics = json['public_metrics']
        user = User(
            id=json['id'],
            handle=json['username'],
            name=json['name'],
            followers=metrics['followers_count'],
            following=metrics['following_count'],
            tweets=metrics['tweet_count'],
            profile_pic=json['profile_image_url'],
            description=json['description'],
            url=json['url'],
            created_at=json['created_at'],
            verified=json['verified'],
        )

        if 'location' in json:
            user.location = json['location']

        user.save()
        return user
