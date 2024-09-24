import json
file_path = r"C:\Users\I8924\projects\os_safety-ai-rules\compliance_rules.json"

with open(file_path, 'r') as json_file:
    data = json.load(json_file)

result = data["analyze_result"] 

def save_to_json(data, file):
    output_file_path = f"{file}.json"
    with open(output_file_path, "w") as json_file:
        json.dump(data, json_file, indent=4)

pages = result["pages"]
pages_dict = {"pages": pages}
save_to_json(pages_dict, "pages_compliance")

tables = result["tables"]
tables_dict = {"tables": tables}
save_to_json(tables_dict, "tables")

paragraphs = result["paragraphs"]
paragraphs_dict = {"paragraphs": paragraphs}
save_to_json(paragraphs_dict, "paragraphs_compliance")  # Fixed the typo in the file name

styles = result["styles"]
styles_dict = {"styles": styles}
save_to_json(styles_dict, "styles")

contentFormat = result["contentFormat"]
contentFormat_dict = {"contentFormat": contentFormat}
save_to_json(contentFormat_dict, "contentFormat_compliance")

sections = result["sections"]
sections_dict = {"sections": sections}
save_to_json(sections_dict, "sections_compliance")

figures = result["figures"]
figures_dict = {"figures": figures}
save_to_json(figures_dict, "figures_compliance")