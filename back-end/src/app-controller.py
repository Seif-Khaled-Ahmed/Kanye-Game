from flask import Flask, send_file, session,request
from  imageproc import hide_random_word
import os
import random
import pymongo
import time

app = Flask(__name__)

mongoclient = pymongo.MongoClient("mongodb://localhost:27017/")
mongodb = mongoclient["KANYE_GAME"]
answers = mongodb["answers"]
leaderboard = mongodb["leaderboard"]



folder_path = "../media"
png_count = len([f for f in os.listdir(folder_path) if f.lower().endswith(".png")])



app.config['SECRET_KEY'] = 'string1'

@app.route('/')
def set_session():
    session["id"] = str(int(time.time())) +"howa_keda"+ str(random.randint(0,2147483647))
    print(session.get("id"))
    return ("",204)


@app.route('/image', methods=['GET']) 
def get_image():
    if (not 'id' in session):
        set_session()
    img_id = random.randint(0, png_count)
    words = hide_random_word(f"../media/{img_id}.png", output_path=f"output/output_{img_id}.png")
    print(img_id)
    print (words)
    fiveara = {'id':str (session.get('id')) ,'words':words}
    answers.insert_one(fiveara)
    return(send_file(f'output/output_{img_id}.png'))


@app.route('/random_answers', methods=['GET']) 
def get_answers():
    notrandom = answers.find_one({'id': str(session.get('id'))})['words']
    if len(notrandom) == 1:
        return notrandom
    randomized ={}
    sample  = random.sample(notrandom.keys(),len(notrandom))
    for i in range(len(notrandom)):
        randomized[i] = notrandom[sample[i]]

    return (randomized)

@app.route('/answer', methods=['GET']) 
def get_answer():
    data = request.get_json()
    return({})




if __name__ == '__main__':
    app.run(debug=True, port=3001)