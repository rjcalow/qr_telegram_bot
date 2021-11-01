import qrcode
import cv2
import pathlib
import telegram
from telegram.ext import Updater, MessageHandler, Filters
import uuid


key = "KEY HERE"
root = pathlib.Path(__file__).parent.resolve()


def qr_gen(data, path):
    img = qrcode.make(data)
    type(img)  # qrcode.image.pil.PilImage
    img.save(path)
    return path


def qr_read(img):
    data = cv2.imread(img)
    det = cv2.QRCodeDetector()
    val, pts, st_code = det.detectAndDecode(data)
    return val


def photo(update, context):
    file = context.bot.get_file(update.message.photo[-1].file_id)
    filename = uuid.uuid4().hex + ".jpg"
    path = root / filename
    file.download(str(path))

    result = qr_read(str(path))

    # if result is emtpy inform user by changing result to msg
    if result == "":
        result = "Error. No readable qr. Try again?"

    context.bot.send_message(chat_id=update.message.chat_id, text=result)

    path.unlink()


def text(update, context):
    filename = uuid.uuid4().hex + ".jpg"
    path = root / filename
    text = update.message.text
    context.bot.send_photo(chat_id=update.message.chat_id,
                           photo=open(qr_gen(text, path), 'rb'))
    path.unlink()


def main():
    updater = Updater(key, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.text, text))
    dp.add_handler(MessageHandler(Filters.photo, photo))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
