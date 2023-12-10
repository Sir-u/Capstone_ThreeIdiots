import json

# File paths
input_file_path = "./Downloads/NIKL_MP(v1.1)/NXMP1902008040.json"
output_file_path = "./Downloads/NIKL_MP(v1.1)/NNG_SET.tsv"

# Read the JSON file and load its content
with open(input_file_path, "r", encoding="utf-8") as file:
    data = json.load(file)

# Set to keep track of unique form values
unique_forms = set()

# Open the TSV file for writing
with open(output_file_path, "w", encoding="utf-8") as tsv_file:
    # Iterate through all documents
    for document in data["document"]:
        # Iterate through all sentences in the document
        for sentence in document["sentence"]:
            # Extract the "form" and "label" values from the sentence's morphemes
            form = [morpheme["form"] for morpheme in sentence["morpheme"]]
            labels = [morpheme["label"] for morpheme in sentence["morpheme"]]

            # Write each "form" and "label" pair to the TSV file, excluding "ss" and "sn" labels and forms with less than 2 characters
            for i in range(len(form)):
                if labels[i] not in ["SS", ""] and len(form[i]) >= 2 and form[i] not in unique_forms:
                    tsv_file.write(form[i] + "\t" + labels[i] + "\n")
                    unique_forms.add(form[i])
