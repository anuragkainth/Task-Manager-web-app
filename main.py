
import streamlit as st
import requests

BASE_URL = "http://localhost:4000/api/tasks/"

# Function to fetch all tasks from the backend
def fetch_tasks():
    response = requests.get(BASE_URL)
    return response.json()

# Function to add a new task
def add_task(title, description):
    data = {"title": title, "description": description}
    response = requests.post(BASE_URL, json=data)
    return response.json()

# Function to update an existing task
def update_task(task_id, title, description, removed):
    data = {"title": title, "description": description, "removed": removed}
    response = requests.patch(f"{BASE_URL}{task_id}", json=data)
    return response.json()

# Function to delete a task
def delete_task(task_id):
    response = requests.delete(f"{BASE_URL}{task_id}")
    return response.json()

# Function to remove or un-remove a task
def remove_task(task_id, is_removed):
    data = {"removed": is_removed}
    response = requests.patch(f"{BASE_URL}remove/{task_id}", json=data)
    return response.json()


def main():
    st.title("To-Do Task Manager")

    # Fetch tasks from the backend
    tasks = fetch_tasks()
    

    not_done_tasks = [task for task in tasks if not task["removed"]]
    done_tasks = [task for task in tasks if task["removed"]]
    
    if(not_done_tasks):
        st.write("### Pending Tasks:")
        for task in reversed(not_done_tasks): 
            task_id = task["_id"]
            with st.expander(task["title"], expanded=False):
                title = st.text_input("Title", task["title"], key=f"title_{task_id}")
                description = st.text_area("Description", task["description"], key=f"description_{task_id}")
                if st.button("Update", key=f"update_{task_id}"):
                    update_task(task_id, title, description, task["removed"])
                    st.write("Task updated successfully!")
                    st.experimental_rerun()
                if st.button("Remove", key=f"remove_{task_id}"):
                    remove_task(task_id, True)
                    st.write("Task removed successfully!")
                    st.experimental_rerun()
                if st.button("Delete", key=f"delete_{task_id}"):
                    delete_task(task_id)
                    st.write("Task deleted successfully!")
                    st.experimental_rerun()

    if done_tasks:
        st.write("### Completed Tasks:")
        for task in reversed(done_tasks): 
            task_id = task["_id"]
            with st.expander(task["title"], expanded=False):
                st.markdown(f"<s>{task['title']}</s>", unsafe_allow_html=True)
                st.text_area("Description", task["description"], key=f"description_{task_id}", disabled=True)
                if st.button("Un-Remove", key=f"unremove_{task_id}"):
                    remove_task(task_id, False)
                    st.write("Task un-removed successfully!")
                    st.experimental_rerun()


    st.write("### Add New Tasks:")
    new_title = st.text_input("New Task Title")
    new_description = st.text_area("New Task Description")
    if st.button("Add Task"):
        if new_title:
            added_task = add_task(new_title, new_description)
            st.experimental_rerun()



if __name__ == "__main__":
    main()
