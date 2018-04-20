import plotly.plotly as py
import plotly.graph_objs as go
import sqlite3 as sqlite
from flask import Flask, render_template
import requests
import webbrowser, threading

app = Flask(__name__)

# A bar chart that demonstrates the total number of
# different types of crime since 09/20/2016.
def option_one():
    conn = sqlite.connect('crimes.db')
    cur = conn.cursor()

    statement = "SELECT CrimeType, COUNT(*) FROM CrimeCases "
    statement += "GROUP BY CrimeType"

    diff_crimes = ["Theft", "Other", "Robbery", "Assault", "Arrest", "Vandalism", "Burglary"]
    num_crimes = []
    cur.execute(statement)

    for row in cur:
        num_crimes.append(int(row[1]))

    conn.close()

    data = [go.Bar(
                x=diff_crimes,
                y=num_crimes
        )]

    layout = go.Layout(
        title="Total number of different crimes since 09/20/2016",
        yaxis = dict(
            range=[0, 40]
        ),
        height=500,
        width=1000
    )

    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename='basic-bar')

    return num_crimes



def option_two():
    conn = sqlite.connect('crimes.db')
    cur = conn.cursor()

    statement = "SELECT CrimeType, COUNT(*) FROM CrimeCases "
    statement += "GROUP BY CrimeType"

    diff_crimes = ["Theft", "Other", "Robbery", "Assault", "Arrest", "Vandalism", "Burglary"]
    num_crimes = []
    cur.execute(statement)

    for row in cur:
        num_crimes.append(int(row[1]))

    conn.close()

    data = [go.Pie(
                labels=diff_crimes,
                values=num_crimes
        )]

    layout = go.Layout(
        title="Percentage of different types of crimes since 09/20/2016"
    )

    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename='basic-pie')
    return num_crimes


def option_three():
    conn = sqlite.connect('crimes.db')
    cur = conn.cursor()

    statement = "SELECT COUNT(*) FROM CrimeCases "
    statement += "GROUP BY Month"

    diff_crimes = ["Sept", "Oct", "Nov", "Dec", "Jan", "Feb", "Mar", "Apr"]
    num_crimes = []
    cur.execute(statement)

    for row in cur:
        num_crimes.append(int(row[0]))

    conn.close()

    ## reverse num_crimes
    first_half = num_crimes[4:]
    second_half = num_crimes[:4]
    num_crimes = first_half + second_half

    data = [go.Bar(
                x=diff_crimes,
                y=num_crimes
        )]

    layout = go.Layout(
        title="Total number of crimes each month since 09/20/2016",
        yaxis = dict(
            range=[0, 40]
        ),
        height=500,
        width=1000
    )

    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename='basic-bar_2')
    return num_crimes


def option_four():
    conn = sqlite.connect('crimes.db')
    cur = conn.cursor()

    statement = "SELECT COUNT(*) FROM CrimeCases, Crimes "
    statement += "WHERE CrimeCases.CrimeType=Crimes.Id AND Crimes.Id=1 "
    statement += "GROUP BY Month"

    diff_crimes = ["Sept", "Oct", "Nov", "Dec", "Jan", "Feb", "Mar", "Apr"]
    num_crimes = []
    cur.execute(statement)

    for row in cur:
        num_crimes.append(int(row[0]))

    conn.close()

    ## reverse num_crimes
    first_half = num_crimes[4:]
    second_half = num_crimes[:4]
    num_crimes = first_half + second_half

    data = [go.Pie(
                labels=diff_crimes,
                values=num_crimes
        )]

    layout = go.Layout(
        title="Percentage of theft each month since 09/20/2016"
    )

    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename='basic-pie_2')
    return num_crimes


# A flask web page that shows the most recent 30 tweets of
# three crimes(Theft, Assault and Robbery) and
# any news about arrest(Arrest) in Michigan.
@app.route('/<crime_input>')
def hello_name(crime_input):
    conn = sqlite.connect('crimes.db')
    cur = conn.cursor()

    statement = "SELECT CrimeTweets.TweetText FROM CrimeTweets, Crimes "
    if crime_input == "Theft":
        statement += "WHERE CrimeTweets.CrimeTypeTweet=Crimes.Id AND Crimes.CrimeName='Theft'"
    elif crime_input == "Assault":
        statement += "WHERE CrimeTweets.CrimeTypeTweet=Crimes.Id AND Crimes.CrimeName='Assault'"
    elif crime_input == "Robbery":
        statement += "WHERE CrimeTweets.CrimeTypeTweet=Crimes.Id AND Crimes.CrimeName='Robbery'"

    cur.execute(statement)
    all_tweets = []
    for row in cur:
        all_tweets.append(row[0])

    conn.close()

    print(all_tweets)

    data = {
        "current_tweets": all_tweets,
        "current_crime": crime_input
    }

    return render_template('crime.html', **data)




## main program
if __name__=="__main__":
    user_choice = input("Enter menu option(1, 2, 3, 4, 5 or exit): ")
    while (user_choice != "5" and user_choice != "exit"):
        if user_choice == "1":
            option_one()
            user_choice = input("Enter menu option(1, 2, 3, 4, 5 or exit): ")
        elif user_choice == "2":
            option_two()
            user_choice = input("Enter menu option(1, 2, 3, 4, 5 or exit): ")
        elif user_choice == "3":
            option_three()
            user_choice = input("Enter menu option(1, 2, 3, 4, 5 or exit): ")
        elif user_choice == "4":
            option_four()
            user_choice = input("Enter menu option(1, 2, 3, 4, 5 or exit): ")
        else:
            user_choice = input("Invalid menu choice, please enter a valid choice: ")

    if user_choice == "5":
        crime_interested = input("Which crime tweets you want to read(Theft, Assault or Robbery): ")
        while (crime_interested != "Theft" and crime_interested != "Assault" and crime_interested != "Robbery"):
            crime_interested = input("Enter a valid crime name(Theft, Assault or Robbery): ")
        cur_url = 'http://127.0.0.1:5000' + '/' + crime_interested
        threading.Timer(1.25, lambda: webbrowser.open(cur_url) ).start()
        app.run(debug=False)
    elif user_choice == "exit":
        print("Bye!!")
