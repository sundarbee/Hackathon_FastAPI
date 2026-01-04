# Employee Promotion Prediction API

A FastAPI application for predicting employee promotions based on various features using a trained XGBoost model.

## Features

- RESTful API for employee promotion prediction
- Input validation using Pydantic
- Automatic handling of unknown categories
- Docker containerization for easy deployment
- Optimized for Google Cloud Run

## API Endpoints

### GET /
Returns a welcome message.

### POST /predict
Predicts employee promotion probability.

**Request Body:**
```json
{
  "department": "Sales & Marketing",
  "region": "region_7",
  "education": "Master's & above",
  "gender": "f",
  "recruitment_channel": "sourcing",
  "no_of_trainings": 1,
  "age": 35,
  "previous_year_rating": 5.0,
  "length_of_service": 8,
  "KPIs_met_80_percent": 1,
  "awards_won": 0,
  "avg_training_score": 49
}
```

**Response:**
```json
{
  "promotion_prediction": 1,
  "promotion_probability": 0.85
}
```

## Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
uvicorn api:app --reload
```

3. Open http://127.0.0.1:8000/docs for interactive API documentation.

## Docker Deployment

### Build and Run Locally
```bash
# Build the image
docker build -t employee-promotion-api .

# Run locally
docker run -p 8080:8080 employee-promotion-api
```

### Deploy to Google Cloud Run

1. **Enable required APIs:**
```bash
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

2. **Build and push to Google Container Registry:**
```bash
# Set your project ID
PROJECT_ID=your-project-id

# Build the image
docker build -t employee-promotion-api .

# Tag for GCR
docker tag employee-promotion-api gcr.io/$PROJECT_ID/employee-promotion-api

# Push to GCR
docker push gcr.io/$PROJECT_ID/employee-promotion-api
```

3. **Deploy to Cloud Run:**
```bash
gcloud run deploy employee-promotion-api \
  --image gcr.io/$PROJECT_ID/employee-promotion-api \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8080 \
  --memory 1Gi \
  --cpu 1 \
  --max-instances 10
```

4. **Get the service URL:**
```bash
gcloud run services describe employee-promotion-api --region=us-central1 --format="value(status.url)"
```

## Environment Variables

- `PORT`: Port for the application (automatically set by Cloud Run, defaults to 8080)

## Model Information

- **Algorithm**: XGBoost Classifier
- **Features**: Department, region, education, gender, recruitment channel, training metrics, performance ratings
- **Output**: Binary classification (0/1) with probability score

## Dependencies

- fastapi==0.128.0
- uvicorn==0.40.0
- pydantic==2.12.5
- pandas==2.3.3
- joblib==1.5.3
- scikit-learn==1.6.1
- xgboost==2.1.4

## Error Handling

The API includes robust error handling for:
- Unknown categorical values (automatically mapped to known categories)
- Model loading failures
- Invalid input data
- Prediction errors

## Health Check

The API includes automatic health checks through FastAPI's startup event that validates model loading.