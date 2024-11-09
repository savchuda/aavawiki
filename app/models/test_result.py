from app import db

class TestResult(db.Model):
    __tablename__ = 'test_results'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    score = db.Column(db.String) # JSON stringify 
    sdt_rose = db.Column(db.String) # JSON stringify 
    date_taken = db.Column(db.DateTime, default=db.func.current_timestamp())
