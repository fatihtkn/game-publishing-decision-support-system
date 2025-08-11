from flask import Flask, request, jsonify,render_template,redirect,url_for,request
import mysql.connector
import base64
app = Flask(__name__)


conn = mysql.connector.connect(
    host="localhost",
    user="root",        
    password="",            
    database="oyun_sistemi"   
)

cursor = conn.cursor()


@app.route('/')
def home():
     return render_template('loginScreen.html')


@app.route('/prototype_reports')
def prototype_reports():
     return render_template('prototypeReports.html')



@app.route("/login", methods=['GET','POST'])
def login():

    data = request.get_json()
    userId = data.get('userId')
    userPassword = data.get('userPassword')
    
    conn = mysql.connector.connect(
        host="localhost",
        user="root",        
        password="",            
        database="logindatabase"
    )   

    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE userId = %s", (userId,))
    result = cursor.fetchone()
    
    if result:
        if result[0] == userPassword:
          
            
            return jsonify({"success": True, "redirect_url": url_for('mainPage')}), 200
           
        else:
            return jsonify({"success": False, "message": "Invalid Id and password"}), 401
           
    else:
        return jsonify({"success": False, "message": "Invalid Id and password"}), 401
       





@app.route('/add_company', methods=['GET','POST'])
def addcompany():
    data = request.get_json()

    name = data['name']
    contact_email = data['contact_email']
    
    try:
        cursor.execute("INSERT INTO companies (name, contact_email) VALUES (%s, %s)", (name, contact_email))
        conn.commit()
        return jsonify({"message": "Şirket başarıyla eklendi."}), 201
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500


@app.route('/add_game', methods=['POST'])
def add_game():
    data = request.get_json()
    company_id = data['company_id']
    game_name = data['game_name']
    genre = data['genre']
    cpi = data['cpi']
    retention_rate = data['retention_rate']

    try:
        cursor.execute(
            "INSERT INTO games (company_id, game_name, genre, cpi, retention_rate) VALUES (%s, %s, %s, %s, %s)",
            (company_id, game_name, genre, cpi, retention_rate)
        )
        conn.commit()
        return jsonify({"message": "Oyun başarıyla eklendi."}), 201
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500


@app.route('/evaluate_game/<int:game_id>', methods=['POST'])
def evaluate_game(game_id):
    try:
        cursor.execute("SELECT cpi, retention_rate FROM games WHERE id = %s", (game_id,))
        result = cursor.fetchone()
       
        if result:
            cpi, retention_rate = result
            if cpi < 1.0 and retention_rate > 0.3:
                decision = True
                reason = "CPI düşük ve Retention Rate yüksek"
            else:
                decision = False
                reason = "CPI veya Retention Rate uygun değil"

            return jsonify({"decision": decision, "reason": reason,"resultId":str(5)}), 200
        else:
            return jsonify({"error": "Oyun bulunamadı."}), 404
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500



@app.route('/mainPage')
def mainPage():



   
    return render_template('mainPage.html')



