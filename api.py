import joblib
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd

app = FastAPI(
    title="Employee Promotion Prediction API",
    description="API for predicting employee promotion based on various features.",
    version="1.0.0",
)

model = None
preprocessor_categories = {}

@app.on_event("startup")
async def load_model():
    global model, preprocessor_categories
    try:
        model = joblib.load('promotion_model.pkl')
        print("Model loaded successfully during startup.")

        # Extract categories from the preprocessor
        if hasattr(model, 'named_steps'):
            preprocessor = model.named_steps.get('prepocess')  # Note: there's a typo in 'prepocess'
            print(f"Preprocessor type: {type(preprocessor)}")

        # Extract categories from the preprocessor
        if hasattr(model, 'named_steps'):
            preprocessor = model.named_steps.get('prepocess')  # Note: there's a typo in 'prepocess'
            print(f"Preprocessor type: {type(preprocessor)}")

            if preprocessor and hasattr(preprocessor, 'transformers_'):
                print(f"Found {len(preprocessor.transformers_)} transformers")
                for name, transformer, columns in preprocessor.transformers_:
                    print(f"Transformer: {name}, Type: {type(transformer)}, Columns: {list(columns)}")
                    if name == 'cat' and hasattr(transformer, 'steps'):  # Categorical pipeline
                        print("  Categorical pipeline steps:")
                        for step_name, step in transformer.steps:
                            print(f"    Step: {step_name}, Type: {type(step)}")
                            if hasattr(step, 'categories_'):
                                print(f"    Found OneHotEncoder with {len(step.categories_)} feature categories")
                                for i, cats in enumerate(step.categories_):
                                    if i < len(columns):
                                        col_name = columns[i]
                                        preprocessor_categories[col_name] = list(cats)
                                        print(f"      Column '{col_name}': {list(cats)[:3]}..." if len(cats) > 3 else f"      Column '{col_name}': {list(cats)}")
                    elif hasattr(transformer, 'categories_'):
                        print(f"  Has categories_: {len(transformer.categories_)} feature categories")
                        for i, cats in enumerate(transformer.categories_):
                            if i < len(columns):
                                col_name = columns[i]
                                preprocessor_categories[col_name] = list(cats)
                                print(f"    Column '{col_name}': {list(cats)[:3]}..." if len(cats) > 3 else f"    Column '{col_name}': {list(cats)}")

        print(f"Extracted categories for {len(preprocessor_categories)} columns")

    except FileNotFoundError:
        print("Error: promotion_model.pkl not found. Make sure it's in the same directory.")
    except Exception as e:
        print(f"Error loading model: {e}")
        import traceback
        traceback.print_exc()


class EmployeeData(BaseModel):
    department: str
    region: str
    education: str
    gender: str
    recruitment_channel: str
    no_of_trainings: int
    age: int
    previous_year_rating: float
    length_of_service: int
    KPIs_met_80_percent: int
    awards_won: int
    avg_training_score: int

    model_config = {
        "json_schema_extra": {
            "example": {
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
        }
    }


@app.get("/")
async def read_root():
    return {"message": "Welcome to the Employee Promotion Prediction API! Use /predict for predictions."}


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    if model is None:
        return {"status": "unhealthy", "message": "Model not loaded"}
    return {"status": "healthy", "message": "Service is running"}


@app.post("/predict")
async def predict_promotion(data: EmployeeData):
    input_dict = data.dict()

    # Rename keys to match original DataFrame column names
    input_dict['KPIs_met >80%'] = input_dict.pop('KPIs_met_80_percent')
    input_dict['awards_won?'] = input_dict.pop('awards_won')

    # Handle unknown categories by mapping to known ones
    for col, categories in preprocessor_categories.items():
        if col in input_dict and input_dict[col] not in categories:
            # Use the first category as fallback (most common approach)
            input_dict[col] = categories[0]
            print(f"Warning: Unknown category '{input_dict[col]}' in column '{col}', using '{categories[0]}' instead")

    input_df = pd.DataFrame([input_dict])

    if model is None:
        return {"error": "Model not loaded. Please check server logs."}

    try:
        prediction = model.predict(input_df)
        probability = model.predict_proba(input_df)[:, 1]

        return {
            "promotion_prediction": int(prediction[0]),
            "promotion_probability": float(probability[0])
        }
    except Exception as e:
        return {
            "error": "Prediction failed.",
            "details": str(e)
        }