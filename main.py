from flask import Flask,request
import os
from firebase import firebase

url = os.environ['url']
def get_db_data(id):
  fdb = firebase.FirebaseApplication(url, None)
  result = fdb.get('/',id)
  if result == None:
    return "Error"
  else:
    return result
def set_db_data(id:str,data):
  fdb = firebase.FirebaseApplication(url, None)
  fdb.put('/rank',id,data)

app = Flask(__name__)
@app.route("/")
def main():
    return "Hello!"
  
@app.route("/name", methods=["GET"])
def name():
    name = request.args.get('name')
    score = request.args.get('score')
    set_db_data(name,int(score))
    print(score)
    return name

@app.route("/rank", methods=["GET"])
def rank():
    data = get_db_data("rank")
    sorted_ids = sorted(data.keys(), key=lambda x: data[x],reverse=True)
    print(sorted_ids)
    lb = ''
    for data_id in sorted_ids:
      try:
        lb += f'{data_id}：{data[data_id]}\n'
      except Exception as e:
        print(e)
    return lb

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3000)