@app.route('/updategamestable', methods=['GET', 'POST'])
def updategamestable():
    if request.method == 'GET':
      
        cursor.execute("SELECT company_id, name FROM companies")
        companies = cursor.fetchall()
        return jsonify([{"id": c[0], "name": c[1]} for c in companies])
    
    if request.method == 'POST':
      
        company_id = request.json.get('company_id')
        if not company_id:
            return jsonify({"error": "No company ID provided"}), 400
        
        gamesIdQuery="SELECT game_id FROM games WHERE company_id=%s"

        cursor.execute(gamesIdQuery,(company_id, ))
        gamesIdRaw=cursor.fetchall()
        game_ids = [row[0] for row in gamesIdRaw]

        metricDatas=[]
        for id in game_ids:

            metricsQuery= """
            SELECT 
            SUM(cp.cost) AS total_cost,
            SUM(cp.impression) AS total_impressions,
            SUM(cp.click) AS total_clicks,
            SUM(cp.install) AS total_installs
            FROM 
            creative_performance cp
            JOIN 
            creative c ON cp.creative_id = c.creative_id
            JOIN 
            ad_set a ON c.adSet_id = a.adSet_id
            WHERE 
            a.game_id = %s;
            """
            cursor.execute(metricsQuery,(id, ))
            result=cursor.fetchone()
            
            total_cost = result[0] if result[0] is not None else 0
            total_impression = result[1] if result[1] is not None else 0
            total_click = result[2] if result[2] is not None else 0
            total_install = result[3] if result[3] is not None else 0
        
            cpi = round(total_cost / total_install, 2) if total_install > 0 else 0
            ctr = round((total_click / total_impression) * 100, 2) if total_impression > 0 else 0
            cvr = round((total_install / total_click) * 100, 2) if total_click > 0 else 0
            metricDatas.append({"cpi":cpi,"ctr":ctr,"cvr":cvr})
      

        cursor.execute(
            "SELECT icon, title, status FROM games WHERE company_id = %s", 
            (company_id,)
        )
        games_data = cursor.fetchall()
     
        games = []

        index=0
        for game in games_data:
            icon_blob, title, status = game
            icon_url = f"data:image/png;base64,{base64.b64encode(icon_blob).decode('utf-8')}"
            games.append({
                "icon": icon_url,
                "title": title,
                "status": status,
                "cpi": metricDatas[index]["cpi"],
                "cvr": metricDatas[index]["cvr"],
                "ctr": metricDatas[index]["ctr"] 
            })
            index+=1
        return jsonify(games)
                

def fetch_performance_data(game_id):
    query = """
    SELECT 
        cp.date,
        SUM(cp.install) AS total_installs,
        SUM(cp.click) / SUM(cp.install) AS cpi
    FROM 
        creative_performance cp
    JOIN 
        creative c ON cp.creative_id = c.creative_id
    JOIN 
        ad_set a ON c.adSet_id = a.adSet_id
    WHERE 
        a.game_id = %s
    GROUP BY 
        cp.date
    ORDER BY 
        cp.date ASC;
    """
    cursor.execute(query, (game_id,))
    results = cursor.fetchall()
    return results

@app.route('/get_chart_data', methods=['POST'])
def get_chart_data():
    game_id = 1
    

    data = fetch_performance_data(game_id)

    return jsonify(data)

@app.route("/get_companies", methods=["GET"])
def get_companies():
  
    cursor.execute("""
        SELECT 
            c.name AS company_name, 
            g.title AS game_title, 
            g.game_id
        FROM 
            companies c
        LEFT JOIN 
            games g
        ON 
            c.company_id = g.company_id
        ORDER BY 
            c.name, g.title;
    """)
    
    rows = cursor.fetchall()

  
    companies = {}

    for row in rows:
        company_name = row[0]
        game_title = row[1]
        game_id = row[2]

        
        if company_name not in companies:
            companies[company_name] = []

        companies[company_name].append({"game_id": game_id, "title": game_title})

   
    return jsonify(companies)


@app.route("/get_game_details", methods=["POST"])
def get_game_details():
  
    data = request.get_json()
    game_id = data.get('game_id')
    
    if not game_id:
        return jsonify({"error": "game_id is required"}), 400

  
    cursor.execute("""
        SELECT 
            games.title, games.icon , companies.name, companies.company_id
        FROM 
            games, companies
        WHERE 
            game_id = %s AND games.company_id=companies.company_id
    """, (game_id, ))
   
    game = cursor.fetchone()
   
    if game:
        icon_blob=game[1]
        icon_url = f"data:image/png;base64,{base64.b64encode(icon_blob).decode('utf-8')}"
        return jsonify({
            "title": game[0],
            "icon": icon_url,
            "companyName": game[2],
            "company_id" : game[3]

        })
    else:
        return jsonify({"error": "Game not found"}), 404



