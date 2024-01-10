from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk import events
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.types import DomainDict
import json

json_data = open("actions/database.json", "r")
answer_database = json.load(json_data)
json_data.close()


class ActionMainInfo(Action):

    def name(self) -> Text:
        return "action_utter_main_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        choice = tracker.get_slot("main_info_choice").lower()
        answers = answer_database["main_info"]
        if choice in answers:
            dispatcher.utter_message(text=answers[choice])
        else:
            dispatcher.utter_message(text="Sorry, I didn't get it. Can you repeat please?")

        return []


class ActionApplicationInfo(Action):

    def name(self) -> Text:
        return "action_application_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        choice = tracker.get_slot("application_choice")
        answers = answer_database["application_info"]
        if choice in answers:
            dispatcher.utter_message(text=answers[choice])
        else:
            dispatcher.utter_message(text="Sorry, I didn't get it. Can you repeat please?")

        return [events.SlotSet("application_choice", None)]


class ValidateOrientationWeekForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_orientation_week_form"

    async def required_slots(
        self,
        domain_slots: List[Text],
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: "DomainDict",
    ) -> List[Text]:
        additional_slots = []
        if tracker.get_slot("campus_choice") == "deggendorf":
            additional_slots.append("deggendorf_orientation_choice")
        elif tracker.get_slot("campus_choice") == "cham":
            additional_slots.append("cham_orientation_choice")

        return additional_slots + domain_slots

    @staticmethod
    def campus_db() -> List[Text]:
        """Database of supported cuisines"""

        return ["deggendorf", "pfarrkirchen", "cham"]

    def validate_campus_choice(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate campus value."""

        if slot_value in self.campus_db():
            # validation succeeded
            return {"campus_choice": slot_value}
        else:
            # validation failed, set this slot to None so that the
            # user will be asked for the slot again
            return {"campus_choice": None}


class ActionOrientationWeekInfo(Action):

    def name(self) -> Text:
        return "action_orientation_week_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        campus = tracker.get_slot("campus_choice").lower()
        answers = {"deggendorf": f"Deggendorf, great!The Orientation Week with intensive German prep course is an\
         essential event for international students. During the Orientation Week, we will help you make friends,\
          settle in and guide you into a smooth start. Would you like to know the activities, participants, date or\
location of the orientation week\n",
                   "pfarrkirchen": "European campus, sure! On your arrival at the European Campus Rottal-Inn you will\
                    take part in a so-called \"Orientation Day.\" In addition to many social events you will receive\
                     detailed course information and practical support with all necessary formalities, such as \
                     registration at the town hall, health insurance, opening a bank account, German courses and\
                      application for a students card. The International Office informs students about events in\
                       the coming semester and international students will have the opportunity to ask all questions\
                        about studying and living in Pfarrkirchen.",
                   "cham": "Campus cham, great! Would you like to know the dates or programme of the week?"}
        if campus in answers:
            dispatcher.utter_message(text=answers[campus])
        else:
            dispatcher.utter_message(text="Sorry, I didn't get the right campus")

        return []


class ActionOrientationWeekAdditional(Action):

    def name(self) -> Text:
        return "action_orientation_week_additional"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        campus = tracker.get_slot("campus_choice").lower()
        answers = answer_database["orientation_week_info"]
        deggendorf_answers = answers["deggendorf"]
        cham_answers = answers["cham"]
        if campus == "deggendorf":
            choice = tracker.get_slot("deggendorf_orientation_choice")
            if choice in deggendorf_answers:
                dispatcher.utter_message(text=deggendorf_answers[choice])
        elif campus == "cham":
            choice = tracker.get_slot("cham_orientation_choice")
            dispatcher.utter_message(text=cham_answers[choice])
        elif campus == "pfarrkirchen":
            dispatcher.utter_message(text=answers["pfarrkirchen"])
        else:
            dispatcher.utter_message(text="Sorry, I didn't get the right campus")

        return [events.SlotSet("campus_choice", None), events.SlotSet("deggendorf_orientation_choice", None),
                events.SlotSet("cham_orientation_choice", None)]


class ValidateExchangeCoursesForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_exchange_courses_form"

    @staticmethod
    def campus_db() -> List[Text]:
        """Database of supported campuses"""

        return ["deggendorf", "pfarrkirchen"]

    def validate_campus_choice(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate campus value."""

        if slot_value in self.campus_db():
            # validation succeeded
            return {"campus_choice": slot_value}
        else:
            # validation failed, set this slot to None so that the
            # user will be asked for the slot again
            return {"campus_choice": None}


class ActionSubmitExchangeCourses(Action):

    def name(self) -> Text:
        return "action_submit_exchange_courses"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        answers = answer_database["exchange_courses_info"]
        exchange_choice = tracker.get_slot("exchange_course").lower()
        if exchange_choice == "management":
            dispatcher.utter_message(text=answers[exchange_choice])
        else:
            specific = tracker.get_slot("deggendorf_exchange_specific")
            dispatcher.utter_message(text=answers[exchange_choice][specific])
        return [events.SlotSet("exchange_course", None), events.SlotSet("deggendorf_exchange_specific", None)]


class ValidateReviewsForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_reviews_form"

    @staticmethod
    def country_db() -> List[Text]:
        """Database of supported campuses"""

        return ["poland", "ecuador", "mexico", "jordan", "indonesia", "slovakia", "brazil"]

    def validate_reviews_country_choice(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:

        if slot_value in self.country_db():
            # validation succeeded
            return {"reviews_country_choice": slot_value}
        else:
            # validation failed, set this slot to None so that the
            # user will be asked for the slot again
            return {"reviews_country_choice": None}


class ActionAskStudent(Action):

    def name(self) -> Text:
        return "action_ask_student"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        answers = answer_database["ask_student"]
        country = tracker.get_slot("reviews_country_choice").lower()
        dispatcher.utter_message(text=answers[country])
        return []


class ActionSubmitReviewsForm(Action):

    def name(self) -> Text:
        return "action_submit_reviews_form"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        answers = answer_database["student_testimonials"]
        student = tracker.get_slot("student_choice").lower()
        dispatcher.utter_message(text=answers[student])
        return [events.SlotSet("reviews_country_choice", None), events.SlotSet("student_choice", None)]
