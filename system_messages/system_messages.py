import os
from datetime import date, datetime
from agent_profile import AgentProfile
from user_profile import UserProfile

def read_file(file_name):
    with open(os.path.join("system_messages", file_name), "r") as f:
        return f.read()

class SystemMessages:
    def role_msg(self, user, agent_id):
        print(f"user: {user}, agent_id: {agent_id}")
        agent_profile = AgentProfile.load(user, agent_id)
        user_profile = UserProfile.load(user)
        self.raw_message = read_file("role_msg.txt")

        if agent_profile is None or user_profile is None:
            raise Exception("No agent or user found with the provided keys")

        agent_details = agent_profile.get('agent_details', {})
        user_details = user_profile.get('user_profile_details', {})
        # print the details
        print('Agent Details:', agent_details)
        print('User Details:', user_details)

        # calculate agent's age from DOB
        today = date.today()
        dob = datetime.strptime(agent_details.get('agent_dob', ''), "%Y-%m-%d").date()  # assuming dob is in this format
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        # calculate user's age from DOB, assuming the user's DOB is also provided

        return self.raw_message.format(
            a_name=agent_profile.get('agent_name', ''),
            a_age=age,
            a_ethnicity=agent_details.get('agent_ethnicity', ''),
            a_gender=agent_details.get('agent_gender', ''),
            a_iq=agent_details.get('agent_IQ', ''),
            a_labels=agent_details.get('agent_physical_characteristic', ''),
            a_eq=agent_details.get('agent_EQ', ''),
            a_personality=agent_details.get('agent_personality', ''),  # Assuming humor is covered under 'agent_personality'
            relationship=agent_details.get('agent_relationship', ''),
            u_name=user_profile.get('u_name', ''),
            u_age=user_profile.get('u_age', ''),
            u_ethnicity=user_details.get('u_ethnicity', ''),
            u_gender=user_details.get('u_gender', ''),
            u_iq=user_details.get('u_iq', ''),
            u_labels=user_details.get('u_labels', ''),
            u_personality=user_details.get('u_personality', '')
        )
    
    def chat_msg(self, user, agent_id):
        agent_profile = AgentProfile.load(user, agent_id)
        user_profile = UserProfile.load(user)
        self.raw_message = read_file("chat_msg.txt")

        if agent_profile is None or user_profile is None:
            raise Exception("No agent or user found with the provided keys")

        agent_details = agent_profile.get('agent_details', {})
        # calculate user's age from DOB, assuming the user's DOB is also provided
        return self.raw_message.format(
            a_ethnicity=agent_details.get('agent_ethnicity', ''),
            u_name=user_profile.get('u_name', ''),
        )
    
    def ssml_msg(self):
        self.raw_message = read_file("ssml_msg.txt")

        return self.raw_message
    