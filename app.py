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

# 2. Custom CSS: Artistic Journal & Digital Garden Aesthetic
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Rubik:ital,wght@0,300..900;1,300..900&display=swap');

        .block-container {
            padding-top: 3rem !important;
            max-width: 700px; /* Nighter, more intimate editorial width */
        }

        /* Warm, earthy canvas background */
        .stApp {
            background-color: #E8EFE1; 
            color: #2C352D;            
            font-family: 'Rubik', sans-serif;
        }
        
        h1, h2, h3, h4, h5, h6 {
            color: #2C352D !important;
            font-family: 'Rubik', sans-serif;
        }

        /* Clean Organic Navigation Bar */
        .artistic-nav {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background-color: rgba(253, 251, 247, 0.6);
            padding: 12px 24px;
            border-radius: 16px;
            border: 1px solid #D0DEC9;
            margin-bottom: 35px;
            backdrop-filter: blur(4px);
        }

        /* Journal-style Post Cards (Warm Cream Paper Feel) */
        .blog-card {
            background-color: #FDFBF7; /* Warm eggshell paper */
            padding: 32px;
            border-radius: 18px;
            margin-bottom: 28px;
            color: #2C352D;
            border: 1px solid #D5E1CE;
            box-shadow: 0 10px 30px rgba(44, 53, 45, 0.03); /* Ultra-soft natural shadow */
            transition: transform 0.2s ease;
        }
        .blog-card:hover {
            transform: translateY(-2px); /* Gentle organic lift */
        }

        /* Subtle Journal Metadata */
        .post-date {
            font-size: 0.85rem;
            color: #6A7B6B;
            font-style: italic;
            letter-spacing: 0.2px;
            margin-bottom: 12px;
        }

        /* Navigation Radio Styling */
        [data-testid="stRadio"] label {
            color: #2C352D !important;
            font-weight: 500 !important;
        }

        /* Stealth Admin Expander */
        [data-testid="stExpander"] {
            background-color: transparent !important;
            border: 1px dashed #A8BCA0 !important;
            border-radius: 8px;
        }
        [data-testid="stExpander"] summary {
            color: #5A6E5C !important; 
            font-size: 0.8rem !important;
        }

        /* Organic Earthy Buttons */
        .stButton>button {
            background-color: #384A39; 
            color: #FDFBF7;            
            border: none;
            border-radius: 8px;
            padding: 0.4rem 1.1rem;
            font-weight: 500;
            font-size: 0.9rem;
            box-shadow: 0 2px 6px rgba(0,0,0,0.05);
        }
        .stButton>button:hover {
            background-color: #4D634E;
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

# 4. REFINED ARTISTIC NAVBAR CONTAINER (No ghost bars, perfectly integrated)
col_title, col_nav, col_admin = st.columns([1.5, 2.2, 1.1])

with col_title:
    st.markdown("<div style='font-size: 1.4rem; font-weight: 700; color: #2C352D; padding-top: 6px; white-space: nowrap;'>🌿 My Blog</div>", unsafe_allow_html=True)

nav_options = ["Home / Feed", "About Me"]
if st.session_state.is_admin:
    nav_options.append("Write a Post")

with col_nav:
    page = st.radio(
        "Navigation", 
        nav_options, 
        horizontal=True,
        label_visibility="collapsed"
    )

with col_admin:
    with st.expander("🔐 Admin"):
        if not st.session_state.is_admin:
            pwd = st.text_input("Password", type="password", key="admin_pwd", label_visibility="collapsed", placeholder="Password")
            if st.button("Enter"):
                if pwd == "mysecretpassword":
                    st.session_state.is_admin = True
                    st.rerun()
                else:
                    st.error("Wrong")
        else:
            st.write("✓ Logged In")
            if st.button("Log Out"):
                st.session_state.is_admin = False
                st.rerun()

st.markdown("<div style='margin-bottom: 25px;'></div>", unsafe_allow_html=True)

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
            
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="blog-card">
                <h1 style="font-size: 1.8rem; margin-bottom: 8px;">{post['title']}</h1>
                <div class="post-date">Written on {post['date']}</div>
                <hr style="border: none; border-top: 1px solid #E2EAE0; margin: 18px 0;">
                <p style="font-size: 1.05rem; line-height: 1.7; color: #3A473B;">{post['content']}</p>
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
        st.markdown("<h2 style='font-weight: 600; letter-spacing: -0.5px;'>🌱 Feed</h2>", unsafe_allow_html=True)
        st.markdown("<p style='color: #556656; margin-bottom: 25px;'>A digital garden of raw thoughts, code snippets, and stories.</p>", unsafe_allow_html=True)

        if not st.session_state.posts:
            st.info("No blog posts found.")

        # Render Blog Posts
        for i, post in enumerate(st.session_state.posts):
            if "id" not in post:
                post["id"] = i + 1
                
            st.markdown(
                f"""
                <div class="blog-card">
                    <h2 style="font-size: 1.5rem; margin-bottom: 4px;">{post['title']}</h2>
                    <div class="post-date">Published on {post['date']}</div>
                    <p style="color: #445345; line-height: 1.6; margin-top: 10px;">{post['content'][:110]}...</p>
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
        st.markdown("<h2 style='font-weight: 600;'>👤 About Me</h2>", unsafe_allow_html=True)
        st.markdown(
            """
            <div class="blog-card">
                <h3 style="margin-bottom: 10px;">Hello there!</h3>
                <p style="line-height: 1.7; color: #445345;">I'm a creator sharing my journey through code, writing, and minimalist design. This blog serves as my personal cabin on the web, away from the noise of standard social platforms.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    elif page == "Write a Post" and st.session_state.is_admin:
        st.markdown("<h2 style='font-weight: 600;'>✍️ Plant a New Thought</h2>", unsafe_allow_html=True)
        
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
