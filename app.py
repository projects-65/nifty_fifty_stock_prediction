from flask import Flask, request, render_template
import joblib
from datetime import datetime

app = Flask(__name__)

# Load the pre-trained ARIMA model
model = joblib.load("C:\\Users\\User\\Downloads\\nifty\\nifty\\final_arima_model.pkl")

# Function to calculate steps to forecast
def calculate_steps_to_forecast(last_date, forecast_date):
    last_date = datetime.strptime(last_date, '%Y-%m')
    forecast_date = datetime.strptime(forecast_date, '%Y-%b')
    return (forecast_date.year - last_date.year) * 12 + forecast_date.month - last_date.month

# Function to make forecast
def make_forecast(model, steps_to_forecast):
    if steps_to_forecast <= 0:
        return None, "Error: Please enter a future date."
    forecast = model.get_forecast(steps=steps_to_forecast)
    return forecast.predicted_mean[-1], None

@app.route('/', methods=['GET', 'POST'])
def index():
    forecast_value = None
    month_name = None
    year = None
    error = None
    if request.method == 'POST':
        year = request.form.get('year')
        month = request.form.get('month')
        month_name = datetime.strptime(month, "%m").strftime("%b")  # For displaying the month name in the result
        steps_to_forecast = calculate_steps_to_forecast('2023-12', f'{year}-{month_name}')
        print(steps_to_forecast)
        
        # Debug: print or log the steps to forecast to check if they are correct
        print(f'Steps to forecast: {steps_to_forecast}')  # Remove or comment out this line in production

        forecast_value, error = make_forecast(model, steps_to_forecast)
        
    # Pass all the variables back to index.html
    return render_template('index.html', forecast_value=forecast_value, month_name=month_name, year=year, error=error)


if __name__ == '__main__':
    app.run(debug=True)
