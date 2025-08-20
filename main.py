from flask import Flask , request , jsonify
import os as so
import random
from datetime import datetime
from  llama_index.core import SimpleDirectoryReader

os = Flask(__name__)
UPLOAD_FOLDER = 'C:/Users/kowsh/OneDrive/Desktop/NITRO'
so.makedirs(UPLOAD_FOLDER, exist_ok=True)

file_ids = {}
file_names = {}


@os.route("/files",methods=["POST"]) 
def get_files():
    id = 0
    if 'file' in request.files:
        file = request.files['file']
        if file.filename != '':
            while True:
                id = random.randint(1000, 9999)
                if id not in file_ids.keys() and str(file.filename) not in file_names.keys():
                    file_ids[id] = [file.filename,file.content_type,f"{(len(file.read()) / (1024 * 1024)):.2f} MB",datetime.utcnow().isoformat()]
                    file_names[str(file.filename)] = int(id)
                    file.seek(0)
                    break
                else:
                    file_id = file_names[str(file.filename)]
                    return jsonify({"message":"File already uploaded" ,"Metadata": {"file id":file_id ,"filename": file_ids[file_id][0],"status": "ready to use","size": file_ids[file_id][2],"progress": "100%"}}),400
            file.save(f'C:/Users/kowsh/OneDrive/Desktop/NITRO/{file.filename}')
            return jsonify({'message': 'File uploaded successfully',"file id":id , 'filename': file_ids[id][0] , "File Type":file_ids[id][1] ,"File size":file_ids[id][2] , "Date Created":file_ids[id][-1]}), 200
    return jsonify({"message":"Error uploading file"}),400

@os.route("/files",methods = ["GET"])
def alldet():

    return jsonify({"Complete Data Info":(file_ids)})


@os.route("/files/<int:file_id>/progress",methods=["GET"])
def get_prof(file_id):
    if file_id not in file_ids.keys():
        return jsonify({"error": "unknown file_id"}), 404
        
    file_created_time = datetime.fromisoformat(file_ids[file_id][-1])
    current_time = datetime.utcnow()
    elapsed_seconds = (current_time - file_created_time).total_seconds()
        
    processing_duration = 10  
        
    if elapsed_seconds < processing_duration:
        progress_percent = min(100, int((elapsed_seconds / processing_duration) * 100))
        if progress_percent < 20:
            status = "uploading"
        elif progress_percent < 100:
            status = "processing"
        else:
            status = "ready to use"
        

        progress = f"{progress_percent}%"
    else:
        status = "ready to use"
        progress = "100%"
    
    return jsonify({"file id": file_id, "filename": file_ids[file_id][0],"status": status, "Size": file_ids[file_id][2], "Progress": progress}) , 200


    # if file_id  not in file_ids.keys():
    #     return jsonify({"error": "unknown file_id"}), 404
    # return jsonify({"file id":file_id ,"filename": file_ids[file_id][0],"status": "ready to use","size": file_ids[file_id][2],"progress": "100%"}),200


@os.route("/files/<int:file_id>/",methods=["GET"])
def get_onef(file_id):
    if file_id  not in file_ids.keys():
        return jsonify({"error": "unknown file_id"}), 404 #"message": "File upload or processing in progress. Please try again later."
    
    file_id = int(file_id)
    reader = SimpleDirectoryReader(input_files=["./" + str(file_ids[file_id][0])])
    serialized_docs = []
    documents = reader.load_data()
    for doc in documents:
        doc_dict = {
            "doc_id": str(doc.id_),   
            "text": doc.text,         
            "metadata": {
                k: str(v)  for k, v in doc.metadata.items() if k in ["page_label","text"]
            }
        }
        serialized_docs.append(doc_dict)

    # reader = SimpleDirectoryReader(input_files=[file_path])    
    
    return jsonify({"file id":file_id , "filename": file_ids[file_id][0] ,"File Type":file_ids[file_id][1] ,"File size":file_ids[file_id][2] , "Date Created":file_ids[file_id][-1] , "file content": serialized_docs}) 
    
@os.route("/files/<int:file_id>",methods=["DELETE"])
def dele(file_id):
    if file_id not in file_ids.keys():
        return jsonify({"error": "unknown file_id"}), 404 #"message": "File upload or processing in progress. Please try again later."
    t = file_ids[file_id][0]
    file_path = UPLOAD_FOLDER+"/"+str(t)
    if so.path.exists(file_path):
        so.remove(file_path)
        del file_ids[file_id]
        del file_names[str(t)]
        return jsonify({"message": f"File '/{str(t)}' deleted successfully."})
    else:
        print({"message" : f"File '/{str(t)}' not found."})

if __name__ == '__main__':
    os.run(debug=True)
