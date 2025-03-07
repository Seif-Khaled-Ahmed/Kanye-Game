from flask import Flask, send_file, session,request
from flask_cors import CORS
from  imageproc import hide_random_word
import os
import random
import pymongo
import time
from datetime import timedelta

app = Flask(__name__)
CORS(app, supports_credentials=True)

mongoclient = pymongo.MongoClient("mongodb://localhost:27017/")
mongodb = mongoclient["KANYE_GAME"]
answers = mongodb["answers"]
leaderboard = mongodb["leaderboard"]



folder_path = "../media"
png_count = len([f for f in os.listdir(folder_path) if f.lower().endswith(".png")])


app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)

app.config['SECRET_KEY'] = 'string1'

@app.route('/')
def set_session():
    session["id"] = str(int(time.time())) +"howa_keda"+ str(random.randint(0,2147483647))
    print(session.get("id"))
    leaderboard.insert_one({'id':session.get('id'),'name':None,'score':0})
    return ("", 204)


@app.route('/image', methods=['GET'])
def get_image():
    sid = session.get('id')
    if(answers.find_one(sid) != "none"):
        print("should delete")
        delete()
    if (not 'id' in session):
        set_session()
    img_id = random.randint(0, png_count - 1)
    print("image number:", img_id)
    try:
        words = hide_random_word(f"../media/{img_id}.png", output_path=f"output/{sid}_output_{img_id}.png")
        if words == "No words detected!":get_image()
    except Exception as e:
        return(e,"internal server error", 500)
    print(words)
    answer = {'id':str (session.get('id')), 'words':words , 'imageId' : img_id}
    answers.insert_one(answer)
    return(send_file(f'output/{sid}_output_{img_id}.png'))


@app.route('/random_answers', methods=['GET']) 
def get_answers():
    try:
        notrandom = answers.find_one({'id': str(session.get('id'))})['words']
    except:
        return("user not found", 404)
    if len(notrandom) == 1:
        return notrandom
    randomized = {}
    sample  = random.sample(notrandom.keys(),len(notrandom))
    for i in range(len(notrandom)):
        randomized[i] = notrandom[sample[i]]
    return (randomized)

@app.route('/answer/<number>/<word>', methods=['PUT']) 
def get_answer(number,word):
    number = int(number)
    try:
        sid = str(session.get('id'))
    except Exception as e:
        return(f"session id error {e}",400)
    try:
        round = answers.find_one({'id':sid})
    except Exception as e:
        return (f"round not found {e}", 404)
    score = leaderboard.find_one({'id':sid})
    print(score['score'])
    try:
        if(number > len(round['words'])):
            return("wrong input", 400)
        if(round['words'][str(number)] == word):
            newvalue = {"$set": { "score": score['score'] + 1 }}
        else :
            newvalue = {"$set": { "score": score['score'] - 1 }}
    except Exception as e:
        return(f"server error {e}", 500)
    leaderboard.update_one(score,newvalue)
    score = leaderboard.find_one({'id':sid})
    return(str(score))

@app.route('/score', methods=['GET'])
def get_score():
    sid = str(session.get('id'))
    try:
        score = leaderboard.find_one({'id':sid})['score']
    except:
        return("score not found", 404)
    return(str(score))


@app.route('/leaderboard', methods=['GET'])
def get_leaderboard():
    try:
        scores = []
        scoreall = leaderboard.find().sort("score")
        num = min(leaderboard.count_documents({}),30)
        for x in range(num):
            scores.append(scoreall[x])

    except:
        return("server error", 500)
    
    return(str(scores))


@app.route('/name/<name1>', methods=['POST'])
def set_username(name1):
    set = {"$set": { "name": name1 }}
    try:
        sid = str(session.get('id'))
    except Exception as e:
        return(e,"user not found", 404)
    try:
        leaderboard.update_one({ "id": sid },set)
    except Exception as e:
        return(e,"server error", 500)
    
    return(str(name1))


@app.route('/submit',methods=['DELETE'])
def submit():
    return(0)

@app.route('/delete',methods=['DELETE'])
def delete():
    sid = str (session.get('id'))
    try:
        round = answers.find_one_and_delete({'id':sid})
    except Exception as e:
        return(e," could not find round",404)
    try:
        os.remove(f"output/{sid}_output_{round['imageId']}.png")
    except Exception as e:
        return (e,"could not find image",500)
    print("deleted")
    return (str(round))

@app.route('/*')
def notfound():
    return(404,'route not found')


if __name__ == '__main__':
    app.run(debug=True, port=3001)