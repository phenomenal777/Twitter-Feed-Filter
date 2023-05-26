from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize
import os
import csv
from statistics import mean
import torch
import pandas as pd
from transformers import BertTokenizer, BertModel

def embeddings():
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertModel.from_pretrained("bert-base-uncased")

    # Define a function to create embeddings for each tweet
    def create_avg_embeddings(tweet):
        # Tokenize the tweet and convert tokens to IDs
        inputs = tokenizer.encode_plus(tweet, add_special_tokens=True, return_tensors='pt')

        # Pass the input IDs through the model to get embeddings
        with torch.no_grad():
            outputs = model(**inputs)
            embeddings = outputs.last_hidden_state.mean(dim=1).squeeze()

        # Convert embeddings to a numpy array and return it
        return embeddings.mean(dim=0).numpy()

    # Create the 'data' directory if it doesn't exist
    data_folder = 'data/'
    os.makedirs(data_folder, exist_ok=True)

    # Initialize the list for average embeddings
    avg_embeddings = []

    # Loop through each text file in the data folder and create average embeddings
    for file_name in os.listdir(data_folder):
        file_path = os.path.join(data_folder, file_name)
        if not os.path.isfile(file_path):
            continue

        # Create average embeddings for the current text file
        current_avg_embeddings = create_avg_embeddings(file_path)

        # Convert current_avg_embeddings from NumPy array to list
        current_avg_embeddings = current_avg_embeddings.tolist()

        # Append the current average embeddings to the list
        avg_embeddings.append(current_avg_embeddings)

    # Print the type of avg_embeddings (should be list)
    print(avg_embeddings)

    # Create the 'embeddings' directory if it doesn't exist
    embeddings_directory = 'embeddings/'
    os.makedirs(embeddings_directory, exist_ok=True)

    # Loop through all the CSV files in the directory
    directory = '../go/files/'
    output_directory = 'embeddings'  # Output directory for saving the files

    # Create the output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            # Read in the tweets from the file
            filepath = os.path.join(directory, filename)
            # Create a DataFrame from the CSV file
            df = pd.read_csv(filepath)
            # Create embeddings for each tweet and store in a list
            embeddings = [create_avg_embeddings(tweet) for tweet in df['Tweet']]
            df['embedding'] = embeddings

            # Save the DataFrame with the new column as a new CSV file
            output_filename = 'embeddings_' + filename
            output_filepath = os.path.join(output_directory, output_filename)
            df.to_csv(output_filepath, index=False)

    # Define the directory path containing the CSV files
    directory = 'embeddings/'

    # Initialize the list for mean embedding differences
    mean_embedding_diff = []

    # Loop through all the CSV files in the directory
    for i, filename in enumerate(os.listdir(directory)):
        if filename.endswith('.csv'):
            # Read the CSV file
            file_path = os.path.join(directory, filename)
            df = pd.read_csv(file_path)

            # Get the current element from the list
            current_element = avg_embeddings[i]

            # Initialize the list for embedding differences
            embedding_diff = []

            # Calculate the absolute difference for each tweet in the current file
            for tweet_embedding in df['embedding']:
                embedding_diff.append(abs(tweet_embedding - current_element))

            # Calculate the mean embedding difference and append it to the list
            mean_diff = mean(embedding_diff)
            mean_embedding_diff.append(mean_diff)

    print(mean_embedding_diff)

    # Create the 'answers' directory if it doesn't exist
    output_directory = 'answers/'
    os.makedirs(output_directory, exist_ok=True)

    directory = 'embeddings/'

    for i, filename in enumerate(os.listdir(directory)):
        if filename.endswith('.csv'):
            file_path = os.path.join(directory, filename)
            df = pd.read_csv(file_path)

            # Get the current element from the list
            current_element = avg_embeddings[i]

            # Initialize the list for embedding differences
            embedding_diff = []

            # Calculate the absolute difference for each tweet in the current file
            for tweet_embedding in df['embedding']:
                embedding_diff.append(abs(tweet_embedding - current_element))

            # Add the differences to the dataframe as a new column
            df['difference'] = embedding_diff

            # Save the merged dataframe to the current file
            df.to_csv(file_path, index=False)

    directory = 'embeddings/'

    # Loop through all the CSV files in the directory
    for i, filename in enumerate(os.listdir(directory)):
        if filename.endswith('.csv'):
            # Read the CSV file
            file_path = os.path.join(directory, filename)
            df = pd.read_csv(file_path)

            # Get the current element from the list
            current_element = avg_embeddings[i]
            mean_diff = mean_embedding_diff[i]

            # Filter out tweets where the difference is greater than the mean difference
            df = df[df['difference'] <= mean_diff]

            # Drop the "difference" column
            df = df.drop(columns=['difference'])

            # Extract the trend name from the original filename
            trend = filename.split('_')[1].split('.')[0]

            # Define the output filename
            output_filename = f"answer_{trend}.csv"

            # Save the "Tweet" column to a new CSV file in the answers directory
            output_file_path = os.path.join(output_directory, output_filename)
            df['Tweet'].to_csv(output_file_path, index=False)


#embeddings()
