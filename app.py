from flask import Flask, request, jsonify
import psycopg2
import os
import config  # Import the config module

app = Flask(__name__)


def get_db_connection():
    try:
        print(f"Connecting to database {config.DB_NAME} at {config.DB_HOST} with user {config.DB_USER}")
        conn = psycopg2.connect(
            host=config.DB_HOST,
            dbname=config.DB_NAME,
            user=config.DB_USER,
            password=config.DB_PASS
        )
        print("Database connection successful")
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None


# Routes
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user_name = data.get('user_name')
    password = data.get('password')

    conn = get_db_connection()
    if conn is None:
        return jsonify({'message': 'Database connection failed', 'status': 0}), 500

    try:
        cur = conn.cursor()
        cur.execute("SELECT user_name, password FROM public.user_master WHERE user_name = %s and status='true'",
                    (user_name,))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user and user[1] == password:
            return jsonify({'message': 'Login successful', 'status': 1}), 200
        else:
            return jsonify({'message': 'Invalid credentials', 'status': 0}), 401
    except Exception as e:
        print(f"Error during login: {e}")
        return jsonify({'message': 'Internal server error', 'status': 0}), 500


# Route to fetch job details
@app.route('/jobs', methods=['GET'])
def get_jobs():
    conn = get_db_connection()
    if conn is None:
        return jsonify({'message': 'Database connection failed', 'status': 0}), 500

    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM public.jobs where status='true'")
        jobs = cur.fetchall()
        cur.close()
        conn.close()

        # Convert the fetched job details to a list of dictionaries
        jobs_list = []
        for job in jobs:
            jobs_list.append({
                'id': job[0],
                'job_reference_no': job[1],
                'title': job[2],
                'client_name': job[3],
                'venue_address': job[4],
                'status': job[5],
                'crew_type': job[6],
                'no_of_container': job[7],
                'employee': job[8],
                'setup_date': job[9],
                'rehearsal_date': job[10],
                'show_start_date': job[11],
                'show_end_date': job[12],
                'category_name': job[13],
                'equipment_name': job[14],
                'quantity': job[15],
                'number_of_days': job[16],
                'amount': job[17]
            })

        return jsonify({'jobs': jobs_list, 'status': 1}), 200
    except Exception as e:
        print(f"Error fetching job details: {e}")
        return jsonify({'message': 'Internal server error', 'status': 0}), 500


if __name__ == '__main__':
    app.run(debug=True)
