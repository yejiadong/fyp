
# Main Annotation Website

The annotation website runs on **Vue 3.0** frontend and **Django** backend. Due to limited development time, it is not guaranteed to be free from all bugs. Careful testing and customization is still required and strongly reccomended.

It uses the built-in Django SQL-LITE database. 

### Set-up
1. Unzip the file in order to get both backend and frontend folders. 
2. Navigate into the `backend` folder and do a `pip install requirements.txt` to install the dependencies for the backend database.
3. Navigate into the `frontend/label-app` folder and do a `npm install` to install all dependencies of the frontend folder. The node-modules have been included in case it makes it easier for the installation process.
4. In order to migrate the Django databases, do the following in the `backend/temporal_backend` folder:
`python manage.py makemigrations` followed by `python manage.py migrate`.


#### Running
1. Start the backend Django server first. Navigate into the `temporal_backend` folder and run `python manage.py runserver`. This should start the Django server.
2. Start the frontend next. Navigate into the `frontend/label-app` folder and run `npm run serve`. 
3. This should give you a link to access the frontend. 


#### File format that should be uploaded for annotation
- **id** - original id to identify the claim evidence pair
- **claim** - the claim
- **0** - the evidence
- **1** - the temporal labels in the claim (i.e. `"['born in 1919']"`)
- **2** - the temporal labels in the evidence
- **3** - the general justification by the GPT model
- **4** - the general facts label
- **5** - the relevant parts of the evidence sentence
- **6** - justification for whether the claim and evidence refer to the same entity
- **7** - whether the claim and evidence refer to the same entity
- **8** - the temporal facts label
- **9** - justification for the temporal facts label
- **10** - the topic of the claim and evidence
- **11** - the overall model label taking into consideration the temporal and general labels

Take note that you do not need to include **1** to **11** as those can be fetched by the model when annotators access the annotation page. However, you can also pre-fill these so that annotators will not have to waste time in waiting for the model to provide an output. 

Take note that you HAVE to follow the json structure exactly as it is. Two example JSON files that are supported are provided to you in the same folder for your reference. Please convert the data to the supported JSON format. 