import datetime


class func():
    def __init__(self):
        self.func = ['gettime']

    def get_date():
      x = datetime.datetime.now()
      err = datetime.timedelta(hours=8)
      x += err
      y = x.year
      m = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul',
            'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][x.month - 1]
      d = x.day
      h = x.hour
      mi = x.minute
      s = x.second
      w = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu',
            'Fri', 'Sat'][(x.weekday() + 1) % 7]
      res = '{} {} {:02d} {} {:02d}:{:02d}:{:02d}'.format(
          y, m, d, w, h, mi, s)
      return res
    def get_time():
      return datetime.datetime.now().strftime("%y %m %d")


def To_string(list_: list):
  string = f" price: {list_[0]}\n min price: {list_[1]}\n price difference: {list_[2]}\n last time it get data : {list_[3]}"
  return string