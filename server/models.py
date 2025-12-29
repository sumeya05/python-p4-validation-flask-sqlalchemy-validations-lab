from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String(10), nullable=False)

    posts = db.relationship('Post', backref='author', lazy=True)

    @validates('phone_number')
    def validate_phone_number(self, key, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must be exactly 10 digits")
        return value

    @validates('name')
    def validate_name(self, key, value):
        if not value:
            raise ValueError("Author must have a name")
        return value

    def __init__(self, **kwargs):
        # Check for name uniqueness before initialization
        if 'name' in kwargs:
            existing_author = Author.query.filter_by(name=kwargs['name']).first()
            if existing_author:
                raise ValueError("Author name must be unique")
        super(Author, self).__init__(**kwargs)


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.Text, nullable=False)
    summary = db.Column(db.String(250), nullable=False)
    category = db.Column(db.String, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'), nullable=False)

    @validates('content')
    def validate_content(self, key, value):
        if len(value) < 250:
            raise ValueError("Content must be at least 250 characters long")
        return value

    @validates('summary')
    def validate_summary(self, key, value):
        if len(value) > 250:
            raise ValueError("Summary must be 250 characters or fewer")
        return value

    @validates('category')
    def validate_category(self, key, value):
        if value not in ["Fiction", "Non-Fiction"]:
            raise ValueError("Category must be either 'Fiction' or 'Non-Fiction'")
        return value

    @validates('title')
    def validate_title(self, key, value):
        clickbait_keywords = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(keyword in value for keyword in clickbait_keywords):
            raise ValueError(f"Title must contain one of: {', '.join(clickbait_keywords)}")
        return value
