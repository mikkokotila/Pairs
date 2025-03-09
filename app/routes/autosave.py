def autosave(self):

    from flask import request, jsonify
    
    content = request.json["content"]
    row = request.json["row"]

    data = self.read_csv()
    data.iloc[row, 1] = content

    data.to_csv(self.csv_file_path + self.filename,
                index=False,
                header=False,
                sep="~",
                encoding="utf-8")

    return jsonify(status="saved")
