from flask import Flask,render_template
from flask import request
from model import User, SessionLevel
from utils import respond, add_session
from menu import LowerLevelMenu, HighLevelMenu, RegistrationMenu


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'jose'

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    ussdChannel = "*384*73621#" # Your ussd channel from Africa's Talking
    return render_template('index.html', channel=ussdChannel)
  


@app.route('/ussd', methods=['POST', 'GET'])
def ussd_callback():

    # GET values from the AT's POST request
    session_id = request.values.get("sessionId", None)

    servicecode =  request.values.get("serviceCode",None)
    phone_number = request.values.get("phoneNumber", None)
    text = request.values.get("text", "default")
    text_array = text.split("*")
    user_response = text_array[len(text_array) - 1]


    # 4. Check the level of the user from the DB and retain default level if none is found for this session
    session = SessionLevel.query.filter_by(session_id=session_id).first()
    # 5. Check if the user is in the d
    user = User.query.filter_by(phone_number=phone_number).first()
  	# 6. Check if the user is available (yes)->Serve the menu; (no)->Register the user
    if user:
		# 7. Serve the Services Menu

        if session:
            level = session.level
            # if level is less than 2 serve lower level menus
            if level < 2:

                menu = LowerLevelMenu(
                    session_id=session_id, phone_number=phone_number)

                # initialise menu dict
                menus = {
                    "0": menu.home,
                    "1": menu.place_your_order,
                    "2": menu.checkout_other_items,
                    "3": menu.pay,
                    "default": menu.default_menu
                }
                # serve menu

                if user_response in menus.keys():
                    return menus.get(user_response)()
                else:
                    return menus.get("default")()


            # if level is between 9 and 12 serve high level response
            elif level <= 11:
                menu = HighLevelMenu(user_response, phone_number, session_id)
                # initialise menu dict
                menus = {
                    9: {

                        # user_response : c2b_checkout(
                        # phone_number= phone_number, amount = int(user_response)
                        # )

                        "1": menu.default_mpesa_c,
                        "2": menu.default_mpesa_c,
                        "3": menu.default_mpesa_c,
                        "default": menu.default_mpesa_c
                    },
                    10: {

                        # user_response : b2c_checkout(
                        # phone_number=phone_number, amount=int(user_response)
                        # )

                        "1": menu.b2c_default,
                        "2": menu.b2c_default,
                        "3": menu.b2c_default,
                        "default": menu.b2c_default
                    },
                    11: {
                        # "4": re_pay_loan(session_id, phone_number, amount)
                        "4": menu.pay_for_order,  # 1
                        "5": menu.pay_for_order,  # 2
                        "6": menu.pay_for_order,  # 3
                        "default": menu.b2c_default
                    },
                    "default": {
                        "default": menu.b2c_default
                    }
                }

                if user_response in menus[level].keys():
                    return menus[level].get(user_response)()
                else:
                    return menus[level]["default"]()
            elif level <= 22:
                menu = RegistrationMenu(
                    session_id=session_id, phone_number=phone_number, user_response=user_response)
                # handle higher level user registration
                menus = {
                    # params = (session_id, phone_number=phone_number)
                    0: menu.get_number,
                    21: menu.get_name,
                    # params = (session_id, phone_number=phone_number,
                    # user_response=user_response)
                    22: menu.get_city,
                    # params = (session_id, phone_number=phone_number,
                    # user_response=user_response)
                    "default": menu.register_default,  # params = (session_id)

                }

                return menus.get(level or "default")()
            else:
                return LowerLevelMenu.class_menu(session)
        else:
            # add a new session level
            add_session(session_id=session_id, phone_number=phone_number)
            # create a menu instance

            menu = LowerLevelMenu(session_id=session_id,
                                  phone_number=phone_number)

            # serve home menu
            return menu.home()

    else:
        # create a menu instance

        menu = RegistrationMenu(
            session_id=session_id, phone_number=phone_number, user_response=user_response)

        # register user
        return menu.get_number()

if __name__ == '__main__':
    from db import db
    db.init_app(app)
app.run(port=5000, debug=True)
