from flask import Flask, render_template, request, redirect, url_for, session, jsonify,flash
from werkzeug.utils import secure_filename
import os
from models import db, Place

app = Flask(__name__)
app.secret_key = "x!7R$ecretK3y2025"

# إعداد قاعدة البيانات
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tourism.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# إنشاء الجداول
with app.app_context():
    db.create_all()

# ========== الصفحة الرئيسية ==========
@app.route("/")
def home():
    return render_template("index.html")

# ========== عرض كل الأماكن ==========
@app.route("/info")
def info():
    places = Place.query.all()
    return render_template("info.html", place=places)

# ========== صفحة عرض مكان ==========
@app.route("/place/<int:place_id>")
def show_place(place_id):
    place = Place.query.get_or_404(place_id)
    
    return render_template("place.html", place=place)


# ========== لوحة الأدمن ==========
@app.route("/admin-dashboard")
def admin_dashboard():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    places = Place.query.all()
    return render_template("admin_dashboard.html", places=places)

# ========== تسجيل دخول ==========
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == "admin" and password == "000":
            session["logged_in"] = True
            return redirect(url_for("admin_dashboard"))
        else:
            return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    return redirect(url_for("login"))

@app.route("/admin/place/<int:place_id>")
def admin_show_place(place_id):
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    place = Place.query.get_or_404(place_id)
    return render_template("admin_place.html", place=place)


# ==============================
# إضافة مكان جديد
# ==============================
@app.route('/add_place', methods=['GET', 'POST'])
def add_place():
    if request.method == 'POST':
        name_place = request.form['name_place']
        name_country = request.form['name_country']
        description = request.form['description']
        lat = request.form.get('lat', type=float)
        lng = request.form.get('lng', type=float)
        link_photo = request.form.get('link_photo')
        flag = request.form.get('flag')
        link_pa = request.form.get('link_pa')
        details_url = request.form.get('details_url')

        new_place = Place(
            name_place=name_place,
            name_country=name_country,
            description=description,
            lat=lat,
            lng=lng,
            link_photo=link_photo,
            flag=flag,
            link_pa=link_pa,
            details_url=details_url
        )

        db.session.add(new_place)
        db.session.commit()
        flash("✅ Place added successfully!", "success")
        return redirect(url_for('admin_dashboard'))

    return render_template('add_place.html')


# ==============================
# تعديل مكان
# ==============================
@app.route('/update_place/<int:place_id>', methods=['GET', 'POST'])
def update_place(place_id):
    place = Place.query.get_or_404(place_id)

    if request.method == 'POST':
        place.name_place = request.form['name_place']
        place.name_country = request.form['name_country']
        place.description = request.form['description']
        place.lat = request.form.get('lat', type=float)
        place.lng = request.form.get('lng', type=float)
        place.flag = request.form.get('flag')
        place.link_pa = request.form.get('link_pa')
        place.details_url = request.form.get('details_url')

        # لو المستخدم دخل صورة جديدة
        new_photo = request.form.get('link_photo')
        if new_photo and new_photo.strip():
            place.link_photo = new_photo

        db.session.commit()
        flash("✅ Place updated successfully!", "success")
        return redirect(url_for('admin_dashboard'))

    return render_template('edit_place.html', place=place)


# ==============================
# حذف مكان
# ==============================
@app.route('/delete_place/<int:place_id>', methods=['POST', 'GET'])
def delete_place(place_id):
    place = Place.query.get_or_404(place_id)
    db.session.delete(place)
    db.session.commit()
    flash("🗑️ Place deleted successfully!", "danger")
    return redirect(url_for('admin_dashboard'))



@app.route("/chatbot")
def chatbot():
    return render_template("chatbot.html")

@app.route("/chat", methods=["POST"])
def chat():
    """Handles chat requests from the frontend."""
    if not request.is_json or "message" not in request.json:
        return jsonify(error="Invalid request format"), 400
    user_input = request.json["message"].lower()
    response = get_bot_response(user_input)
    return jsonify(response=response)

