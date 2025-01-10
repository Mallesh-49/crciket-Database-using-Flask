
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql.functions import count

app=Flask(__name__)
#to create a database called cricket
app.config["SQLALCHEMY_DATABASE_URI"]='sqlite:///cricket_data.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
class Base(DeclarativeBase):
    pass
db = SQLAlchemy(model_class=Base)
db.init_app(app)

class Batsman(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250),nullable=False)
    country: Mapped[str] = mapped_column(String(250), nullable=False)
    matches: Mapped[int] = mapped_column(Integer, nullable=False)
    runs: Mapped[int] = mapped_column(Integer, nullable=False)
    centuries: Mapped[int] = mapped_column(Integer, nullable=False,default=0)
    def __repr__(self):
        return f'<Batsman {self.name}>'
class Bowler(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250),nullable=False)
    country: Mapped[str] = mapped_column(String(250), nullable=False)
    matches: Mapped[int] = mapped_column(Integer, nullable=False)
    wickets: Mapped[int] = mapped_column(Integer, nullable=False)
    economy: Mapped[float] = mapped_column(Float, nullable=False)
    def __repr__(self):
        return f'<Bowler {self.name}>'

class All_Rounder2(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250),nullable=False)
    country: Mapped[str] = mapped_column(String(250), nullable=False)
    matches: Mapped[int] = mapped_column(Integer, nullable=False)
    runs: Mapped[int] = mapped_column(Integer, nullable=False)
    wickets: Mapped[int] = mapped_column(Integer, nullable=False)
    def __repr__(self):
        return f'<All_Rounder {self.name}>'
with app.app_context():
    db.create_all()
@app.route("/")
def home():
    return render_template("index.html")
@app.route("/select_role",methods=["GET","POST"])
def select_role():
    if request.method=="POST":
        role=request.form["role"]
        return redirect(url_for("add_players",role=role))
    return render_template("select_role.html")
@app.route("/players/<role>/<int:id>",methods=["GET","POST"])
def details(role,id):
    if role=="Batsman":
        player=Batsman.query.get_or_404(id)

    elif role=="Bowler":
        player=Bowler.query.get_or_404(id)
    elif role=="All-rounder":
        player=All_Rounder2.query.get_or_404(id)
    else:
        return "Invalid one",404
    return render_template("details.html",role=role,player=player)

#to add player  based on role in this database
@app.route("/add/<role>",methods=["POST","GET"])
def add_players(role):
    if request.method=="POST":
        name=request.form["name"]
        country=request.form["country"]
        matches=request.form["matches"]
        if role=="Batsman":
            runs=int(request.form["runs"])
            centuries=int(request.form.get("centuries",0))
            new_player=Batsman(name=name,country=country,matches=matches,runs=runs,centuries=centuries)
            db.session.add(new_player)
            db.session.commit()
        elif role=="Bowler":
            wickets=int(request.form["wickets"])
            economy=float(request.form["economy"])
            new_player=Bowler(name=name,country=country,matches=matches,wickets=wickets,economy=economy)
            db.session.add(new_player)
            db.session.commit()
        elif role == "All-rounder":
            print(request.form)
            runs = int(request.form["runs"])
            wickets= int(request.form["wickets"])
            new_player = All_Rounder2(name=name, country=country, matches=matches,runs=runs, wickets=wickets)
            db.session.add(new_player)
            db.session.commit()
        else:
            return "Invalid role", 400
        return redirect(url_for("view_players"))
    return render_template("add_players.html",role=role)

#for view players
@app.route("/players",methods=["GET","POST"])
def view_players():
        query = request.args.get('query', "").strip()

        # If a query is provided, filter the results
        if query:
            batsman = Batsman.query.filter(
                (Batsman.name.ilike(f"%{query}%")) | (Batsman.country.ilike(f"%{query}%"))
            ).all()

            bowlers = Bowler.query.filter(
                (Bowler.name.ilike(f"%{query}%")) | (Bowler.country.ilike(f"%{query}%"))
            ).all()

            rounders = All_Rounder2.query.filter(
                (All_Rounder2.name.ilike(f"%{query}%")) | (All_Rounder2.country.ilike(f"%{query}%"))
            ).all()


            return render_template('players.html', batsman=batsman, bowlers=bowlers, allrounders=rounders, query=query)

        # If no query, show all players
        else:
            batsman = Batsman.query.all()
            bowlers = Bowler.query.all()
            rounders = All_Rounder2.query.all()
            print("Batsman:", batsman)
            print("Bowlers:", bowlers)
            print("All-rounders:", rounders)
            return render_template("players.html", batsman=batsman, bowlers=bowlers, allrounders=rounders)






@app.route("/delete/<role>/<int:id>",methods=["GET"])
def delete(role,id):
    if role=="Batsman":
        player=Batsman.query.get_or_404(id)
    elif role=="Bowler":
        player=Bowler.query.get_or_404(id)
    elif role=="All-rounder":
        player=All_Rounder2.query.get_or_404(id)
    else:
        return "Invalid one",404
    db.session.delete(player)
    db.session.commit()
    return redirect(url_for("view_players"))





if __name__=="__main__":
       app.run(debug=True)









