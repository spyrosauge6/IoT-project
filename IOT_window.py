import mysql.connector
from PyQt6.QtWidgets import QLabel, QWidget, QMainWindow, QPushButton, QLineEdit, QComboBox, QVBoxLayout, QHBoxLayout, \
    QTableWidget, QTableWidgetItem, QMessageBox, QFormLayout, QSpinBox
from PyQt6.QtGui import QIcon, QPixmap, QCursor, QDoubleValidator, QIntValidator
from PyQt6.QtCore import Qt
from decimal import Decimal


def create_connection():
    """Create a database connection to the MySQL server."""
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='sports_management',
            port=3307
        )
        return conn
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL Platform: {e}")
        return None


def get_table_count(table_name):
    """Fetch the count of records from the given table."""
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            query = f"SELECT COUNT(*) FROM {table_name}"
            cursor.execute(query)
            count = cursor.fetchone()[0]
            conn.close()
            return count
        except mysql.connector.Error as e:
            print(f"Error fetching count from {table_name}: {e}")
    return 0


def fetch_costs():
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            query = """
            SELECT teams.name, SUM(iot_products.price * team_products.quantity) AS total_cost
            FROM team_products
            JOIN teams ON team_products.team_id = teams.id
            JOIN iot_products ON team_products.product_id = iot_products.id
            GROUP BY teams.name
            """
            cursor.execute(query)
            return cursor.fetchall()
        except mysql.connector.Error as e:
            print(f"Error fetching cost data: {e}")
        finally:
            conn.close()
    return []


