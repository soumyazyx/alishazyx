import json
import re
import urllib.request

import requests
from django.core.files import File

from bot.models import TelegramMessage
from hello.models import Product, Category, ProductImage

base_url = "https://api.telegram.org/"
bot_token = "1220904092:AAFa_l0w-ycsnldjLpk_noalgGRk0g0PMJo"
default_photo_url = "https://res.cloudinary.com/hxjbk5wno/image/upload/v1594845942/logo_alisha_min_vra4dr.png"


def save_telegram_message(update_id, json_msg):

    try:
        telegram_msg = TelegramMessage(update_id=update_id, json_msg=json_msg)
        telegram_msg.save()
        return telegram_msg.id
    except Exception as e:
        print("Failed to save telegram message: " + str(e))
        return -1


def scan_messages():

    print("Fetching ALL telegram messages from DB..")
    telegram_msges_qs = TelegramMessage.objects.all()
    print("Fetching ALL telegram messages from DB..Done")

    print("Analysing messages to find potential products..")
    all_blocks = split_msges_to_blocks(telegram_msges_qs)
    print("Analysing messages to find potential products..Done")

    # print("Creating new products..")
    # save_products(all_blocks)
    # print("Creating new products..Done")


def split_msges_to_blocks(telegram_msges_qs):
    '''Takes in ALL the messages and splits into blocks
    Each block starts with 'startzyx' and ends with 'endzyx' 
    startzyx & endzyx behave as markers here
    '''
    start_marker = 'startzyx'
    end_marker = 'endzyx'
    block_in_progress = False
    each_block = []
    all_blocks = []
    beep = []
    block = {}
    counter = 1
    block = {}
    block['text'] = []
    block['desc'] = ''
    block['title'] = ''
    block["photos"] = []

    for telegram_record in telegram_msges_qs:

        line = ""
        message = json.loads(telegram_record.json_msg)

        if "text" in message["message"]:
            line = message["message"]["text"]
            if line.strip().lower() == start_marker:
                block_in_progress = True
                block = {}
                block['text'] = []
                block['desc'] = ''
                block['title'] = ''
                block["photos"] = []
            elif line.strip().lower() == end_marker and block_in_progress:
                block_in_progress = False
                beep.append(block)
                block = {}
                block['text'] = []
                block['desc'] = ''
                block['title'] = ''
                block["photos"] = []

            elif block_in_progress:
                block["text"].append(line)
        elif ("photo" in message["message"] and block_in_progress):
            line = get_photo_id(message)
            block["photos"].append(line)
        elif ("animation" in message["message"] and block_in_progress):
            pass  # Not supported
        elif ("video" in message["message"] and block_in_progress):
            pass  # Not supported
        # elif "text" in message["message"]
        # line = message["message"]["text"]
        # block["text"].append(line)

        # # Split lines into chunks depending upon startzyx and endzyx
        # if line.strip().lower() == start_marker:
        #     block_in_progress = True
        # elif line.strip().lower() == end_marker and block_in_progress:
        #     block_in_progress = False
        #     all_blocks.append(each_block)
        #     each_block = []
        #     beep.append(block)

        #     counter = counter + 1
        #     block = {}
        #     block['text'] = []
        #     block['desc'] = ''
        #     block['title'] = ''
        #     block["photos"] = []

        # elif block_in_progress:
        #     each_block.append(line)
    # Finished scanning through ALL the messages.Return the list of blocks
    # print(all_blocks)
    print(beep)
    return all_blocks


