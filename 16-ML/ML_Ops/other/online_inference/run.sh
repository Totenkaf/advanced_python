if [ -z $PATH_TO_MODEL ]
then
    export PATH_TO_MODEL="model.pkl"
fi

if [ -z $PATH_TO_TRANSFORMER ]
then
    export PATH_TO_TRANSFORMER="transformer.pkl"
fi

if [[ ! -f $PATH_TO_MODEL ]]
then
    gdown https://drive.google.com/uc?id=1K-InZyYWkCdsMpE3FfGpBD3keNWoNk8h --output=$PATH_TO_MODEL
else
    echo "model exists"
fi

if [[ ! -f $PATH_TO_TRANSFORMER ]]
then
    gdown https://drive.google.com/uc?id=11OW_epYTQjJIgKXoTQWGSZkNS9VbmVpM --output=$PATH_TO_TRANSFORMER
else 
    echo "transformer exists"
fi

uvicorn main:app --reload --host 0.0.0.0 --port 8000
