from sqlalchemy.orm import DeclarativeBase, declarative_base



"""
관계성 설정하려면 하나로 설정해야 한다고 함.
따라서 여기서 한번 선언하고 import 해서 다른 모델에 사용하는 걸로 함.
"""
Base: DeclarativeBase = declarative_base()


LocalBase: DeclarativeBase = declarative_base()

