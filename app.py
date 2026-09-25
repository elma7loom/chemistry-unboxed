import streamlit as st

# 1. Page Configuration
st.set_page_config(
    page_title="My Personal Blog",
    page_icon="🌿",
    layout="centered",
    initial_sidebar_state="expanded",
)

# 2. Custom CSS Injection for the Earthy Palette
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

        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: #5B764C; /* Secondary color (30%) */
            color: #F4F5F0;
        }
        [data-testid="stSidebar"] h1, 
        [data-testid="stSidebar"] h2, 
        [data-testid="stSidebar"] h3, 
        [data-testid="stSidebar"] label {
            color: #F4F5F0 !important;
        }

        /* Main Content Cards / Containers (Main Color 60% influence) */
        div.stMarkdownContainer {
            background-color: transparent;
        }
        
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

# 3. Sidebar Navigation
st.sidebar.title("🌿 Navigation")
page = st.sidebar.radio("Go to", ["Home / Feed", "About Me", "Write a Post"])

# 4. Dummy Database / State for Blog Posts
if "posts" not in st.session_state:
    st.session_state.posts = [
        {
            "title": "Welcome to My Earthy Blog",
            "date": "September 25, 2026",
            "content": "This is the first post on my new blog. You'll read about chemistry, interesting molecules, and more.",
        },
        {
            "title": "Why Simple Tech Matters",
            "date": "September 20, 2026",
            "content": "How we can make chocolate cheaper",
        },
    ]

# 5. Page Routing
if page == "Home / Feed":
    st.title("My personal blog")
    st.write("Welcome to my digital base.")
    st.markdown("---")

    # Render Blog Posts inside Custom Cards
    for post in st.session_state.posts:
        st.markdown(
            f"""
            <div class="blog-card">
                <h2>{post['title']}</h2>
                <p><em>Published on {post['date']}</em></p>
                <p>{post['content']}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

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
                st.session_state.posts.insert(
                    0, {"title": title, "date": date, "content": content}
                )
                st.success("Post published successfully!")
                st.rerun()
            else:
                st.error("Please fill out both the title and content fields.")
