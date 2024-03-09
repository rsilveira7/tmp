import streamlit as st
from streamlit_chat import message
from langchain_community.llms import Bedrock
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import (ConversationBufferMemory, 
                                                  ConversationSummaryMemory, 
                                                  ConversationBufferWindowMemory
               
                                                  )

#Validatoin of password ########################################################################
import hmac
def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""        
        if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password.
        else:
            st.session_state["password_correct"] = False

    # Return True if the password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show input for password.
    st.text_input(
        "Password", type="password", on_change=password_entered, key="password"
    )
    if "password_correct" in st.session_state:
        st.error("😕 Password incorrect")
    return False


if not check_password():
    st.stop()  # Do not continue if check_password is not True.

# Main Streamlit app starts here #########################################################################################
##########################################################################################################################
if 'conversation' not in st.session_state:
    st.session_state['conversation'] =None
if 'messages' not in st.session_state:
    st.session_state['messages'] =[]


# Setting page title and header ##########################################################################################
st.set_page_config(page_title="Chat GPT Clone", page_icon=":robot_face:")
st.markdown("<h1 style='text-align: center;'>O que você deseja saber? </h1>", unsafe_allow_html=True)


def getresponse(userInput):

    if st.session_state['conversation'] is None:

        llm = Bedrock( credentials_profile_name="bedrockadmin", model_id="meta.llama2-70b-chat-v1" )
        
        st.session_state['conversation'] = ConversationChain(
            llm=llm,
            verbose=True,
            memory=ConversationSummaryMemory(llm=llm)
        )

    response=st.session_state['conversation'].predict(input=userInput)
    print(st.session_state['conversation'].memory.buffer)
    

    return response



response_container = st.container()
# Here we will have a container for user input text box
container = st.container()


with container:
    with st.form(key='my_form', clear_on_submit=True):
        user_input = st.text_area("Digite sua consulta aqui:", key='input', height=100)
        submit_button = st.form_submit_button(label='Enviar')

        if submit_button:
            st.session_state['messages'].append(user_input)
            model_response=getresponse(user_input)
            st.session_state['messages'].append(model_response)
            

            with response_container:
                for i in range(len(st.session_state['messages'])):
                        if (i % 2) == 0:
                            message(st.session_state['messages'][i], is_user=True, key=str(i) + '_user')
                        else:
                            message(st.session_state['messages'][i], key=str(i) + '_AI')
        
             

        
