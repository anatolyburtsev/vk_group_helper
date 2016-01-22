import vk_post
import os
from vk_auth import ExistsPostponedPostForThisTimeException

IMAGE_EXTENSION = ["jpg", "jpeg", "png"]


def post_picture_dir(group_id, path_to_dir, time_to_post, text="", delete_pics=False):
    counter = 0

    for filename in os.listdir(path_to_dir):
        path_to_pic = os.path.join(path_to_dir, filename)
        if os.path.isfile(path_to_pic) and (filename.split(".")[-1].lower() in IMAGE_EXTENSION):
            success_posted = False
            p = vk_post.Post(group_id)
            p.add_picture(path_to_pic)
            if text:
                p.add_text(text)
            p.set_time(time_to_post, counter+1)
            while not success_posted:
                try:
                    p.publish()
                except ExistsPostponedPostForThisTimeException:
                    counter += 1
                    p.set_time(time_to_post, counter)
                else:
                    success_posted = True

            if delete_pics:
                os.remove(path_to_pic)
            counter += 1

    return "Picture successfully published"


if __name__ == "__main__":
    print(post_picture_dir("http://vk.com/x_community", "memes_102015", "18", "", True))
