import streamlit as strl
import requests
import time

# إعدادات الصفحة الرسمية باسم تطبيقك الجديد Just Ride
strl.set_page_config(page_title="Just Ride - Global Beat Platform", page_icon="🎵", layout="centered")

# كود التنسيق لتغيير الألوان للأزرق الغامق المريح (Deep Ocean) وتظبيط الاستايل الرسمي
strl.markdown("""
    <style>
    .stApp { background-color: #0a192f; color: #ffffff; }
    div.stButton > button:first-child {
        background-color: #ffffff; color: #0a192f; font-weight: bold; border-radius: 8px; width: 100%;
    }
    .main-nav { display: flex; justify-content: space-around; background-color: #112240; padding: 15px; border-radius: 12px; position: fixed; bottom: 10px; left: 10px; right: 10px; z-index: 100; }
    .nav-btn { background: none; border: none; color: #64ffda; font-size: 24px; cursor: pointer; }
    </style>
""", unsafe_allow_html=True)

# الـ Token السري بتاعك ورابط نموذج ميتا المتصل بـ Hugging Face
HF_TOKEN = "hf_twsNBPdTdRNGgdhbpGCACqivxXFYyrWxMehf_hxQGQWuHhGiFHIGHrbuLhfJuWzmRINeNyn"
API_URL = "https://huggingface.co"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

# --- قاعدة البيانات الكبرى لجميع أنواع المزيكا في العالم (تم دمجها بالكامل في قلب التطبيق) ---
GLOBAL_MUSIC_DATABASE = {
    "Hip_Hop_And_Rap": {
        "US_Trap": {"tempo": 140, "instruments": "808 Bass, Hi-Hats, Synthesizer Lead, Digital Snare", "desc": "Double-time Hi-Hats, heavy 808 sub-bass syncopation"},
        "Boom_Bap": {"tempo": 90, "instruments": "Vinyl Crackle, Acoustic Drum Samples, Rhodes Piano, Upright Bass", "desc": "Classic Neck-snapping Kick and Snare, heavy swing"},
        "UK_Drill": {"tempo": 142, "instruments": "Sliding 808 Bass, Dark Grand Piano, Minor Strings, Vocal Chops", "desc": "Skipping Counter-Snares, hard-hitting kicks, triplet hi-hat"},
        "US_Drill": {"tempo": 140, "instruments": "Aggressive 808, Dark Synths, Brass Stabs", "desc": "Chop-hop snare placements, fast-paced syncopation"},
        "Lo_Fi_Hip_Hop": {"tempo": 80, "instruments": "Muted Guitar, Jazz Chords, Ambient Noise", "desc": "Dusty, unquantized kick-snare with high-cut filter"}
    },
    "Egyptian_And_North_African": {
        "Mahraganat_Street_Shaabi": {"tempo": 132, "instruments": "Distorted Electro Synth, Heavy Digital Kicks, Rababa, Auto-tune FX", "desc": "Aggressive Electronic Maqsoum with accelerated snare rolls"},
        "Trap_Shaabi": {"tempo": 138, "instruments": "808 Bass Line, Mizmar Synth, Electronic Tabla, Hi-Hats", "desc": "Hybrid Trap hi-hats layered over Egyptian Shaabi kick"},
        "Shaabi_Classical": {"tempo": 115, "instruments": "Kawala, Accordions, Acoustic Tabla, Sagat", "desc": "Traditional Maqsoum (Dum-Tak-Tak-Dum-Tak)"},
        "Rai_Algerian": {"tempo": 108, "instruments": "Synthesizer Accordion, Gasba Flute, Acoustic Darbuka", "desc": "Traditional Rai rhythm, 6/8 swing variant"},
        "Gnawa_Moroccan": {"tempo": 120, "instruments": "Sintir, Qraqeb, Vocal Call-and-Response", "desc": "Polyrhythmic triple-meter hypnotic loop"}
    },
    "Levantine_And_Iraqi": {
        "Dabke_Levantine": {"tempo": 126, "instruments": "Mejwez, Yarghoul, Heavy Studio Def, Keyboard Pitch-bend", "desc": "Dabke rhythm with heavy emphasis on the downbeat"},
        "Iraqi_Chobi": {"tempo": 130, "instruments": "Kashba Flute, Iraqi Rababa, Heavy Hand Claps", "desc": "Chobi rhythm, rapid syncopated percussion"},
        "Levantine_Hip_Hop": {"tempo": 92, "instruments": "Sad Oud samples, Minor Violins, Boom Bap Drums", "desc": "Classic Hip-Hop layout blended with microtonal oriental instruments"}
    },
    "Khaleeji_And_Yemeni": {
        "Khaleeji_Khabaiti": {"tempo": 140, "instruments": "Khaleeji Mirwas Drums, Oud, Clap Ensembles", "desc": "Khabaiti polyrhythmic fast tempo"},
        "Khaleeji_Dosari": {"tempo": 145, "instruments": "Heavy Tar Percussion, Urgent Vocal Shouts", "desc": "High-energy Dosari tribal rhythm"},
        "Sanaa_Yemeni": {"tempo": 85, "instruments": "Yemeni Oud, Copper Plate Sahn, Soft Percussion", "desc": "Slow, intricate traditional Yemeni rhythmic cycles"}
    },
    "Electronic_And_Dance": {
        "Synthwave_80s": {"tempo": 115, "instruments": "Analog Synths, DX7 Electric Piano, LinnDrum Samples", "desc": "Four-on-the-floor kick with gated reverb snare"},
        "Techno_House": {"tempo": 126, "instruments": "909 Kick Drum, Acid Bassline 303, Open Hi-Hats", "desc": "Continuous driving 4/4 Kick, off-beat hi-hats"},
        "Afrobeat": {"tempo": 112, "instruments": "Congas, Shekere, Muted Electric Guitar, Brass Section", "desc": "Complex polyrhythmic groove, interlocking percussion"},
        "Reggaeton": {"tempo": 95, "instruments": "Dem Bow Riddim, Synthesizer Chords, Sub-Bass", "desc": "Classic Dem Bow kick-snare syncopation (Tresillo)"},
        "Amapiano": {"tempo": 113, "instruments": "Log Drum Heavy Bass, Shakers, Deep House Pads, Flutes", "desc": "Percussive, bass-heavy South African deep house"}
    }
}

