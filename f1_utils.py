import pandas as pd

def read_f1(filename):
    df = pd.read_csv(filename)
    df.columns = ['model_id', 'run_id', 'element_count', 'seed', 'accuracy', 'f1', 'memory']
    df = df[['element_count', 'f1']]
    # df = df[['element_count', 'accuracy']]
    # df.columns = ['element_count', 'f1']
    df = df.groupby(['element_count']).agg(['mean', 'std']).reset_index()
    df.columns = ['element_count', 'Mean F1', 'f1 std']
    return df

