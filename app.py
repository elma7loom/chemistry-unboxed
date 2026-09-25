import streamlit as st
import json
import os

# 1. Page Configuration
st.set_page_config(
    page_title="My Personal Blog",
    page_icon="🌿",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# 2. Custom CSS: Rubik Font, Leafy Green Background, and Large White Title
st.markdown(
    """
    <style>
        /* Import Rubik font from Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Rubik:ital,wght@0,300..900;1,300..900&display=swap');

        /* Give the top proper breathing room */
        .block-container {
            padding-top: 4.5rem !important;
        }

        /* Global Background and Typography */
        .stApp {
            background-color: #E2EFE0; /* Light leafy green background */
            color: #2D3E2E;            /* Deep forest green for text */
            font-family: 'Rubik', sans-serif;
        }
        
        /* Headers */
        h1, h2, h3, h4, h5, h6 {
            color: #2D3E2E !important;
            font-family: 'Rubik', sans-serif;
        }

        /* Make Navigation Text Perfectly Legible */
        [data-testid="stRadio"] label, 
        [data-testid="stRadio"] span, 
        [data-testid="stRadio"] div, 
        [data-testid="stRadio"] p {
            color: #2D3E2E !important;
            font-weight: 600 !important;
            font-family: 'Rubik', sans-serif;
        }

        /* Stealth Low-Contrast Admin Login */
        [data-testid="stExpander"] {
            background-color: transparent !important;
            border: 1px solid #b8cbc0 !important;
            border-radius: 6px;
            box-shadow: none !important;
        }
        [data-testid="stExpander"] summary {
            color: #728c7b !important; 
            font-size: 0.8rem !important;
            font-family: 'Rubik', sans-serif;
        }

        /* Main Content Cards */
        .blog-card {
            background-color: #FFFFFF; /* Crisp white cards to pop against leafy green */
            padding: 25px;
            border-radius: 12px;
            margin-bottom: 20px;
            color: #2D3E2E;
            box-shadow: 0 4px 12px rgba(45, 62, 46, 0.06);
            border: 1px solid #cce0d0;
        }

        /* Buttons */
        .stButton>button {
            background-color: #2D3E2E; 
            color: #E2EFE0;            
            border: none;
            border-radius: 6px;
            padding: 0.5rem 1rem;
            font-weight: bold;
            font-family: 'Rubik', sans-serif;
        }
        .stButton>button:hover {
            background-color: #435E44; 
            color: #FFFFFF;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# 3. Persistent Storage Handlers
POSTS_FILE = "posts.json"

def load_posts():
    if os.path.exists(POSTS_FILE):
        try:
            with open(POSTS_FILE, "r") as f:
                return json.load(f)
        except:
            pass
    return [
        {
            "id": 1,
            "title": "Welcome to My Earthy Blog",
            "date": "September 25, 2026",
            "content": "This is the first post on my new Streamlit blog. I'm using a natural, calming color palette to share my thoughts on tech, life, and nature.",
        },
        {
            "id": 2,
            "title": "Why Simple Tech Matters",
            "date": "September 20, 2026",
            "content": "Building lightweight apps using tools like Streamlit keeps development fast, clean, and enjoyable.",
        },
    ]

def save_posts(posts_list):
    with open(POSTS_FILE, "w") as f:
        json.dump(posts_list, f, indent=4)

if "posts" not in st.session_state:
    st.session_state.posts = load_posts()

if "selected_post_id" not in st.session_state:
    st.session_state.selected_post_id = None

if "is_admin" not in st.session_state:
    st.session_state.is_admin = False

# 4. TOP HEADER BAR (Massive White Title, Navigation, and Stealth Admin)
top_col1, top_col2, top_col3 = st.columns([1.5, 2.5, 1])

with top_col1:
    # Large, bold, white title using Rubik
    st.markdown("<h1 style='color: #FFFFFF !important; font-size: 2.8rem; font-weight: 700; margin: 0; line-height: 1.1;'>🌿 My Blog</h1>", unsafe_allow_html=True)

nav_options = ["Home / Feed", "About Me"]
if st.session_state.is_admin:
    nav_options.append("Write a Post")

with top_col2:
    page = st.radio(
        "Navigation", 
        nav_options, 
        horizontal=True,
        label_visibility="collapsed"
    )

with top_col3:
    with st.expander("🔐 Admin"):
        if not st.session_state.is_admin:
            pwd = st.text_input("Password", type="password", key="admin_pwd", label_visibility="collapsed", placeholder="Password")
            if st.button("Enter"):
                if pwd == "mysecretpassword":  # Change this to your chosen password!
                    st.session_state.is_admin = True
                    st.rerun()
                else:
                    st.error("Wrong")
        else:
            st.write("✓ Logged In")
            if st.button("Log Out"):
                st.session_state.is_admin = False
                st.rerun()

st.markdown("---")

# 5. Page Routing & Detail View Logic
if st.session_state.selected_post_id is not None:
    # --- INDIVIDUAL POST VIEW ---
    post = next((p for p in st.session_state.posts if p.get("id") == st.session_state.selected_post_id), None)
    
    if post:
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("← Back"):
                st.session_state.selected_post_id = None
                st.rerun()
        with col2:
            if st.session_state.is_admin:
                if st.button("🗑️ Delete Post", key="delete_full_view"):
                    st.session_state.posts = [p for p in st.session_state.posts if p.get("id") != post["id"]]
                    save_posts(st.session_state.posts)
                    st.session_state.selected_post_id = None
                    st.success("Post deleted successfully!")
                    st.rerun()
            
        st.markdown(f"<br>", unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="blog-card">
                <h1>{post['title']}</h1>
                <p><em>Published on {post['date']}</em></p>
                <hr style="border-color: #cce0d0;">
                <p style="font-size: 1.1rem; line-height: 1.6;">{post['content']}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.error("Post not found.")
        if st.button("Back to Feed"):
            st.session_state.selected_post_id = None
            st.rerun()

else:
    # --- STANDARD NAVIGATION PAGES ---
    if page == "Home / Feed":
        st.title("🌱 Feed")
        st.write("Welcome to my digital garden of thoughts and stories.")
        st.markdown("<br>", unsafe_allow_html=True)

        if not st.session_state.posts:
            st.info("No blog posts found.")

        # Render Blog Posts
        for i, post in enumerate(st.session_state.posts):
            if "id" not in post:
                post["id"] = i + 1
                
            st.markdown(
                f"""
                <div class="blog-card">
                    <h2>{post['title']}</h2>
                    <p><em>Published on {post['date']}</em></p>
                    <p>{post['content'][:100]}...</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            
            if st.session_state.is_admin:
                b_col1, b_col2 = st.columns([3, 1])
                with b_col1:
                    if st.button(f"Read Full Post", key=f"read_{post['id']}_{i}"):
                        st.session_state.selected_post_id = post['id']
                        st.rerun()
                with b_col2:
                    if st.button(f"🗑️ Delete", key=f"del_{post['id']}_{i}"):
                        st.session_state.posts = [p for p in st.session_state.posts if p.get("id") != post['id']]
                        save_posts(st.session_state.posts)
                        st.success(f"Deleted '{post['title']}'")
                        st.rerun()
            else:
                if st.button(f"Read Full Post", key=f"read_{post['id']}_{i}"):
                    st.session_state.selected_post_id = post['id']
                    st.rerun()

            st.markdown("<br>", unsafe_allow_html=True)

    elif page == "About Me":
        st.title("👤 About Me")
        st.markdown(
            """
            <div class="blog-card">
                <h3>Hello there!</h3>
                <p>I'm a creator sharing my journey through code, writing, and minimalist design. This blog serves as my personal space on the web.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    elif page == "Write a Post" and st.session_state.is_admin:
        st.title("✍️ Create a New Post")
        
        with st.form("blog_form"):
            title = st.text_input("Post Title")
            date = st.text_input("Date (e.g., October 12, 2026)")
            content = st.text_area("Post Content")
            submitted = st.form_submit_button("Publish Post")
            
            if submitted:
                if title and content:
                    max_id = max([p.get("id", 0) for p in st.session_state.posts], default=0)
                    new_id = max_id + 1
                    
                    new_post = {"id": new_id, "title": title, "date": date, "content": content}
                    st.session_state.posts.insert(0, new_post)
                    save_posts(st.session_state.posts)
                    
                    st.success("Post published and saved successfully!")
                    st.rerun()
                else:
                    st.error("Please fill out both the title and content fields.")
