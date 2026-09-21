from flask import Flask, render_template, request, jsonify
import random
from PIL import Image
import base64, io

app = Flask(__name__)

DESIGNS = {
    "Minimalist": {"description": "Clean, uncluttered and functional.", "space":0.95,"color":0.80,"function":0.95,"budget":0.90,"coziness":0.55,"colors":["🤍 White","🩶 Grey","🌿 Sage"],"features":["Declutter","Clean shapes","Simple palette"],"icon":"✨"},
    "Cozy": {"description": "Warm and comfortable.","space":0.70,"color":0.90,"function":0.75,"budget":0.80,"coziness":1.00,"colors":["🤎 Beige","🧡 Warm orange","🤍 Cream"],"features":["Warm lighting","Soft cushions","Focal point"],"icon":"🧸"},
    "Biophilic": {"description": "Bring nature indoors.","space":0.72,"color":0.95,"function":0.72,"budget":0.75,"coziness":0.88,"colors":["🌿 Green","🤎 Brown","🤍 Cream"],"features":["Indoor plants","Natural materials","Earthy colors"],"icon":"🌿"},
    "Scandinavian": {"description": "Bright, practical Nordic.","space":0.88,"color":0.90,"function":0.92,"budget":0.82,"coziness":0.85,"colors":["🤍 White","🪵 Light wood","🌿 Sage"],"features":["Light furniture","Max natural light","Function+comfort"],"icon":"❄️"},
    "Color Pop": {"description": "Playful personality.","space":0.65,"color":1.00,"function":0.72,"budget":0.75,"coziness":0.80,"colors":["💗 Pink","💛 Yellow","💙 Blue"],"features":["Accent wall","Colorful accessories","Neutral base"],"icon":"🌈"},
    "Modern Luxury": {"description": "Elegant premium.","space":0.65,"color":0.88,"function":0.80,"budget":0.45,"coziness":0.70,"colors":["🖤 Black","✨ Gold","🤍 Ivory"],"features":["Statement lighting","Metallic accents","Focal point"],"icon":"💎"},
    "Zen": {"description": "Calm and peaceful.","space":0.90,"color":0.92,"function":0.90,"budget":0.88,"coziness":0.90,"colors":["🤍 White","🌿 Green","🪵 Wood"],"features":["Reduce clutter","Natural textures","Soft lighting"],"icon":"🧘"},
    "Study Focus": {"description": "Productivity focused.","space":0.90,"color":0.78,"function":1.00,"budget":0.90,"coziness":0.65,"colors":["🤍 White","🩶 Grey","💙 Blue"],"features":["Dedicated work zone","Desk organization","Reduce distractions"],"icon":"📚"},
    "Space Saving": {"description": "Smart for small rooms.","space":1.00,"color":0.70,"function":1.00,"budget":0.92,"coziness":0.70,"colors":["🤍 White","🌿 Sage","🩶 Grey"],"features":["Vertical storage","Multi-purpose","Clear walkways"],"icon":"📦"},
    "Pastel Dream": {"description": "Soft cute relaxing.","space":0.75,"color":0.98,"function":0.70,"budget":0.80,"coziness":0.95,"colors":["🌸 Pink","💜 Lavender","💙 Baby blue"],"features":["Pastel accessories","Soft textures","Cute theme"],"icon":"🎀"}
}

DECOR_ITEMS = {
    "Minimalist":[("🪴","Small Ceramic Plant","₹399"),("💡","Minimal Desk Lamp","₹799"),("🖼️","Abstract Wall Art","₹599")],
    "Cozy":[("🕯️","Warm Scented Candle","₹349"),("🧸","Soft Cushion","₹449"),("🧶","Chunky Throw","₹899")],
    "Biophilic":[("🌿","Money Plant","₹399"),("🪴","Mini Succulent","₹249"),("🌱","Hanging Plant","₹499")],
    "Scandinavian":[("🪵","Light Wood Table","₹1,299"),("💡","Nordic Lamp","₹899"),("🪴","White Ceramic Pot","₹449")],
    "Color Pop":[("🌸","Pink Cushion","₹399"),("💛","Yellow Lamp","₹799"),("🖼️","Colorful Art","₹499")],
    "Modern Luxury":[("✨","Gold Vase","₹699"),("💡","Statement Lamp","₹1,499"),("🪞","Decorative Mirror","₹1,299")],
    "Zen":[("🪴","Bonsai Plant","₹899"),("🕯️","Zen Candle","₹399"),("🪵","Wooden Tray","₹499")],
    "Study Focus":[("💡","Study Lamp","₹899"),("📚","Floating Bookshelf","₹1,299"),("🗂️","Desk Organizer","₹399")],
    "Space Saving":[("🧺","Under-Bed Storage","₹799"),("📚","Floating Shelf","₹699"),("🪝","Wall Hook","₹299")],
    "Pastel Dream":[("🌸","Pastel Vase","₹399"),("🧸","Cute Plushie","₹499"),("💜","Lavender Candle","₹349")]
}

def calculate_score(design, room, budget, space_need, pref):
    data=DESIGNS[design]
    space_score = data["space"] if space_need=="Very important" else (data["space"]+0.70)/2 if space_need=="Somewhat important" else 0.70
    budget_score = data["budget"] if budget=="Low" else min(1,data["budget"]+0.10) if budget=="Medium" else min(1,data["budget"]+0.20)
    style_score = 1.0 if pref==design else 0.75 if pref=="Surprise me" else 0.55
    room_score=0.75
    if room=="Study / Workspace" and design=="Study Focus": room_score=1.0
    if room=="Small Room" and design=="Space Saving": room_score=1.0
    if room=="Bedroom" and design in ["Cozy","Pastel Dream","Zen"]: room_score=0.95
    if room=="Living Room" and design in ["Minimalist","Scandinavian","Modern Luxury"]: room_score=0.95
    final = space_score*0.25 + data["color"]*0.15 + data["function"]*0.20 + budget_score*0.15 + style_score*0.15 + room_score*0.10
    return round(max(0,min(1,final))*100)

@app.route('/')
def home(): return render_template('index.html', designs=DESIGNS)

@app.route('/analyze', methods=['POST'])
def analyze():
    data=request.json
    results=[]
    for name in DESIGNS:
        score=calculate_score(name, data['room'], data['budget'], data['space_need'], data['pref'])
        results.append({"name":name,"score":score,"desc":DESIGNS[name]["description"],"colors":DESIGNS[name]["colors"],"icon":DESIGNS[name]["icon"],"features":DESIGNS[name]["features"]})
    results.sort(key=lambda x:x["score"],reverse=True)
    return jsonify(results[:6])

@app.route('/decor/<style>')
def decor(style): return jsonify(DECOR_ITEMS.get(style,[]))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
    


