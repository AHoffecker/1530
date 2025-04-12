## 🧪 Local Setup Instructions

### 📦 1. Clone the Repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

## 🐍 2. Create and Activate a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
.\venv\Scripts\activate         # Windows
```
## 📥 3. Install Dependencies
```bash
pip install -r requirements.txt
```
## 🔐 4. Create a .env File
In the root of the project, create a file named .env and add the following:
```ini
FLASK_APP=app.py
FLASK_ENV=development
GOOGLE_MAPS_API_KEY=your_real_api_key_here
```
## ▶️ 5. Run the App
```bash
flask run
Then open your browser and go to:
```
http://localhost:5000

