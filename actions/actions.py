# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []


from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionApplicationInfo(Action):
    def name(self) -> Text:
        return "action_application_info"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        section_entity = tracker.get_slot("application_section")
        print("Section Entity:", section_entity)
        if section_entity == "language skills":
            extracted_text = "All exchange students must participate in a German course during the semester.\
             Additionally, an intensive German course (level A1) is offered during the Orientation Week\
              which is 1-2 weeks before the start of studies. Language certificates are not required."
        elif section_entity == "application period":
            extracted_text = "The online application portal is only activated during the following\
             application periods:\n- 1 April - 1 June for October entries\n- 1 October - 1 December for March entries"
        elif section_entity == "how to apply":
            extracted_text = "View the application procedure checklist to guide you step-by-step through preparation\
             for your exchange semester at DIT.\nExchange students apply via Mobility Online. The link to access\
              the online application form will be provided after you have offcially been nominated by your home\
               university (free mover applicants: application link will be provided upon request).\nAfter\
                completing the online application form, you will receive an email containing a link and login\
                 details. You then must follow the link and enter a password, before entering further details and\
                  uploading your documents (such as CV, photo, passport/national ID card, grade sheet, certificate\
                   of enrolment).\nApplication as an exchange student at DIT is ONLY via Mobility Online.\
                    All required documents can be uploaded and nothing should be sent through traditional post\
                     or e-mail"
        else:
            extracted_text = "I'm sorry, can you say exactly what do you want to know about application?"
        # Send the extracted text as a response
        dispatcher.utter_message(text=extracted_text)
        return []