import logging
import os
import vk_auth
from vk_auth import call_api,token,APIErrorException,InvalidUserIDError
import requests


def get_group_id_by_url(url2group):
    """
    >>> get_group_id_by_url("http://vk.com/team")
    22822305
    >>> get_group_id_by_url(22822305)
    22822305
    >>> get_group_id_by_url("22822305")
    22822305
    >>> get_group_id_by_url("vk.com/team")
    22822305
    """
    logging.debug("start get_group_id_by_url")
    if str(url2group).isdigit():
        return int(url2group)
    url2group = url2group.split('/')[-1]
    group_info = call_api("groups.getById", [("group_id", url2group)])

    group_id = group_info[0]["gid"]
    return group_id


def get_all_posts(group_id):
    all_posts = []
    group_id = get_group_id_by_url(group_id)
    if int(group_id) > 0:
        group_id = str(-int(group_id))
    posts_data_raw = call_api("wall.get", [("owner_id", group_id), ("count", 1)])
    count = 100
    offset = -count
    while offset + count < posts_data_raw[0]:
        offset += count
        posts_data_raw = call_api("wall.get", [("owner_id", group_id), ("count", count),
                                               ("offset", offset)])
        all_posts += posts_data_raw[1:]
    return all_posts


def get_name_by_id(user_id):
    user_id = str(abs(int(user_id)))
    response = call_api("users.get", [("user_ids", user_id)])
    try:
        result = response[0]["first_name"]+ " " + response[0]["last_name"]
    except IndexError:
        print user_id
        raise
    return result


def get_user_id(username):
    username = username.split('/')[-1]
    try:
        result = call_api("users.get", [("user_ids", username)])
    except APIErrorException:
        raise InvalidUserIDError
    real_user_id = result[0]["uid"]
    return real_user_id


def upload_picture_to_group_from_hdd(group_id, picture_path, force=False):
    # picture_description = "blah"
    statinfo = os.stat(picture_path)
    # if not force and statinfo.st_size < config.small_picture_limit:
    #     return False
    group_id = get_group_id_by_url(group_id)
    if int(group_id) < 0:
        group_id = str(-int(group_id))
    answer = call_api("photos.getWallUploadServer", [("group_id", group_id)])

    album_id = answer["aid"]
    upload_url = answer["upload_url"]
    files = {'file': open(picture_path, 'rb')}
    r = requests.post(upload_url, files=files)

    photo_id = r.json()["photo"]
    photo_hash = r.json()["hash"]
    photo_server = r.json()["server"]
    result_uploading_photo = call_api("photos.saveWallPhoto", [("group_id", group_id),
                                                               ("photo", photo_id),
                                                               ("server", photo_server),
                                                               ("hash", photo_hash)])

    return result_uploading_photo[0]["id"]

if __name__ == "__main__":
    import config
    print(upload_picture_to_group_from_hdd(config.vk_group, "/Users/onotole/Yandex.Disk.localized/IMG_1396.PNG"))