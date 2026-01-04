# Build the Docker image
docker build -t employee-promotion-api .

# Tag for Google Container Registry (replace with your project ID)
# docker tag employee-promotion-api gcr.io/YOUR_PROJECT_ID/employee-promotion-api

# Push to Google Container Registry
# docker push gcr.io/YOUR_PROJECT_ID/employee-promotion-api

# Deploy to Cloud Run
# gcloud run deploy employee-promotion-api \
#   --image gcr.io/YOUR_PROJECT_ID/employee-promotion-api \
#   --platform managed \
#   --region us-central1 \
#   --allow-unauthenticated \
#   --port 8080 \
#   --memory 1Gi \
#   --cpu 1