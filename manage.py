from manager import Manager


from dating_grabber.models import Base, engine


manager = Manager()


@manager.command
def create_db():
    """Create tables"""
    Base.metadata.create_all(engine)


@manager.command
def drop_db():
    """Create tables"""
    Base.metadata.drop_all(engine)


if __name__ == '__main__':
    manager.main()
