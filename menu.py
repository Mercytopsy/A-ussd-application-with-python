from utils import respond, update_session
from model import SessionLevel, User
from db import db



class LowerLevelMenu:
    """


    """
    def __init__(self, session_id, phone_number):
        """
        initialises the Menu class
        :param user, session_id
        sets the user and session_id to be used by the menus
        """
        self.session_id = session_id
        self.user = User.query.filter_by(phone_number=phone_number).first()
        self.session = SessionLevel.query.filter_by(session_id=self.session_id).first()

    def home(self):
        """
        If user level is zero or zero
        Serves the home menu
        :return: a response object with headers['Content-Type'] = "text/plain" headers
        """

        # upgrade user level and serve home menu
        # TODO background task here
        self.session.promote_level()
        db.session.add(self.session)
        db.session.commit()
        # serve the menu
        menu_text = "CON Le Café de Bains,Welcome to our Store\n"
        menu_text += " 1. Please place your order.\n"
        menu_text += " 2. Buy your food items\n"
        menu_text += " 3. Checkout other items\n"
        menu_text += " 4. pay\n"

        # print the response on to the page so that our gateway can read it
        return respond(menu_text)

    
    def place_your_order(self):
        # as how much and Launch teh Mpesa Checkout to the user
        menu_text = "CON choose your choice\n"
        menu_text += " 1. 1 Sharwama.\n"
        menu_text += " 2. 2 Pizza.\n"
        menu_text += " 3. 3 Soup-e Adas (Lentil Soup).\n"

        # Update sessions to level 9
        update_session(self.session_id, SessionLevel, 9)
        # print the response on to the page so that our gateway can read it
        return respond(menu_text)

    def checkout_other_items(self):
        # Ask how much and Launch B2C to the user
        menu_text = "CON Le Café de Bains,Welcome to our Store \n"
        menu_text += " 1. 1 Rice.\n"
        menu_text += " 2. 2 Beans.\n"
        menu_text += " 3. 3 Yam.\n"

        # Update sessions to level 10
        update_session(self.session_id, SessionLevel, 10)

        # Print the response onto the page so that our gateway can read it
        return respond(menu_text)

    def pay(self):
        # Send Another User Some Money
        menu_text = "CON You can only pay in Naira\n"
        menu_text += " Enter a valid phonenumber (like 0722122122)\n"

        # Update sessions to level 11
        update_session(self.session_id, SessionLevel, 11)
        # Print the response onto the page so that our gateway can read it
        return respond(menu_text)


    def default_menu(self):
        # Return user to Main Menu & Demote user's level
        menu_text = "CON You have to choose a service.\n"
        menu_text += "Press 0 to go back to main menu.\n"
        # demote
        self.session.demote_level()
        db.session.add(self.session)
        db.session.commit()
        # Print the response onto the page so that our gateway can read it
        return respond(menu_text)

    @staticmethod
    def class_menu(session):
        # Return user to Main Menu & Demote user's level
        menu_text = "CON You have to choose a service.\n"
        menu_text += "Press 0 to go back to main menu.\n"
        # demote
        session.demote_level()
        db.session.add(session)
        db.session.commit()
        # Print the response onto the page so that our gateway can read it
        return respond(menu_text)

class HighLevelMenu:
    """
    Serves high level callbacks
    """
    def __init__(self, user_response, phone_number, session_id):
        """

        """
        self.phone_number = phone_number
        self.session_id = session_id
        self.user = User.query.filter_by(phone_number=phone_number).first()
        self.session = SessionLevel.query.filter_by(session_id=self.session_id).first()
        self.user_response = user_response




    def default_mpesa_c(self):
        menu_text = "Your orders have been noted... \n"
        # Print the response onto the page so that our gateway can read it
        return respond(menu_text)

    # end level 9


    # level 10

    def b2c_default(self):
        menu_text = "Your orders have been noted... \n"
        # Print the response onto the page so that our gateway can read it
        return respond(menu_text)

    # end level 10


    # level 11
    def pay_for_order(self, ):
        buyer_phone_number = self.user_response
        message = "We have taken care of your orders \nIf \
            this is a wrong number the transaction will fail\n" \
                      "Your number is {} \n\
                      Thank you.\n".format(buyer__phone_number)
            # TODO figure out
            # change user level to 0
            # session_level = SessionLevel.query.filter_by(session_id=session_id).first()
            # session_level.demote_level()
            # db.session.add(session_level)

            # Update DB
        db.session.commit()

            # respond
        menu_text += "CONFIRMED we have seem your orders {} \n".format(message)
        return respond(menu_text)

    
  

        # end higher level responses


class RegistrationMenu:
    """
    Serves registration callbacks
    """
    def __init__(self, phone_number, session_id, user_response):
        """

        """
        self.session_id = session_id
        self.user = User.query.filter_by(phone_number=phone_number).first()
        self.session = SessionLevel.query.filter_by(session_id=self.session_id).first()
        self.user_response = user_response
        self.phone_number = phone_number

    def get_number(self):
        # insert user's phone number
        new_user = User(phone_number=self.phone_number)
        # TODO background task
        db.session.add(new_user)
        db.session.commit()
        # create a new sessionlevel
        session = SessionLevel(
            session_id=self.session_id, phone_number=self.phone_number)

        # promote the user a higher session level
        session.promote_level(21)
        db.session.add(session)
        db.session.commit()
        menu_text = "CON Please enter your name"

        # Print the response onto the page so that our gateway can read it
        return respond(menu_text)

    def get_name(self):
        # Request again for name - level has not changed...
        if self.user_response:

            # insert user name into db request for city
            self.user.name =self.user_response

            # graduate user level

            self.session.promote_level(22)
            db.session.add(self.session)
            db.session.add(self.user)
            menu_text = "CON Enter your city"

        else:
            menu_text = "CON Name not supposed to be empty. Please enter your name \n"

        # Print the response onto the page so that our gateway can read it
        return respond(menu_text)

    def get_city(self):
        if self.user_response:

            # if user response is not an empty string
            # insert user city into db request for city
            self.user.city = self.user_response

            # demote user level to 0
            self.session.demote_level()
            db.session.add(self.session)
            db.session.add(self.user)
            db.session.commit()
            menu_text = "END You have been successfully registered. \n"

        else:

            # if user response is an empty string
            # Request again for city - level has not changed...
            menu_text = "CON City not supposed to be empty. Please enter your city \n"

        # Print the response onto the page so that our gateway can read it
        return respond(menu_text)

    @staticmethod
    def register_default():
        menu_text = "END Apologies something went wrong \n"

        # Print the response onto the page so that our gateway can read it
        return respond(menu_text)


