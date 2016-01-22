import vk_api
import os
import datetime
import time


class Post(object):
    message = ""
    pictures = ""
    pictures_id = ""
    attachments = ""
    publish_date = ""
    owner_id = ""
    signed = 1
    group_id = 0
    url_to_post = ""

    def __init__(self, group_id):
        self.message = ""
        self.pictures = ""
        self.pictures_id = ""
        self.attachments = ""
        self.publish_date = ""
        self.owner_id = ""
        self.signed = 1
        self.group_id = vk_api.get_group_id_by_url(group_id)
        self.owner_id = -abs(int(self.group_id))
        url_to_post = ""


    def add_text(self, text):
        self.message = text

    def add_picture(self, path_to_pic):
        assert os.path.exists(path_to_pic)
        photo_id = vk_api.upload_picture_to_group_from_hdd(self.group_id, path_to_pic)
        if self.attachments:
            self.attachments = self.attachments + "," + photo_id
        else:
            self.attachments = photo_id

    def set_time(self, hour, date_to_skip=0):
        hour = int(hour)
        # TODO improve this code!
        today = datetime.datetime.now()
        secs_in_day = 60*60*24
        set_time = datetime.datetime(today.year, today.month, today.day, hour, 0)
        utc_time = time.mktime(set_time.timetuple())
        utc_time += date_to_skip * secs_in_day
        self.publish_date = int(utc_time)

    def publish(self):
        params = []
        if self.signed:
            params.append(("signed", self.signed))
        if self.owner_id:
            params.append(("owner_id", self.owner_id))
        if self.message:
            params.append(("message", self.message))
        if self.attachments:
            params.append(("attachments", self.attachments))
        if self.publish_date:
            params.append(("publish_date", self.publish_date))
        # print(params)
        return vk_api.call_api("wall.post", params, POST=True)

if __name__ == "__main__":
    import config
    p = Post(config.vk_group)
    p.add_picture("/Users/onotole/Yandex.Disk.localized/IMG_1396.PNG")
    p.add_picture("/Users/onotole/Yandex.Disk.localized/Downloads/Man_reading_512.png")
    p.add_text("Pewpew")
    p.set_time(10, 1)
    print (p.publish())