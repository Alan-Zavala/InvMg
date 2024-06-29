from app import db, create_app
from app.models import User  # Import your User model

app = create_app()

if __name__ == '__main__':
    print("Creating database tables...")
    with app.app_context():
        # Create the database tables if they don't exist
        db.create_all()
        
        # Add values to the database - developtment
        print("Adding values to the database...")
        new_user = User(username='master', password='1234', first_name='Alan', last_name='Zavala', role='admin')
        existing_user = User.query.filter_by(username=new_user.username).first()

        if existing_user:
            print('Username is already taken. Deleting user...')
            db.session.delete(existing_user)
            db.session.commit()

        db.session.add(new_user)
        db.session.commit()
                
    print("Database tables created successfully!")
    app.run(debug=True)
