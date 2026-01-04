import joblib
import pandas as pd

# Load the model
model = joblib.load('promotion_model.pkl')

# Try to inspect the pipeline
print('Model type:', type(model))
print('Model steps:', model.steps if hasattr(model, 'steps') else 'No steps attribute')

# If it's a pipeline, inspect each step
if hasattr(model, 'steps'):
    for i, (name, step) in enumerate(model.steps):
        print(f'Step {i}: {name} - {type(step)}')
        if hasattr(step, 'categories_'):
            print(f'  Categories: {step.categories_}')
        elif hasattr(step, 'feature_names_in_'):
            print(f'  Feature names: {step.feature_names_in_}')