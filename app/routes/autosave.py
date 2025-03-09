def autosave(self):

    from flask import request, jsonify

    from utils.read_csv import read_csv
    
    content = request.json["content"]
    row = request.json["row"]

    data = read_csv(self)
    data.iloc[row, 1] = content

    data.to_csv(self.csv_file_path + self.filename,
                index=False,
                header=False,
                sep="~",
                encoding="utf-8")

    return jsonify(status="saved")