def fetch_players():
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT p.id, p.name, p.age, p.position, t.name AS team_name 
                FROM players p 
                JOIN teams t ON p.team_id = t.id
            """)
            return cursor.fetchall()
        except mysql.connector.Error as e:
            print(f"Error fetching players: {e}")
        finally:
            conn.close()
    return []


def fetch_iot_products():
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, price FROM iot_products")
            products = cursor.fetchall()
            return products
        except mysql.connector.Error as e:
            print(f"Error fetching IoT products: {e}")
        finally:
            conn.close()
    return []


class EarningsDialog(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Earnings by Team")
        self.UPatras_icon = QIcon("Images/up_2017_logo_en.ico")
        self.setWindowIcon(self.UPatras_icon)
        self.layout = QVBoxLayout()

        # Create QTableWidget
        self.table = QTableWidget()

        self.setupUI()

    def setupUI(self):
        table_style = """
        QTableWidget {
            border: 1px solid #C4C4C3;
            border-radius: 5px;
            background-color: #FFFFFF;
        }
        
        QTableWidget::item:selected {
            background-color: #a2d2ff;
            color: #FFFFFF;
        }
        
        QHeaderView::section {
            background-color: #f2f2f2;
            padding: 5px;
            border: 1px solid #C4C4C3;
            font-size: 16px;
            font-weight: bold;
        }
        
        QScrollBar:horizontal {
            border: none;
            background: #f2f2f2;
            height: 14px;
            margin: 0px 21px 0 21px;
        }
        
        QScrollBar::handle:horizontal {
            background: #b1b1b1;
            min-width: 25px;
        }
        
        QScrollBar::add-line:horizontal {
            border: none;
            background: #f2f2f2;
            width: 20px;
            subcontrol-position: right;
            subcontrol-origin: margin;
        }
        
        QScrollBar::sub-line:horizontal {
            border: none;
            background: #f2f2f2;
            width: 20px;
            subcontrol-position: left;
            subcontrol-origin: margin;
        }
        
        QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal {
            background: none;
        }
        
        QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
            background: none;
        }
        
        QScrollBar:vertical {
            border: none;
            background: #f2f2f2;
            width: 14px;
            margin: 21px 0 21px 0;
        }
        
        QScrollBar::handle:vertical {
            background: #b1b1b1;
            min-height: 25px;
        }
        
        QScrollBar::add-line:vertical {
            border: none;
            background: #f2f2f2;
            height: 20px;
            subcontrol-position: bottom;
            subcontrol-origin: margin;
        }
        
        QScrollBar::sub-line:vertical {
            border: none;
            background: #f2f2f2;
            height: 20px;
            subcontrol-position: top;
            subcontrol-origin: margin;
        }
        
        QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
            background: none;
        }
        
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
            background: none;
        }
        """
        self.setStyleSheet(table_style)

        self.table.setColumnCount(2)  # Set number of columns
        self.table.setHorizontalHeaderLabels(['Team Name', 'Total Earnings'])
        self.table.setSortingEnabled(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)

        self.layout.addWidget(self.table)

        self.setLayout(self.layout)

        self.populate_table()

    def populate_table(self):
        # Fetch earnings data
        data = fetch_costs()
        self.table.setRowCount(len(data))
        for i, (team_name, total_cost) in enumerate(data):
            self.table.setItem(i, 0, QTableWidgetItem(team_name))
            self.table.setItem(i, 1, QTableWidgetItem(f"{total_cost:,.2f} €"))  # Format as currency


class AddPlayerDialog(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Player")
        self.setWindowIcon(QIcon("Images/up_2017_logo_en.ico"))
        self.setWindowTitle("Add New Player")
        self.setWindowIcon(QIcon("Images/up_2017_logo_en.ico"))

        self.layout = QVBoxLayout()

        # Creating form elements
        self.nameEdit = QLineEdit()
        self.ageEdit = QLineEdit()
        self.positionCombo = QComboBox()  # Dropdown for player positions
        self.teamCombo = QComboBox()
        self.addButton = QPushButton("Add Player")
        self.cancelButton = QPushButton("Cancel")

        # Populate the combo box with positions
        self.positionCombo.addItems(["Goalkeeper", "Defender", "Midfielder", "Forward"])

        # Setup layout
        formLayout = QFormLayout()
        formLayout.addRow("Name:", self.nameEdit)
        formLayout.addRow("Age:", self.ageEdit)
        formLayout.addRow("Position:", self.positionCombo)
        formLayout.addRow("Team:", self.teamCombo)
        self.layout.addLayout(formLayout)

        # Buttons layout
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.addButton)
        buttonLayout.addWidget(self.cancelButton)
        self.layout.addLayout(buttonLayout)

        self.addButton.clicked.connect(self.add_player)
        self.cancelButton.clicked.connect(self.hide)

        self.setLayout(self.layout)

        self.populate_teams()

    def populate_teams(self):
        # This function populates the QComboBox with team data
        conn = create_connection()
        if conn is not None:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT id, name FROM teams")
                while True:
                    row = cursor.fetchone()
                    if row is None:
                        break
                    self.teamCombo.addItem(row[1], row[0])
            except mysql.connector.Error as e:
                print(f"Error fetching teams: {e}")
            finally:
                conn.close()

    def add_player(self):
        # This function will add the player to the database
        name = self.nameEdit.text()
        age = self.ageEdit.text()
        position = self.positionCombo.currentText()
        team_id = self.teamCombo.currentData()

        if not name or not age.isdigit() or not position:
            QMessageBox.warning(self, "Invalid Input", "Please enter valid data.")
            return

        conn = create_connection()
        if conn is not None:
            try:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO players (name, age, position, team_id) VALUES (%s, %s, %s, %s)",
                               (name, int(age), position, team_id))
                conn.commit()
                QMessageBox.information(self, "Success", "Player added successfully!")
                # self.accept()  # Close the dialog
            except mysql.connector.Error as e:
                QMessageBox.critical(self, "Error", f"Failed to add player: {e}")
            finally:
                conn.close()


class AddProductsDialog(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add new Product")
        self.setWindowIcon(QIcon("Images/up_2017_logo_en.ico"))

        self.layout = QVBoxLayout()

        # Creating form elements
        self.nameEdit = QLineEdit()
        self.description = QLineEdit()
        self.price = QLineEdit()

        # Validators
        self.priceValidator = QDoubleValidator(0.01, 999999.99, 2)
        self.price.setValidator(self.priceValidator)

        self.addButton = QPushButton("Add Product")
        self.cancelButton = QPushButton("Cancel")

        self.setupUI()

    def setupUI(self):
        # Setup layout
        formLayout = QFormLayout()
        formLayout.addRow("Name:", self.nameEdit)
        formLayout.addRow("Description:", self.description)
        formLayout.addRow("Price:", self.price)
        self.layout.addLayout(formLayout)

        # Buttons layout
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.addButton)
        buttonLayout.addWidget(self.cancelButton)
        self.layout.addLayout(buttonLayout)

        self.addButton.clicked.connect(self.add_product)
        self.cancelButton.clicked.connect(self.hide)

        self.setLayout(self.layout)

    def add_product(self):
        # This function will add the product to the database
        name = self.nameEdit.text().strip()
        description = self.description.text().strip()
        price = self.price.text().strip()

        if not name or not description or not price:
            QMessageBox.warning(self, "Invalid Input", "Please ensure all fields are filled correctly.")
            return

        conn = create_connection()
        if conn is not None:
            try:
                cursor = conn.cursor()
                # Corrected SQL query with proper field names and tuple for data
                cursor.execute("INSERT INTO iot_products (name, description, price) VALUES (%s, %s, %s)",
                               (name, description, float(price)))

                conn.commit()
                QMessageBox.information(self, "Success", "Product added successfully!")
                # Optionally reset the fields or close the dialog if needed
                self.nameEdit.clear()
                self.description.clear()
                self.price.clear()
            except mysql.connector.Error as e:
                QMessageBox.critical(self, "Error", f"Failed to add player: {e}")
            finally:
                conn.close()


class AddTeamDialog(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add New Team")
        self.setWindowIcon(QIcon("Images/up_2017_logo_en.ico"))

        self.playerCount = 0
        self.maxPlayers = 21
        self.totalCost = 0.0

        self.layout = QVBoxLayout()

        self.team_name_label = QLabel("Set a new team name: ")
        self.team_name_edit = QLineEdit()
        self.league_name_label = QLabel("Set the league of the new team: ")
        self.leagueComboBox = QComboBox()

        # Player input form
        self.formLayout = QFormLayout()
        self.nameEdit = QLineEdit()
        self.ageEdit = QLineEdit()
        self.positionCombo = QComboBox()
        self.addPlayerButton = QPushButton("Add Player")

        # Players table
        self.playersTable = QTableWidget(0, 3)

        # Remaining players label
        self.remainingLabel = QLabel(f"Remaining Players to Add: {self.maxPlayers - self.playerCount}")

        # Products Section
        self.product_label = QLabel("Select a product:")
        self.productCombo = QComboBox()
        self.loadProducts()
        self.quantitySpin = QSpinBox()
        self.addProductButton = QPushButton("Add Product")
        self.productsTable = QTableWidget(0, 4)  # Simplified for demonstration

        # Total Cost Label
        self.totalCostLabel = QLabel(f"Total Cost: €{self.totalCost:.2f}")

        # Submit Team
        self.submit_button = QPushButton("Submit Team")

        self.setupUI()

    def loadProducts(self):
        products = fetch_iot_products()
        for product_id, name, price in products:
            self.productCombo.addItem(f"{name} - €{price}", (product_id, price))

    def setupUI(self):
        self.leagueComboBox.addItems(
            ["Premier League", "LaLiga", "Serie A", "Bundesliga", "Ligue 1", "Liga Portugal", "Eredivisie", "Super Lig",
             "Jupiler Pro League", "Premier Liga", "Super League 1"])
        self.ageEdit.setValidator(QIntValidator(16, 45))

        self.positionCombo.addItems(["Goalkeeper", "Defender", "Midfielder", "Forward"])
        self.addPlayerButton.clicked.connect(self.addPlayer)

        self.formLayout.addRow("Player Name:", self.nameEdit)
        self.formLayout.addRow("Player Age:", self.ageEdit)
        self.formLayout.addRow("Player Position:", self.positionCombo)
        self.formLayout.addRow(self.addPlayerButton)

        team_name_layout = QHBoxLayout()
        team_name_layout.addWidget(self.team_name_label)
        team_name_layout.addWidget(self.team_name_edit)

        self.layout.addLayout(team_name_layout)

        league_name_layout = QHBoxLayout()
        league_name_layout.addWidget(self.league_name_label)
        league_name_layout.addWidget(self.leagueComboBox)

        self.layout.addLayout(league_name_layout)

        self.layout.addSpacing(50)
        self.layout.addLayout(self.formLayout)

        # Players Table
        self.playersTable.setHorizontalHeaderLabels(["Name", "Age", "Position"])
        self.layout.addWidget(self.playersTable)
        self.layout.addSpacing(20)
        self.layout.addWidget(self.remainingLabel)
        self.layout.addSpacing(50)

        self.productsTable.setHorizontalHeaderLabels(["ID", "Product", "Quantity", "Price"])
        self.quantitySpin.setMinimum(1)
        self.quantitySpin.setMaximum(100)

        product_label_layout = QHBoxLayout()
        product_label_layout.addWidget(self.product_label)
        product_label_layout.addWidget(self.productCombo)
        self.layout.addLayout(product_label_layout)
        self.layout.addWidget(self.addProductButton)
        self.layout.addWidget(self.productsTable)
        self.layout.addSpacing(100)
        self.layout.addWidget(self.totalCostLabel)
        self.addProductButton.clicked.connect(self.addProduct)

        self.layout.addWidget(self.submit_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.submit_button.clicked.connect(self.submit_team)

        self.setLayout(self.layout)

    def addPlayer(self):
        name = self.nameEdit.text()
        age = self.ageEdit.text()
        position = self.positionCombo.currentText()

        if not name or not age or not position:
            QMessageBox.warning(self, "Incomplete Form", "Please fill out all fields.")
            return

        if self.playerCount >= self.maxPlayers:
            QMessageBox.information(self, "Team Full", "The maximum number of players has been reached.")
            return

        self.playersTable.insertRow(self.playersTable.rowCount())
        self.playersTable.setItem(self.playersTable.rowCount() - 1, 0, QTableWidgetItem(name))
        self.playersTable.setItem(self.playersTable.rowCount() - 1, 1, QTableWidgetItem(age))
        self.playersTable.setItem(self.playersTable.rowCount() - 1, 2, QTableWidgetItem(position))

        self.playerCount += 1
        self.remainingLabel.setText(f"Remaining Players to Add: {self.maxPlayers - self.playerCount}")

        self.nameEdit.clear()
        self.ageEdit.clear()

    def addProduct(self):
        product_data = self.productCombo.currentData()
        product_id = product_data[0]  # Get the product ID
        product_name = self.productCombo.currentText().split(" - ")[0]
        quantity = self.quantitySpin.value()
        product_price = float(product_data[1]) * quantity

        row_count = self.productsTable.rowCount()
        self.productsTable.insertRow(row_count)
        product_id_item = QTableWidgetItem(str(product_id))  # Create item for product ID
        product_name_item = QTableWidgetItem(product_name)
        quantity_item = QTableWidgetItem(str(quantity))
        product_price_item = QTableWidgetItem(f"€{product_price:.2f}")

        # Center align the text
        product_id_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        product_name_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        quantity_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        product_price_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

        self.productsTable.setItem(row_count, 0, product_id_item)  # Set product ID in the first column
        self.productsTable.setItem(row_count, 1, product_name_item)  # Ensure correct column index for product name
        self.productsTable.setItem(row_count, 2, quantity_item)
        self.productsTable.setItem(row_count, 3, product_price_item)  # Ensure correct column index for price

        self.totalCost += product_price
        self.totalCostLabel.setText(f"Total Cost: €{self.totalCost:.2f}")

    def submit_team(self):
        team_name = self.team_name_edit.text()
        league = self.leagueComboBox.currentText()
        if not team_name:
            QMessageBox.warning(self, "Error", "Please enter a team name.")
            return
        if self.playersTable.rowCount() < 21:
            QMessageBox.warning(self, "Error", "At least 21 players must be added.")
            return
        if self.productsTable.rowCount() < 1:
            QMessageBox.warning(self, "Error", "At least one product must be added.")
            return

        # Insert team, players, and products into the database
        self.insert_team(team_name, league)

    def insert_team(self, team_name, league):
        conn = create_connection()
        if not conn:
            QMessageBox.critical(self, "Database Error", "Failed to connect to the database.")
            return
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO teams (name, league) VALUES (%s, %s)", (team_name, league))
            team_id = cursor.lastrowid

            for row in range(self.playersTable.rowCount()):
                name = self.playersTable.item(row, 0).text()
                age = self.playersTable.item(row, 1).text()
                position = self.playersTable.item(row, 2).text()
                cursor.execute("INSERT INTO players (name, age, position, team_id) VALUES (%s, %s, %s, %s)",
                               (name, age, position, team_id))

            for row in range(self.productsTable.rowCount()):
                product_id = self.productsTable.item(row, 0).text()  # Now fetching the text directly which is the product ID
                quantity = int(self.productsTable.item(row, 2).text())  # Adjust column index for quantity
                cursor.execute("INSERT INTO team_products (team_id, product_id, quantity) VALUES (%s, %s, %s)",
                               (team_id, product_id, quantity))

            conn.commit()
            QMessageBox.information(self, "Success", "Team successfully added.")
            self.reset_UI()

        except mysql.connector.Error as error:
            QMessageBox.critical(self, "SQL Error", f"Failed to insert team: {error}")
        finally:
            conn.close()

    def reset_UI(self):
        # Reset all widgets when the dialog is closed
        self.totalCost = 0.0
        self.playerCount = 0
        self.clearTables()
        self.resetLabels()
        self.team_name_edit.clear()
        self.leagueComboBox.setCurrentIndex(0)
        self.totalCostLabel.setText("Total Cost: €0.00")

    def closeEvent(self, event):
        # Reset all widgets when the dialog is closed
        self.totalCost = 0.0
        self.playerCount = 0
        self.clearTables()
        self.resetLabels()
        self.team_name_edit.clear()
        self.leagueComboBox.setCurrentIndex(0)
        self.totalCostLabel.setText("Total Cost: €0.00")
        event.accept()

    def clearTables(self):
        self.playersTable.setRowCount(0)
        self.productsTable.setRowCount(0)

    def resetLabels(self):
        self.remainingLabel.setText(f"Remaining Players to Add: {self.maxPlayers - self.playerCount}")
        self.totalCostLabel.setText("Total Cost: €0.00")
        self.playerCount = 0


class ManagePlayersDialog(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.dialog = AddPlayerDialog()
        self.setWindowTitle("Manage Players")
        self.setWindowIcon(QIcon("Images/up_2017_logo_en.ico"))
        self.layout = QVBoxLayout()

        # Create QTableWidget
        self.table = QTableWidget()

        # Add buttons
        self.addButton = QPushButton("Add Player")
        self.updateButton = QPushButton("Update Player")

        # Form fields
        self.nameEdit = QLineEdit()
        self.ageEdit = QLineEdit()
        self.positionEdit = QLineEdit()
        self.teamCombo = QComboBox()

        self.setupUI()

    def setupUI(self):
        self.updateButton.setEnabled(False)  # Initially disabled
        button_style = """
                        QPushButton {
                            background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, 
                                                              stop:0 rgba(105, 181, 255, 255), 
                                                              stop:1 rgba(65, 131, 215, 255));
                            color: white;
                            border-radius: 10px;
                            padding: 10px;
                            font-size: 16px;
                            font-weight: bold;
                        }
                        QPushButton::hover {
                            background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, 
                                                              stop:0 rgba(65, 131, 215, 255), 
                                                              stop:1 rgba(25, 81, 165, 255));
                        }
                        QPushButton::pressed {
                            background-color: rgba(25, 81, 165, 255);
                        }
        """
        self.addButton.setStyleSheet(button_style)
        self.updateButton.setStyleSheet(button_style)

        self.addButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.updateButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        # Set up table to show players details
        self.table.setColumnCount(5)  # Adjust based on the number of columns you need
        self.table.setHorizontalHeaderLabels(['ID', 'Name', 'Age', 'Position', 'Team'])
        self.table.verticalHeader().setVisible(False)  # Hide vertical header
        self.table.setSortingEnabled(True)  # Enable sorting by clicking the column header

        # Buttons layout
        buttonsLayout = QHBoxLayout()
        buttonsLayout.addWidget(self.addButton)
        buttonsLayout.addSpacing(50)
        buttonsLayout.addWidget(self.updateButton)

        # Add functions to click
        self.addButton.clicked.connect(self.add_player)
        self.table.itemChanged.connect(self.enableUpdateButton)
        self.updateButton.clicked.connect(self.update_player)

        self.layout.addWidget(self.table)
        self.layout.addLayout(buttonsLayout)
        self.populate_table()

        self.setLayout(self.layout)
        # Populate the combo box with teams
        self.populate_teams()

        self.addButton.clicked.connect(self.add_player)

    def enableUpdateButton(self):
        self.updateButton.setEnabled(True)

    def populate_table(self):
        # Fetch player data
        data = fetch_players()
        self.table.setRowCount(len(data))
        for i, (player_id, name, age, position, team_name) in enumerate(data):
            # Set alignment to center and add each item to the table
            id_item = QTableWidgetItem(str(player_id))
            name_item = QTableWidgetItem(name)
            age_item = QTableWidgetItem(str(age))
            position_item = QTableWidgetItem(position)
            team_item = QTableWidgetItem(team_name)

            # Set alignment to center for each table item
            id_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            name_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            age_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            position_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            team_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            # Set each item to be editable
            name_item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsEditable)
            age_item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsEditable)
            position_item.setFlags(
                Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsEditable)
            team_item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsEditable)

            # Add items to the table
            self.table.setItem(i, 0, id_item)
            self.table.setItem(i, 1, name_item)
            self.table.setItem(i, 2, age_item)
            self.table.setItem(i, 3, position_item)
            self.table.setItem(i, 4, team_item)

    def populate_teams(self):
        # Fetch and add teams to the combo box
        conn = create_connection()
        if conn is not None:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT id, name FROM teams")
                teams = cursor.fetchall()
                for team_id, team_name in teams:
                    self.teamCombo.addItem(team_name, team_id)
            except mysql.connector.Error as e:
                print(f"Error fetching teams: {e}")
            finally:
                conn.close()

    def update_player(self):
        for row in range(self.table.rowCount()):
            id_ = self.table.item(row, 0).text()
            name = self.table.item(row, 1).text()
            age = self.table.item(row, 2).text()
            position = self.table.item(row, 3).text()
            team_name = self.table.item(row, 4).text()

            conn = create_connection()
            if conn is not None:
                try:
                    cursor = conn.cursor()
                    cursor.execute(
                        "UPDATE players SET name = %s, age = %s, position = %s WHERE id = %s",
                        (name, age, position, id_)
                    )
                    conn.commit()
                except mysql.connector.Error as e:
                    QMessageBox.critical(self, "Database Error", str(e))
                finally:
                    conn.close()
        QMessageBox.information(self, "Update Successful", "Player data updated successfully!")
        self.updateButton.setEnabled(False)  # Disable button after update

    def add_player(self):
        self.dialog.show()


class ManageTeamsDialog(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Manage Teams")
        self.setWindowIcon(QIcon("Images/up_2017_logo_en.ico"))
        self.layout = QVBoxLayout()

        self.table = QTableWidget()
        self.setupUI()

    def setupUI(self):
        self.table.setColumnCount(3)  # For ID, Name, and League
        self.table.setHorizontalHeaderLabels(['ID', 'Name', 'League'])
        self.table.verticalHeader().setVisible(False)
        self.table.setSortingEnabled(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)

        self.layout.addWidget(self.table)
        self.setLayout(self.layout)

        self.populate_table()

    def populate_table(self):
        # Fetch team data
        conn = create_connection()
        if conn is not None:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT id, name, league FROM teams")
                data = cursor.fetchall()
                self.table.setRowCount(len(data))
                for i, (team_id, name, league) in enumerate(data):
                    id_item = QTableWidgetItem(str(team_id))
                    name_item = QTableWidgetItem(name)
                    league_item = QTableWidgetItem(league if league else "N/A")

                    # Set alignment to center
                    id_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    name_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    league_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

                    self.table.setItem(i, 0, id_item)
                    self.table.setItem(i, 1, name_item)
                    self.table.setItem(i, 2, league_item)

            except mysql.connector.Error as e:
                QMessageBox.critical(self, "Database Error", str(e))
            finally:
                conn.close()


class ManageProductsDialog(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.dialog = AddProductsDialog()
        self.setWindowTitle("Manage IoT Products")
        self.setWindowIcon(QIcon("Images/up_2017_logo_en.ico"))
        self.layout = QVBoxLayout()

        # Create QTableWidget for products
        self.table = QTableWidget()

        # Add buttons
        self.addButton = QPushButton("Add Product")
        self.updateButton = QPushButton("Update Product")

        self.setupUI()

    def setupUI(self):
        self.updateButton.setEnabled(False)  # Initially disabled, enabled only when a change is made
        button_style = """
                        QPushButton {
                            background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, 
                                                              stop:0 rgba(105, 181, 255, 255), 
                                                              stop:1 rgba(65, 131, 215, 255));
                            color: white;
                            border-radius: 10px;
                            padding: 10px;
                            font-size: 16px;
                            font-weight: bold;
                        }
                        QPushButton::hover {
                            background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, 
                                                              stop:0 rgba(65, 131, 215, 255), 
                                                              stop:1 rgba(25, 81, 165, 255));
                        }
                        QPushButton::pressed {
                            background-color: rgba(25, 81, 165, 255);
                        }
        """
        self.addButton.setStyleSheet(button_style)
        self.updateButton.setStyleSheet(button_style)

        self.addButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.updateButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        # Set up table to show product details
        self.table.setColumnCount(4)  # Number of columns for id, name, description, and price
        self.table.setHorizontalHeaderLabels(['ID', 'Name', 'Description', 'Price'])
        self.table.verticalHeader().setVisible(False)  # Hide vertical header
        self.table.setSortingEnabled(True)  # Enable sorting

        # Button styling and layout
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.addButton)
        buttonLayout.addSpacing(50)
        buttonLayout.addWidget(self.updateButton)

        # Add functions to click
        self.addButton.clicked.connect(self.add_product_dialog)
        self.updateButton.clicked.connect(self.update_product)
        self.table.itemChanged.connect(self.enableUpdateButton)

        self.layout.addWidget(self.table)
        self.layout.addLayout(buttonLayout)

        self.setLayout(self.layout)
        self.populate_table()

    def populate_table(self):
        # Fetch IoT products data
        conn = create_connection()
        if conn is not None:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT id, name, description, price FROM iot_products")
                data = cursor.fetchall()
                self.table.setRowCount(len(data))
                for i, (product_id, name, description, price) in enumerate(data):
                    items = [
                        QTableWidgetItem(str(product_id)),
                        QTableWidgetItem(name),
                        QTableWidgetItem(description if description else "No Description"),
                        QTableWidgetItem(f"{price:.2f} €")
                    ]
                    # Set each item to be non-editable but center-aligned
                    for item in items:
                        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                        item.setFlags(
                            Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsEditable)
                    self.table.setItem(i, 0, items[0])
                    self.table.setItem(i, 1, items[1])
                    self.table.setItem(i, 2, items[2])
                    self.table.setItem(i, 3, items[3])
            except mysql.connector.Error as e:
                QMessageBox.critical(self, "Database Error", str(e))
            finally:
                conn.close()

    def add_product_dialog(self):
        self.dialog.show()

    def update_product(self):
        conn = create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                for i in range(self.table.rowCount()):
                    product_id = self.table.item(i, 0).text()
                    name = self.table.item(i, 1).text()
                    description = self.table.item(i, 2).text()
                    price = float(self.table.item(i, 3).text().replace(' €', ''))  # Remove currency formatting
                    cursor.execute("UPDATE iot_products SET name = %s, description = %s, price = %s WHERE id = %s",
                                   (name, description, price, product_id))
                conn.commit()
                QMessageBox.information(self, "Success", "Products updated successfully!")
            except mysql.connector.Error as e:
                QMessageBox.critical(self, "Error", f"Failed to update products: {e}")
            finally:
                conn.close()
                self.updateButton.setEnabled(False)  # Disable button after update

    def enableUpdateButton(self):
        self.updateButton.setEnabled(True)


class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Set Main Window Title
        self.setWindowTitle('Augerinos Thesis')

        self.UPatras_icon = QIcon("Images/up_2017_logo_en.ico")
        self.setWindowIcon(self.UPatras_icon)
        self.setMinimumSize(800, 600)  # Set the minimum size to prevent resizing below one value

        # Layout
        self.layout = QVBoxLayout()
        self.main_widget = QWidget()

        self.UPatras_logo_png = QPixmap("Images/up_2017_logo_en_resized.png")
        self.UPatras_logo = QLabel()

        # Summary Widgets
        self.players_label = QLabel("Total Players:")
        self.teams_label = QLabel("Total Teams:")
        self.products_label = QLabel("IoT Products Registered:")
        self.players_count = QLabel()
        self.teams_count = QLabel()
        self.products_count = QLabel()

        # Quick Access Buttons
        self.btn_manage_players = QPushButton("Manage Players")
        self.btn_manage_teams = QPushButton("Manage Teams")
        self.btn_manage_products = QPushButton("Manage IoT Products")

        # Calculate Earning and add teams button
        self.btn_add_team = QPushButton("Add Team")
        self.btn_calculate_earnings = QPushButton("Calculate Earnings")

        # Calculate Earnings of each Team
        self.dialog = EarningsDialog()
        self.manage_players_dialog = ManagePlayersDialog()
        self.manage_teams_dialog = ManageTeamsDialog()
        self.manage_products_dialog = ManageProductsDialog()
        self.add_team_dialog = AddTeamDialog()

        # SetupUI
        self.setupUI()

    def setupUI(self):
        # Button Styling
        button_style = """
                        QPushButton {
                            background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, 
                                                              stop:0 rgba(105, 181, 255, 255), 
                                                              stop:1 rgba(65, 131, 215, 255));
                            color: white;
                            border-radius: 10px;
                            padding: 10px;
                            font-size: 16px;
                            font-weight: bold;
                        }
                        QPushButton::hover {
                            background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, 
                                                              stop:0 rgba(65, 131, 215, 255), 
                                                              stop:1 rgba(25, 81, 165, 255));
                        }
                        QPushButton::pressed {
                            background-color: rgba(25, 81, 165, 255);
                        }
                        """
        label_style = """
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #333;
                padding: 8px;
                text-shadow: 1px 1px 0px white;
            }
        """
        # Set style
        self.btn_manage_players.setStyleSheet(button_style)
        self.btn_manage_teams.setStyleSheet(button_style)
        self.btn_manage_products.setStyleSheet(button_style)
        self.btn_calculate_earnings.setStyleSheet(button_style)
        self.btn_add_team.setStyleSheet(button_style)
        self.players_label.setStyleSheet(label_style)
        self.teams_label.setStyleSheet(label_style)
        self.products_label.setStyleSheet(label_style)
        self.players_count.setStyleSheet(label_style)
        self.teams_count.setStyleSheet(label_style)
        self.products_count.setStyleSheet(label_style)

        # Set Cursor while hover over buttons
        self.btn_manage_players.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_manage_teams.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_manage_products.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_calculate_earnings.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_add_team.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        # Update labels
        self.players_count.setText(str(get_table_count('players')))
        self.teams_count.setText(str(get_table_count('teams')))
        self.products_count.setText(str(get_table_count('iot_products')))

        # Button function
        self.btn_manage_players.clicked.connect(self.show_manage_players_dialog)
        self.btn_manage_teams.clicked.connect(self.show_manage_teams_dialog)
        self.btn_manage_products.clicked.connect(self.show_manage_products_dialog)
        self.btn_calculate_earnings.clicked.connect(self.show_earnings_dialog)
        self.btn_add_team.clicked.connect(self.show_add_team_dialog)
        # End of button functions

        # Layout
        players_layout = QHBoxLayout()
        teams_layout = QHBoxLayout()
        products_layout = QHBoxLayout()
        button_footer = QHBoxLayout()

        players_layout.addWidget(self.players_label, alignment=Qt.AlignmentFlag.AlignLeft)
        players_layout.addWidget(self.players_count, alignment=Qt.AlignmentFlag.AlignCenter)
        players_layout.addWidget(self.btn_manage_players, alignment=Qt.AlignmentFlag.AlignCenter)

        teams_layout.addWidget(self.teams_label, alignment=Qt.AlignmentFlag.AlignLeft)
        teams_layout.addWidget(self.teams_count, alignment=Qt.AlignmentFlag.AlignCenter)
        teams_layout.addWidget(self.btn_manage_teams, alignment=Qt.AlignmentFlag.AlignCenter)

        products_layout.addWidget(self.products_label, alignment=Qt.AlignmentFlag.AlignLeft)
        products_layout.addWidget(self.products_count, alignment=Qt.AlignmentFlag.AlignCenter)
        products_layout.addWidget(self.btn_manage_products, alignment=Qt.AlignmentFlag.AlignCenter)

        button_footer.addWidget(self.btn_calculate_earnings, alignment=Qt.AlignmentFlag.AlignCenter)
        button_footer.addWidget(self.btn_add_team, alignment=Qt.AlignmentFlag.AlignCenter)

        self.UPatras_logo.setPixmap(self.UPatras_logo_png)
        self.layout.addWidget(self.UPatras_logo, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.layout.addLayout(players_layout)
        self.layout.addLayout(teams_layout)
        self.layout.addLayout(products_layout)
        self.layout.addLayout(button_footer)

        # Set the central widget of the Window.
        self.main_widget.setLayout(self.layout)
        self.setCentralWidget(self.main_widget)

    def show_earnings_dialog(self):
        self.dialog.show()

    def show_add_team_dialog(self):
        self.add_team_dialog.show()

    def show_manage_players_dialog(self):
        self.manage_players_dialog.show()

    def show_manage_teams_dialog(self):
        self.manage_teams_dialog.show()

    def show_manage_products_dialog(self):
        self.manage_products_dialog.show()
