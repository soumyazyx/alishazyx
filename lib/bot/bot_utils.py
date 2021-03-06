import os
import json
import re
import urllib.request

import requests
from django.core.files import File
from django.views.decorators.csrf import csrf_exempt
from bot.models import TelegramMessage
from hello.models import Product, Category, SubCategory, ProductImage

end_marker = "endzyx"
start_marker = "startzyx"
base_url = "https://api.telegram.org/"
bot_token = os.environ["BOT_TOKEN"]
default_title = "Title goes here."
default_desc = "Desc goes here."
default_photo_url = "https://res.cloudinary.com/hxjbk5wno/image/upload/v1594845942/logo_alisha_min_vra4dr.png"
default_subcategory_id = 14  # subcategory - "everything else"


def save_telegram_message(message):

    try:
        body_json = json.loads(message)
        update_id = body_json["update_id"]
        from_id = body_json["message"]["from"]["id"]
        first_name = body_json["message"]["from"]["first_name"]

        print("Saving message to DB..")

        # Check if update_id exist already
        if TelegramMessage.objects.filter(update_id=update_id).exists():
            print("update_id[{}] already exists!".format(update_id))
            print("Saving message to DB..Done [update_id={}]".format(update_id))
            return update_id

        # Record doesn't exist - attempt to insert the record
        telegram_msg = TelegramMessage(from_id=from_id, json_msg=message, update_id=update_id, first_name=first_name,)
        telegram_msg.save()
        print("Saving message to DB..Done [update_id={}]".format(update_id))
        return update_id
    except Exception as e:
        print("Failed to save telegram message: " + str(e))
        print("Saving message to DB..FAILED!")
        return -1


def scan_messages(from_id, update_id, first_name):

    print("Fetching relevant messages from [{}]..".format(first_name))
    telegram_msges_qs = TelegramMessage.objects.filter(
        from_id=from_id,
        update_id__lte=update_id,
        processing_status__iexact="NEW",
    ).order_by("update_id")
    print("Fetching relevant messages from [{}]..Done".format(first_name))
    print("Messages fetched [{}]".format(len(telegram_msges_qs)))
    if len(telegram_msges_qs) == 0:
        return {
            "error": 1,
            "error_msg": "Internal error: No data recieved from DB!",
        }

    print("Changing processing status from [NEW] to [PROCESSING]..")
    TelegramMessage.objects.filter(
        from_id=from_id,
        update_id__lte=update_id,
        processing_status__iexact="NEW",
    ).update(
        processing_status="PROCESSING"
    )
    print("Changing processing status from [NEW] to [PROCESSING]..Done")

    print("Analysing messages to find potential products..")
    all_blocks = split_msges_to_blocks(telegram_msges_qs)
    print("Analysing messages to find potential products..Done")
    if len(all_blocks) == 0:
        return {
            "error": 1,
            "error_msg": "Error: Sufficient information not provided to create a product",
        }

    print("Computing title and desc for all products..")
    all_blocks = compute_title_desc_subcat(all_blocks)
    print("Computing title and desc for all products..Done")

    # print("Check and remove existing products from list..")
    # filtered_blocks = remove_existing_products(all_blocks)
    # print(filtered_blocks)
    # print("Check and remove existing products from list..Done")

    print("Creating new products..")
    save_products_res = save_products(all_blocks)
    print("Creating new products..Done")

    print("Changing processing status from [PROCESSING] to [PROCESSED]..")
    telegram_msges_qs = TelegramMessage.objects.filter(
        from_id=from_id, update_id__lte=update_id, processing_status__iexact="PROCESSING",
    ).update(processing_status="PROCESSED")
    print("Changing processing status from [PROCESSING] to [PROCESSED]..Done")

    # Delete telegram messages which are already [PROCESSED]
    print("Deleting the telegram messages from database..")
    TelegramMessage.objects.filter(processing_status__iexact="PROCESSED").delete()
    print("Deleting the telegram messages from database..Done")

    # Fetch image url from productimage table and update in product table
    # print("Fetching image urls and updating product table..")
    scan_image_urls(save_products_res["product_id"])
    # print("Fetching image urls and updating product table..Done")

    if save_products_res["error"] == 1:
        return {"error": 1, "error_msg": save_products_res["error_msg"]}
    elif save_products_res["error"] == 0:
        return {"error": 0, "product_id": save_products_res["product_id"]}


