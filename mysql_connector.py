import mysql.connector
from mysql.connector import Error


def create_connection():
    """Create a database connection to a MySQL server."""
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            port=3307
        )
        if conn.is_connected():
            print('Connected to MySQL database')
        return conn
    except Error as e:
        print(e)


def create_database(conn, query):
    """Create a MySQL database."""
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        print("Database created successfully")
    except Error as e:
        print(e)


def create_table(conn, query):
    """Create a table in the MySQL database."""
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        print("Table created successfully")
    except Error as e:
        print(e)


def insert_dummy_data(conn):
    """Insert dummy data into the database."""
    try:
        cursor = conn.cursor()
        # Insert into teams
        insert_teams_query = """
        INSERT INTO teams (name, league)
        VALUES
            ('Team Alpha', 'Premier League'),
            ('Team Beta', 'La Liga'),
            ('Team Gamma', 'Serie A'),
            ('Team Delta', 'Bundesliga'),
            ('Team Epsilon', 'Ligue 1'),
            ('Team Zeta', 'Eredivisie'),
            ('Team Eta', 'MLS');
        """
        cursor.execute(insert_teams_query)

        # Insert into players
        insert_players_query = """
        INSERT INTO players (name, age, position, team_id)
        VALUES
            ('John Doe', 25, 'Forward', 1),
            ('Jane Smith', 22, 'Midfielder', 1),
            ('Mike Johnson', 30, 'Defender', 2),
            ('Alice Brown', 28, 'Goalkeeper', 3),
            ('Bob Knight', 24, 'Defender', 3),
            ('Charlie Lee', 27, 'Midfielder', 4),
            ('Diana Fox', 22, 'Forward', 4),
            ('Evan Stone', 20, 'Midfielder', 5),
            ('Fiona Ray', 23, 'Defender', 5),
            ('George Oak', 25, 'Midfielder', 1),
            ('Hannah Lime', 21, 'Forward', 2),
            ('Ivan Maple', 19, 'Goalkeeper', 6),
            ('Julia Ash', 30, 'Midfielder', 6),
            ('Kevin Elm', 29, 'Forward', 7),
            ('Lily Birch', 19, 'Defender', 7);
        """
        cursor.execute(insert_players_query)

        # Insert into IoT products
        insert_products_query = """
        INSERT INTO iot_products (name, description, price)
        VALUES
            ('Heart Rate Monitor', 'Tracks and logs heart rate data.', 149.99),
            ('GPS Tracker', 'Provides real-time position tracking.', 99.99),
            ('Smart Ball', 'A football with embedded sensors to track speed and flight.', 259.99),
            ('Wearable Fitness Tracker', 'Measures fitness metrics and health indicators.', 129.99),
            ('Advanced GPS Watch', 'Provides detailed analytics of movement and pace.', 199.99),
            ('Action Camera', 'For recording training sessions and games.', 120.00),
            ('Virtual Reality Training System', 'Immersive VR system for strategy and training.', 450.00),
            ('Pressure-Sensitive Insoles', 'Tracks foot pressure and stride.', 175.00),
            ('Portable Hydration Monitor', 'Monitors and records hydration levels.', 110.00),
            ('Tactical Smart Glasses', 'Augmented reality glasses for tactical coaching.', 340.00),
            ('Wireless Muscle Stimulator', 'Portable device for muscle recovery and stimulation.', 90.00),
            ('Environmental Condition Monitor', 'Monitors temperature, humidity, and air quality.', 80.00);
        """
        cursor.execute(insert_products_query)

        # Insert into team products
        insert_team_products_query = """INSERT INTO team_products (team_id, product_id, quantity) VALUES
            (1, 1, 10),
            (1, 2, 15),
            (1, 3, 20),
            (1, 4, 5),
            (1, 5, 8);
        """

        # Commit changes
        conn.commit()
        print("Dummy data inserted successfully")
    except Error as e:
        print(e)


def main():
    # Database connection
    conn = create_connection()

    # Create database if it does not exist
    db_name = "sports_management"
    create_db_query = f"CREATE DATABASE IF NOT EXISTS {db_name}"
    create_database(conn, create_db_query)

    # Connect to the newly created database
    conn.database = db_name

    # SQL statements for creating tables
    players_table_query = """
    CREATE TABLE IF NOT EXISTS players (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        age INT,
        position VARCHAR(100),
        team_id INT,
        FOREIGN KEY (team_id) REFERENCES teams(id)
    )
    """
    teams_table_query = """
    CREATE TABLE IF NOT EXISTS teams (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        league VARCHAR(100)
    )
    """
    iot_products_table_query = """
    CREATE TABLE IF NOT EXISTS iot_products (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        description TEXT,
        price DECIMAL(10, 2) NOT NULL
    )
    """
    team_products_table_query = """
    CREATE TABLE team_products (
        team_id INT(11),
        product_id INT(11),
        quantity INT(11) DEFAULT 1,
        PRIMARY KEY (team_id, product_id),
        FOREIGN KEY (team_id) REFERENCES teams(id),
        FOREIGN KEY (product_id) REFERENCES iot_products(id)
    );
    """

    # Create tables
    create_table(conn, teams_table_query)
    create_table(conn, players_table_query)
    create_table(conn, iot_products_table_query)
    create_table(conn, team_products_table_query)

    # Insert dummy data
    insert_dummy_data(conn)

    # Close the connection
    if conn is not None and conn.is_connected():
        conn.close()


if __name__ == "__main__":
    main()
