from app import db, create_app


def before_feature(context, feature):
    context.app = create_app('testing')
    context.client = context.app.test_client()
    context.db = db

    # binds the app to the current context
    with context.app.app_context():
        # create all tables
        context.db.create_all()


def after_feature(context, feature):
    with context.app.app_context():
        context.db.session.remove()
        context.db.drop_all()
