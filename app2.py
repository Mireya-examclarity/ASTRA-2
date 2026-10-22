from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# all my design data - will add more later tho

DESIGNS = {
    "Minimalist": 

       { "description": "Clean, uncluttered and functional.",
        "colors": ["🤍 White", "🩶 Grey", "🌿 Sage"],
        "features": ["Declutter", "Clean shapes", "Simple palette"],
        "icon": "✨",
        "budget_fit": ["Low", "Medium"],
        "space_fit": "Small" },
    
    "Cozy": 

        {"description": "Warm and comfortable, perfect for relaxing.",
        "colors": ["🤎 Beige", "🧡 Warm orange", "🤍 Cream"],
        "features": ["Warm lighting", "Soft cushions", "Focal point"],
        "icon": "🧸",
        "budget_fit": ["Low", "Medium"],
        "space_fit": "Small" },

    "Biophilic": 

      {  "description": "Bring nature indoors, fresh vibes.",
        "colors": ["🌿 Green", "🤎 Brown", "🤍 Cream"],
        "features": ["Indoor plants", "Natural materials", "Earthy colors"],
        "icon": "🌿",
        "budget_fit": ["Low", "Medium", "High"],
        "space_fit": "Any" },
    
    "Scandinavian": 

       { "description": "Bright, practical Nordic style.",
        "colors": ["🤍 White", "🪵 Light wood", "🌿 Sage"],
        "features": ["Light furniture", "Max natural light", "Function+comfort"],
        "icon": "❄️",
        "budget_fit": ["Medium", "High"],
        "space_fit": "Medium" },
    
    "Color Pop": 

       { "description": "Playful and full of personality.",
        "colors": ["💗 Pink", "💛 Yellow", "💙 Blue"],
        "features": ["Accent wall", "Colorful accessories", "Neutral base"],
        "icon": "🌈",
        "budget_fit": ["Low", "Medium"],
        "space_fit": "Any"},
    
    "Modern Luxury": 

       { "description": "Elegant premium look.",
        "colors": ["🖤 Black", "✨ Gold", "🤍 Ivory"],
        "features": ["Statement lighting", "Metallic accents", "Focal point"],
        "icon": "💎",
        "budget_fit": ["High"],
        "space_fit": "Large" },
    
    "Zen": {
        "description": "Calm and peaceful, stress-free.",
        "colors": ["🤍 White", "🌿 Green", "🪵 Wood"],
        "features": ["Reduce clutter", "Natural textures", "Soft lighting"],
        "icon": "🧘",
        "budget_fit": ["Low", "Medium"],
        "space_fit": "Small"},
    
    "Study Focus": 

       { "description": "Productivity focused setup.",
        "colors": ["🤍 White", "🩶 Grey", "💙 Blue"],
        "features": ["Dedicated work zone", "Desk organization", "Reduce distractions"],
        "icon": "📚",
        "budget_fit": ["Low", "Medium"],
        "space_fit": "Small"},
    
    "Space Saving": 

        { "description": "Smart for small rooms, every inch counts.",
        "colors": ["🤍 White", "🌿 Sage", "🩶 Grey"],
        "features": ["Vertical storage", "Multi-purpose", "Clear walkways"],
        "icon": "📦",
        "budget_fit": ["Low", "Medium"],
        "space_fit": "Small"},
    
    "Pastel Dream": 

       { "description": "Soft cute relaxing vibe.",
        "colors": ["🌸 Pink", "💜 Lavender", "💙 Baby blue"],
        "features": ["Pastel accessories", "Soft textures", "Cute theme"],
        "icon": "🎀",
        "budget_fit": ["Low", "Medium"],
        "space_fit": "Small" }}


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
    "Pastel Dream":[("🌸","Pastel Vase","₹399"),("🧸","Cute Plushie","₹499"),("💜","Lavender Candle","₹349")]}


# my scoring - weighted algo
def calculate_score(design_name, user_data):
    info = DESIGNS[design_name]
    
    # 1. space logic (is there any obstacle on your way ?)

    room = user_data.get('room', 'Small')
    if info['space_fit'] == 'Any' or info['space_fit'] == room:
        space_score = 1.0
    elif room == 'Small' and info['space_fit'] == 'Large':
        space_score = 0.5
    else:
        space_score = 0.8

    # 2. budget logic (for all the people checking their wallet)

    budget = user_data.get('budget', 'Medium')
    if budget in info['budget_fit']:
        budget_score = 1.0
    else:
        budget_score = 0.6

    # 3. preference logic
    pref = user_data.get('pref', 'Surprise me')
    if pref == design_name:
        style_score = 1.0
    elif pref == 'Surprise me':
        style_score = 0.8
    else:
        style_score = 0.6

    # 4. golden ratio bonus - just to make it feel mathy
    golden_bonus = random.uniform(0.85, 1.0)

     # golden angle placement

    # final weighted score - main formula

    final = (space_score * 0.3) + (budget_score * 0.25) + (style_score * 0.35) + (golden_bonus * 0.10)
    
    return round(final * 100)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "no data"}), 400
        
        results = []
        for name in DESIGNS:
            score = calculate_score(name, data)
            results.append({"name": name,
                "score": score,
                "desc": DESIGNS[name]["description"],
                "colors": DESIGNS[name]["colors"],
                "icon": DESIGNS[name]["icon"],
                "features": DESIGNS[name]["features"]})
        
        # sort by score and give top 6

        results.sort(key=lambda x: x["score"], reverse=True)
        return jsonify(results[:6])

    except Exception as e:
        print(f"Error: {e}") # for debugging
        return jsonify({"error": str(e)}), 500

@app.route('/decor/<style>')
def decor(style):
    items = DECOR_ITEMS.get(style, [])
    formatted = [{"emoji": i[0], "name": i[1], "price": i[2]} for i in items]
    return jsonify(formatted)

# for  deployment     
      
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

    

