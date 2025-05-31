import streamlit as st

def load_css():
    custom_css = """
    <style>
        /* Main container styling */
        .stApp {
            background-color: #f5f7fa;
        }
        
        /* Task cards styling */
        .pending-task-card {
            background: white;
            padding: 1rem;
            margin: 0.5rem 0;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            border-left: 4px solid #4e79a7;
            transition: all 0.3s ease;
        }
        
        .completed-task-card {
            background: #f0f0f0;
            padding: 1rem;
            margin: 0.5rem 0;
            border-radius: 10px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            border-left: 4px solid #59a14f;
            transition: all 0.3s ease;
        }
        
        .pending-task-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(0,0,0,0.15);
        }
        
        /* Button styling */
        .stButton>button {
            border-radius: 8px;
            transition: all 0.2s;
        }
        
        .stButton>button:hover {
            transform: scale(1.05);
        }
        
        /* Input field styling */
        .stTextInput>div>div>input {
            border-radius: 8px;
            padding: 10px;
        }
        
        /* Date input styling */
        .stDateInput>div>div>input {
            border-radius: 8px;
            padding: 8px;
        }
        
        /* Animation for task completion */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .stLottie {
            animation: fadeIn 0.5s ease-out;
        }
        
        /* Responsive design */
        @media (max-width: 768px) {
            .pending-task-card, .completed-task-card {
                padding: 0.8rem;
            }
        }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)