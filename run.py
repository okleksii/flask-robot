from app import app
from app.user import views
from app.course import views
from app.main import views

if __name__ == '__main__':
    app.run(port=app.config.get("PORT"))
