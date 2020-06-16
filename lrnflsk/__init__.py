from lrnflsk.factories.flask_app import create_app
from lrnflsk.factories.celery_app import configure_celery


def create_full_app():
    app = create_app()
    configure_celery(app)
    return app


##
# Currently to run the application:
#  FLASK_APP = lrnflsk:create_full_app() --> flask run
#  celery -A lrnflsk.celery_worker.celery worker