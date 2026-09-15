import streamlit as st
from PIL import Image


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="ASTRA - Smart Space Designer",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    .stApp {
        background: linear-gradient(135deg, #fff8f3, #f7f4ff);
    }

    .main-title {
        font-size: 55px;
        font-weight: 800;
        color: #6c4ab6;
        margin-bottom: 0;
        line-height: 1.1;
    }

    .subtitle {
        font-size: 20px;
        color: #666;
        margin-bottom: 30px;
    }

    .card {
        background: white;
        padding: 22px;
        border-radius: 20px;
        margin-bottom: 18px;
        box-shadow: 0px 5px 20px rgba(0, 0, 0, 0.07);
        border: 1px solid #eee;
    }

    .score {
        font-size: 30px;
        font-weight: bold;
        color: #6c4ab6;
    }

    .tag {
        display: inline-block;
        background: #eee7ff;
        color: #6743a5;
        padding: 6px 12px;
        border-radius: 20px;
        margin: 4px;
        font-size: 13px;
    }

    .small-text {
        color: #777;
        font-size: 14px;
    }

    .decor-card {
        background: #ffffff;
        padding: 18px;
        border-radius: 18px;
        border: 1px solid #eee;
        text-align: center;
        min-height: 180px;
        box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.05);
        margin-bottom: 10px;
    }

    .decor-icon {
        font-size: 42px;
        margin-bottom: 8px;
    }

    .section-card {
        background: rgba(255, 255, 255, 0.75);
        padding: 20px;
        border-radius: 18px;
        border: 1px solid #eee;
        margin-bottom: 20px;
    }

    .hero-box {
        background: linear-gradient(135deg, #eee7ff, #fff);
        padding: 28px;
        border-radius: 22px;
        border: 1px solid #e4d9ff;
        margin: 20px 0;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# DESIGN DATABASE
# =========================================================

DESIGNS = {

    "Minimalist": {
        "description": (
            "Clean, uncluttered and functional design with lots "
            "of visual breathing space."
        ),
        "space": 0.95,
        "color": 0.80,
        "function": 0.95,
        "budget": 0.90,
        "coziness": 0.55,
        "colors": ["🤍 White", "🩶 Grey", "🌿 Sage"],
        "features": [
            "Declutter unnecessary objects",
            "Use furniture with clean shapes",
            "Keep a simple color palette"
        ]
    },

    "Cozy": {
        "description": (
            "Warm and comfortable design focused on softness, "
            "lighting and relaxation."
        ),
        "space": 0.70,
        "color": 0.90,
        "function": 0.75,
        "budget": 0.80,
        "coziness": 1.00,
        "colors": ["🤎 Beige", "🧡 Warm orange", "🤍 Cream"],
        "features": [
            "Add warm lighting",
            "Use soft cushions and rugs",
            "Create a comfortable focal point"
        ]
    },

    "Biophilic": {
        "description": (
            "Bring nature indoors using plants, natural textures "
            "and earthy colors."
        ),
        "space": 0.72,
        "color": 0.95,
        "function": 0.72,
        "budget": 0.75,
        "coziness": 0.88,
        "colors": ["🌿 Green", "🤎 Brown", "🤍 Cream"],
        "features": [
            "Add indoor plants",
            "Use natural materials",
            "Introduce earthy colors"
        ]
    },

    "Scandinavian": {
        "description": (
            "Bright, practical and cozy design inspired by "
            "Nordic interiors."
        ),
        "space": 0.88,
        "color": 0.90,
        "function": 0.92,
        "budget": 0.82,
        "coziness": 0.85,
        "colors": ["🤍 White", "🪵 Light wood", "🌿 Sage"],
        "features": [
            "Use light-colored furniture",
            "Maximize natural light",
            "Combine comfort with functionality"
        ]
    },

    "Color Pop": {
        "description": (
            "A playful design that adds personality through "
            "carefully selected colors."
        ),
        "space": 0.65,
        "color": 1.00,
        "function": 0.72,
        "budget": 0.75,
        "coziness": 0.80,
        "colors": ["💗 Pink", "💛 Yellow", "💙 Blue"],
        "features": [
            "Choose one accent wall",
            "Add colorful accessories",
            "Keep large furniture neutral"
        ]
    },

    "Modern Luxury": {
        "description": (
            "Elegant and sophisticated design using statement "
            "pieces and premium-looking finishes."
        ),
        "space": 0.65,
        "color": 0.88,
        "function": 0.80,
        "budget": 0.45,
        "coziness": 0.70,
        "colors": ["🖤 Black", "✨ Gold", "🤍 Ivory"],
        "features": [
            "Add statement lighting",
            "Use metallic accents",
            "Create a strong focal point"
        ]
    },

    "Zen": {
        "description": (
            "Calm and peaceful design designed to reduce visual "
            "clutter and create relaxation."
        ),
        "space": 0.90,
        "color": 0.92,
        "function": 0.90,
        "budget": 0.88,
        "coziness": 0.90,
        "colors": ["🤍 White", "🌿 Green", "🪵 Natural wood"],
        "features": [
            "Reduce visual clutter",
            "Use natural textures",
            "Keep lighting soft"
        ]
    },

    "Study Focus": {
        "description": (
            "Productivity-focused arrangement designed for "
            "studying, working and concentration."
        ),
        "space": 0.90,
        "color": 0.78,
        "function": 1.00,
        "budget": 0.90,
        "coziness": 0.65,
        "colors": ["🤍 White", "🩶 Grey", "💙 Blue"],
        "features": [
            "Create a dedicated work zone",
            "Improve desk organization",
            "Reduce distractions"
        ]
    },

    "Space Saving": {
        "description": (
            "Smart organization ideas for smaller rooms or "
            "spaces that need better movement."
        ),
        "space": 1.00,
        "color": 0.70,
        "function": 1.00,
        "budget": 0.92,
        "coziness": 0.70,
        "colors": ["🤍 White", "🌿 Sage", "🩶 Grey"],
        "features": [
            "Use vertical storage",
            "Choose multi-purpose furniture",
            "Keep walkways clear"
        ]
    },

    "Pastel Dream": {
        "description": (
            "Soft, cute and relaxing interior style using "
            "gentle colors and decorative details."
        ),
        "space": 0.75,
        "color": 0.98,
        "function": 0.70,
        "budget": 0.80,
        "coziness": 0.95,
        "colors": ["🌸 Pink", "💜 Lavender", "💙 Baby blue"],
        "features": [
            "Use pastel accessories",
            "Add soft textures",
            "Create a cute visual theme"
        ]
    }
}


# =========================================================
# DECOR DATABASE
# =========================================================

DECOR_ITEMS = {

    "Minimalist": [
        ("🪴", "Small Ceramic Plant", "₹399"),
        ("💡", "Minimal Desk Lamp", "₹799"),
        ("🖼️", "Abstract Wall Art", "₹599"),
        ("🧺", "Neutral Storage Basket", "₹499"),
        ("🕯️", "Simple Candle", "₹299"),
        ("🪞", "Round Minimal Mirror", "₹999")
    ],

    "Cozy": [
        ("🕯️", "Warm Scented Candle", "₹349"),
        ("🧸", "Soft Cushion", "₹449"),
        ("🧶", "Chunky Throw Blanket", "₹899"),
        ("💡", "Warm Fairy Lights", "₹299"),
        ("🪴", "Cute Indoor Plant", "₹399"),
        ("🧺", "Woven Basket", "₹599")
    ],

    "Biophilic": [
        ("🌿", "Indoor Money Plant", "₹399"),
        ("🪴", "Mini Succulent", "₹249"),
        ("🌱", "Hanging Plant", "₹499"),
        ("🪵", "Wooden Plant Stand", "₹899"),
        ("🧺", "Natural Woven Basket", "₹599"),
        ("🖼️", "Botanical Wall Art", "₹499")
    ],

    "Scandinavian": [
        ("🪵", "Light Wood Side Table", "₹1,299"),
        ("💡", "Nordic Table Lamp", "₹899"),
        ("🪴", "White Ceramic Pot", "₹449"),
        ("🧺", "Fabric Storage Basket", "₹499"),
        ("🖼️", "Simple Art Print", "₹399"),
        ("🕯️", "Neutral Candle", "₹299")
    ],

    "Color Pop": [
        ("🌸", "Pink Accent Cushion", "₹399"),
        ("💛", "Yellow Table Lamp", "₹799"),
        ("🖼️", "Colorful Art Print", "₹499"),
        ("🌈", "Colorful Wall Decor", "₹599"),
        ("🪴", "Colorful Plant Pot", "₹349"),
        ("🧸", "Cute Plush Decor", "₹499")
    ],

    "Modern Luxury": [
        ("✨", "Gold Accent Vase", "₹699"),
        ("💡", "Statement Lamp", "₹1,499"),
        ("🪞", "Decorative Mirror", "₹1,299"),
        ("🖼️", "Luxury Abstract Art", "₹899"),
        ("🕯️", "Glass Candle", "₹499"),
        ("🏺", "Ceramic Vase", "₹799")
    ],

    "Zen": [
        ("🪴", "Bonsai Plant", "₹899"),
        ("🕯️", "Zen Candle", "₹399"),
        ("🪵", "Wooden Tray", "₹499"),
        ("🪨", "Decorative Stone Set", "₹299"),
        ("💡", "Soft Ambient Lamp", "₹799"),
        ("🌿", "Bamboo Plant", "₹449")
    ],

    "Study Focus": [
        ("💡", "Adjustable Study Lamp", "₹899"),
        ("📚", "Floating Bookshelf", "₹1,299"),
        ("🗂️", "Desk Organizer", "₹399"),
        ("🪴", "Small Desk Plant", "₹249"),
        ("⏰", "Minimal Desk Clock", "₹499"),
        ("📝", "Planning Board", "₹599")
    ],

    "Space Saving": [
        ("🧺", "Under-Bed Storage", "₹799"),
        ("📚", "Floating Shelf", "₹699"),
        ("🪝", "Wall Hook Organizer", "₹299"),
        ("🪞", "Wall Mirror", "₹799"),
        ("🪴", "Hanging Plant", "₹399"),
        ("📦", "Stackable Storage Box", "₹349")
    ],

    "Pastel Dream": [
        ("🌸", "Pastel Flower Vase", "₹399"),
        ("🧸", "Cute Plushie", "₹499"),
        ("💜", "Lavender Candle", "₹349"),
        ("💗", "Pink Cushion", "₹399"),
        ("🪞", "Cute Decorative Mirror", "₹699"),
        ("💡", "Pastel Night Lamp", "₹599")
    ]
}


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def normalize(value):
    """Keep a numeric value between 0 and 1."""
    return max(0.0, min(1.0, float(value)))


def calculate_score(
    design,
    room,
    budget,
    space_need,
    preferred_style
):
    """
    Calculate compatibility score using a weighted model.
    """

    data = DESIGNS[design]

    # -----------------------------------------------------
    # SPACE SCORE
    # -----------------------------------------------------

    if space_need == "Very important":
        space_score = data["space"]

    elif space_need == "Somewhat important":
        space_score = (data["space"] + 0.70) / 2

    else:
        space_score = 0.70

    # -----------------------------------------------------
    # BUDGET SCORE
    # -----------------------------------------------------

    if budget == "Low":
        budget_score = data["budget"]

    elif budget == "Medium":
        budget_score = min(1.0, data["budget"] + 0.10)

    else:
        budget_score = min(1.0, data["budget"] + 0.20)

    # -----------------------------------------------------
    # STYLE SCORE
    # -----------------------------------------------------

    if preferred_style == design:
        style_score = 1.0

    elif preferred_style == "Surprise me":
        style_score = 0.75

    else:
        style_score = 0.55

    # -----------------------------------------------------
    # ROOM SCORE
    # -----------------------------------------------------

    room_score = 0.75

    if room == "Study / Workspace" and design == "Study Focus":
        room_score = 1.00

    elif room == "Small Room" and design == "Space Saving":
        room_score = 1.00

    elif room == "Bedroom" and design in [
        "Cozy",
        "Pastel Dream",
        "Zen"
    ]:
        room_score = 0.95

    elif room == "Living Room" and design in [
        "Minimalist",
        "Scandinavian",
        "Modern Luxury"
    ]:
        room_score = 0.95

    elif room == "Balcony" and design == "Biophilic":
        room_score = 1.00

    elif room == "Kitchen" and design in [
        "Minimalist",
        "Scandinavian",
        "Space Saving"
    ]:
        room_score = 0.95

    elif room == "New Apartment" and design in [
        "Minimalist",
        "Scandinavian",
        "Space Saving"
    ]:
        room_score = 0.95

    # -----------------------------------------------------
    # FINAL WEIGHTED SCORE
    # -----------------------------------------------------

    final_score = (
        space_score * 0.25
        + data["color"] * 0.15
        + data["function"] * 0.20
        + budget_score * 0.15
        + style_score * 0.15
        + room_score * 0.10
    )

    return round(normalize(final_score) * 100)


def generate_reason(design, room, budget):
    """Generate a human-readable explanation."""

    reasons = []

    if design == "Space Saving":
        reasons.append(
            "excellent for improving movement and storage"
        )

    if design == "Study Focus" and room == "Study / Workspace":
        reasons.append("matches your workspace")

    if design == "Biophilic":
        reasons.append("adds natural elements")

    if design == "Cozy":
        reasons.append("increases warmth and comfort")

    if design == "Minimalist":
        reasons.append("reduces visual clutter")

    if design == "Scandinavian":
        reasons.append(
            "balances functionality and comfort"
        )

    if design == "Zen":
        reasons.append(
            "creates a calmer environment"
        )

    if design == "Pastel Dream":
        reasons.append(
            "adds a soft and playful atmosphere"
        )

    if design == "Color Pop":
        reasons.append(
            "adds personality through color"
        )

    if design == "Modern Luxury":
        reasons.append(
            "creates a sophisticated visual focal point"
        )

    if budget == "Low":
        reasons.append(
            "can be adapted using budget-friendly decor"
        )

    if not reasons:
        reasons.append(
            "fits your selected preferences"
        )

    return ", ".join(reasons).capitalize() + "."


# =========================================================
# SESSION STATE
# =========================================================

if "recommendations" not in st.session_state:
    st.session_state.recommendations = []

if "selected_design" not in st.session_state:
    st.session_state.selected_design = None

if "uploaded_image" not in st.session_state:
    st.session_state.uploaded_image = None


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">ASTRA 🏠</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="subtitle">
        Adaptive Space Transformation & Recommendation Assistant
    </div>
    """,
    unsafe_allow_html=True
)

st.write(
    "Turn an ordinary space into something that feels uniquely yours."
)

st.divider()


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("⚙️ Your Preferences")

    room = st.selectbox(
        "What are you customizing?",
        [
            "Bedroom",
            "Living Room",
            "Study / Workspace",
            "Kitchen",
            "Balcony",
            "Small Room",
            "New Apartment"
        ]
    )

    preferred_style = st.selectbox(
        "Preferred design style",
        [
            "Surprise me",
            "Minimalist",
            "Cozy",
            "Biophilic",
            "Scandinavian",
            "Color Pop",
            "Modern Luxury",
            "Zen",
            "Study Focus",
            "Space Saving",
            "Pastel Dream"
        ]
    )

    budget = st.select_slider(
        "Budget",
        options=[
            "Low",
            "Medium",
            "High"
        ],
        value="Medium"
    )

    space_need = st.select_slider(
        "How important is space optimization?",
        options=[
            "Not important",
            "Somewhat important",
            "Very important"
        ],
        value="Somewhat important"
    )

    st.divider()

    st.caption(
        "ASTRA uses a weighted recommendation model "
        "to rank design possibilities."
    )


# =========================================================
# PHOTO UPLOAD
# =========================================================

st.header("📸 1. Show us your space")

uploaded_file = st.file_uploader(
    "Upload a photo of the room or object you want to customize",
    type=["jpg", "jpeg", "png"],
    help="Supported formats: JPG, JPEG and PNG."
)

if uploaded_file is not None:

    try:

        image = Image.open(uploaded_file)

        # Force loading so corrupted files are caught.
        image.load()

        st.session_state.uploaded_image = image

        col1, col2 = st.columns(
            [1, 1],
            gap="large"
        )

        with col1:

            st.image(
                image,
                caption="Your uploaded space",
                use_container_width=True
            )

        with col2:

            st.info(
                "ASTRA combines your uploaded space with "
                "your preferences to create design recommendations."
            )

            st.write("### 🔎 What ASTRA considers")

            st.write("📐 Space optimization")
            st.write("🎨 Color compatibility")
            st.write("🪑 Functionality")
            st.write("💰 Budget")
            st.write("✨ Style preference")
            st.write("🏠 Room type")

    except Exception:
        st.error(
            "The uploaded file could not be read. "
            "Please upload a valid JPG, JPEG or PNG image."
        )

else:

    st.info(
        "Upload a room photo above, or continue without "
        "a photo using your preferences."
    )


# =========================================================
# ANALYZE BUTTON
# =========================================================

st.header("🧠 2. Find your best designs")

if st.button(
    "✨ ANALYZE MY SPACE",
    type="primary",
    use_container_width=True
):

    with st.spinner(
        "Analyzing your preferences..."
    ):

        results = []

        for design in DESIGNS:

            score = calculate_score(
                design=design,
                room=room,
                budget=budget,
                space_need=space_need,
                preferred_style=preferred_style
            )

            reason = generate_reason(
                design=design,
                room=room,
                budget=budget
            )

            results.append(
                {
                    "name": design,
                    "score": score,
                    "reason": reason
                }
            )

        # Highest score first.
        results.sort(
            key=lambda item: item["score"],
            reverse=True
        )

        # Keep all 10 available styles.
        st.session_state.recommendations = results[:10]

        # Clear previous selection.
        st.session_state.selected_design = None

    st.success(
        "✨ Analysis complete! "
        "Here are your top 10 personalized possibilities."
    )


# =========================================================
# RESULTS
# =========================================================

if st.session_state.recommendations:

    st.header("🏆 Your Recommendations")

    for index, result in enumerate(
        st.session_state.recommendations
    ):

        name = result["name"]
        score = result["score"]
        reason = result["reason"]

        data = DESIGNS[name]

        st.markdown(
            '<div class="card">',
            unsafe_allow_html=True
        )

        col1, col2, col3 = st.columns(
            [0.6, 2.4, 1],
            gap="large"
        )

        with col1:

            st.markdown(
                f"### #{index + 1}"
            )

        with col2:

            st.subheader(name)

            st.write(
                data["description"]
            )

            for color in data["colors"]:

                st.markdown(
                    f'<span class="tag">{color}</span>',
                    unsafe_allow_html=True
                )

            st.write("")

            st.caption(
                f"Why it fits: {reason}"
            )

        with col3:

            st.markdown(
                f'<div class="score">{score}%</div>',
                unsafe_allow_html=True
            )

            st.caption("Compatibility")

            st.progress(
                score / 100
            )

            if st.button(
                "Choose",
                key=f"choose_design_{index}",
                use_container_width=True
            ):

                st.session_state.selected_design = name

                # Rerun so the selected section appears immediately.
                st.rerun()

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )


# =========================================================
# SELECTED DESIGN
# =========================================================

if st.session_state.selected_design:

    selected = st.session_state.selected_design
    data = DESIGNS[selected]

    st.divider()

    st.header(
        f"✨ Your Selected Style: {selected}"
    )

    st.markdown(
        f"""
        <div class="hero-box">
            <h2>{selected}</h2>
            <p>{data["description"]}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(
        2,
        gap="large"
    )

    with col1:

        st.subheader("💡 Transformation Ideas")

        for feature in data["features"]:

            st.write(
                f"✓ {feature}"
            )

    with col2:

        st.subheader("🎨 Suggested Palette")

        for color in data["colors"]:

            st.write(color)


# =========================================================
# DECOR SECTION
# =========================================================

if st.session_state.selected_design:

    selected = st.session_state.selected_design

    st.divider()

    st.header("🛍️ Cute Decor Inspiration")

    st.write(
        f"Here are some items that match your "
        f"**{selected}** style."
    )

    items = DECOR_ITEMS[selected]

    cols = st.columns(3, gap="medium")

    for index, item in enumerate(items):

        icon, item_name, price = item

        with cols[index % 3]:

            st.markdown(
                f"""
                <div class="decor-card">
                    <div class="decor-icon">
                        {icon}
                    </div>
                    <h4>{item_name}</h4>
                    <p class="small-text">
                        Starting at {price}
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.button(
                "♡ Add to inspiration",
                key=f"decor_{selected}_{index}",
                use_container_width=True
            )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "🏠 ASTRA • Smart Space Designer • "
    "Personalized interior inspiration"
)


