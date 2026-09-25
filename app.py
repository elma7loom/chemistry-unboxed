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

# 2. Custom CSS for Clean Top Layout & Legible Navigation
st.markdown(
    """
    <style>
        /* Reduce top padding so elements sit nicely near the top */
        .block-container {
            padding-top: 2rem !important;
        }

        /* Global Background and Text Colors */
        .stApp {
            background-color: #F4F5F0; /* Light neutral canvas */
            color: #3B4733;            /* Minor accent for text */
        }
        
        /* Headers */
        h1, h2, h3, h4, h5, h6 {
            color: #3B4733 !important;
        }

        /* Make Navigation Text Perfectly Legible */
        [data-testid="stRadio"] label, 
        [data-testid="stRadio"] span, 
        [data-testid="stRadio"] div, 
        [data-testid="stRadio"] p {
            color: #3B4733 !important;
            font-weight: 600 !important;
        }

        /* Stealth Low-Contrast Admin Login */
        [data-testid="stExpander"] {
            background-color: transparent !important;
            border: 1px solid #e0e2db !important;
            border-radius: 6px;
            box-shadow: none !important;
        }
        [data-testid="stExpander"] summary {
            color: #9a9c94 !important; /* Low contrast, blends into background */
            font-size: 0.8rem !important;
        }

        /* Main Content Cards (Main Color 60%) */
        .blog-card {
            background-color: #CABC54; /* Main color */
            padding: 25px;
            border-radius: 10px;
            margin-bottom: 20px;
            color: #3B4733;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        }

        /* Buttons */
        .stButton>button {
            background-color: #3B4733; /* Minor accent */
            color: #CABC54;            /* Main color */
            border: none;
            border-radius: 5px;
            padding: 0.5rem 1rem;
            font-weight: bold;
        }
        .stButton>button:hover {
            background-color: #5B764C; 
            color: #F4F5F0;
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
            "content": "This is the first post on my new Streamlit blog. I'm using a natural, calming color palette to share my thoughts on tech, life, and nature. Building a digital garden requires patience, clean design, and a love for simple aesthetics.",
        },
        {
            "id": 2,
            "title": "Why Simple Tech Matters",
            "date": "September 20, 2026",
            "content": "Building lightweight apps using tools like Streamlit keeps development fast, clean, and enjoyable. You don't always need massive frameworks to share your ideas with the world.",
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

# 4. TOP HEADER BAR (Title, Navigation, and Stealth Admin)
top_col1, top_col2, top_col3 = st.columns([1.5, 2.5, 1])

with top_col1:
    st.markdown("<h3 style='margin: 0; padding-top: 5px;'>🌿 My Blog</h3>", unsafe_allow_html=True)

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
            <div class="blog-card" style="background-color: #CABC54;">
                <h1>{post['title']}</h1>
                <p><em>Published on {post['date']}</em></p>
                <hr style="border-color: #3B4733;">
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
