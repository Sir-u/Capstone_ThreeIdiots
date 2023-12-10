import json

# File paths
input_file_path = "./Downloads/NIKL_MP(v1.1)/NXMP1902008040.json"
output_file_path = "./Downloads/NIKL_MP(v1.1)/ner_SET.txt"

# Read the JSON file and load its content
with open(input_file_path, "r", encoding="utf-8") as file:
    data = json.load(file)

# Open the TSV file for writing
with open(output_file_path, "w", encoding="utf-8") as tsv_file:
    # Iterate through all documents
    for document in data["document"]:
        # Iterate through all sentences in the document
        for sentence in document["sentence"]:
            # Write the sentence text to the TSV file
            tsv_file.write(";" + sentence["form"] + "\n$" + sentence["form"] + "\n")

            count = 1
            # Write each "form" and "label" pair to the TSV file, excluding "SS" and "SN" labels
            # and forms with less than 2 characters
            for morpheme in sentence["morpheme"]:
                form, label = morpheme["form"], morpheme["label"]
                if label not in ["SS", "SN"] and len(form) >= 2:
                    tsv_file.write(str(count) + "\t" + form + "\t" + label + "\n")
                    count += 1
            tsv_file.write("\n")
