from flask import Flask, render_template, request, redirect, url_for, session
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
import os
import uuid

# Initialize the Flask application 

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Generates a random key

api_key = 'SECRET KEY'
configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = api_key
api_instance = sib_api_v3_sdk.ContactsApi(
    sib_api_v3_sdk.ApiClient(configuration))

@app.route('/', methods=['GET', 'POST'])
def home():
    selected_room = session.get('selected_room', '')  # Retrieve the last selected room from the session
    if request.method == 'POST':
        names = request.form.getlist('name[]')
        agent_ids = request.form.getlist('agent_id[]')
        emails = request.form.getlist('email[]')
        room = request.form.get('room')
        # Generate a new team ID for each submission
        team_id = str(uuid.uuid4())  # Generate a unique team ID
        if room:  # Ensure room is not None or empty
            for name, agent_id, email in zip(names, agent_ids, emails):
                manage_contact(name, email, agent_id, room, team_id)
            session['selected_room'] = room  # Save the selected room in the session
        else:
            # Handle the case where no room is selected
            print("No room selected")
        return redirect(url_for('home'))
    return render_template('form.html', selected_room=selected_room)


def manage_contact(name, email, agent_id, room, team_id):
    try:
        # Fetch existing contact information to check if updates are needed
        contact_info = api_instance.get_contact_info(email)
        print(f"Contact {email} exists. Updating information...")
        
        # Update the specific room with the agent ID and team ID
        attributes = {room: agent_id, 'TEAM_ID': team_id}  # Set the room variable to agent_id
        update_contact = sib_api_v3_sdk.UpdateContact(attributes=attributes)
        api_instance.update_contact(email, update_contact)
        print(f"Contact '{email}' updated with '{room}' set to agent ID '{agent_id}' and TEAM_ID set to '{team_id}'.")
    except ApiException as e:
        print(f"An error occurred while updating or retrieving contact: {e}")
        if e.status == 404:
            # If contact does not exist, create it
            print(f"Contact {email} does not exist. Creating new contact...")
            attributes = {'FIRSTNAME': name, 'ALCHEMIST': '', 'ARCHITECT': '', 'VAULT': '', 'TEAM_ID': team_id}
            attributes[room] = agent_id  # Set only the selected room to agent_id
            create_contact = sib_api_v3_sdk.CreateContact(email=email, attributes=attributes)
            try:
                api_response = api_instance.create_contact(create_contact)
                print(f"Contact created: {api_response}")
            except ApiException as e:
                print(f"An error occurred while creating contact: {e}")
        else:
            print("An error occurred:", e)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)