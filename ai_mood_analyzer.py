import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os
import hashlib
from datetime import datetime, timedelta
import random

# Page configuration
st.set_page_config(
    page_title="AI Mood Analyzer",
    page_icon="🌈",
    layout="wide",
    initial_sidebar_state="collapsed"
)
#THIS SI A TEST CSE

# Vibrant Colorful CSS
st.markdown("""
<style>
    /* Hide sidebar completely */
    [data-testid="stSidebar"] {
        display: none;
    }
    
    /* Main container styling */
    .main .block-container {
        max-width: 100%;
        padding: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    /* Content area with glass effect */
    .content-area {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    /* Header styling */
    .main-header {
        text-align: center;
        background: linear-gradient(135deg, #FF6B6B 0%, #4ECDC4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Mood cards with vibrant colors */
    .mood-card {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        margin: 1.5rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        border: none;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .mood-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.2);
    }
    
    .positive { 
        background: linear-gradient(135deg, #a8e6cf 0%, #dcedc1 100%);
        border-left: 8px solid #4CAF50;
    }
    .negative { 
        background: linear-gradient(135deg, #ffaaa5 0%, #ff8b94 100%);
        border-left: 8px solid #FF5252;
    }
    .neutral { 
        background: linear-gradient(135deg, #ffd3b6 0%, #ffaaa5 100%);
        border-left: 8px solid #FF9800;
    }
    
    /* Navigation buttons */
    .nav-container {
        display: flex;
        justify-content: center;
        gap: 1rem;
        margin: 2rem 0;
        flex-wrap: wrap;
    }
    
    .nav-btn {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem 2rem;
        border-radius: 50px;
        margin: 0.5rem;
        border: none;
        cursor: pointer;
        font-size: 1.1rem;
        font-weight: bold;
        text-decoration: none;
        display: inline-block;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .nav-btn:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
        color: white;
    }
    
    .nav-btn.active {
        background: linear-gradient(135deg, #FF6B6B 0%, #4ECDC4 100%);
    }
    
    /* Stats cards */
    .stats-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 2rem 0;
    }
    
    .stat-card {
        background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 6px 20px rgba(0,0,0,0.1);
    }
    
    .stat-card:nth-child(2) {
        background: linear-gradient(135deg, #fd79a8 0%, #e84393 100%);
    }
    
    .stat-card:nth-child(3) {
        background: linear-gradient(135deg, #00cec9 0%, #00b894 100%);
    }
    
    /* Text area styling */
    .stTextArea textarea {
        border-radius: 15px;
        border: 2px solid #ddd;
        padding: 1rem;
        font-size: 1.1rem;
        transition: all 0.3s ease;
    }
    
    .stTextArea textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
    }
    
    /* Button styling */
    .stButton button {
        background: linear-gradient(135deg, #FF6B6B 0%, #4ECDC4 100%);
        color: white;
        border: none;
        padding: 0.8rem 2rem;
        border-radius: 50px;
        font-size: 1.1rem;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }
    
    /* Welcome message */
    .welcome-message {
        text-align: center;
        color: #2d3436;
        font-size: 1.3rem;
        margin-bottom: 2rem;
        background: linear-gradient(135deg, #ffeaa7 0%, #fab1a0 100%);
        padding: 1rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    /* Analysis result styling */
    .analysis-result {
        background: linear-gradient(135deg, #dfe6e9 0%, #b2bec3 100%);
        padding: 2rem;
        border-radius: 20px;
        margin: 2rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }
    
    /* Emoji styling */
    .emoji-large {
        font-size: 4rem;
        text-align: center;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Storage functions
def ensure_data_dir():
    if not os.path.exists('data'):
        os.makedirs('data')

def save_entry(username, text, mood_data):
    ensure_data_dir()
    entries = load_entries(username)
    entry = {
        'id': len(entries) + 1,
        'date': datetime.now().isoformat(),
        'text': text,
        **mood_data
    }
    
    entries.append(entry)
    
    with open(f'data/{username}_entries.json', 'w') as f:
        json.dump(entries, f, indent=2)
    
    return entry

def load_entries(username):
    ensure_data_dir()
    filename = f'data/{username}_entries.json'
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return []

def get_stats(entries):
    if not entries:
        return {
            'total_entries': 0,
            'most_common_mood': 'N/A',
            'avg_mood_score': 0
        }
    
    mood_scores = [entry['mood_score'] for entry in entries]
    moods = [entry['primary_mood'] for entry in entries]
    
    from collections import Counter
    mood_counts = Counter(moods)
    most_common_mood = mood_counts.most_common(1)[0][0] if mood_counts else 'N/A'
    
    return {
        'total_entries': len(entries),
        'most_common_mood': most_common_mood,
        'avg_mood_score': sum(mood_scores) / len(mood_scores) if mood_scores else 0
    }

# Improved Mood Analysis with better detection
def analyze_mood(text):
    text_lower = text.lower()
    
    # Enhanced mood patterns
    mood_patterns = {
        'positive': {
            'words': ['happy', 'good', 'great', 'excellent', 'amazing', 'wonderful', 'joy', 
                     'love', 'nice', 'fantastic', 'awesome', 'perfect', 'beautiful', 'grateful',
                     'blessed', 'excited', 'proud', 'relieved', 'peaceful', 'content', 'fun',
                     'smile', 'laugh', 'enjoy', 'success', 'achievement', 'progress', 'better',
                     'improved', 'glad', 'pleased', 'delighted', 'ecstatic', 'optimistic'],
            'score_range': (7, 10),
            'moods': ['happy', 'joyful', 'content', 'excited', 'peaceful', 'grateful', 'proud', 'optimistic'],
            'emojis': ['😊', '😄', '🥳', '🌟', '💫', '✨', '🎉', '❤️']
        },
        'negative': {
            'words': ['sad', 'bad', 'terrible', 'awful', 'horrible', 'angry', 'hate', 
                     'worst', 'depressed', 'anxious', 'stress', 'tired', 'exhausted',
                     'frustrated', 'disappointed', 'worried', 'scared', 'lonely', 'hurt',
                     'upset', 'mad', 'fear', 'pain', 'sick', 'broken', 'lost', 'cry',
                     'miserable', 'hopeless', 'alone', 'empty', 'numb'],
            'score_range': (1, 4),
            'moods': ['sad', 'anxious', 'stressed', 'tired', 'frustrated', 'worried', 'angry', 'depressed'],
            'emojis': ['😢', '😔', '😞', '💔', '🌧️', '⚡', '🔥', '💀']
        },
        'neutral': {
            'words': ['okay', 'fine', 'normal', 'regular', 'usual', 'typical', 'average',
                     'decent', 'moderate', 'balanced', 'calm', 'steady', 'alright', 'meh',
                     'whatever', 'routine', 'ordinary', 'neutral', 'so-so'],
            'score_range': (5, 6),
            'moods': ['calm', 'balanced', 'neutral', 'reflective', 'thoughtful', 'relaxed', 'okay'],
            'emojis': ['😐', '🙂', '💭', '⚖️', '🌤️', '🌀', '📝']
        }
    }
    
    import random
    
    # Count mood words
    mood_scores = {}
    for mood_type, pattern in mood_patterns.items():
        count = sum(1 for word in pattern['words'] if word in text_lower)
        mood_scores[mood_type] = count
    
    # Determine primary mood type
    primary_mood_type = max(mood_scores, key=mood_scores.get)
    
    # Special case for very strong negative indicators
    if any(phrase in text_lower for phrase in ['very sad', 'extremely sad', 'so sad', 'really depressed']):
        mood_score = 2
        primary_mood = "very sad"
        secondary_mood = "depressed"
        analysis = "I can sense you're feeling very down right now. Remember that these feelings are temporary and it's okay to not be okay. Consider reaching out to someone you trust or doing something gentle for yourself."
        keywords = ["sadness", "support", "self-care", "understanding"]
        emoji = "😢"
        
    elif mood_scores[primary_mood_type] == 0:
        # No clear mood words detected
        mood_score = 5
        primary_mood = "thoughtful"
        secondary_mood = "reflective"
        analysis = "This entry shows deep thought and reflection. You're taking time to process your experiences, which is a healthy practice for emotional awareness."
        keywords = ["reflective", "thoughtful", "balanced", "contemplative"]
        emoji = "💭"
        
    else:
        # Calculate mood score based on intensity
        min_score, max_score = mood_patterns[primary_mood_type]['score_range']
        intensity = min(mood_scores[primary_mood_type], 5)
        mood_score = min_score + (intensity * (max_score - min_score) // 5)
        
        # Get random mood and emoji from the pattern
        available_moods = mood_patterns[primary_mood_type]['moods']
        available_emojis = mood_patterns[primary_mood_type]['emojis']
        primary_mood = random.choice(available_moods)
        secondary_mood = random.choice([m for m in available_moods if m != primary_mood])
        emoji = random.choice(available_emojis)
        
        # Generate appropriate analysis
        if primary_mood_type == 'positive':
            analysis = f"Your writing radiates positive energy! You're experiencing {primary_mood} feelings, which is wonderful. Keep nurturing these positive emotions!"
            keywords = ["positive", "upbeat", "optimistic", "energetic", "growth"]
        elif primary_mood_type == 'negative':
            analysis = f"I notice you're feeling {primary_mood}. Remember that all emotions are valid and temporary. Be gentle with yourself during this time."
            keywords = ["reflective", "challenging", "growth", "understanding", "self-care"]
        else:
            analysis = f"You're feeling {primary_mood} and balanced. This shows good emotional awareness and stability in your daily experiences."
            keywords = ["balanced", "thoughtful", "aware", "mindful", "stable"]
    
    return {
        "mood_score": mood_score,
        "primary_mood": primary_mood,
        "secondary_mood": secondary_mood,
        "keywords": keywords,
        "analysis": analysis,
        "emoji": emoji
    }

def get_insights(entries):
    if not entries:
        return {
            "insights": ["🌟 Start journaling to see your mood patterns emerge!", 
                        "📝 Write daily to build emotional awareness",
                        "💫 Your journey to self-discovery begins here"],
            "recommendation": "Try writing your first entry today!",
            "trend": "No data yet - your story is waiting to be written! ✨"
        }
    
    # Basic statistics
    mood_scores = [entry['mood_score'] for entry in entries]
    avg_mood = sum(mood_scores) / len(mood_scores)
    
    # Trend analysis
    if len(entries) >= 7:
        recent_avg = sum(mood_scores[-7:]) / 7
        if recent_avg > avg_mood + 0.5:
            trend = "🎉 Your mood has been improving recently! Amazing progress!"
        elif recent_avg < avg_mood - 0.5:
            trend = "💭 You've been facing more challenges lately. Remember, growth comes from all experiences."
        else:
            trend = "⚖️ Your mood has been beautifully balanced and stable."
    else:
        trend = "🌱 Continue your journaling journey to see wonderful patterns emerge!"
    
    # Generate insights
    insights = []
    
    if avg_mood >= 7:
        insights.append("🌈 You maintain a radiant positive outlook overall!")
        insights.append("😊 Your energy and optimism shine through your entries")
    elif avg_mood <= 4:
        insights.append("🫂 You've been navigating some challenging emotions recently")
        insights.append("💪 Your strength in acknowledging these feelings is powerful")
    else:
        insights.append("⚖️ You show beautiful emotional balance in your reflections")
        insights.append("🧠 Your self-awareness is growing with each entry")
    
    insights.append(f"📚 You've created {len(entries)} meaningful journal entries!")
    
    # Recommendation
    if avg_mood <= 5:
        recommendation = "Try incorporating small joyful activities into your day - even 5 minutes of something you love can make a difference!"
    else:
        recommendation = "Keep shining! Your positive energy is inspiring. Consider sharing your light with others!"
    
    return {
        "insights": insights,
        "recommendation": recommendation,
        "trend": trend
    }

# Authentication functions
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    if os.path.exists('data/users.json'):
        with open('data/users.json', 'r') as f:
            return json.load(f)
    return {}

def save_user(username, password):
    users = load_users()
    users[username] = hash_password(password)
    ensure_data_dir()
    with open('data/users.json', 'w') as f:
        json.dump(users, f, indent=2)

# Login Page
def login_page():
    st.markdown('<div class="content-area">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<h1 class="main-header">🌈 AI Mood Analyzer</h1>', unsafe_allow_html=True)
        st.markdown("""
        <div style='text-align: center; color: #666; font-size: 1.2rem; margin-bottom: 2rem;'>
            Discover your emotional patterns with beautiful AI insights ✨
        </div>
        """, unsafe_allow_html=True)
        
        st.image("https://cdn.pixabay.com/photo/2021/01/29/08/10/mindfulness-5960390_1280.png", 
                use_column_width=True, caption="Your Journey to Emotional Awareness")
    
    with col2:
        tab1, tab2 = st.tabs(["🚀 Login", "💫 Register"])
        
        with tab1:
            st.subheader("Welcome Back!")
            username = st.text_input("👤 Username")
            password = st.text_input("🔒 Password", type="password")
            if st.button("🌟 Login", use_container_width=True):
                users = load_users()
                if username in users and users[username] == hash_password(password):
                    st.session_state.authenticated = True
                    st.session_state.current_user = username
                    st.session_state.entries = load_entries(username)
                    st.session_state.current_page = "Journal"
                    st.success("🎉 Login successful! Welcome back!")
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password")
        
        with tab2:
            st.subheader("Start Your Journey")
            new_username = st.text_input("✨ Choose Username", key="new_user")
            new_password = st.text_input("🔑 Choose Password", type="password", key="new_pass")
            confirm_password = st.text_input("✅ Confirm Password", type="password", key="confirm_pass")
            if st.button("🚀 Create Account", use_container_width=True):
                if not new_username or not new_password:
                    st.error("📝 Please fill in all fields")
                elif new_password != confirm_password:
                    st.error("🔒 Passwords don't match")
                elif new_username in load_users():
                    st.error("👤 Username already exists")
                else:
                    save_user(new_username, new_password)
                    st.success("🎊 Account created successfully! Please login.")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Navigation Component
def render_navigation():
    st.markdown('<div class="nav-container">', unsafe_allow_html=True)
    
    pages = ["📖 Journal", "📊 History", "📈 Trends", "👤 Profile"]
    current_page = st.session_state.get('current_page', 'Journal')
    
    for page in pages:
        page_name = page.split(' ')[1]
        is_active = current_page == page_name
        button_class = "nav-btn active" if is_active else "nav-btn"
        
        if st.button(page, key=f"nav_{page_name}"):
            st.session_state.current_page = page_name
            st.rerun()
    
    if st.button("🚪 Logout"):
        st.session_state.authenticated = False
        st.session_state.current_user = None
        st.session_state.entries = []
        st.session_state.current_page = "Journal"
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Journal Page
def journal_page():
    st.markdown('<div class="content-area">', unsafe_allow_html=True)
    
    st.markdown('<h1 class="main-header">📖 Your Mood Journal</h1>', unsafe_allow_html=True)
    
    # Welcome message
    st.markdown(f"""
    <div class="welcome-message">
        🌟 Welcome back, <strong>{st.session_state.current_user}</strong>! How are you feeling today?
    </div>
    """, unsafe_allow_html=True)
    
    # Quick stats
    if st.session_state.entries:
        stats = get_stats(st.session_state.entries)
        st.markdown('<div class="stats-container">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f'<div class="stat-card"><h3>📚 Total</h3><h2>{stats["total_entries"]}</h2></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="stat-card"><h3>😊 Common Mood</h3><h2>{stats["most_common_mood"].title()}</h2></div>', unsafe_allow_html=True)
        with col3:
            st.markdown(f'<div class="stat-card"><h3>⭐ Average</h3><h2>{stats["avg_mood_score"]:.1f}/10</h2></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Journal input
    st.subheader("💭 Share Your Thoughts")
    journal_text = st.text_area(
        "Write about your day, feelings, or anything on your mind...",
        height=200,
        placeholder="Today I felt... 🌈"
    )
    
    if st.button("🔍 Analyze My Mood", use_container_width=True):
        if journal_text:
            with st.spinner("✨ Analyzing your emotions..."):
                mood_data = analyze_mood(journal_text)
                entry = save_entry(st.session_state.current_user, journal_text, mood_data)
                st.session_state.entries.append(entry)
                
                st.success("🎉 Entry saved successfully!")
                
                # Display mood analysis with emoji
                mood_class = "positive" if mood_data['mood_score'] >= 7 else "negative" if mood_data['mood_score'] <= 4 else "neutral"
                
                st.markdown(f"""
                <div class="analysis-result">
                    <div class="emoji-large">{mood_data['emoji']}</div>
                    <div class="mood-card {mood_class}">
                        <h3>🎯 Mood Analysis</h3>
                        <p><strong>Mood Score:</strong> {mood_data['mood_score']}/10</p>
                        <p><strong>Primary Mood:</strong> {mood_data['primary_mood'].title()}</p>
                        <p><strong>Secondary Mood:</strong> {mood_data['secondary_mood'].title()}</p>
                        <p><strong>Analysis:</strong> {mood_data['analysis']}</p>
                        <p><strong>Keywords:</strong> {', '.join(mood_data['keywords'])}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("📝 Please write something before analyzing!")
    
    # Recent entries
    if st.session_state.entries:
        st.subheader("📚 Recent Entries")
        recent_entries = st.session_state.entries[-3:]
        
        for entry in reversed(recent_entries):
            date = datetime.fromisoformat(entry['date']).strftime("%B %d, %Y %H:%M")
            mood_class = "positive" if entry['mood_score'] >= 7 else "negative" if entry['mood_score'] <= 4 else "neutral"
            
            st.markdown(f"""
            <div class="mood-card {mood_class}">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <strong>📅 {date}</strong>
                    <span>🎯 Mood: {entry['mood_score']}/10 ({entry['primary_mood'].title()})</span>
                </div>
                <p>{entry['text'][:200]}...</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Main App
def main():
    # Initialize session state
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'current_user' not in st.session_state:
        st.session_state.current_user = None
    if 'entries' not in st.session_state:
        st.session_state.entries = []
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Journal"

    # Authentication check
    if not st.session_state.authenticated:
        login_page()
        return

    # Render navigation
    render_navigation()

    # Page routing
    if st.session_state.current_page == "Journal":
        journal_page()
    elif st.session_state.current_page == "History":
        st.markdown('<div class="content-area">', unsafe_allow_html=True)
        st.markdown('<h1 class="main-header">📊 Your History</h1>', unsafe_allow_html=True)
        st.info("📖 History page coming soon!")
        st.markdown('</div>', unsafe_allow_html=True)
    elif st.session_state.current_page == "Trends":
        st.markdown('<div class="content-area">', unsafe_allow_html=True)
        st.markdown('<h1 class="main-header">📈 Your Trends</h1>', unsafe_allow_html=True)
        st.info("📊 Trends page coming soon!")
        st.markdown('</div>', unsafe_allow_html=True)
    elif st.session_state.current_page == "Profile":
        st.markdown('<div class="content-area">', unsafe_allow_html=True)
        st.markdown('<h1 class="main-header">👤 Your Profile</h1>', unsafe_allow_html=True)
        st.info("👤 Profile page coming soon!")
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()