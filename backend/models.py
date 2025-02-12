from config import db

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255), nullable=True)
    type = db.Column(db.String(10), nullable=False)  # "Income" or "Expense"
    balance = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=True)  # Adding category field for later use

    def __repr__(self):
        return f"<Transaction {self.id} - {self.amount} - {self.category}>"
    
    def to_json(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "amount": self.amount,
            "category": self.category,  # will add keyword-based categorization
            "date": self.date.strftime('%Y-%m-%d') if self.date else None,  # Formatting date
            "description": self.description,
            "type": self.type,
            "balance": self.balance
        }


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique ID for each user
    email = db.Column(db.String(120), unique=True, nullable=False)  # Unique email
    password_hash = db.Column(db.String(255), nullable=False)  # Hashed password
    transactions = db.relationship('Transaction', backref='user', lazy=True)  # One-to-many relationship

    def __repr__(self):
        return f'<User {self.email}>'
    
    def to_json(self):
        return {
            "id": self.id,
            "email": self.email
        }
    
    
    

