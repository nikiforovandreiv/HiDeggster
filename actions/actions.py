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
        """Database of supported campuses"""

        return ["deggendorf", "pfarrkirchen", "cham"]

    @staticmethod
    def deggendorf_choice_db() -> List[Text]:
        """Database of supported campuses"""

        return ["activities", "participants", "date", "location"]

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

    def validate_deggendorf_orientation_choice(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        if slot_value in self.deggendorf_choice_db():
            # validation succeeded
            return {"deggendorf_orientation_choice": slot_value}
        else:
            # validation failed, set this slot to None so that the
            # user will be asked for the slot again
            return {"deggendorf_orientation_choice": None}


class ActionOrientationWeekInfo(Action):

    def name(self) -> Text:
        return "action_orientation_week_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        campus = tracker.get_slot("campus_choice").lower()
        answers = answer_database["orientation_week_main"]
        if campus in answers:
            dispatcher.utter_message(text=answers[campus])
        else:
            dispatcher.utter_message(text="Sorry, I didn't get the right campus. Can you rephrase it?")

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
    def exchange_db() -> List[Text]:
        return ["business", "engineering", "computer science", "management"]

    @staticmethod
    def deggendorf_exchange_db() -> List[Text]:
        return ["prerequisites", "target group", "content", "overview", "starting date", "fees", "contact"]

    def validate_exchange_course(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate campus value."""

        if slot_value in self.exchange_db():
            # validation succeeded
            return {"exchange_course": slot_value}
        else:
            # validation failed, set this slot to None so that the
            # user will be asked for the slot again
            return {"exchange_course": None}

    def validate_deggendorf_exchange_specific(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        if slot_value in self.deggendorf_exchange_db():
            # validation succeeded
            return {"deggendorf_exchange_specific": slot_value}
        else:
            # validation failed, set this slot to None so that the
            # user will be asked for the slot again
            return {"deggendorf_exchange_specific": None}


class ActionSubmitExchangeCourses(Action):

    def name(self) -> Text:
        return "action_submit_exchange_courses"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        answers = answer_database["exchange_courses_info"]
        exchange_choice = tracker.get_slot("exchange_course").lower()
        if exchange_choice in answers:
            if exchange_choice == "management":
                dispatcher.utter_message(text=answers[exchange_choice])
            else:
                specific = tracker.get_slot("deggendorf_exchange_specific")
                dispatcher.utter_message(text=answers[exchange_choice][specific])
        else:
            dispatcher.utter_message(text="Sorry, I didn't get what you meant")
        return [events.SlotSet("exchange_course", None), events.SlotSet("deggendorf_exchange_specific", None)]


class ValidateReviewsForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_reviews_form"

    @staticmethod
    def country_db() -> List[Text]:
        """Database of supported campuses"""

        return ["poland", "ecuador", "mexico", "jordan", "indonesia", "slovakia", "brazil"]

    @staticmethod
    def student_db() -> List[Text]:
        """Database of supported campuses"""

        return ["rebeka", "romana", "tri", "yangyang", "antonia", "vinicius", "mayara", "qais", "alejandro",
                "denisse", "kornelia", "barbara"]

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

    def validate_student_choice(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:

        if slot_value in self.student_db():
            # validation succeeded
            return {"student_choice": slot_value}
        else:
            # validation failed, set this slot to None so that the
            # user will be asked for the slot again
            return {"student_choice": None}


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
        if student in answers:
            dispatcher.utter_message(text=answers[student])
        else:
            dispatcher.utter_message(text="Sorry, I didn't get what you meant")
        return [events.SlotSet("reviews_country_choice", None), events.SlotSet("student_choice", None)]
