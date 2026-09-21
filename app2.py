from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

DESIGNS = {
    "Minimalist": {"description": "Clean, uncluttered and functional.", "colors":["🤍 White","🩶 Grey","🌿 Sage"],"features":["Declutter","Clean shapes","Simple palette"],"icon":"✨"},
    "Cozy": {"description": "Warm and comfortable.", "colors":["🤎 Beige","🧡 Warm orange","🤍 Cream"],"features":["Warm lighting","Soft cushions","Focal point"],"icon":"🧸"},
    "Biophilic": {"description": "Bring nature indoors.", "colors":["🌿 Green","🤎 Brown","🤍 Cream"],"features":["Indoor plants","Natural materials","Earthy colors"],"icon":"🌿"},
    "Scandinavian": {"description": "Bright, practical Nordic.", "colors":["🤍 White","🪵 Light wood","🌿 Sage"],"features":["Light furniture","Max natural light","Function+comfort"],"icon":"❄️"},
    "Color Pop": {"description": "Playful personality.", "colors":["💗 Pink","💛 Yellow","💙 Blue"],"features":["Accent wall","Colorful accessories","Neutral base"],"icon":"🌈"},
    "Modern Luxury": {"description": "Elegant premium.", "colors":["🖤 Black","✨ Gold","🤍 Ivory"],"features":["Statement lighting","Metallic accents","Focal point"],"icon":"💎"},
    "Zen": {"description": "Calm and peaceful.", "colors":["🤍 White","🌿 Green","🪵 Wood"],"features":["Reduce clutter","Natural textures","Soft lighting"],"icon":"🧘"},
    "Study Focus": {"description": "Productivity focused.", "colors":["🤍 White","🩶 Grey","💙 Blue"],"features":["Dedicated work zone","Desk organization","Reduce distractions"],"icon":"📚"},
    "Space Saving": {"description": "Smart for small rooms.", "colors":["🤍 White","🌿 Sage","🩶 Grey"],"features":["Vertical storage","Multi-purpose","Clear walkways"],"icon":"📦"},
    "Pastel Dream": {"description": "Soft cute relaxing.", "colors":["🌸 Pink","💜 Lavender","💙 Baby blue"],"features":["Pastel accessories","Soft textures","Cute theme"],"icon":"🎀"}
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
    space_score = data.get("space",0.8) if space_need=="Very important" else 0.7
    if space_need=="Very important": space_score=0.95
    elif space_need=="Somewhat important": space_score=0.80
    else: space_score=0.70
    budget_score = 0.9 if budget=="Low" else 0.85
    style_score = 1.0 if pref==design else 0.75 if pref=="Surprise me" else 0.55
    final = space_score*0.3 + style_score*0.3 + budget_score*0.2 + 0.75*0.2
    return round(final*100)

@app.route('/')
def home():
    return render_template('index.html')

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
def decor(style):
    return jsonify(DECOR_ITEMS.get(style,[]))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
    