# إدارة الشاشات والبيانات
if "screen" not in strl.session_state:
    strl.session_state.screen = "auth"
if "beat_generated" not in strl.session_state:
    strl.session_state.beat_generated = False
if "current_prompt" not in strl.session_state:
    strl.session_state.current_prompt = ""

# ----------------- الشاشة الأولى: تسجيل الدخول -----------------
if strl.session_state.screen == "auth":
    strl.markdown("<h1 style='text-align: center; color: #64ffda; font-size: 50px; font-weight: bold;'>Just Ride 🎵</h1>", unsafe_allow_html=True)
    strl.markdown("<h3 style='text-align: center; color: #8892b0;'>منصة هندسة وتوليد المقاطع الموسيقية العالمية</h3>", unsafe_allow_html=True)
    strl.write("")
    if strl.button("🌐 تسجيل الدخول بواسطة Google"):
        with strl.spinner("فضلاً انتظر.. جاري تحديد البريد الإلكتروني الخاص بك..."):
            time.sleep(1.5)
            strl.session_state.screen = "dashboard"
            strl.rerun()

# ----------------- الشاشة الثانية: اللوحة النظيفة الفاضية -----------------
elif strl.session_state.screen == "dashboard":
    # الشاشة نظيفة تماماً من فوق بناءً على طلبك
    strl.write("")
    
    # إذا تم توليد تراك يظهر هنا بنظافة مع كفر الصورة وقائمة الـ 3 نقط للتعديل
    if strl.session_state.beat_generated:
        strl.markdown("<div style='background-color: #112240; padding: 25px; border-radius: 12px; text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.3);'>", unsafe_allow_html=True)
        strl.markdown("<h4 style='color: #64ffda;'>Just Ride Track Ready</h4>", unsafe_allow_html=True)
        strl.image("https://placehold.co", width=200) # كفر الصورة التلقائي
        strl.audio("https://soundhelix.com") # المقطع الصوتي للبيت
        
        # قائمة الـ 3 نقط السحرية للتعديل الجراحي
        opt = strl.selectbox("⚙️ خيارات التعديل الجراحي (النقاط الثلاث)", ["اختر التعديل المطلوب...", "Change Drums", "Change Melody", "Change Bass/Pad"])
        if opt in ["Change Drums", "Change Melody", "Change Bass/Pad"]:
            strl.session_state.screen = "generator"
            strl.session_state.modify_target = opt
            strl.rerun()
        strl.markdown("</div>", unsafe_allow_html=True)

    # شريط الأزرار السفلي (Bottom Navigation)
    strl.write("---")
    col1, col2, col3 = strl.columns(3)
    with col1:
        if strl.button("👤 ملفي"): pass
    with col2:
        if strl.button("🎵 إنتاج"):
            strl.session_state.screen = "generator"
            strl.rerun()
    with col3:
        if strl.button("⚙️ إعدادات"): pass

