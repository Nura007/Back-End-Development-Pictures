# Back-End-Development-Pictures

Flask Pictures service for the IBM Back-End Development capstone.
Based on [IBM's official starter](https://github.com/ibm-developer-skills-network/luggb-Back-End-Development-Pictures).
The original Apache 2.0 license and original course tests are preserved.

## Run locally

Use Python 3.14. Create and activate a virtual environment, then run:

```sh
python -m pip install -r requirements.txt
python app.py
```

The service listens on http://127.0.0.1:8080.
Endpoints: GET /health, GET /count, GET /picture, GET /picture/<id>,
POST /picture, PUT /picture/<id>, DELETE /picture/<id>.

Picture fields: integer id; pic_url, event_country, event_state, event_city,
event_date strings. New records return 201; deletion returns 204; missing records
return 404. Duplicate creation returns 302 to match the course's test contract.
Data is held in memory and resets on restart, as in the starter project.

## Course tests

```sh
python -m pytest -v -k "test_health or test_count"
python -m pytest -v -k "test_data_contains_10_pictures or test_get_picture or test_pictures_json_is_not_empty"
python -m pytest -v -k test_post_picture
python -m pytest -v
```

All 11 original tests passed locally. Run the full suite for update/delete
evidence: those original tests depend on the POST test adding its fixture first.

## Container and Code Engine

```sh
docker build -t pictures:1.0 .
docker run --rm -p 3000:3000 pictures:1.0
```

The container listens on port 3000. Push the image to your lab registry, then
use your selected IBM Cloud Code Engine project:

```sh
ibmcloud ce project current
ibmcloud ce app create --name pictures --image YOUR_REGISTRY/YOUR_NAMESPACE/pictures:1.0 --port 3000
```

Replace the registry placeholders with your actual image. Cloud deployment has
not yet been performed; no deployment output is supplied as if it had succeeded.

