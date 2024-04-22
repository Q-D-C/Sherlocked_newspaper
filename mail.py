# pip install sib-api-v3-sdk

import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

api_key = 'SECRAT KEY'
configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = api_key

# Create an instance of the Contacts API class
api_instance = sib_api_v3_sdk.ContactsApi(
    sib_api_v3_sdk.ApiClient(configuration))


def manage_contact(name, email, id, room):
    # Check if contact already exists
    try:
        # Get information about a contact by email
        contact_info = api_instance.get_contact_info(email)
        print("Contact already exists:")
        # print(contact_info)
        print("Updating attribute")
        # Update contact attributes
        update_contact = sib_api_v3_sdk.UpdateContact(attributes={room: 'YES'})
        api_instance.update_contact(email, update_contact)
        print(f"Contact '{email}' updated with '{room}'=YES.")
    except ApiException as e:
        if e.status == 404:  # Contact does not exist
            print("Contact does not exist, adding new contact...")
            # Create a contact
            if room == 'ALCHEMIST':
                create_contact = sib_api_v3_sdk.CreateContact(email=email, attributes={
                                                              'FIRSTNAME': name, 'AGENT_ID': id, 'ALCHEMIST': 'YES', 'ARCHETECT': 'NO', 'VALT': 'NO'})
            elif room == 'ARCHETECT':
                create_contact = sib_api_v3_sdk.CreateContact(email=email, attributes={
                                                              'FIRSTNAME': name, 'AGENT_ID': id, 'ALCHEMIST': 'NO', 'ARCHETECT': 'YES', 'VALT': 'NO'})
            elif room == 'VALT':
                create_contact = sib_api_v3_sdk.CreateContact(email=email, attributes={
                                                              'FIRSTNAME': name, 'AGENT_ID': id, 'ALCHEMIST': 'NO', 'ARCHETECT': 'NO', 'VALT': 'YES'})

            try:
                # Add the new contact
                api_response = api_instance.create_contact(create_contact)
                print(api_response)
                # print(contact_info)
            except ApiException as e:
                print("An error occurred while creating contact:")
                print(e)
        else:
            print("An error occurred while retrieving contact:")
            print(e)


manage_contact('Woody', 'Woody@cowboy.org', '400', 'ARCHETECT')
