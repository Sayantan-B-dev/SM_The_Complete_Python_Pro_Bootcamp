from flask import Flask,render_template, request,session
import requests
import math


app=Flask(__name__)

app.secret_key = "asdgadsgadgadgadg"

AGEAPI="https://api.agify.io/?name="
GENDERAPI="https://api.genderize.io/?name="
FAKEAPI="https://dummyjson.com/products"
BLOG_API_URL = "https://jsonfakery.com/blogs"

def get_age(name):
    ageapi=AGEAPI+name

    response=requests.get(ageapi)

    data=response.json()

    return data.get("age")

def get_gender(name):

    genderapi=GENDERAPI+name

    response=requests.get(genderapi)

    data=response.json()

    return data.get("gender")
    
@app.route('/', methods=['GET', 'POST'])
def name():

    stored_name = session.get("name")
    stored_age = session.get("age")
    stored_gender = session.get("gender")
    stored_fakeapi_data = session.get("fakeapi_data")

    name=request.args.get('name')

    if name:
        stored_name = name
        stored_age = get_age(name)
        stored_gender = get_gender(name)   

        session["name"] = stored_name
        session["age"] = stored_age
        session["gender"] = stored_gender
        

    if request.method == "POST":
        response = requests.get(FAKEAPI)
        stored_fakeapi_data = response.json()

        session["fakeapi_data"] = stored_fakeapi_data  

    return render_template(
        'index.html',
        name=stored_name,
        age=stored_age,
        gender=stored_gender,
        fakeapi_data=stored_fakeapi_data
    )

@app.route("/blogs")
def blogs():

    current_page = request.args.get("page", 1, type=int)

    response = requests.get(BLOG_API_URL)
    blogs_data = response.json()

    blogs_per_page = 1

    total_blogs = len(blogs_data)

    total_pages = math.ceil(total_blogs / blogs_per_page)

    if current_page < 1:
        current_page = 1
    if current_page > total_pages:
        current_page = total_pages
    start_index = (current_page - 1) * blogs_per_page
    end_index = start_index + blogs_per_page

    paginated_blogs = blogs_data[start_index:end_index]

    return render_template(
        "blogs.html",
        blogs=paginated_blogs,
        current_page=current_page,
        total_pages=total_pages
    )


if __name__=='__main__':
    app.run(debug=True)
