# Code from https://programminghistorian.org/en/lessons/creating-apis-with-python-and-flask
# https://www.kdnuggets.com/2019/01/build-api-machine-learning-model-using-flask.html

# Imports the Flask library, making the code available to the rest of the application.
from flask import Flask, request, jsonify
import pickle as p
from tensorflow.keras.models import load_model
from keras.preprocessing.sequence import pad_sequences

app = Flask(
    __name__)  # Creates the Flask application object, which contains data about the application and also methods (
# object functions) that tell the application to do certain actions.
app.config[
    "DEBUG"] = True  # Starts the debugger. With this line, if your code is malformed, you’ll see an error when you
# visit your app. Otherwise you’ll only see a generic message such as Bad Gateway in the browser when there’s a
# problem with your code.


@app.route('/api/', methods=['POST'])
def makecalc():
    data = request.get_json()
    word_index_y = vect_Y.word_index
    reverse_word_index_y = dict(
        [(value, key) for (key, value) in word_index_y.items()]
    )
    x_to_predict = vect_X.texts_to_sequences(data)
    x_to_predict_padded = pad_sequences(x_to_predict, padding="post", maxlen=1000)
    y_predict = (model.predict(x_to_predict_padded))
    tag = vector_to_list_of_tags(y_predict[0], reverse_word_index_y)

    return jsonify(tag)


def vector_to_list_of_tags(vect_tag, reverse_word_ind):
    tag_list = []
    for i in range(len(vect_tag)):
        if vect_tag[i] > 0.5:
            tag_list.append(reverse_word_ind.get(i, '?'))
    return tag_list


if __name__ == '__main__':
    modelfile = 'models/keras_embedding.h5'
    vect_X_file = 'models/keras_tokenizer_X.pickle'
    vect_Y_file = 'models/keras_tokenizer_Y.pickle'
    model = load_model('models/keras_embedding.h5')
    vect_X = p.load(open(vect_X_file, 'rb'))
    vect_Y = p.load(open(vect_Y_file, 'rb'))
    app.run(debug=True, host='0.0.0.0')


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Distant Reading Archive</h1>
<p>A prototype API for distant reading of science fiction novels.</p>'''


@app.errorhandler(404)
def page_not_found():
    return "<h1>404</h1><p>The resource could not be found.</p>", 404
