## Drone Classification Web App

1. **Install all required dependencies:**
   `pip install -r requirements.txt`
2. **Navigate to the web application folder:**
   `cd webapp`
3. **Run the initial database migrations** (only needed once):
   `python manage.py migrate`

## Running the Web Server

Whenever you want to test the app locally, run:
`python manage.py runserver`

Then open your browser and go to: **http://127.0.0.1:8000/**

## Updating webapp

When testing another version of the drone detection model, follow these steps to update the web app:

1. **Replace the Model File:** Drop the new `.pt` file into the root directory of this project.
2. **Update the Target File:** Open `webapp/detector/web_inference.py` and update the `MODEL_PATH` variable to match the exact name of your new file.
   ```python
   # Change 'yolov8n.pt' to new model name
   MODEL_PATH = os.path.join(PROJECT_ROOT, 'new_drone_model.pt')
The html is located in `detector\templates\detector` if people want to change that as well.

## Testing
Not really formatting this for now but to access the database behind the scene go to http://127.0.0.1:8000/admin/
The user and password are admin.
Depending on your webcam, you might have to change the number of the camera variable in the generate frames function in web_inference.py to either a different number or a ip + port in this format "192.168.X.X:XXXX"