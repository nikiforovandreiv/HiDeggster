from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.types import DomainDict


class ActionMainInfo(Action):

    def name(self) -> Text:
        return "action_utter_main_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        choice = tracker.get_slot("main_info_choice")
        answers = {"german courses": "Attending a German language course is obligatory for all exchange students.\
You can expect an extensive range of courses on the levels A1 to C1, which will enable you to improve\
and extend your German language skills and at the same time get to know Germany and the German culture better.\
You can obtain official certificates for German as a foreign language directly here at the DIT (TestDAF, telc).",
                   "application": "Sure! What exactly do would you like to know? Do you want to know about language \
skills, application period or how to apply?",
                   "orientation week": "Sure! On which campus the orientation week, that you are interested in, will\
be held ? Deggendorf, European Rottal-Inn (Pfarrkirchen) campus, or campus Cham?",
                   "exchange": "Which course are you interested in ? Business, engineering, computer science\
                   management",
                   "reviews": "Sure! I can share opinions of students from all around the globe with you!\
There are student testimonials from Brazil, Slovakia, Indonesia, Jordan, Mexico, Ecuador and Poland! Tell me the \
country you want to know opinions from"}
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
        answers = {"how to apply": "Exchange students apply via Mobility Online. The link to access the online\
        application form will be provided after you have offcially been nominated by your home university\
        (free mover applicants: application link will be provided upon request).After completing the online\
        application form, you will receive an email containing a link and login details. You then must follow\
        the link and enter a password, before entering further details and uploading your documents (such as CV,\
        photo, passport/national ID card, grade sheet, certificate of enrolment).Application as an exchange\
        student at DIT is ONLY via Mobility Online. All required documents can be uploaded and nothing should\
        be sent through traditional post or e-mail",
                   "application period": "1 April - 1 June for October entries October - 1 December for March entries",
                   "language requirements": "All exchange students must participate in a German course during the\
                    semester. Additionally, an intensive German course (level A1) is offered during the Orientation\
                     Week which is 1-2 weeks before the start of studies. Language certificates are not required"}
        if choice in answers:
            dispatcher.utter_message(text=answers[choice])
        else:
            dispatcher.utter_message(text="Sorry, I didn't get it. Can you repeat please?")

        return []


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
        campus = tracker.get_slot("campus_choice")
        answers = {"deggendorf": f"Deggendorf, great!The Orientation Week with intensive German prep course is an\
         essential event for international students. During the Orientation Week, we will help you make friends,\
          settle in and guide you into a smooth start.\n",
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
        campus = tracker.get_slot("campus_choice")
        deggendorf_answers = {"date": "date of deggendorf orientation", "participants": "participants in deggendorf",
                              "activities": "activities deggendorf", "location": "location deggendorf"}
        cham_answers = {"date": "date of cham orientation", "programme": "programme cham"}
        if campus == "deggendorf":
            choice = tracker.get_slot("deggendorf_orientation_choice")
            if choice in deggendorf_answers:
                dispatcher.utter_message(text=deggendorf_answers[choice])
        elif campus == "cham":
            choice = tracker.get_slot("cham_orientation_choice")
            dispatcher.utter_message(text=cham_answers[choice])
        elif campus == "pfarrkirchen":
            pass
        else:
            dispatcher.utter_message(text="Sorry, I didn't get the right campus")

        return []


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
        answers = {"business": {"target group": "business target",
                                           "prerequisites": "business prereq",
                                           "content": "business content",
                                           "overview": "business overview",
                                           "starting date": "business date",
                                           "fees": "business fees",
                                           "contact": "business cont"},
                              "engineering": {"target group": "engineering target",
                                              "prerequisites": "engineering prereq",
                                              "content": "engineering content",
                                              "overview": "engineering overview",
                                              "starting date": "engineeringdate",
                                              "fees": "engineering fees",
                                              "contact": "engineering cont"},
                              "computer science": {"target group": "computer science target",
                                                   "prerequisites": "computer science prereq",
                                                   "content": "computer science content",
                                                   "overview": "computer science overview",
                                                   "starting date": "computer science date",
                                                   "fees": "computer science fees",
                                                   "contact": "computer science cont"},
                              "management": "management",
                              }
        exchange_choice = tracker.get_slot("exchange_course")
        if exchange_choice == "management":
            dispatcher.utter_message(text=answers[exchange_choice])
        else:
            specific = tracker.get_slot("deggendorf_exchange_specific")
            dispatcher.utter_message(text=answers[exchange_choice][specific])
        return []


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
        answers = {"brazil": "re", "slovakia": "ro",
                                "indonesia": "Ind", "jordan": "Jor",
                                "mexico": "Mex", "ecuador": "Ecu",
                                "poland": "Pol"
                              }
        country = tracker.get_slot("reviews_country_choice").lower()
        dispatcher.utter_message(text=answers[country])
        return []


class ActionSubmitReviewsForm(Action):

    def name(self) -> Text:
        return "action_submit_reviews_form"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        answers = {"rebeka": "re", "romana": "ro",
                                "tri": "tr", "yangyang": "ya",
                                "antonia": "an", "vinicius": "vi",
                                "mayara": "ma", "qais": "qa",
                                "alejandro": "al", "denisse": "de",
                                "kornelia": "ko", "barbara": "ba"
                              }
        student = tracker.get_slot("student_choice").lower()
        dispatcher.utter_message(text=answers[student])
        return []