def get_bot_response(user_input):
    """Generates a response based on user input about Arab material/non-material heritage and tourism."""
    #nature welcome
    if "hello" in user_input or "hi" in user_input or "hey" in user_input:
        return "Hello! How can I assist you with information about Arab heritage and tourism today?"
    elif "help" in user_input or "assist" in user_input:
        return "Sure! I can provide information about Arab heritage, including tangible and intangible aspects, as well as tourism sites. What would you like to know?"
    elif "arab heritage" in user_input:
        return "Arab heritage includes both tangible and intangible elements, such as historical sites, architecture, traditional crafts, music, dance, and oral traditions. Would you like to know more about a specific aspect?"
    elif "tourism" in user_input:
        return "Arab countries offer a rich variety of tourism experiences, from ancient ruins and modern cities to cultural festivals and natural wonders. Are you interested in a specific country or type of tourism?"
    # Arab tangible heritage
    if "oldest mosque" in user_input:
        return "The oldest mosque in Islam is Quba Mosque in Medina."
    elif "saladin citadel" in user_input:
        return "The famous citadel in Cairo is the Citadel of Saladin."
    elif "alhambra" in user_input:
        return "The Alhambra Palace is located in Granada, Spain."
    elif "petra" in user_input:
        return "Petra is a historic rock-carved city located in Jordan."
    elif "palmyra" in user_input:
        return "Palmyra in Syria is famous for its ancient ruins like the Temple of Baalshamin."
    elif "giza pyramids" in user_input:
        return "The Pyramids of Giza in Egypt are among the Seven Wonders of the World."
    elif "sanaa market" in user_input:
        return "The historic market in Old Sana'a is known as Souq Al-Milh."
    elif "umayyad palace" in user_input:
        return "A famous Umayyad palace is Qasr Amra in Jordan."
    elif "mud tower" in user_input:
        return "The mud tower in Najdi architecture is used for ventilation and cooling."
    elif "umayyad mosque" in user_input:
        return "The Umayyad Mosque in Damascus is one of the oldest and most significant mosques in the Islamic world."
    elif "chefchaouen" in user_input:
        return "Chefchaouen in Morocco is known for its blue alleyways."
    elif "nouakchott mosque" in user_input:
        return "The Grand Mosque in Nouakchott is a major Islamic landmark in Mauritania."
    elif "aleppo citadel" in user_input:
        return "Aleppo Citadel is one of the oldest and most prominent Islamic fortresses."
    elif "kutubiyya minaret" in user_input:
        return "The Kutubiyya Minaret is located in Marrakesh, Morocco."
    elif "roman amphitheater amman" in user_input:
        return "The Roman Amphitheater is located in the heart of Amman, Jordan."
    elif "nizwa fort" in user_input:
        return "The famous fort in Nizwa, Oman is Nizwa Fort."
    elif "tutankhamun treasures" in user_input:
        return "Tutankhamun's treasures are displayed in the Egyptian Museum in Cairo."
    elif "baghdad wall" in user_input:
        return "The old wall of Baghdad is a historical defensive landmark."
    elif "old algiers" in user_input:
        return "The Casbah of Algiers is listed as a UNESCO World Heritage Site."
    elif "ghardaia palace" in user_input:
        return "Ghardaïa in Algeria features ancient architectural landmarks."
    elif "roman bridge lebanon" in user_input:
        return "The Roman bridge in Qannoubine is one of Lebanon's famous landmarks."
    elif "sidon phoenician site" in user_input:
        return "The Sea Castle in Sidon is a prominent Phoenician site."
    elif "yemeni traditional house" in user_input:
        return "The traditional Yemeni house has multiple floors and ornate windows."
    elif "qasr al-mshatta" in user_input:
        return "Qasr al-Mshatta is located in Jordan and is an example of Umayyad architecture."
    elif "fes gates" in user_input:
        return "A famous historic gate in Fes is Bab Boujloud."
    elif "karbala shrine" in user_input:
        return "A famous shrine in Karbala is the Shrine of Imam Hussein."
    elif "bahrain fort" in user_input:
        return "The old fort in Bahrain is known as Qal'at al-Bahrain."
    elif "leptis magna" in user_input:
        return "Leptis Magna is an ancient city in Libya."
    elif "tunisia palace" in user_input:
        return "The famous palace in Tunisia is Dar Hussein."
    elif "buried buildings libya" in user_input:
        return "Ghadames in Libya is known for its partially underground buildings."

    # Arab intangible heritage
    elif "intangible heritage" in user_input:
        return "Intangible heritage includes oral arts, customs, rituals, and cultural practices."
    elif "dabke" in user_input:
        return "Dabke is a group dance popular in the Levant."
    elif "ayyala" in user_input:
        return "Ayyala is a traditional performance practiced in the UAE and Oman."
    elif "muwashahat" in user_input:
        return "Andalusian muwashahat are a type of poetry and song that originated in Al-Andalus."
    elif "folk tales" in user_input:
        return "Folk tales are traditional stories passed orally between generations."
    elif "zajal" in user_input:
        return "Zajal is a form of improvised folk poetry recited musically."
    elif "rebab and oud" in user_input:
        return "The rebab is a Bedouin string instrument, and the oud is a traditional Arab instrument."
    elif "samri" in user_input:
        return "Samri is a popular folk music genre in the Gulf region."
    elif "huda" in user_input:
        return "Huda is a type of chant sung during camel caravans in the desert."
    elif "types of arabic poetry" in user_input:
        return "Types of Arabic poetry include classical, Nabati, and free verse."
    elif "moroccan beliefs" in user_input:
        return "Moroccan popular beliefs include rituals of luck, the evil eye, and blessing."
    elif "literary gatherings" in user_input:
        return "Traditional literary gatherings were held for poetry and cultural discussions."
    elif "sudanese dances" in user_input:
        return "One of the Sudanese folk dances is the Kambala dance."
    elif "tanbura art" in user_input:
        return "Tanbura is a popular art form in the Gulf and Sudan."
    elif "handicrafts" in user_input:
        return "Handicrafts reflect the identity of Arab communities and are important heritage elements."
    elif "levant tales" in user_input:
        return "Levantine heritage stories include Antar and Abla, and Abu Zayd al-Hilali."
    elif "sadu" in user_input:
        return "Sadu is a Bedouin weaving art used to make tents and rugs."
    elif "bedouin weddings" in user_input:
        return "Bedouin weddings involve traditions like parades and chants."
    elif "malouf" in user_input:
        return "Malouf is a traditional music style in North Africa."
    elif "prophetic praises" in user_input:
        return "Prophetic praises are religious chants praising Prophet Muhammad."
    elif "sufi poetry" in user_input:
        return "Sufi poetry expresses divine love."
    elif "nay and mijwiz" in user_input:
        return "The nay is a soft wind instrument and the mijwiz has a sharp sound."
    elif "desert hospitality" in user_input:
        return "Generosity is a core value in desert culture."
    elif "storytelling in education" in user_input:
        return "Folk stories are used to instill values and transmit knowledge."
    elif "arabic calligraphy" in user_input:
        return "Arabic calligraphy is considered a visual art and heritage."
    elif "harvest songs" in user_input:
        return "They are traditional songs sung during harvest seasons."
    elif "ardha" in user_input:
        return "Ardha is a dance and sword performance practiced in Saudi Arabia."
    elif "arabic maqams" in user_input:
        return "Maqams are used to define melodic modes in Arabic singing."
    elif "hakawati" in user_input:
        return "Hakawati is a storyteller in popular gatherings."
    elif "arab proverbs" in user_input:
        return "Proverbs express inherited wisdom and experience."

    # Arab tourism
    elif "tourism" in user_input and "egypt" in user_input:
        return "Tourism in Egypt includes the Pyramids, Luxor, Aswan, and the Red Sea."
    elif "marrakech" in user_input:
        return "Marrakech is a unique tourist destination known for its markets and architecture."
    elif "lebanon" in user_input and "tourism" in user_input:
        return "Lebanon is rich in landmarks such as Baalbek, Jounieh, and Tripoli."
    elif "saudi arabia" in user_input:
        return "Tourist spots include AlUla, Riyadh, Jeddah, and Mecca."
    elif "alula" in user_input:
        return "AlUla is known for Nabatean sites like Madain Saleh."
    elif "oman" in user_input:
        return "Popular destinations in Oman include Salalah, Jebel Akhdar, and Muscat."
    elif "tourism" in user_input and "tunisia" in user_input:
        return "The best time to visit Tunisia is spring and fall."
    elif "dubai" in user_input:
        return "Famous landmarks include Burj Khalifa, Dubai Fountain, and Dubai Mall."
    elif "dead sea" in user_input:
        return "It is a major site for tourism and wellness."
    elif "religious tourism" in user_input and "iraq" in user_input:
        return "Najaf and Karbala are key religious tourism destinations."
    elif "morocco beaches" in user_input:
        return "Famous beaches include Agadir, Essaouira, and Tangier."
    elif "arab museums" in user_input:
        return "Notable ones include the Museum of Islamic Art in Doha and the Egyptian Museum."
    elif "mountain climbing" in user_input:
        return "The Atlas Mountains and Mount Toubkal are top climbing spots."
    elif "diving" in user_input:
        return "The Red Sea in Egypt offers some of the best diving spots."
    elif "empty quarter" in user_input:
        return "It is one of the world's largest sand deserts, located in Saudi Arabia."
    elif "algeria destinations" in user_input:
        return "Include Tassili, Hoggar, and M'zab Valley."
    elif "traditional markets" in user_input:
        return "Famous ones are in Fes, Marrakesh, and Aleppo."
    elif "baalbek" in user_input:
        return "An archaeological site in Lebanon known for its festivals."
    elif "eco-tourism" in user_input:
        return "It helps preserve nature and boosts local economies."
    elif "desert tourism" in user_input:
        return "It attracts adventurers and nature lovers to dunes and oases."
    elif "cultural tourism" in user_input:
        return "It focuses on heritage and history, unlike nature tourism."
    elif "islamic architecture" in user_input:
        return "Notable cities include Cordoba, Fes, and Cairo."
    elif "coastal cities" in user_input:
        return "Such as Alexandria, Tyre, and Agadir."
    elif "festivals" in user_input:
        return "They attract tourists and promote culture, like Carthage Festival."
    elif "emirates cities" in user_input:
        return "Abu Dhabi, Sharjah, and Al Ain are top destinations."
    elif "fes" in user_input:
        return "A heritage city known for its markets and Al-Qarawiyyin Mosque."
    elif "mount toubkal" in user_input:
        return "The highest peak in Morocco and a destination for climbers."
    elif "nile river" in user_input:
        return "A vital part of Egypt's Nile tourism."
    elif "cultural exhibitions" in user_input:
        return "They promote heritage understanding and boost tourism."
    elif "skiing lebanon" in user_input:
        return "Top spots include Faraya and the Cedars."
    elif "local food" in user_input:
        return "It provides a unique tourism experience."
    elif "heritage promotion" in user_input:
        return "It supports cultural tourism."
    elif "bahrain islands" in user_input:
        return "Includes Amwaj Islands and Sitra."
    elif "digital platforms" in user_input:
        return "They enhance tourism promotion via visual content."
    elif "unesco cities" in user_input:
        return "Such as Fes, Zabid, and Old Sana'a."
    elif "winter tourism" in user_input:
        return "Practiced in Lebanon, Morocco, and Tunisia's mountains."
    elif "traditional crafts" in user_input:
        return "They attract tourists and are showcased in local markets."
    elif "qatar attractions" in user_input:
        return "Includes Souq Waqif, Corniche, and Qatar National Museum."
    elif "historical tourism experience" in user_input:
        return "Offered in cities like Jerusalem, Cairo, and Damascus."

    #arab aritsts
    elif "arab artists" in user_input:
        return "Arab artists include Fairouz, Umm Kulthum, and Marcel Khalife."
    elif "fairouz" in user_input:
        return "Fairouz is a legendary Lebanese singer known for her unique voice and timeless songs."
    elif "umm kulthum" in user_input:
        return "Umm Kulthum was an iconic Egyptian singer and actress, celebrated for her powerful voice and emotional performances."
    elif "marcel khalife" in user_input:
        return "Marcel Khalife is a renowned Lebanese composer and oud player, known for his contributions to Arabic music and culture."
    elif "najwa karam" in user_input:
        return "Najwa Karam is a popular Lebanese singer and songwriter, often referred to as the 'Sun of Lebanese Song'."
    elif "elissa" in user_input:
        return "Elissa is a famous Lebanese pop singer known for her romantic ballads and powerful voice."
    elif "amr diab" in user_input:
        return "Amr Diab is an Egyptian singer and composer, often called the 'Father of Mediterranean Music'."
    elif "ragheb alama" in user_input:
        return "Ragheb Alama is a well-known Lebanese singer and television personality, famous for his romantic songs."
    elif "nawal al zoghbi" in user_input:
        return "Nawal Al Zoghbi is a popular Lebanese singer known for her catchy pop songs and vibrant performances."  
    # Arab arts
    elif "arab arts" in user_input:
        return "Arab arts include music, dance, visual arts, and literature, reflecting the rich cultural heritage of the Arab world."
    elif "arab music" in user_input:
        return "Arab music is diverse, with genres like classical, folk, pop, and contemporary styles."
    elif "arab dance" in user_input:
        return "Traditional Arab dance includes styles like belly dance, folk dances, and modern interpretations."
    elif "arab visual arts" in user_input:
        return "Arab visual arts encompass calligraphy, painting, sculpture, and contemporary art forms."
    elif "arab literature" in user_input:
        return "Arab literature includes poetry, prose, and storytelling traditions that have shaped the region's cultural identity."
    elif "arab cinema" in user_input:
        return "Arab cinema has a rich history with influential filmmakers and actors contributing to the global film industry."
    elif "arab theater" in user_input:
        return "Arab theater combines traditional storytelling with modern performances, often addressing social and political themes."
    elif "arab architecture" in user_input:
        return "Arab architecture showcases a blend of historical styles, including Islamic, Ottoman, and modern influences."
    elif "arab fashion" in user_input:
        return "Arab fashion reflects cultural diversity with traditional garments and contemporary designs gaining international recognition."
    elif "arab photography" in user_input:
        return "Arab photography captures the region's landscapes, people, and cultural heritage through various artistic lenses."
    elif "arab crafts" in user_input:
        return "Traditional Arab crafts include pottery, weaving, metalwork, and glassblowing, showcasing skilled artisanship."
    else:
        return "Sorry, I didn't understand your question. Try asking about Arab heritage or tourism."
@app.route('/map')
def map():
    places = Place.query.all()
    landmarks = [
        {
            "lat": p.lat,
            "lng": p.lng,
            "name_place": p.name_place,
            "url": url_for('show_place', place_id=p.id),
            "size": 0.3
        }
        for p in places
    ]
    return render_template("map.html", landmarks=landmarks)




@app.route('/booking_hotel')
def booking_hotel():
    return render_template("booking_hotel.html")

@app.route('/booking_flight')
def booking_flight():
    return render_template("booking_flight.html")

if __name__ == '__main__':
    app.run(port=5000, debug=True)
