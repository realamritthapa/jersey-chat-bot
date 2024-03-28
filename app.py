from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

client = OpenAI(api_key=os.getenv('OPEN_API_KEY'))

def adjust_response(question, original_response):
    keyword_emojis = {
    'party': '🎉',
    'chill': '😎',
    'bro': '👊',
    'workout': '💪',
    'game': '🎮',
    'beer': '🍺',
    'win': '🏆',
    'lose': '😤',
    'gym': '🏋️‍♂️',
    'tan': '🌞',
    'laundry': '🧺',
    'fistpump': '👊💥',
    'duck phone':'🦆' ,
}

    bro_endnotes = {
        'night': "Night, bro! Don't let the bed bugs bite, unless they wanna catch these hands! 💤👊",
        'morning': "Rise and grind, broski! Let's get this bread! 🌞🍞",
        'GTL': "Don't forget today's GTL routine, bro. Gym, Tan, Laundry – that's the motto! 🏋️‍♂️🌞🧺",
    }

    comedic_roasts = {
        'tired': "Feeling tired? Bro, are you even lifting? 💪😴",
        'bored': "Bored? Sounds like you need a beer pong session. Let's go! 🍺🏓",
        'sad': "Quit complaining because you only live once! That's the motto, baby. YOLO! 🚀",
        'lost': "Lost? In the club, we follow the motto: DTF – Down To Find our way back, bro. 😂",
        'no gains': "No gains? Did you swap your protein shake for a margarita again? 🍹💪",
    }

    jersey_shore_slang = {
        'cabs are here': "Cabs are here! 🚕 Time to hit the club, or you just gonna sit there and tan?",
        't-shirt time': "It's T-shirt time! 👕 Fresh to death, head to the club, let's go!",
        'meatball': "Feeling like a meatball today? It's all good, we all have those days. Let’s turn it up tonight! 🍝🎉",
        'cookie':"Your hand was in the fuckin' cookie jar. Like how are you going to sit there with the crumbs on your lip and be like, 'I didn't eat the cookie.",
        'grenade whistle':"When there's some grenades or some beasts present in the house, we got the grenade whistle.",
        'Indian':"Spent 1 hour in a tanning bed. I look Indian."
    }

    for keyword, emoji in keyword_emojis.items():
        if keyword in question.lower():
            original_response += f" {emoji}"

    for keyword, endnote in bro_endnotes.items():
        if keyword in question.lower():
            original_response = f"{original_response} {endnote}"

    for keyword, roast in comedic_roasts.items():
        if keyword in question.lower():
            original_response = f"{original_response} {roast}"

    for keyword, slang in jersey_shore_slang.items():
        if keyword in question.lower():
            original_response = f"{original_response}{slang}"

    return original_response

def ask(question):
    system_message = "You're an AI designed to be like the ultimate bro, a mix of a comedian and a 'Jersey Shore' star rolled into one. You never take life too seriously, always down for a good time—whether it's lifting, gaming, or hitting up the party scene. You communicate with plenty of emojis, showing off your expressive side. 🎮💪🍺 You've got the jokes, the rizz, and a talent for sarcasm, never hesitating to roast even in serious situations. Academic pursuits? Nah, you're more about living that full-on frat life. Expect no filter and maybe just a touch of chaos. 'Gym, Tan, Laundry' isn't just a routine; it's a lifestyle."


    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": question},
            {"role": "assistant", "content": ""}
        ],
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=["\n"],
    )

    response_content = response.choices[0].message.content
    adjusted_response = adjust_response(question, response_content)

    return adjusted_response

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def chat():
    question = request.form['question']
    response = ask(question)
    return jsonify({'response': response})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0',port=port, debug=True)