def save_products(all_blocks):

    titles = Product.objects.values_list('title', flat=True)
    # Each block represents a potential product
    for each_block in all_blocks:
        text = ""
        photos = []
        for item in each_block:
            if item.startswith(base_url) and (bot_token in item) and ("photos" in item):
                photos.append(item)  # most likely a photo file location
            else:
                # At the time of writing, only text and photos are supported
                # So, if it is not a photo, its a 'text' - concatenate.
                text += item

        # Form a PRODUCT Object
        get_product_title_desc_res = get_product_title_desc(text)
        title = get_product_title_desc_res["title"]
        description = get_product_title_desc_res["desc"]
        print("Creating product with title[{}]..".format(title))
        if (title in titles):
            # item already exists. Skip.
            print("Creating product with title[{}]..SKIPPED!".format(title))
            print("Item already exists!")
            continue
        if(len(photos) == 0):
            photo_url = default_photo_url
        else:
            photo_url = photos.pop(0)
        product = Product(
            title=title,
            image=get_photo_from_url(photo_url),
            category=Category.objects.get(id=15),
            description=description
        )
        product.save()
        print("Creating product with title[{}]..Done [productid={}]".format(
            title, product.id))
        print("Adding additional photos for product(if any)..")
        for photo_url in photos:
            productimage = ProductImage(
                product=product,
                image=get_photo_from_url(photo_url))
            productimage.save()
        print("Adding additional photos for product(if any)..Done")
        print("--")


def get_product_title_desc(text):

    #   - PRODUCT has a title and description.
    #   - Attempt to extract the title
    #       - The line generally looks like: Catalog Name: Title goes here
    #       - In few cases, the "Catalog Name" is not present.
    #           - In such cases fall back to use the first line as title
    desc = []
    title = ""
    for line in text.splitlines():
        if re.search("Catalog Name", line, re.IGNORECASE):
            # We found the line. Ex. Catalog Name: blah blah blah
            # Strip off the 'Catalog Name' so that we end up with 'blah blah blah' as title
            # Using regex substitution to do so - substitute 'Catalog Name' with ''
            title = re.sub("Catalog\s*Name:?", "", line, flags=re.IGNORECASE)
            title = re.sub("^\*", "", title)
            title = re.sub("\s*\*\s*$", "", title)
        else:
            desc.append(line)

    if title == "":
        # It means there is NO line matching 'Catalog Name'.
        # In such csaes, use the first line as title
        title = desc.pop(0)
    desc = "\n".join(desc)
    return {"title": title, "desc": desc}


def get_photo_id(message):
    """It takes in the message and returns the file_id LARGEST photo file 
    """

    # Telegram returns an array containing more than one version of the photo file
    # The photo files vary in size and shape
    # Most likely - the last entry of the array is the largest file
    # But just to be sure, loop over them and find the largest one manually
    file_size = 0  # Stores the max file size
    file_id = 0  # Stored the id corresponding to max file size
    for photo_file in message["message"]["photo"]:
        if photo_file["file_size"] > file_size:
            file_size = photo_file["file_size"]
            file_id = photo_file["file_id"]
    # Fetch the relatve file path from the fileid fetched above
    # https://api.telegram.org/bot<secretid>/getFile?file_id=<fileid>
    # url = "https://api.telegram.org/bot{}/getFile?file_id={}".format(
    #     bot_token, file_id)
    # file_path = requests.get(url).json()["result"]["file_path"]
    # Form the "fully qualified" path to the photo file
    # https://api.telegram.org/file/bot<secretid>/<file_path>
    # photo_url = "https://api.telegram.org/file/bot{}/{}".format(
    #     bot_token, file_path)
    return file_id


def get_photo_from_url(photo_url):
    print("Downloading image from URL[{}]..".format(photo_url))
    opener = urllib.request.build_opener()
    opener.addheaders = [("User-agent", "Mozilla/5.0")]
    urllib.request.install_opener(opener)
    result = urllib.request.urlretrieve(photo_url)
    reopen = open(result[0], "rb")
    django_file = File(reopen)
    print("Downloading image from URL[{}]..Done".format(photo_url))
    return django_file


def get_categories():
    print("get categories")
    categories = Category.objects.all()
    print(categories)
    for category in categories:
        print(category.id)
        print(category.sequence)
        print(category.name)
