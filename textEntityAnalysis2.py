from google.cloud import language_v1

# Initialize the client for Google Cloud Natural Language API
client = language_v1.LanguageServiceClient()

# List of words to exclude from the item name if tagged as NOUN
exclude_words = {"wait", "holdon"}

def analyze_text(input_text):
    # Prepare the document for analysis
    document = language_v1.Document(content=input_text, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Call the API to analyze entities and syntax
    response = client.analyze_entities(document=document)
    syntax_response = client.analyze_syntax(document=document)

    # Debug: Print tokens and their parts of speech
    print("\nTokens and parts of speech:")
    for token in syntax_response.tokens:
        print(f"Word: {token.text.content}, POS: {language_v1.PartOfSpeech.Tag(token.part_of_speech.tag).name}")

    # Extract the quantity and use it as a marker for starting item name construction
    quantity_found = False
    item_name_parts = []
    quantity = None

    # Iterate through the entities to extract the quantity
    for entity in response.entities:
        if entity.type_ == language_v1.Entity.Type.NUMBER:
            quantity = entity.name
            quantity_found = True
            print(f"Quantity found: {quantity}")  # Debug: Print quantity
            break  # Use the first matching quantity

    # Start processing tokens after the quantity to build the item name
    if quantity_found:
        start_collecting = False
        for token in syntax_response.tokens:
            word = token.text.content
            pos_tag = language_v1.PartOfSpeech.Tag(token.part_of_speech.tag).name

            # Begin collecting item name parts after the number is found
            if word == quantity:
                start_collecting = True
                continue

            if start_collecting:
                # Include both nouns and adjectives, but exclude specific unwanted words
                if pos_tag in ['NOUN', 'ADJ'] and word.lower() not in exclude_words:
                    item_name_parts.append(word)
                    print(f"Added to item name: {word} (POS: {pos_tag})")  # Debug: Print added word

    # Join the collected parts to form the full item name
    item_name = " ".join(item_name_parts) if item_name_parts else None

    # Debug: Print the constructed item name
    print(f"\nConstructed item name: {item_name}")

    return item_name, quantity

if __name__ == "__main__":
    # Prompt for input text
    input_text = input("Enter the text to analyze (e.g., 'Add 2 large blue Adidas string bags'): ")

    # Analyze the input text
    item_name, quantity = analyze_text(input_text)

    # Print results
    if item_name and quantity:
        print(f"\nName of item: {item_name}")
        print(f"Quantity: {quantity}")
    else:
        print("\nCould not extract both item name and quantity. Please try a different input.")
