import streamlit as st
from rapidfuzz import process, fuzz


# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="AI FAQ Chatbot",
    page_icon="🤖",
    layout="centered"
)


# =====================================================
# TITLE
# =====================================================

st.title("🤖 AI FAQ Chatbot")
st.write("Ask questions and get answers from my FAQ knowledge base.")

st.divider()


# =====================================================
# FAQ KNOWLEDGE BASE
# =====================================================

faq = {

    # -------- General AI --------

    "what is artificial intelligence":
        "Artificial Intelligence (AI) is technology that enables computers to perform tasks that normally require human intelligence.",

    "what is machine learning":
        "Machine Learning is a branch of AI that allows computers to learn patterns from data and make predictions or decisions.",

    "what is deep learning":
        "Deep Learning is a type of machine learning that uses neural networks with multiple layers to learn from large amounts of data.",

    "what is chatbot":
        "A chatbot is a software application that communicates with users through text or voice.",

    "what is generative ai":
        "Generative AI is a type of AI that can create new content such as text, images, audio, or code.",


    # -------- Programming --------

    "what is python":
        "Python is a popular programming language used for web development, automation, data science, machine learning, and artificial intelligence.",

    "what is java":
        "Java is a popular object-oriented programming language used to build many types of applications.",

    "what is html":
        "HTML stands for HyperText Markup Language. It is used to create and structure web pages.",

    "what is css":
        "CSS stands for Cascading Style Sheets. It is used to style and design web pages.",

    "what is sql":
        "SQL stands for Structured Query Language. It is used to store, retrieve, and manage data in databases.",

    "what is database":
        "A database is an organized collection of data that can be stored, managed, and retrieved efficiently.",


    # -------- Education --------

    "what is btech":
        "B.Tech stands for Bachelor of Technology. It is an undergraduate degree focused on engineering and technology.",

    "what is engineering":
        "Engineering is the application of science, mathematics, and technology to design and develop solutions to real-world problems.",

    "what is jntu gv":
        "JNTU-GV stands for Jawaharlal Nehru Technological University Gurajada Vizianagaram.",

    "what is jntu gv full form":
        "JNTU-GV stands for Jawaharlal Nehru Technological University Gurajada Vizianagaram.",

    "what does jntu gv stand for":
        "JNTU-GV stands for Jawaharlal Nehru Technological University Gurajada Vizianagaram.",


    # -------- General Knowledge --------

    "what is the capital of india":
        "The capital of India is New Delhi.",

    "what is the capital of france":
        "The capital of France is Paris.",

    "where is eiffel tower located":
        "The Eiffel Tower is located in Paris, France.",

    "where is taj mahal located":
        "The Taj Mahal is located in Agra, Uttar Pradesh, India.",

    "what is the largest planet":
        "Jupiter is the largest planet in our Solar System.",

    "how many continents are there":
        "There are seven continents: Asia, Africa, North America, South America, Antarctica, Europe, and Australia.",


    # -------- Common Questions --------

    "hello":
        "Hello! 👋 How can I help you?",

    "hi":
        "Hi! 👋 Ask me anything from my FAQ knowledge base.",

    "good morning":
        "Good morning! ☀️ How can I help you?",

    "thank you":
        "You're welcome! 😊",

    "thanks":
        "You're welcome! 😊",

    "who are you":
        "I am an AI FAQ chatbot created to answer frequently asked questions.",

    "what can you do":
        "I can answer questions from my FAQ knowledge base and understand different ways of asking questions."
}


# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.header("📚 FAQ Categories")

    st.write("🤖 Artificial Intelligence")
    st.write("💻 Programming")
    st.write("🎓 Education")
    st.write("🌍 General Knowledge")
    st.write("💬 Common Questions")

    st.divider()

    st.subheader("💡 Sample Questions")

    st.write("• What is Python?")
    st.write("• Tell me about SQL")
    st.write("• Explain Artificial Intelligence")
    st.write("• What is Java?")
    st.write("• Where is Eiffel Tower located?")
    st.write("• What is B.Tech?")


# =====================================================
# CHAT HISTORY
# =====================================================

if "messages" not in st.session_state:

    st.session_state.messages = []


# =====================================================
# DISPLAY CHAT HISTORY
# =====================================================

for message in st.session_state.messages:

    if message["role"] == "user":

        st.info(
            "👤 You: " + message["content"]
        )

    else:

        st.success(
            "🤖 Bot: " + message["content"]
        )


# =====================================================
# QUESTION INPUT
# =====================================================

question = st.text_input(
    "💬 Ask your question:",
    placeholder="Example: Tell me about SQL"
)


# =====================================================
# ASK BUTTON
# =====================================================

if st.button(
    "🤖 Ask",
    use_container_width=True
):

    if not question.strip():

        st.warning(
            "⚠️ Please enter a question."
        )

    else:

        # ---------------------------------------------
        # Clean question
        # ---------------------------------------------

        question_lower = question.lower().strip()

        cleaned_question = ""

        for character in question_lower:

            if character.isalnum() or character == " ":

                cleaned_question += character

        question_lower = " ".join(
            cleaned_question.split()
        )


        # ---------------------------------------------
        # Common words
        # ---------------------------------------------

        stop_words = {

            "what",
            "is",
            "are",
            "the",
            "a",
            "an",
            "tell",
            "me",
            "about",
            "can",
            "you",
            "please",
            "explain",
            "do",
            "know",
            "give",
            "information",
            "on",
            "for",
            "define",
            "meaning",
            "of",
            "does",
            "stand",
            "standfor"
        }


        # ---------------------------------------------
        # Get important words
        # ---------------------------------------------

        question_words = question_lower.split()

        important_words = []

        for word in question_words:

            if word not in stop_words:

                important_words.append(word)


        clean_question = " ".join(
            important_words
        )


        # ---------------------------------------------
        # Fuzzy matching
        # ---------------------------------------------

        result1 = process.extractOne(
            question_lower,
            faq.keys(),
            scorer=fuzz.token_set_ratio
        )


        result2 = process.extractOne(
            clean_question,
            faq.keys(),
            scorer=fuzz.token_set_ratio
        )


        # ---------------------------------------------
        # Choose best result
        # ---------------------------------------------

        if result2[1] > result1[1]:

            best_match = result2[0]
            score = result2[1]

        else:

            best_match = result1[0]
            score = result1[1]


        # ---------------------------------------------
        # Save user message
        # ---------------------------------------------

        st.session_state.messages.append({

            "role": "user",

            "content": question

        })


        # ---------------------------------------------
        # Answer
        # ---------------------------------------------

        if score >= 60:

            answer = faq[best_match]

        else:

            answer = (
                "Sorry, I don't know the answer to that "
                "question yet. Please try asking another question."
            )


        # ---------------------------------------------
        # Save bot message
        # ---------------------------------------------

        st.session_state.messages.append({

            "role": "bot",

            "content": answer

        })


        # ---------------------------------------------
        # Refresh
        # ---------------------------------------------

        st.rerun()


# =====================================================
# CLEAR CHAT
# =====================================================

if st.session_state.messages:

    st.divider()

    if st.button(
        "🗑️ Clear Chat",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.rerun()