
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# room designs I chose for my project

MY_DESIGNS = {
    "Minimalist": 
       { "about": "simple room, not too many things",
        "colors": ["White", "Grey", "Sage green"],
        "stuff": ["less furniture", "clean table", "simple colours"],
        "emoji": "✨",
        "budget": ["Low", "Medium"],
        "room_size": "Small"},
 

    "Cozy": 
      {  "about": "a warm and comfy room",
        "colors": ["Beige", "warm orange", "cream"],
        "stuff": ["warm light", "soft blanket", "candles"],
        "emoji": "🧸",
        "budget": ["Low", "Medium"],
        "room_size": "Small"},
    
   
    "Biophilic": 
        { "about": "a room with lots of plants",
        "colors": ["Green", "Brown", "Cream"],
        "stuff": ["money plant", "wood table", "earthy vibe"],
        "emoji": "🌿",
        "budget": ["Low", "Medium", "High"],
        "room_size": "Any"},
    

    "Scandinavian":      
       {  "about": "bright room with simple furniture",
        "colors": ["White", "Light wood", "Sage"],
        "stuff": ["light wood", "sunlight", "simple"],
        "emoji": "❄️",
        "budget": ["Medium", "High"],
        "room_size": "Medium" },
   

    "Color Pop":
        {   "about": "a room with fun and bright colours",
        "colors": ["Pink", "Yellow", "Blue"],
        "stuff": ["one bright wall", "colorful pillows"],
        "emoji": "🌈",
        "budget": ["Low", "Medium"],
        "room_size": "Any" },
   

    "Modern Luxury": 
      {  "about": "a fancy room with a rich look",
        "colors": ["Black", "Gold", "Ivory"],
        "stuff": ["big lamp", "gold decor", "mirror"],
        "emoji": "💎",
        "budget": ["High"],
        "room_size": "Large" },
   

    "Zen": 
       { "about": "a calm room with less clutter",
        "colors": ["White", "Green", "Wood"],
        "stuff": ["less clutter", "wood", "soft light"],
        "emoji": "🧘",
        "budget": ["Low", "Medium"],
        "room_size": "Small" },
   

    "Study Focus": 
       { "about": "a simple setup for studying",
        "colors": ["White", "Grey", "Blue"],
        "stuff": ["study table", "shelf", "no distraction"],
        "emoji": "📚",
        "budget": ["Low", "Medium"],
        "room_size": "Small" },
      

    "Space Saving": 
        { "about": "useful for  small rooms with less space",
        "colors": ["White", "Sage", "Grey"],
        "stuff": ["wall shelf", "bed storage", "foldable furniture"],
        "emoji": "📦",
        "budget": ["Low", "Medium"],
        "room_size": "Small" },
     

    "Pastel Dream": 
       { "about": "soft colours and cute decorations",
        "colors": ["Pink", "Lavender", "Baby blue"],
        "stuff": ["pastel cushions", "fairy light"],
        "emoji": "🎀",
        "budget": ["Low", "Medium"],
        "room_size": "Small" }}
   



# decor items with estimated prices

decor_list = {
    "Minimalist": 
       [ ("🪴", "Small Plant", "₹399"),
        ("💡", "Simple Lamp", "₹799")],
    
    "Cozy": 
      [  ("🕯️", "Candle", "₹349"),
        ("🧸", "Cushion", "₹449")],
    
    "Biophilic":
       [ ("🌿", "Money Plant", "₹399"),
        ("🪴", "Succulent", "₹249")],
    
    "Scandinavian":  
       [   ("🪵", "Wood Table", "₹1299"),
        ("💡", "Nordic Lamp", "₹899") ], 
      
    "Color Pop": 
       [ ("🌸", "Pink Pillow", "₹399"),
        ("🖼️", "Color Art", "₹499") ],
   
    "Modern Luxury":
         [("✨", "Gold Vase", "₹699"),
        ("🪞", "Mirror", "₹1299")],
      
    "Zen": 
       [ ("🪴", "Bonsai tree", "₹899"),
        ("🕯️", "Zen Candle", "₹399")],
    
    "Study Focus":
       [ ("💡", "Study Lamp", "₹899"),
        ("📚", "Book Shelf", "₹1299")],
     

    "Space Saving": 
        [("🧺", "Storage Box", "₹799"),
        ("🪝", "Wall Hook", "₹299")],
    
    "Pastel Dream": 
        [("🌸", "Pastel Vase", "₹399"),
        ("🧸", "Plushie", "₹499")]}
     



def my_score(name, user):
    design = MY_DESIGNS[name]

    room = user.get("room", "Small")
    budget = user.get("budget", "Medium")
    pref = user.get("pref", "Surprise me")

    # check the room size

    if design["room_size"] == "Any" or design["room_size"] == room:
        room_score = 1.0
    elif room == "Small" and design["room_size"] == "Large":
        room_score = 0.4
    else:
        room_score = 0.7
         
    # check the budget

    if budget in design["budget"]:
        budget_score = 1.0
    else:
        budget_score = 0.5

    # check which style the user likes

    if pref == name:
        pref_score = 1.0
    elif pref == "Surprise me":
        pref_score = 0.75
    else:
        pref_score = 0.5

    score =( 
     room_score * 0.3
        + budget_score * 0.25
        + pref_score * 0.35
        + 0.9 * 0.1)
    

    return round(score * 100)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Please send valid JSON data"}), 400

    results = []

    for name, design in MY_DESIGNS.items():
        score = my_score(name, data)

        results.append({
    "name": name,
    "score": score,
    "desc": design["about"],
    "colors": design["colors"],
    "icon": design["emoji"],
    "features": design["stuff"]
                                  })

    results.sort(key=lambda item: item["score"], reverse=True)

    return jsonify(results[:6])


@app.route("/decor/<style>")
def decor(style):
    items = decor_list.get(style)

    if items is None:
        return jsonify({"error": "Design not found"}), 404

    result = []

    for emoji, name, price in items:
        result.append({
            "emoji": emoji,
            "name": name,
            "price": price
        })

    return jsonify(result)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