def split_msges_to_blocks(telegram_msges_qs):
    """Takes in ALL the messages and splits into blocks
    Each block starts with 'startzyx' and ends with 'endzyx'
    startzyx & endzyx behave as markers here
    """

    all_blocks = []
    block_in_progress = False

    for telegram_record in telegram_msges_qs:
        message = json.loads(telegram_record.json_msg)
        if "text" in message["message"]:
            line = message["message"]["text"]
            if line.strip().lower() == start_marker:
                block_in_progress = True
                block = {}
                block["text"] = []
                block["desc"] = ""
                block["title"] = ""
                block["photos"] = []
            elif line.strip().lower() == end_marker and block_in_progress:
                block_in_progress = False
                all_blocks.append(block)
                block = {}
                block["text"] = []
                block["desc"] = ""
                block["title"] = ""
                block["photos"] = []
            elif block_in_progress:
                block["text"].append(line)
        elif "photo" in message["message"] and block_in_progress:
            block["photos"].append(get_photo_id(message))
        elif "animation" in message["message"] and block_in_progress:
            pass  # Not supported
        elif "video" in message["message"] and block_in_progress:
            pass  # Not supported

    return all_blocks


def save_products(all_blocks):

    # Each block represents a new product
    for block in all_blocks:
        try:
            desc = block["desc"]
            title = block["title"]
            subcategory_id = block["subcategory_id"]

            print("Creating product with title[{}]..".format(title))
            product = Product()
            product.title = title
            product.description = desc
            product.subcategory = SubCategory.objects.get(id=subcategory_id)

            # Handle cover image
            photos = block["photos"]
            if len(photos) == 0:
                cover_photo_url = default_photo_url
                cover_photo_obj = get_photo_from_url(cover_photo_url)
                product.coverimage.save("logo.png", cover_photo_obj, save=False)
            else:
                cover_photo_id  = photos.pop(0)
                cover_photo_url = get_photo_url_from_id(cover_photo_id)
                cover_photo_obj = get_photo_from_url(cover_photo_url)
                product.coverimage.save("logo.png", cover_photo_obj, save=False)

            # Handle additional images - WORST POSSIBLE IMPLEMENTATION
            for index, photo_id in enumerate(photos, start=1):
                photo_url = get_photo_url_from_id(photo_id)
                photo_obj = get_photo_from_url(photo_url)
                if(index == 1):  product.additional_image_1.save("logo.jpg", photo_obj, save=False)        
                if(index == 2):  product.additional_image_2.save("logo.jpg", photo_obj, save=False)        
                if(index == 3):  product.additional_image_3.save("logo.jpg", photo_obj, save=False)        
                if(index == 4):  product.additional_image_4.save("logo.jpg", photo_obj, save=False)        
                if(index == 5):  product.additional_image_5.save("logo.jpg", photo_obj, save=False)        
                if(index == 6):  product.additional_image_6.save("logo.jpg", photo_obj, save=False)        
                if(index == 7):  product.additional_image_7.save("logo.jpg", photo_obj, save=False)        
                if(index == 8):  product.additional_image_8.save("logo.jpg", photo_obj, save=False)        
                if(index == 9):  product.additional_image_9.save("logo.jpg", photo_obj, save=False)        
                if(index == 10): product.additional_image_10.save("logo.jpg", photo_obj, save=False)        
                if(index == 11): product.additional_image_11.save("logo.jpg", photo_obj, save=False)        
                if(index == 12): product.additional_image_12.save("logo.jpg", photo_obj, save=False)        
                if(index == 13): product.additional_image_13.save("logo.jpg", photo_obj, save=False)        
                if(index == 14): product.additional_image_14.save("logo.jpg", photo_obj, save=False)        
                if(index == 15): product.additional_image_15.save("logo.jpg", photo_obj, save=False)        
                if(index == 16): product.additional_image_16.save("logo.jpg", photo_obj, save=False)        
                if(index == 17): product.additional_image_17.save("logo.jpg", photo_obj, save=False)        
                if(index == 18): product.additional_image_18.save("logo.jpg", photo_obj, save=False)        
                if(index == 19): product.additional_image_19.save("logo.jpg", photo_obj, save=False)        
                if(index == 20): product.additional_image_20.save("logo.jpg", photo_obj, save=False)        
                if(index == 21): product.additional_image_21.save("logo.jpg", photo_obj, save=False)        
                if(index == 22): product.additional_image_22.save("logo.jpg", photo_obj, save=False)        
                if(index == 23): product.additional_image_23.save("logo.jpg", photo_obj, save=False)        
                if(index == 24): product.additional_image_24.save("logo.jpg", photo_obj, save=False)        
                if(index == 25): product.additional_image_25.save("logo.jpg", photo_obj, save=False)        
                if(index == 26): product.additional_image_26.save("logo.jpg", photo_obj, save=False)        
                if(index == 27): product.additional_image_27.save("logo.jpg", photo_obj, save=False)        
                if(index == 28): product.additional_image_28.save("logo.jpg", photo_obj, save=False)        
                if(index == 29): product.additional_image_29.save("logo.jpg", photo_obj, save=False)        
                if(index == 30): product.additional_image_30.save("logo.jpg", photo_obj, save=False)        
                if(index == 31): product.additional_image_31.save("logo.jpg", photo_obj, save=False)        
                if(index == 32): product.additional_image_32.save("logo.jpg", photo_obj, save=False)        
                if(index == 33): product.additional_image_33.save("logo.jpg", photo_obj, save=False)        
                if(index == 34): product.additional_image_34.save("logo.jpg", photo_obj, save=False)        
                if(index == 35): product.additional_image_35.save("logo.jpg", photo_obj, save=False)        
                if(index == 36): product.additional_image_36.save("logo.jpg", photo_obj, save=False)        
                if(index == 37): product.additional_image_37.save("logo.jpg", photo_obj, save=False)        
                if(index == 38): product.additional_image_38.save("logo.jpg", photo_obj, save=False)        
                if(index == 39): product.additional_image_39.save("logo.jpg", photo_obj, save=False)        
                if(index == 40): product.additional_image_40.save("logo.jpg", photo_obj, save=False)        
                if(index == 41): product.additional_image_41.save("logo.jpg", photo_obj, save=False)        
                if(index == 42): product.additional_image_42.save("logo.jpg", photo_obj, save=False)        
                if(index == 43): product.additional_image_43.save("logo.jpg", photo_obj, save=False)        
                if(index == 44): product.additional_image_44.save("logo.jpg", photo_obj, save=False)        
                if(index == 45): product.additional_image_45.save("logo.jpg", photo_obj, save=False)        
                if(index == 46): product.additional_image_46.save("logo.jpg", photo_obj, save=False)        
                if(index == 47): product.additional_image_47.save("logo.jpg", photo_obj, save=False)        
                if(index == 48): product.additional_image_48.save("logo.jpg", photo_obj, save=False)        
                if(index == 49): product.additional_image_49.save("logo.jpg", photo_obj, save=False)        
                if(index == 50): product.additional_image_50.save("logo.jpg", photo_obj, save=False)        

            product.save()
            print("Creating product with title[{}]..Done [productid={}]".format(title, product.id))
            return {"error": 0, "product_id": product.id}
        except Exception as e:
            print("Exception occured:")
            print(e.message)
            print(e.args)
            return {"error": 1, "error_msg": e.message}


