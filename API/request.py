import requests
import json
import pandas as pd

url = 'http://ec2-35-181-51-177.eu-west-3.compute.amazonaws.com:5000/api/'
#url = "http://0.0.0.0:5000/api/"

dtypes_questions = {'Id':'int32', 'Score': 'int16', 'Title': 'str',
                    'Body': 'str', 'Title_raw': 'str', 'Text': 'str',
                    'Tags': 'str','Text_raw':'str'}
nrows = 20000

df_questions = pd.read_csv('df_questions_fullclean.csv',
                           usecols=dtypes_questions.keys(),
                           encoding = "utf-8",
                           dtype=dtypes_questions,
                           nrows=nrows
                          )


text_train, tag_train = df_questions.Text_raw, df_questions.Tags


text1= "How can I    django django django check if a keyboard modifier is pressed (Shift, Ctrl, or Alt)"
text2 = text_train[2]
text = text2
data = [text]
# data = [input()]
j_data = json.dumps(data)
headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
r = requests.post(url, data=j_data, headers=headers)
print("Texte à prédire : ",'\n ',text,'\n ')
print("Reponse du serveur : ","\n")
print(r, r.text)
