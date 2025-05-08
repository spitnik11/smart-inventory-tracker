import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def predict_stockouts(df):
    prompt = (
        "Given the following inventory data:\n"
        f"{df.to_csv(index=False)}\n"
        "Which items are likely to stock out next month? Provide the SKU and reason."
    )
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an inventory management assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message['content']
    except Exception as e:
        return f"An error occurred: {e}"
