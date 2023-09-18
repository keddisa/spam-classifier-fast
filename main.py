import boto3
import torch
import tempfile
from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoTokenizer
from src.model import SpamClassifier


app = FastAPI()
s3 = boto3.client('s3')


BUCKET_NAME = "spam-classifier-ml-model"
MODEL_FILE_NAME = "spam_classifier.pt"
TOKENIZER_PATH = 'bert-base-multilingual-uncased'

class ClassifyBody(BaseModel):
    comments: list[str]

def load_model(bucket, model_file):
    print("loading model")
    tmp = tempfile.NamedTemporaryFile(delete=False)
    print(tmp.name)
    s3.download_file(bucket, model_file, tmp.name)
    print("2")
    # Initialize the model architecture
    n_classes = 2
    model_arch = SpamClassifier(n_classes)
    
    # Load the state dictionary into the model architecture
    state_dict = torch.load(tmp.name)
    model_arch.load_state_dict(state_dict)
    
    # Make sure the model is in evaluation mode and return it
    model = model_arch.eval()
    print("3")
    
    return model

tokenizer = AutoTokenizer.from_pretrained(TOKENIZER_PATH)
model = load_model(BUCKET_NAME, MODEL_FILE_NAME)

@app.get("/health", tags=["health"])  # enum
def health_check():
    return {"message": "OK"}


@app.post("/classify", summary="Classify a list of comments", response_description="An array of spam classification")
def classify_comments(body: ClassifyBody):
    comments = body.comments

    results = []
    for comment in comments:
        #print comment
        print(comment)
        inputs = tokenizer(comment, return_tensors='pt')
        print("inputs")
        outputs = model(**inputs)
        print("outputs")
        # print('outputs', outputs)
        _, prediction = torch.max(outputs, dim=1)
        print(prediction.item())
        results.append(prediction.item())
    return {
        "classifications": results
    }