def compute_title_desc_subcat(all_blocks):

    #   - PRODUCT has a title and description.
    #   - Attempt to extract the title
    #       - The line generally looks like: Catalog Name: Title goes here
    #       - In few cases, the "Catalog Name" is not present.
    #           - In such cases fall back to use the first line as title
    for block in all_blocks:
        text = block["text"]
        merged_text = "\n".join(text)
        desc = []
        title = ""
        subcategory_id = ""
        for line in merged_text.splitlines():
            if re.search("Catalog Name", line, re.IGNORECASE):
                # We found the line. Ex. Catalog Name: blah blah blah
                # Strip off the 'Catalog Name' so that we end up with 'blah blah blah' as title
                # Using regex substitution to do so - substitute 'Catalog Name' with ''
                title = re.sub(r"Catalog\s*Name:?", "", line, flags=re.IGNORECASE)
                title = re.sub(r"^\*", "", title)
                title = re.sub(r"\s*\*\s*$", "", title)
            elif re.search(r"^\s*Sub\s*=\s*\d+\s*$", line, re.IGNORECASE):
                subcategory_id = re.search(r"^\s*Sub\s*=\s*(\d+)\s*$", line, re.IGNORECASE).group(1)
            else:
                desc.append(line)

        # Validate that we have all necessary details.If not, use the default values set
        # Validate TITLE
        if title == "":
            # It means there is NO line matching 'Catalog Name'.In such cases, use first line as title
            if len(desc) > 0:
                title = desc.pop(0)
            else:
                title = "Title goes here"
        # Validate DESCRIPTION
        if len(desc) == 0:
            desc.append(default_desc)
        # Validate SUBCATEGORY
        if subcategory_id == "":
            # It means there is NO line matching 'Sub=100'.Use the default subcategory id
            subcategory_id = default_subcategory_id

        block["title"] = title
        block["desc"] = "\n".join(desc)
        block["subcategory_id"] = subcategory_id
        # Delete "text" as We have extracted 'title'/'desc'/'category' from it
        del block["text"]
    return all_blocks


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
    return file_id


