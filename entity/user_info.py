class UserInfo:
    def __init__(self, question=None, address=None, create_time=None,
                 id=None, header=None, uuid=None, answer=None, model=None, msg=None):
        self.id = id
        self.question = question
        self.address = address
        self.header = header
        self.create_time = create_time
        self.uuid = uuid
        self.answer = answer
        self.model = model
        self.msg = msg
