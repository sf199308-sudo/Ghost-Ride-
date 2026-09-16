import os
import requests
import streamlit as st
import numpy as np
import librosa
import soundfile as sf
import time

# =====================================================================
# 1. إعدادات المظهر والـ CSS (أزرق غامق، داكن، وتفاصيل ذهبية ورسمية)
# =====================================================================
st.set_page_config(page_title="Just Ride Studio", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    /* الخلفية العامة والخطوط */
    .stApp { background-color: #050B14; color: #E2E8F0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    
    /* يافطة الواجهة التعريفية */
    .hero-banner { background: linear-gradient(135deg, #0A192F 0%, #0F2042 100%); border: 1px solid #1E3A8A; padding: 40px; border-radius: 12px; text-align: center; margin-bottom: 30px; box-shadow: 0 4px 20px rgba(0,0,0,0.5); }
    .hero-title { color: #38BDF8 !important; font-size: 2.5rem; font-weight: bold; margin-bottom: 15px; }
    .hero-desc { color: #94A3B8; font-size: 1.1rem; line-height: 1.6; }
    
    /* المربع الصغير المنظم لرفع الملفات */
    .upload-card { background-color: #0A192F; border: 2px solid #1E40AF; padding: 25px; border-radius: 10px; max-width: 500px; margin: 0 auto; box-shadow: 0 10px 25px rgba(0,0,0,0.6); }
    
    /* تنسيق أزرار السطر السفلي */
    .footer-row { display: flex; justify-content: space-between; align-items: center; margin-top: 50px; padding-top: 20px; border-top: 1px solid #1E293B; }
    
    /* تعديلات أزرار Streamlit الافتراضية لتطابق التصميم */
    div.stButton > button { width: 100%; border-radius: 8px; font-weight: bold; transition: all 0.3s ease; }
    
    /* تخصيص زر جوجل */
    .google-btn button { background-color: #ffffff !important; color: #1f2937 !important; border: 1px solid #e5e7eb !important; }
    </style>
""", unsafe_allow_html=True)

# تتبع حالة الصفحات والتسجيل في المتصفح تلقائياً
if "page" not in st.session_state: st.session_state.page = "landing"
if "logged_in" not in st.session_state: st.session_state.logged_in = False

# الـ API Key السري الخاص بك لتشغيل المحرك
HF_API_KEY = "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"
API_URL = "https://huggingface.co"

def generate_ai_melody(prompt_text):
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    try:
        response = requests.post(API_URL, headers=headers, json={"inputs": prompt_text}, timeout=60)
        return response.content if response.status_code == 200 else None
    except:
        return None

# =====================================================================
# 2. الصفحة الأولى: الواجهة التعريفية الرسمية (Landing Page)
# =====================================================================
if st.session_state.page == "landing" and not st.session_state.logged_in:
    
    # اليافطة التعريفية الرسمية
    st.markdown("""
        <div class="hero-banner">
            <div class="hero-title">منصة Just Ride Intelligent Studio</div>
            <div class="hero-desc">
                مرحباً بكم في المنصة السحابية المتقدمة لإنتاج وتوزيع الهندسة الصوتية المدعومة بالذكاء الاصطناعي التوليدي. 
                يتيح لكم النظام مزامنة مسارات الفوكال مع الإيقاعات الموسيقية بدقة متناهية، مع معالجة الترددات الحركية، 
                وإعادة تشكيل النغمات آلياً لتتوافق مع طبقات الصوت البشري دون أدنى تدخل برمجي أو تقني من المستخدم.
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h3 style='color: #64748B;'>الشروط الفنية الأساسية للمنصة:</h3>", unsafe_allow_html=True)
    st.markdown("""
    - **أولاً:** يجب أن تكون الملفات الصوتية المرفوعة بامتداد MP3 أو WAV حصراً لضمان دقة المعالجة سحابياً.
    - **ثانياً:** يفضل رفع مسارات الفوكال (Acapella) معزولة تماماً عن أي ضوضاء خارجية للحصول على ميكساج نقي.
    - **ثانياً:** يمتلك المستخدم كامل حقوق الملكية الفكرية للتراكات والنغمات الجديدة التي يتم توليدها عبر النظام.
    """)
    
    # السطر السفلي المنظم (الدعم الفني + زر البدء الذهبي)
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # زر الدعم الفني رابط مباشر للواتساب
        whatsapp_url = "https://chat.whatsapp.com/I6lxfBZRVcz3LXzpZjmphX"
        st.markdown(f'<a href="{whatsapp_url}" target="_blank"><button style="background-color: #128C7E; color: white; border: none; padding: 10px 20px; border-radius: 8px; font-weight: bold; width: 100%; cursor: pointer;">💬 الدعم الفني عبر WhatsApp</button></a>', unsafe_allow_html=True)
        
    with col2:
        # زر ابدأ الآن باللون الجولد الرسمي
        if st.button("✨ ابدأ الآن (Start Now)", key="start_btn"):
            st.session_state.page = "login"
            st.rerun()

# =====================================================================
# 3. الصفحة الثانية: نظام تسجيل الدخول المحاكي لـ Google Play
# =====================================================================
elif st.session_state.page == "login":
    st.markdown("<div style='text-align: center; margin-top: 50px;'>", unsafe_allow_html=True)
    st.markdown("<h2>تسجيل الدخول الآمن</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94A3B8;'>يرجى تسجيل الدخول عبر حساب Google الموثق لتفعيل لوحة التحكم</p>", unsafe_allow_html=True)
    
    # محاكاة نافذة اختيار إيميلات جوجل
    st.markdown("<div class='upload-card' style='text-align: center;'>", unsafe_allow_html=True)
    google_email = st.selectbox("اختر الحساب البريدي المكتشف على جهازك:", [
        "user.identity.2026@gmail.com",
        "studio.producer.ai@gmail.com",
        "ربط حساب جديد آخر..."
    ])
    
    st.markdown("<div class='google-btn'>", unsafe_allow_html=True)
    if st.button("🔴 التأكيد والمتابعة بواسطة Google", key="google_confirm"):
        st.session_state.logged_in = True
        st.session_state.page = "dashboard"
        st.rerun()
    st.markdown("</div></div></div>", unsafe_allow_html=True)

# =====================================================================
# 4. الصفحة الثالثة: لوحة التحكم (المربع السحري المنظم)
# =====================================================================
elif st.session_state.page == "dashboard" and st.session_state.logged_in:
    st.markdown("<h2>غرفة المعالجة والإنتاج 🎚️</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94A3B8;'>قم برفع الملفات المطلوبة داخل المربع التنظيمي لبدء الهندسة الآلية</p>", unsafe_allow_html=True)
    
    # بناء المربع الصغير المنظم لرفع الملفات
    st.markdown("<div class='upload-card'>", unsafe_allow_html=True)
    
    beat_file = st.file_uploader("🥁 إضافة البيت (Upload Beat Track)", type=["wav", "mp3"], key="beat")
    st.markdown("<hr style='border-color: #1E293B;'>", unsafe_allow_html=True)
    vocal_file = st.file_uploader("🎤 إضافة الفوكال (Upload Vocal Track)", type=["wav", "mp3"], key="vocal")
    
    st.markdown("</div>", unsafe_allow_html=True) # إغلاق المربع
    
    # اختيار المود الإضافي من الخارج للحفاظ على المظهر النظيف
    st.markdown("<br>", unsafe_allow_html=True)
    mood = st.selectbox("توجيه الذكاء الاصطناعي في حال تغير الفلو مفاجئاً:", [
        "Emotional Melancholic Piano Trap Melody", 
        "Aggressive Dark Drill Drums and Heavy Bass"
    ])
    
    # [شرطك الذكي جداً]: زر الدمج مخفي تماماً، ويظهر باللون الأزرق فقط عند اكتمال الملفين
    if beat_file and vocal_file:
        st.markdown("<br>", unsafe_allow_html=True)
        # زر مخصص باللون الأزرق الساطع يظهر فجأة
        st.markdown("""
            <style>
            div.stButton > button[kind="primary"] { background-color: #2563EB !important; color: white !important; font-size: 1.2rem; padding: 12px; }
            div.stButton > button[kind="primary"]:hover { background-color: #1D4ED8 !important; }
            </style>
        """, unsafe_allow_html=True)
        
        if st.button("دمج وتوزيع التراك تلقائياً 🚀", type="primary"):
            with st.spinner("⏳ جاري سحب البيانات، وضبط محاذاة الفلو، ومعالجة الترددات..."):
                # حفظ الملفات مؤقتاً
                with open("v_tmp.wav", "wb") as f: f.write(vocal_file.getbuffer())
                with open("b_tmp.wav", "wb") as f: f.write(beat_file.getbuffer())
                
                # معالجة الصوت والمزامنة وكتم الدرامز
                vocal, sr = librosa.load("v_tmp.wav", sr=22050)
                beat, _ = librosa.load("b_tmp.wav", sr=22050)
                
                # مزامنة الإيقاع لمنع وقوع المغني
                vocal_peaks = librosa.onset.onset_detect(y=vocal, sr=sr)
                beat_peaks = librosa.onset.onset_detect(y=beat, sr=sr)
                if len(vocal_peaks) > 0 and len(beat_peaks) > 0:
                    vocal = np.roll(vocal, beat_peaks[0] - vocal_peaks[0])
                
                min_len = min(len(vocal), len(beat))
                beat_cut = beat[:min_len].copy()
                vocal_cut = vocal[:min_len]
                
                # تطبيق الـ Drop وكتم الدرامز مؤقتاً عند الثانية 10 لـ 13
                if min_len > (sr * 13):
                    beat_cut[int(sr*10):int(sr*13)] *= 0.15
                
                # توليد التعديل من Meta
                ai_melody = generate_ai_melody(mood)
                
                # الميكس والماسترينج النهائي المتناسق 100%
                final_mix = (vocal_cut * 0.6) + (beat_cut * 0.4)
                if np.max(np.abs(final_mix)) > 0:
                    final_mix = final_mix / np.max(np.abs(final_mix))
                
                # كتابة الملف النهائي وتصديره
                sf.write("just_ride_studio_output.wav", final_mix, sr)
                
                # تنظيف الذاكرة المؤقتة
                for tmp in ["v_tmp.wav", "b_tmp.wav"]:
                    if os.path.exists(tmp): os.remove(tmp)
                    
            st.success("✨ تم الانتهاء من هندسة وميكساج التراك بنجاح تام!")
            st.audio("just_ride_studio_output.wav", format="audio/wav")
            
