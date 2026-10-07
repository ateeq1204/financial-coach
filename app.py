import os

import streamlit as st

from config import DOCUMENTS_PATH

from vector_store import ingest_documents

from generator import generate_answer


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AI Financial Coach",
    page_icon="💰",
    layout="wide"
)


# --------------------------------------------------
# CUSTOM TITLE
# --------------------------------------------------

st.title("💰 AI Financial Coach")

st.write(
    "Upload your financial documents and ask questions "
    "about your income, expenses, loans, debt and savings."
)


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "messages" not in st.session_state:

    st.session_state.messages = []


if "documents_processed" not in st.session_state:

    st.session_state.documents_processed = False


if "processed_chunks" not in st.session_state:

    st.session_state.processed_chunks = 0


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.header("📄 Financial Documents")

    uploaded_files = st.file_uploader(
        "Upload your financial PDFs",
        type=["pdf"],
        accept_multiple_files=True
    )

    if uploaded_files:

        st.write(
            f"**{len(uploaded_files)} document(s) selected**"
        )

        for uploaded_file in uploaded_files:

            st.write(
                f"📄 {uploaded_file.name}"
            )


    st.divider()


    # --------------------------------------------------
    # SAVE DOCUMENTS
    # --------------------------------------------------

    if st.button(
        "📥 Save Documents",
        use_container_width=True
    ):

        if not uploaded_files:

            st.warning(
                "Please upload at least one PDF."
            )

        else:

            os.makedirs(
                DOCUMENTS_PATH,
                exist_ok=True
            )

            for uploaded_file in uploaded_files:

                file_path = os.path.join(
                    DOCUMENTS_PATH,
                    uploaded_file.name
                )

                with open(
                    file_path,
                    "wb"
                ) as file:

                    file.write(
                        uploaded_file.getbuffer()
                    )

            st.success(
                "Documents saved successfully."
            )


    # --------------------------------------------------
    # PROCESS DOCUMENTS
    # --------------------------------------------------

    if st.button(
        "⚙️ Process Documents",
        use_container_width=True
    ):

        with st.spinner(
            "Extracting, chunking and embedding documents..."
        ):

            try:

                chunks = ingest_documents()

                st.session_state.documents_processed = True

                st.session_state.processed_chunks = chunks

                st.success(
                    f"Processed {chunks} document chunks."
                )

            except Exception as error:

                st.error(
                    f"Error processing documents: {error}"
                )


    st.divider()


    st.subheader("📊 System Status")

    if st.session_state.documents_processed:

        st.success("RAG system ready")

        st.metric(
            "Chunks Indexed",
            st.session_state.processed_chunks
        )

    else:

        st.info(
            "Upload and process documents to begin."
        )


# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

st.header("📊 Financial Overview")

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Monthly Income",
        "₹1,37,500"
    )


with col2:

    st.metric(
        "Home Loan EMI",
        "₹43,391"
    )


with col3:

    st.metric(
        "Credit Card Balance",
        "₹52,200"
    )


with col4:

    st.metric(
        "Monthly Expenses",
        "₹1,20,000"
    )


st.caption(
    "Dashboard values are demo values based on the synthetic financial documents."
)


st.divider()


# --------------------------------------------------
# QUICK QUESTIONS
# --------------------------------------------------

st.header("💡Quick Financial Questions")

quick_questions = [

    "What is my monthly take-home salary?",

    "What is my home loan EMI?",

    "How much do I currently owe on my credit card?",

    "How much did I spend last month?",

    "How much should I save every month?",

    "Can I afford an additional ₹10,000 EMI?"
]


cols = st.columns(3)


for index, question in enumerate(quick_questions):

    with cols[index % 3]:

        if st.button(
            question,
            key=f"quick_{index}",
            use_container_width=True
        ):

            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": question
                }
            )

            st.session_state.pending_question = question

            st.rerun()


st.divider()


# --------------------------------------------------
# CHAT HISTORY
# --------------------------------------------------

st.header("🤖 AI Financial Coach")


for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# --------------------------------------------------
# PROCESS PENDING QUICK QUESTION
# --------------------------------------------------

if "pending_question" in st.session_state:

    question = st.session_state.pending_question

    del st.session_state.pending_question

    with st.chat_message("assistant"):

        with st.spinner(
            "Analyzing your financial documents..."
        ):

            try:

                result = generate_answer(
                    question
                )

                answer = result["answer"]

                sources = result["sources"]

                st.markdown(answer)


                # ------------------------------------------
                # SOURCES
                # ------------------------------------------

                if sources:

                    with st.expander(
                        "📚 View Sources"
                    ):

                        for source in sources:

                            st.write(
                                f"📄 {source}"
                            )


                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )


            except Exception as error:

                error_message = (
                    f"Something went wrong: {error}"
                )

                st.error(
                    error_message
                )

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": error_message
                    }
                )


# --------------------------------------------------
# CHAT INPUT
# --------------------------------------------------

question = st.chat_input(
    "Ask your financial coach a question..."
)


if question:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):

        st.markdown(question)


    with st.chat_message("assistant"):

        with st.spinner(
            "Searching your financial documents..."
        ):

            try:

                result = generate_answer(
                    question
                )

                answer = result["answer"]

                sources = result["sources"]

                st.markdown(answer)


                if sources:

                    with st.expander(
                        "📚 View Sources"
                    ):

                        for source in sources:

                            st.write(
                                f"📄 {source}"
                            )


                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )


            except Exception as error:

                error_message = (
                    f"Something went wrong: {error}"
                )

                st.error(
                    error_message
                )

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": error_message
                    }
                )