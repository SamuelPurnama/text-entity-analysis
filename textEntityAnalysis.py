from google.cloud import language_v1

# Initialize the client for Google Cloud Natural Language API
client = language_v1.LanguageServiceClient()

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

    # Extract the base item name from entities and include brand names (ORGANIZATION)
    item_name = None
    for entity in response.entities:
        print(f"Entity: {entity.name}, Type: {entity.type_}")  # Debug: Print entity details

        # Check if entity is an organization
        if entity.type_ == language_v1.Entity.Type.ORGANIZATION:
            print(f"Brand or organization found: {entity.name}")  # Debug: Print if brand is recognized

        if entity.type_ in [language_v1.Entity.Type.CONSUMER_GOOD, language_v1.Entity.Type.OTHER, language_v1.Entity.Type.ORGANIZATION]:
            item_name = entity.name
            print(f"Base item name or brand found: {item_name}")  # Debug: Print base item name
            break  # Use the first matching entity

    # If an item name was found, concatenate adjectives to it
    if item_name:
        adjectives = []
        for token in syntax_response.tokens:
            word = token.text.content
            pos_tag = language_v1.PartOfSpeech.Tag(token.part_of_speech.tag).name

            # Skip verbs (POS: VERB)
            if pos_tag == 'VERB':
                print(f"Skipping verb: {word}")  # Debug: Print skipped verb
                continue

            # Collect adjectives to prepend to the item name
            if pos_tag == 'ADJ':
                adjectives.append(word)
                print(f"Adjective found: {word}")  # Debug: Print each found adjective

        # Concatenate adjectives and the item name
        if adjectives:
            item_name = " ".join(adjectives) + " " + item_name
            print(f"Final constructed item name with adjectives: {item_name}")  # Debug: Print final item name

    # Extract quantity from the entities
    quantity = None
    for entity in response.entities:
        if entity.type_ == language_v1.Entity.Type.NUMBER:
            quantity = entity.name
            print(f"Quantity found: {quantity}")  # Debug: Print quantity

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
