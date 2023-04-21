
# Classifier Code (Transformers and Feature Generation)

The code here contains all the necessary code used for the following:

- Preprocessing the initial data to the format that was used for subsequent model generation
- Transformer model usage and tests (from Huggingface Repositories)
- Feature Generation (using a mixture of Python libraries)
- Model trials (tree-based, and LSTMs)

#### samples.json
- Original json dataset

#### samples.csv
- Original main dataset

#### samples_12870.csv
- Filtered dataset with only 12870 entries

#### Preprocessing + Modelling.ipynb
- This file contains the main code for all preprocessing and modelling for the classifier model (non-gpt)

#### xgboost_final_model
- Final xgboost model used

#### xgboost_final_reduced
- Final xgboost model with reduced feature set

#### test_df.csv
- Test set used for final model evaluation

#### Predict.ipynb
- This prediction file can be used to pass new entries / data to predict a label for. Take note that files should be taken in as csvs with a claim and evidence column. 

Also, embeddings used in the code are the Glove 300D ones, so please download them and ensure that they are accessible by the code.