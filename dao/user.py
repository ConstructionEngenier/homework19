from dao.model.user import User


class UserDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, uid):
        return self.session.query(User).get(uid)

    def get_all(self):
        return self.session.query(User).all()

    def get_filter(self,filter_dict):
        return self.session.query(User).filter_by(**filter_dict).all()

    def create(self, data):
        obj = User(**data)
        self.session.add(obj)
        self.session.commit()
        return obj

    def delete(self, uid):
        obj = self.get_one(uid)
        if obj:
            self.session.delete(obj)
            self.session.commit()
            return obj
        return None

    def update(self, data):
        obj = self.get_one(data.get('id'))
        if obj:
            if data.get('username'):
                obj.username = data.get('username')
            if data.get('password'):
                obj.password = data.get('password')
            if data.get('role'):
                obj.role = data.get('role')
            self.session.add(obj)
            self.session.commit()
            return obj
        return None
