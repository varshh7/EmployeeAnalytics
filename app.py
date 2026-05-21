import os
import oracledb
from dotenv import load_dotenv

# Load credentials from the .env file
load_dotenv()

class EmployeeAnalytics:
    def __init__(self):
        """Initialize database credentials from environment variables."""
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.dsn = os.getenv("DB_DSN")

    def get_connection(self):
        """Establish and return a connection to the Oracle Database."""
        try:
            return oracledb.connect(
                user=self.user,
                password=self.password,
                dsn=self.dsn
            )
        except oracledb.Error as e:
            print(f"Connection Error: {e}")
            return None

    def fetch_all_employees(self):
        """Task 1: Fetch All Employees"""
        query = """
            SELECT employee_id, first_name, last_name, salary 
            FROM SYSTEM.employees 
            ORDER BY employee_id
        """
        self._execute_query("--- ALL EMPLOYEES ---", query)

    def filter_by_salary(self, min_salary):
        """Task 2: Salary-Based Employee Filter"""
        query = """
            SELECT employee_id, first_name, last_name, salary 
            FROM SYSTEM.employees 
            WHERE salary >= :min_sal 
            ORDER BY salary DESC
        """
        self._execute_query(f"--- EMPLOYEES EARNING >= ${min_salary} ---", query, {"min_sal": min_salary})

    def department_summary(self):
        """Task 3: Department Summary Report"""
        query = """
            SELECT d.department_name, 
                   COUNT(e.employee_id) as headcount, 
                   ROUND(AVG(e.salary), 2) as avg_salary
            FROM departments d
            LEFT JOIN SYSTEM.employees e ON d.department_id = e.department_id
            GROUP BY d.department_name
            ORDER BY avg_salary DESC
        """
        self._execute_query("--- DEPARTMENT SUMMARY REPORT ---", query)

    def recent_hires(self, days_ago):
        """Task 4: Recent Hires Report"""
        query = """
            SELECT first_name, last_name, hire_date, department_id 
            FROM SYSTEM.employees 
            WHERE hire_date >= SYSDATE - :days 
            ORDER BY hire_date DESC
        """
        self._execute_query(f"--- RECENT HIRES (LAST {days_ago} DAYS) ---", query, {"days": days_ago})

    def _execute_query(self, title, query, params=None):
        """Helper method to execute SQL queries and format the output."""
        conn = self.get_connection()
        if not conn:
            return

        try:
            with conn.cursor() as cursor:
                # Execute the query with optional bind variables
                cursor.execute(query, params or {})
                
                # Fetch column names for the header
                columns = [col[0] for col in cursor.description]
                results = cursor.fetchall()

                # Print formatted results
                print(f"\n{title}")
                print("-" * 50)
                print(" | ".join(columns))
                print("-" * 50)
                
                if not results:
                    print("No records found.")
                else:
                    for row in results:
                        print(" | ".join(str(val) if val is not None else "NULL" for val in row))
                        
        except oracledb.Error as e:
            print(f"Database Error: {e}")
            print("Note: If you are logged in as SYSTEM/ADMIN, you may need to add 'hr.' before your table names (e.g., hr.employees).")
        finally:
            conn.close()

# --- Interactive Application Flow ---
if __name__ == "__main__":
    app = EmployeeAnalytics()
    
    print("Welcome to the Employee Analytics System")
    
    while True:
        print("\nSelect an option:")
        print("1. Fetch All Employees")
        print("2. Filter Employees by Salary")
        print("3. View Department Summary Report")
        print("4. View Recent Hires Report")
        print("5. Exit")
        
        choice = input("Enter your choice (1-5): ")
        
        if choice == '1':
            app.fetch_all_employees()
        elif choice == '2':
            try:
                min_sal = float(input("Enter minimum salary: "))
                app.filter_by_salary(min_sal)
            except ValueError:
                print("Please enter a valid number.")
        elif choice == '3':
            app.department_summary()
        elif choice == '4':
            try:
                days = int(input("Enter number of days to look back (e.g., 30, 365): "))
                app.recent_hires(days)
            except ValueError:
                print("Please enter a valid whole number.")
        elif choice == '5':
            print("Exiting application. Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1-5.")