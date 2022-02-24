# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
#
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, EventType
from rasa_sdk.types import DomainDict
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

EQUIPE = ["Advise", "Ambre", "TOPO", "IGWAN", "NewSFC", "MOBI", "Parnasse", "ENOV"]
DOMAINE = ["orange", "dsi", "b2b", "C2S"]

class ValidateInfosForm(FormValidationAction):

    def name(self) -> Text:
        return "validate_agile_form"

    def validate_equipe(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:

        dispatcher.utter_message(text=f"Super !")
        return {"equipe": slot_value}

    
    def validate_nb_personne(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:

        dispatcher.utter_message(text= f"Bien noté")
        return {"nb_personne": slot_value}

    def validate_domaine(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:

        dispatcher.utter_message(text=f"Parfait !")
        return {"domaine": slot_value}
    
class ValidateFormationForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_formation_form"
    
    def validate_type_formation(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:

        dispatcher.utter_message(text=f"Parfait! Vous voulez suivre la formation {slot_value} ")
        return {"type_formation": slot_value}
    
    def validate_niveau(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    )-> Dict[Text, Any]:

        dispatcher.utter_message(text=f"D'accord..")
        return {"niveau": slot_value}
    
    def validate_session(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    )-> Dict[Text, Any]:

        dispatcher.utter_message(text=f"D'accord..")
        return {"session": slot_value}
        
    
    

class ActionUnlikelyIntent(Action):

    def name(self) -> Text:
        return "action_unlikely_intent"

    async def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        # Implement custom logic here
        dispatcher.utter_message(text="Vous n'avez pas répandu !")
        return []