# ----------------- الشاشة الثالثة: خانة الـ 🎵 (الإنتاج والوصف لكل أنواع العالم) -----------------
elif strl.session_state.screen == "generator":
    strl.markdown("<h2 style='color: #64ffda;'>Just Ride - استوديو الإنتاج</h2>", unsafe_allow_html=True)
    
    # التحقق إذا كنا راجعين من الـ 3 نقط للتعديل الجراحي
    if "modify_target" in strl.session_state:
        strl.warning(f"⚠️ وضع التعديل الجراحي نشط: أنت تقوم بتغيير الـ [{strl.session_state.modify_target}] فقط.")
    
    # زرار الدندنة بالبوق أعلى اليمين
    col_mic, _ = strl.columns([2, 2])
    with col_mic:
        audio_file = strl.audio_input("🎙️ تحويل الدندنة الصوتية")
        if audio_file:
            strl.info("🎙️ تم التقاط الدندنة الصوتية بنجاح.")

    # حقل الوصف النصي العادي
    prompt = strl.text_area("الوصف الموسيقي المطلوب", placeholder="يرجى كتابة وصف النمط الموسيقي هنا (مثال: US Drill, Trap Shaabi, Mahraganat, Boom Bap)...")
    
    if strl.button("🔥 توليد المقطع الموسيقي"):
        # الشاشة الرابعة: شاشة الانتظار الرسمية الصارمة
        with strl.spinner("جاري معالجة وهندسة المقطع الموسيقي.. فضلاً انتظر."):
            
            # فلترة ووصف المقطع بناءً على الموسيقى العالمية اللي في الـ Database
            final_prompt = prompt
            for region, styles in GLOBAL_MUSIC_DATABASE.items():
                for style, data in styles.items():
                    if style.lower() in prompt.lower() or style.replace("_", " ").lower() in prompt.lower():
                        # تدعيم طلب المستخدم بكل تفاصيل الآلات والإيقاع من قاعدة البيانات عشان تطلع احترافية
                        final_prompt = f"{prompt}, Style: {style}, Instruments: {data['instruments']}, BPM: {data['tempo']}, Rhythm: {data['desc']}"
                        break
            
            # إرسال الطلب النهائي المدعم بالكامل لـ Meta MusicGen عبر الـ API Token بتاعك
            payload = {"inputs": final_prompt if final_prompt else "Premium universal rap beat", "parameters": {"duration": 15}}
            res = requests.post(API_URL, headers=headers, json=payload)
            
            if res.status_code == 200:
                # مسح خيارات التعديل الجراحي بعد النجاح لتهيئة السيستم
                if "modify_target" in strl.session_state:
                    del strl.session_state.modify_target
                strl.session_state.beat_generated = True
strl.session_state.screen = "dashboard" # العودة لعرض النتيجة والكفرstrl.rerun()else:strl.error("فضلاً انتظر.. السيرفر يقوم بالتحميل الآن، أعد المحاولة بعد ثوانٍ.")if strl.button("⬅️ العودة للرئيسية"):if "modify_target" in strl.session_state:del strl.session_state.modify_targetstrl.session_state.screen = "dashboard"strl.rerun()
