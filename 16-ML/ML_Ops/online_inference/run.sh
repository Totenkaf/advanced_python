if [ -z $PATH_TO_MODEL ]
then
    export PATH_TO_MODEL="LogisticRegressionCV_model.pkl"
fi

if [[ ! -f $PATH_TO_MODEL ]]
then
    wget https://ml_project.hb.bizmrg.com/models/LogisticRegressionCV_model.pkl --output-document=$PATH_TO_MODEL
    echo $PATH_TO_MODEL
else
    echo "Model exists"
fi

uvicorn main:app --reload --host 0.0.0.0 --port 8000
