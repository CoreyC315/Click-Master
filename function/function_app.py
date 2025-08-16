import azure.functions as func
import logging
import json
import pyodbc # Import pyodbc
import os # Import os to get environment variables

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="submitScore", methods=["POST"])
def submitScore(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse(
            json.dumps({"error": "Please pass a JSON object in the request body"}),
            mimetype="application/json",
            status_code=400
        )

    name = req_body.get('name')
    clicks = req_body.get('clickTotal')

    if name and clicks is not None:
        try:
            # Get connection string from local.settings.json
            conn_string = os.environ["SqlConnectionString"]

            # Connect to the database and insert the data
            with pyodbc.connect(conn_string) as conn:
                with conn.cursor() as cursor:
                    sql_command = "INSERT INTO Leaderboard (PlayerName, ClickCount) VALUES (?, ?)"
                    cursor.execute(sql_command, name, clicks)
                conn.commit()

            response_body = {
                "message": f"Hello, {name}! Your score of {clicks} has been received and saved.",
                "status": "success"
            }
            return func.HttpResponse(
                json.dumps(response_body),
                mimetype="application/json",
                status_code=200
            )
        except Exception as e:
            logging.error(f"Database error: {e}")
            return func.HttpResponse(
                json.dumps({"error": f"An error occurred while saving the score: {str(e)}"}),
                mimetype="application/json",
                status_code=500
            )
    else:
        return func.HttpResponse(
            json.dumps({"error": "Please pass 'name' and 'clickTotal' in the request body"}),
            mimetype="application/json",
            status_code=400
        )
    
@app.route(route="getTopScores", methods=["GET"])
def getTopScores(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        conn_string = os.environ["SqlConnectionString"]
        with pyodbc.connect(conn_string) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT TOP 20 PlayerName, ClickCount FROM Leaderboard ORDER BY ClickCount DESC")
                rows = cursor.fetchall()

                top_scores = []
                for row in rows:
                    top_scores.append({"name": row.PlayerName, "clickTotal": row.ClickCount})

        return func.HttpResponse(
            json.dumps(top_scores),
            mimetype="application/json",
            status_code=200
        )
    except Exception as e:
        logging.error(f"Database error: {e}")
        return func.HttpResponse(
            json.dumps({"error": f"An error occurred while retrieving scores: {str(e)}"}),
            mimetype="application/json",
            status_code=500
        )