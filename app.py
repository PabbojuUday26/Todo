import streamlit as st
from datetime import datetime
import pandas as pd
import json
import time
from streamlit_lottie import st_lottie
from utils.animations import load_lottieurl
from utils.database import (
    init_db,
    get_tasks,
    add_task,
    update_task,
    delete_task,
    clear_completed
)
from utils.styles import load_css

# Set page config first — must be the very first Streamlit command
st.set_page_config(
    page_title="Beautiful To-Do List",
    page_icon="✅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database and load styles
init_db()
load_css()

# Load animations
lottie_todo = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_2znxgjyt.json")
lottie_complete = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_puciaact.json")

# App header with animation
def render_header():
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("✨ Beautiful To-Do List")
        st.markdown("Organize your tasks with style and animations!")
    with col2:
        if lottie_todo:
            st_lottie(lottie_todo, height=100, key="header-animation")

# Task input form with floating effect
def task_input_form():
    with st.form("task_form", clear_on_submit=True):
        cols = st.columns([3, 1])
        with cols[0]:
            new_task = st.text_input("Add a new task", placeholder="Enter your task here...", key="new_task")
        with cols[1]:
            task_date = st.date_input("Due date", key="task_date")
        submit_button = st.form_submit_button("➕ Add Task", help="Click to add your task")
        
        if submit_button and new_task:
            add_task(new_task, task_date)
            st.success("Task added successfully!")
            time.sleep(0.5)
            st.experimental_rerun()

# Display tasks with animations and interactive elements
def display_tasks():
    tasks = get_tasks()
    
    if not tasks.empty:
        st.subheader("Your Tasks")
        
        # Filter options
        filter_col1, filter_col2, filter_col3 = st.columns([2, 2, 2])
        with filter_col1:
            show_completed = st.checkbox("Show completed tasks", value=True)
        with filter_col2:
            show_pending = st.checkbox("Show pending tasks", value=True)
        with filter_col3:
            sort_option = st.selectbox("Sort by", ["Due Date", "Added Date", "Priority"])
        
        # Apply filters
        filtered_tasks = tasks.copy()
        if not show_completed:
            filtered_tasks = filtered_tasks[~filtered_tasks['completed']]
        if not show_pending:
            filtered_tasks = filtered_tasks[filtered_tasks['completed']]
        
        # Apply sorting
        if sort_option == "Due Date":
            filtered_tasks = filtered_tasks.sort_values(by='due_date', ascending=True)
        elif sort_option == "Added Date":
            filtered_tasks = filtered_tasks.sort_values(by='created_at', ascending=False)
        
        # Display tasks with cards
        for _, task in filtered_tasks.iterrows():
            task_id = task['id']
            task_completed = task['completed']
            
            # Different card style based on completion status
            card_class = "completed-task-card" if task_completed else "pending-task-card"
            
            with st.container():
                st.markdown(f"""<div class="{card_class}">""", unsafe_allow_html=True)
                
                cols = st.columns([1, 8, 1, 1])
                with cols[0]:
                    # Checkbox with animation on change
                    new_status = st.checkbox(
                        "", 
                        value=task_completed, 
                        key=f"status_{task_id}",
                        label_visibility="collapsed"
                    )
                    if new_status != task_completed:
                        update_task(task_id, completed=new_status)
                        if new_status and lottie_complete:
                            st_lottie(lottie_complete, height=50, key=f"complete_{task_id}")
                        time.sleep(0.5)
                        st.experimental_rerun()
                
                with cols[1]:
                    due_date_str = ""
                    if task['due_date']:
                        # Parse string date to datetime object before formatting
                        due_date_dt = datetime.strptime(task['due_date'], "%Y-%m-%d")
                        due_date_str = f"📅 {due_date_dt.strftime('%b %d, %Y')}"
                    
                    task_text = f"**{task['task']}** {due_date_str}"
                    if task_completed:
                        task_text = f"~~{task_text}~~"
                    st.markdown(task_text)
                
                with cols[2]:
                    if st.button("✏️", key=f"edit_{task_id}"):
                        st.session_state.editing = task_id
                
                with cols[3]:
                    if st.button("🗑️", key=f"delete_{task_id}"):
                        delete_task(task_id)
                        st.success("Task deleted!")
                        time.sleep(0.5)
                        st.experimental_rerun()
                
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Edit form (appears when edit button is clicked)
                if st.session_state.get('editing') == task_id:
                    with st.form(f"edit_form_{task_id}"):
                        edit_cols = st.columns([3, 1, 1])
                        with edit_cols[0]:
                            edited_task = st.text_input("Edit task", value=task['task'], key=f"edit_task_{task_id}")
                        with edit_cols[1]:
                            # Parse string date to datetime.date object for date_input
                            if task['due_date']:
                                initial_date = datetime.strptime(task['due_date'], "%Y-%m-%d").date()
                            else:
                                initial_date = None
                            edited_date = st.date_input("Edit date", value=initial_date, key=f"edit_date_{task_id}")
                        with edit_cols[2]:
                            if st.form_submit_button("💾 Save"):
                                update_task(task_id, task=edited_task, due_date=edited_date)
                                del st.session_state.editing
                                st.experimental_rerun()
        
        # Clear completed tasks button
        if st.button("🧹 Clear Completed Tasks", use_container_width=True):
            clear_completed()
            st.success("Completed tasks cleared!")
            time.sleep(0.5)
            st.experimental_rerun()
    else:
        st.info("No tasks found. Add some tasks to get started!")

# Main app function
def main():
    render_header()
    task_input_form()
    display_tasks()

if __name__ == "__main__":
    if 'editing' not in st.session_state:
        st.session_state.editing = None
    main()