def get_photo_url_from_id(photo_id):

    # Fetch the relatve file path from the fileid fetched above
    # https://api.telegram.org/bot<secretid>/getFile?file_id=<fileid>
    url = "https://api.telegram.org/bot{}/getFile?file_id={}".format(bot_token, photo_id)
    file_path = requests.get(url).json()["result"]["file_path"]
    # Form the "fully qualified" path to the photo file
    # https://api.telegram.org/file/bot<secretid>/<file_path>
    photo_url = "https://api.telegram.org/file/bot{}/{}".format(bot_token, file_path)
    return photo_url


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
    text = "Select category.\nReply like Category=10\n"
    categories = Category.objects.all().order_by("id")
    for category in categories:
        text += "{}: {}\n".format(category.id, category.name)

    return text


def send_message(chat_id, message):
    """Bot sends message to user
    https://api.telegram.org/bot{bot-toke}/sendMessage?chat_id={chat-id}&text={message}
    """
    url = "https://api.telegram.org/bot{}/sendMessage".format(bot_token)
    # myobj = {"chat_id": chat_id, "text": message}
    requests.post(url, data={"chat_id": chat_id, "text": message})


def get_sub_categories():

    print("Fetching sub-categories..")
    text = ""
    categories = Category.objects.all().order_by("sequence")
    for category in categories:
        text += "\n{}".format(category.name)
        subcategories = SubCategory.objects.filter(category=category).order_by("id")
        for subcategory in subcategories:
            text += "\n        {}:{}".format(subcategory.id, subcategory.name)
    text += "\n\n----------\nSelect sub-category.Ex: \nSub=10\n----------"
    print("Fetching sub-categories..Done")
    return text


def remove_existing_products(all_blocks):
    # This block of code was written when we had title=unique constraint
    # Now, the unique constraint is removed - so no need of this block anymore
    titles = Product.objects.values_list("title", flat=True)
    filtered_blocks = []
    for block in all_blocks:
        title = block["title"]
        if title.upper() in (x.upper() for x in titles):
            print("Product with title[{}] already exists!Skipping.".format(title))
        else:
            filtered_blocks.append(block)
    return filtered_blocks


def scan_image_urls(product_id):
    """ This method takes in the product id and fetches the urls to all the images
    Once fetched, it writes the urls into the product table
    """
    print("Fetching image url for [productid={}]..".format(product_id))
    # Get the product concerned from DB
    product = Product.objects.filter(id=product_id).first()
    # Handle product cover image
    product.cover_img_url = product.coverimage.url
    # Handle product additional images
    product_images_urls = []
    for record in ProductImage.objects.filter(product_id=product_id):
        product_images_urls.append(record.image.url)
    product.product_img_urls_csv = ",".join(product_images_urls)
    product.save()
    print("Fetching image url for [productid={}]..Done".format(product_id))
    print("Product table updated.")
    print("Deleting the records from productimage table..")
    # ProductImage.objects.filter(product_id=product_id).delete()
    print("Deleting the records from productimage table..Done")
