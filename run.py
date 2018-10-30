import os
from app import app, service, create_db

# Pull options from environment
DEBUG = (os.getenv('DEBUG', 'False') == 'True')
PORT = os.getenv('PORT', '5000')

if __name__ == "__main__":
    print("**********************************************")
    print(" P R O D U C T   S E R V I C E   R U N N I N G")
    print("**********************************************")
    service.initialize_logging()
    service.init_db()
    create_db.dbcreate()
    app.run(host='0.0.0.0', port=int(PORT), debug=DEBUG)