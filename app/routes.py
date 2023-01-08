from app import app
from app.views import HomeAPIView, CreateAccountAPIView, GetAccountAPIView


app.add_url_rule('/', view_func=HomeAPIView.as_view('home'))
app.add_url_rule('/accounts', view_func=CreateAccountAPIView.as_view('create_account'))
app.add_url_rule('/accounts/<int:id>', view_func=GetAccountAPIView.as_view('get_account'))
