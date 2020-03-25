class User_data:

    def __init__(self, pdata=None, slot_data=None, state=None, filename=None, locations=(None,None,None), imgurl=None, end_flag=True):
        self.pdata = pdata
        self.slot_data = slot_data
        self.state = state
        self.filename = filename
        self.locations = locations
        self.imgurl = imgurl
        self.end_flag = end_flag