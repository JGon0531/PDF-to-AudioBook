from gtts import gTTS
import PyPDF2
language = "en"

valid_file = True
while valid_file:
    print("Give a text based pdf file to convert to an audiobook mp3")
    pdf_file_name = input("Please enter the name of your file: ")
    if pdf_file_name[-4] == ".pdf":
        valid_file = False
    elif "." in pdf_file_name:
        print("Please input a valid file type")
    else:
        pdf_file_name += ".pdf"
        valid_file = False
    
    

pdf_file_obj = open(pdf_file_name, "rb")
pdfreader = PyPDF2.PdfReader(pdf_file_obj)
page_length = len(pdfreader.pages)
converted_doc = {}

for i in range(page_length):
    pageObj = pdfreader.pages[i]

    converted_doc[i] = {
        "Page": f"{i + 1}",
        "Chapter": "",
        "Text": []}

    raw_text = pageObj.extract_text().split(".")
    sentences = [item.replace("\n", " ") + "." for item in raw_text]

    for line in sentences:
        if "Chapter" in line:
            ending_index = line.index("Chapter") + len("Chapter XX")
            converted_doc[i]["Chapter"] = line[:ending_index]
            sentences[sentences.index(line)] = line[ending_index:]
    converted_doc[i]["Text"] = sentences

for page in converted_doc:
    to_be_read_out = ""
    new_files_name = pdf_file_name[:-4] + "-page-" + str(page+1) + ".mp3"

    for item in converted_doc[page]["Text"]:
        to_be_read_out += item

    to_be_converted = gTTS(text=to_be_read_out, lang=language, slow=False)
    to_be_converted.save(new_files_name)
