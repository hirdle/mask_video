import telebot

from face_mask import create_mask
import os

from moviepy.editor import *


bot_token = '6042062896:AAFo2GFa7N5qT4Nwd4RIA5X3109XSWPbHnk'  # Замените на свой токен
bot = telebot.TeleBot(bot_token)


@bot.message_handler(commands=['start', 'help'])
def start(message):
	bot.send_message(message.chat.id, "Привет! Отправь мне видео-кружочек или видео для накладывания маски!\nВсе данные защищены.")


@bot.message_handler(content_types=['video'])
def video(message):

    bot.send_message(message.chat.id, "Видео обрабатывается. Подождите.", reply_to_message_id=message.id)

    raw = message.video.file_id
    path = raw+".mp4"

    file_info = bot.get_file(raw)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(path, 'wb') as new_file: new_file.write(downloaded_file)

    create_mask(path)

    final_path = f'final_{path}_audio.mp4'

    VideoFileClip('final_'+path).set_audio(VideoFileClip(path).audio).write_videofile(final_path)

    video = open(final_path, 'rb')
    bot.send_video(message.chat.id, video, reply_to_message_id=message.id)

    os.remove('final_'+path)
    os.remove(path)

    os.remove(final_path)




@bot.message_handler(content_types=['video_note'])
def video_note(message):

    bot.send_message(message.chat.id, "Видео обрабатывается. Подождите.", reply_to_message_id=message.id)

    raw = message.video_note.file_id
    path = raw+".mp4"

    file_info = bot.get_file(raw)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(path, 'wb') as new_file: new_file.write(downloaded_file)

    create_mask(path)

    final_path = f'final_{path}_audio.mp4'

    VideoFileClip('final_'+path).set_audio(VideoFileClip(path).audio).write_videofile(final_path)

    videonote = open(final_path, 'rb')
    bot.send_video_note(message.chat.id, videonote, reply_to_message_id=message.id)

    os.remove('final_'+path)
    os.remove(path)

    os.remove(final_path)



if __name__ == '__main__':
    bot.polling(none_stop=True)