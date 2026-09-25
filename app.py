import streamlit as st

# 1. Page Configuration
st.set_page_config(
    page_title="My Personal Blog",
    page_icon="✍️",
    layout="centered"
)

# 2. Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Blog Posts", "About Me"])

# 3. Sample Blog Data (You can later replace this with a database or Markdown files)
posts = {
    "Hello World: My First Blog Post": {
        "date": "September 25, 2026",
        "content": "Welcome to my new personal blog! Built with Streamlit, this space will house my thoughts, code snippets, projects, and daily updates. Stay tuned for more!"
    },
    "Why I Love Building with Python": {
        "date": "September 20, 2026",
        "content": "Python makes rapid prototyping so satisfying. From quick data scripts to full interactive web apps using Streamlit, it is incredible how fast you can turn an idea into reality."
    }
}

# 4. Page Routing Logic
if page == "Home":
    st.title("Welcome to My Blog 🚀")
    st.write("Hi there! I'm glad you stopped by. This is my digital garden where I share my journey, ideas, and projects.")
    
    st.markdown("---")
    st.subheader("✨ Latest Posts")
    
    # Display the latest 2 posts on the home page
    for title, info in list(posts.items())[:2]:
        st.markdown(f"### {title}")
        st.caption(f"Published on {info['date']}")
        st.write(info["content"][:120] + "...")
        st.markdown("---")

elif page == "Blog Posts":
    st.title("All Articles 📖")
    st.write("Browse through my complete archive of thoughts and write-ups below.")
    
    # Selectbox to choose which post to read
    selected_post = st.selectbox("Choose a post to read:", list(posts.keys()))
    
    if selected_post:
        st.markdown(f"## {selected_post}")
        st.caption(f"Published on {posts[selected_post]['date']}")
        st.write(posts[selected_post]["content"])

elif page == "About Me":
    st.title("About Me 👨‍💻")
    st.write("Hello! I'm a passionate creator exploring technology, code, and writing.")
    
    st.markdown("### Let's Connect")
    st.markdown("- **GitHub:** [github.com/yourusername](https://github.com)")
    st.markdown("- **Twitter:** [@yourusername](https://twitter.com)")
    st.markdown("- **Email:** youremail@example.com")
