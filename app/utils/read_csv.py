def read_csv(self):

    import pandas as pd

    # Read in the local datastore from csv
    data = pd.read_csv(self.csv_file_path + self.filename,
                        header=None,
                        sep="~",
                        dtype=str,
                        keep_default_na=False,
                        engine="c")
    
    # If the CSV has just one column, add a target column
    if data.shape[1] == 1:
        data["target"] = ""
        data['style'] = "Normal"

    return data
