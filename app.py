from flask import Flask, request, jsonify, render_template
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import openai


app = Flask(__name__)


model_name = "gpt2"  
lm_model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
#can also use langchain for better prompt engineering

openai.api_key = "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"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend-content', methods=['POST'])
def recommend_content():
    data = request.form
    user_preferences = data.getlist('preferences')
    historical_data = data.getlist('historical_data')
    num_recommendations = int(data.get('num_recommendations', 5))

    prompt = "You are best movie recommendation system there is. You recommend movies based on movie preferences and genre preferences.\n My genre preferences are:\n"
    prompt += "\n".join(["- " + preference for preference in user_preferences]) + "\n"
    prompt += "My movie preferences are:\n"
    prompt += "\n".join(["- " + data_item for data_item in historical_data]) + "\n"
    prompt += "Suggest me {num_recommendations} recommendations:\n"

    completion = openai.Completion.create(
        engine='text-davinci-002',
        prompt=prompt,
        max_tokens=num_recommendations * 20,
        n=num_recommendations,
        stop=None,
        temperature=0.7
    )
    recommendations= (completion['choices'][0]['text'].strip())
    return render_template('index.html', recommendations=recommendations)


if __name__ == '__main__':
    app.run()