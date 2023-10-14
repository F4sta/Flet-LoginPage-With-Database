""" Import modules """
import flet as ft
import assets.database as database
import assets.validate as validate
import os

if not os.path.isfile(database.db_file):
    database.Create.database(database.db_file)
    database.Create.table(database.db_file)

def main(page: ft.Page): 

    """ Setting up the main windows """
    page.title = "Register Page"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.window_resizable = False
    page.window_width = 500
    page.window_height = 600
    page.window_center()
    page.window_to_front()
    
    ''' Set Controls '''
    UserField = ft.TextField(hint_text="Username")
    UserField.width = 350
    PassField = ft.TextField(hint_text="Password", password=True)
    PassField.width = 350
    NameField = ft.TextField(hint_text="Name")
    NameField.width = 350
    EmailField = ft.TextField(hint_text="Email")
    EmailField.width = 350
    acceptBox = ft.Checkbox(label="Accept the term of policies")
    responseText = ft.Text(value="", color="red")
    
    BeforeLoginText = ft.Text(value="Already have an account?")
    Login = ft.TextButton(text="Login")
    BeforeRegisterText = ft.Text(value="Don't have an account?")
    Register = ft.TextButton(text="Register")
    LoginButton = ft.ElevatedButton(text="Login", disabled=True)
    RegisterButton = ft.ElevatedButton(text="Register", disabled=True)
    
    ''' Set Views '''
    RegisterView = ft.View("/", controls=[ft.Column(controls=[
                                ft.Row(controls=[UserField], alignment=ft.MainAxisAlignment.CENTER),
                                ft.Row(controls=[PassField], alignment=ft.MainAxisAlignment.CENTER),
                                ft.Row(controls=[NameField], alignment=ft.MainAxisAlignment.CENTER),
                                ft.Row(controls=[EmailField], alignment=ft.MainAxisAlignment.CENTER),
                                ft.Row(controls=[BeforeLoginText, Login], alignment=ft.MainAxisAlignment.CENTER, spacing=2),
                                ft.Row(controls=[acceptBox], alignment=ft.MainAxisAlignment.CENTER),
                                ft.Row(controls=[RegisterButton], alignment=ft.MainAxisAlignment.CENTER),
                                ft.Row(controls=[responseText], alignment=ft.MainAxisAlignment.CENTER)
                        ]
                    )
                ],
                    vertical_alignment=ft.MainAxisAlignment.CENTER
            )
    
    LoginView = ft.View("register", controls=[
                        ft.Column(controls=[
                                ft.Column(controls=[
                                        ft.Container(content=ft.Image(
                                                src="https://i.pinimg.com/736x/11/95/05/119505b6b530cbc0e8d65d8e56eea80b.jpg",
                                                width=100,
                                                height=100,
                                                border_radius=ft.border_radius.all(30)
                                            ), 
                                            alignment=ft.alignment.center),
                                        ft.Row(controls=[UserField], alignment=ft.MainAxisAlignment.CENTER)
                                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=60
                                ),
                                ft.Row(controls=[PassField], alignment=ft.MainAxisAlignment.CENTER),
                                ft.Row(controls=[BeforeRegisterText, Register], alignment=ft.MainAxisAlignment.CENTER, spacing=2),
                                ft.Row(controls=[acceptBox], alignment=ft.MainAxisAlignment.CENTER),
                                ft.Row(controls=[LoginButton], alignment=ft.MainAxisAlignment.CENTER),
                                ft.Row(controls=[responseText], alignment=ft.MainAxisAlignment.CENTER)
                        ]
                    )
                ],
                    vertical_alignment=ft.MainAxisAlignment.CENTER
            )
    
    LogonView = ft.View("/logon",controls=[ft.Row(controls=[ft.Text(value="GoodJob")],
                                        alignment=ft.MainAxisAlignment.CENTER)],
                    vertical_alignment=ft.MainAxisAlignment.CENTER)

    """ Handler for the page views """
    def views_handler(route):
        match route:
            case '/' :
                return LoginView
            case '/register' :
                return RegisterView
            case '/logon' :
                return LogonView
    
    """ Route changer """
    def switch_route(e):
        match page.route:
            case '/' :
                clear_values()
                page.go('/register')
                UserField.on_change = validate_controls
                PassField.on_change = validate_controls
                acceptBox.on_change = validate_controls
                Register.on_click = switch_route
                LoginButton.on_click = login_callback
                
            case '/register' :
                clear_values()
                page.go('/')
                UserField.on_change = validate_controls
                PassField.on_change = validate_controls
                NameField.on_change = validate_controls
                EmailField.on_change = validate_controls
                acceptBox.on_change = validate_controls
                Login.on_click = switch_route
                RegisterButton.on_click = register_callback
    
    """ Callback for the Login Button on the Login Page:
                    Main login callback """
    def login_callback(e):
        Username = UserField.value
        Password = PassField.value
        
        result = database.Get.AccountBy.Username(Username)
        if result != None:
            u = result[1]
            p = result[2]
            
            print(u,p,result)
            if Username == u and Password == p:
                page.go("/logon")
            else:
                UserField.value = ""
                PassField.value = ""
                responseText.value = "Username or Password is incorrect!"
                page.update()
            
        else:
            UserField.value = ""
            PassField.value = ""
            responseText.value = "Username or Password is incorrect!"
            page.update()
    
    """ Callback for the Register Button on the Register Page:
            Insert the User account into the database """
    def register_callback(e):
        Username = UserField.value
        Password = PassField.value
        Name = NameField.value
        Email = EmailField.value
        
        def __respFunc(response_text):
            responseText.disabled = False
            responseText.color = "Red"
            responseText.value = response_text
            page.update()
            
        pswd_bool, pswd_resp = validate.isPasswordValid(Password)
            
        if database.Check.Username(Username) != True:
            if pswd_bool:
                if database.Check.Email(Email) != True:
                    if validate.isEmailValid(Email):
                        database.Insert.account(username=Username, password=Password, name=Name, email=Email)
                        clear_values()
                        responseText.disabled = False
                        responseText.value = "Registed"
                        responseText.color = "Green"
                        page.update()
                    else: __respFunc("Email is not valid!")
                else: __respFunc("Email is registed already!")
            else: __respFunc(pswd_resp)
        else:__respFunc("Username is taken already!")
        
    
    """ Callback that Validate that the textfields and other controls have values,
                if they have values the button turns pressable """
    def validate_controls(e):
        match page.route:
            case "/":
                if all([UserField.value, PassField.value, acceptBox.value]):
                    LoginButton.disabled = False
                    page.update()
                else:
                    LoginButton.disabled = True
                    page.update()
            case "/register":
                if all([UserField.value, PassField.value, NameField.value, EmailField.value, acceptBox.value]):
                    RegisterButton.disabled = False
                    page.update()
                    
                else:
                    RegisterButton.disabled = True
                    page.update()
    
    """ Clear the values of controls """
    def clear_values():
        UserField.value = ""
        PassField.value = ""
        NameField.value = ""
        EmailField.value = ""
        acceptBox.value = False
        LoginButton.disabled = True 
        RegisterButton.disabled = True 
        
    """ Changes the app route """
    def route_change(route):
        print(page.route)
        page.views.clear()
        page.views.append(
            views_handler(page.route)
        )
    
    ''' Set Functions to Controls '''
    UserField.on_change = validate_controls
    PassField.on_change = validate_controls
    NameField.on_change = validate_controls
    EmailField.on_change = validate_controls
    acceptBox.on_change = validate_controls
    Register.on_click = switch_route
    LoginButton.on_click = login_callback
    Login.on_click = switch_route
    RegisterButton.on_click = register_callback
    page.on_route_change = route_change
    
    ''' Login Page Show '''
    page.go('/')
    
if __name__ == '__main__':
    ft.app(target=main)