@app.route('/get_selected_game_metrics',methods=["POST"])
def get_selected_game_metrics():

    data = request.get_json()
    game_id = data.get('game_id')
    metricDatas=[]
    
    metricsQuery= """
    SELECT 
    SUM(cp.cost) AS total_cost,
    SUM(cp.impression) AS total_impressions,
    SUM(cp.click) AS total_clicks,
    SUM(cp.install) AS total_installs
    FROM 
    creative_performance cp
    JOIN 
    creative c ON cp.creative_id = c.creative_id
    JOIN 
    ad_set a ON c.adSet_id = a.adSet_id
    WHERE 
    a.game_id = %s;
    """
    cursor.execute(metricsQuery,(game_id, ))
    result=cursor.fetchone()
    
    total_cost = result[0] if result[0] is not None else 0
    total_impression = result[1] if result[1] is not None else 0
    total_click = result[2] if result[2] is not None else 0
    total_install = result[3] if result[3] is not None else 0

    cpi = round(total_cost / total_install, 2) if total_install > 0 else 0
    ctr = round((total_click / total_impression) * 100, 2) if total_impression > 0 else 0
    cvr = round((total_install / total_click) * 100, 2) if total_click > 0 else 0
    metricDatas.append({"cpi":cpi,"ctr":ctr,"cvr":cvr})
   
    return jsonify({"cpi":cpi,"ctr":ctr,"cvr":cvr})





@app.route('/update_line_chart_data',methods=['POST'])
def update_line_chart_data():
    data=request.get_json()
    game_id = data.get('game_id')

    datas=[]
    query="""SELECT date, SUM(cost) AS total_cost, SUM(install) AS total_install, (SUM(cost) / NULLIF(SUM(install), 0)) AS cpi 
    FROM creative_performance cp
    JOIN 
    creative c ON cp.creative_id = c.creative_id
    JOIN 
    ad_set a ON c.adSet_id = a.adSet_id
    WHERE 
    a.game_id = %s
    GROUP BY date 
    ORDER BY date ASC"""

    cursor.execute(query,(game_id, ))
    result=cursor.fetchall()
    
    
    for data in result:
        
        datas.append({"date":data[0],"cost":data[1],"install":data[2],"cpi":data[3]})

    
   
    return jsonify(datas)


@app.route('/creatives', methods=['GET'])
def get_creatives():

    game_id = request.args.get('game_id', type=int)
    
    metricDatas=[]

    campaignMetricsQuery= """
            SELECT SUM(cp.cost) AS total_cost, SUM(cp.impression) AS total_impressions, SUM(cp.click) AS total_clicks, SUM(cp.install) AS total_installs, a.adSet_id, c.creative_id 
            FROM creative_performance cp 
            JOIN creative c ON cp.creative_id = c.creative_id JOIN ad_set a ON c.adSet_id = a.adSet_id WHERE a.game_id = %s GROUP BY c.creative_id
            """
    cursor.execute(campaignMetricsQuery,(game_id, ))
    result=cursor.fetchall()
   
    for data in result:

        total_cost = data[0] if data[0] is not None else 0
        total_impression = data[1] if data[1] is not None else 0
        total_click = data[2] if data[2] is not None else 0
        total_install = data[3] if data[3] is not None else 0
        idset_id=data[4]
        creative_id=data[5]

        cpi = round(total_cost / total_install, 2) if total_install > 0 else 0
        ctr = round((total_click / total_impression) * 100, 2) if total_impression > 0 else 0
        cvr = round((total_install / total_click) * 100, 2) if total_click > 0 else 0
        metricDatas.append({"cpi":cpi,"ctr":ctr,"cvr":cvr,"creative_id":creative_id,"adset_id":idset_id,"install":total_install,"click":total_click,"impression":total_impression,"cost":total_cost})
    


    return jsonify(metricDatas)



@app.route('/playtime_cohort', methods=['GET'])
def playtime_cohort():


    campaignMetricsQuery= """
            SELECT play_time.date, play_time.user_count, play_time.playtime FROM play_time WHERE play_time.game_id=1
            """
    cursor.execute(campaignMetricsQuery)
    result=cursor.fetchall()
    print(result)
   
    


    return jsonify(result)









if __name__ == '__main__':
    app.run(debug=True)
