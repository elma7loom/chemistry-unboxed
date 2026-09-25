import streamlit as st

# 1. Page Configuration
st.set_page_config(
    page_title="My Personal Blog",
    page_icon="🌿",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# 2. Custom CSS Injection for the Earthy Palette & Radio Text Fix
st.markdown(
    """
    <style>
        /* Global Background and Text Colors */
        .stApp {
            background-color: #F4F5F0; /* Light neutral canvas */
            color: #3B4733;            /* Minor accent for text (10%) */
        }
        
        /* Headers */
        h1, h2, h3, h4, h5, h6 {
            color: #3B4733 !important;
        }

        /* Radio Text Fix */
        [data-testid="stRadio"] label, 
        [data-testid="stRadio"] span, 
        [data-testid="stRadio"] div, 
        [data-testid="stRadio"] p {
            color: #3B4733 !important;
            font-weight: 600 !important;
        }

        /* Main Content Cards (Main Color 60%) */
        .blog-card {
            background-color: #CABC54; /* Main color (60%) */
            padding: 20px;
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
            background-color: #5B764C; /* Secondary color on hover */
            color: #F4F5F0;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# 3. Dummy Database & Navigation State
if "posts" not in st.session_state:
    st.session_state.posts = [
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

if "selected_post_id" not in st.session_state:
    st.session_state.selected_post_id = None

# 4. Horizontal Top Navigation
st.markdown("### 🌿 My Personal Blog")

page = st.radio(
    "Navigation", 
    ["Home / Feed", "About Me", "Write a Post"], 
    horizontal=True,
    label_visibility="collapsed"
)

st.markdown("---")

# 5. Page Routing & Detail View Logic
if st.session_state.selected_post_id is not None:
    # --- INDIVIDUAL POST VIEW ---
    post = next((p for p in st.session_state.posts if p["id"] == st.session_state.selected_post_id), None)
    
    if post:
        if st.button("← Back to Feed"):
            st.session_state.selected_post_id = None
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

        # Render Blog Posts with Interactive Buttons
        for post in st.session_state.posts:
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
            # Button directly beneath each card to open it
            if st.button(f"Read Full Post: {post['title']}", key=f"btn_{post['id']}"):
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

    elif page == "Write a Post":
        st.title("✍️ Create a New Post")
        
        with st.form("blog_form"):
            title = st.text_input("Post Title")
            date = st.text_input("Date (e.g., October 12, 2026)")
            content = st.text_area("Post Content")
            submitted = st.form_submit_button("Publish Post")
            
            if submitted:
                if title and content:
                    new_id = len(st.session_state.posts) + 1
                    st.session_state.posts.insert(
                        0, {"id": new_id, "title": title, "date": date, "content": content}
                    )
                    st.success("Post published successfully!")
                    st.rerun()
                else:
                    st.error("Please fill out both the title and content fields.")
