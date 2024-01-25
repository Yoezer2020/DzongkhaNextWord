# views.py


from django.shortcuts import render
from .models import UserInput
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
import pandas as pd
from django.http import JsonResponse
import re
import pickle
from django.shortcuts import redirect
from django.http import JsonResponse


#to delete the recent predictions
def delete_prediction(request, prediction_id):
    prediction = UserInput.objects.get(id=prediction_id)
    prediction.delete()
    return redirect('predict')


# Load the saved model
model_path = r"dzo_nextword\model_tokenizer_dataset\Final_GruModel.h5"
model = load_model(model_path)

# Load the tokenizer
tokenizer_path = r"dzo_nextword\model_tokenizer_dataset\tokenizer.pkl"  # Update with the actual path
with open(tokenizer_path, 'rb') as tokenizer_file:
    tokenizer = pickle.load(tokenizer_file)

def predict_next_word(seed_text, top_n):
    token_list = tokenizer.texts_to_sequences([seed_text])[0]
    
    # Ensure that the token list has a length greater than 0
    if len(token_list) == 0:
        return []

    max_sequence_len = len(token_list)

    # Pad the token list to match the model's input length
    token_list = pad_sequences([token_list], maxlen=max_sequence_len, padding='pre')

    # Predict the next word probabilities
    predicted_probs = model.predict(token_list)

    # Get the top N predictions
    top_indices = predicted_probs[0].argsort()[-top_n:][::-1]

    # Create a list of words corresponding to the top indices
    top_words = [word for word, index in tokenizer.word_index.items() if index in top_indices]

    return top_words

def home(request):
    return render(request, 'home.html',)

def aboutus(request):
    return render(request, 'aboutus.html',)

def predict(request):
    if request.method == 'POST':
        seed_text = request.POST.get('seed_text', '')
        if seed_text[-1] == "་":
            seed_text = seed_text[:-1]

        top_n = int(request.POST.get('top_n', 1))

        # Perform prediction
        predictions = predict_next_word(seed_text, top_n)

        # Save user input and prediction
        UserInput.objects.create(seed_text=seed_text, top_n=top_n, prediction=', '.join(predictions))

        # Return predictions as JSON
        return JsonResponse({'predictions': predictions})

    user_inputs = UserInput.objects.all()
    return render(request, 'predict.html', {'user_inputs': user_inputs})

def tokenize_text(request):
    # Provide the path to your Excel file
    excel_file_path = r"dzo_nextword\model_tokenizer_dataset\Dataset5k.xlsx"

    try:
        # Load the Excel file into a DataFrame
        df = pd.read_excel(excel_file_path, sheet_name='Sheet1', usecols=['Dzongkha'])

        # Extract the text data from a specific column (e.g., 'Dzongkha')
        text = df['Dzongkha'].to_string(index=False)

        # Preprocessing the text
        text = re.sub(r'[a-zA-Z0-9]', '', text)
        text = text.replace('#', '')
        text = text.replace('?', '')
        text = text.replace('།', '')

        # Removing the dzongkha period after the word
        text = text.replace(' ', '$')
        text = text.replace('$', ' ')
        text = text.replace(' $', ' ')
        text = text.replace('$', '')

        # Tokenize the words
        tokenizer = Tokenizer()
        tokenizer.fit_on_texts([word for word in text.split()])

        # Save the tokenizer using pickle
        with open('/content/tokenizer.pkl', 'wb') as tokenizer_file:
            pickle.dump(tokenizer, tokenizer_file)

        return JsonResponse({'success': 'Tokenizer saved successfully.'})

    except Exception as e:
        # Handle exceptions appropriately
        return JsonResponse({'error': str(e)})