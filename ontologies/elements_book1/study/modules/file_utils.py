import datetime
import pandas as pd

def output_df(analyses: list, filename: str="output/analyses"):
    analyses_df = pd.DataFrame(analyses, columns=["proof_number", "background_concepts", "diff"])
    t = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{filename}_{t}.csv"
    analyses_df.to_csv(filename, index=False)
    print(f"Output: {filename}")
    return analyses_df