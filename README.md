# API for calculating Salary Details
This repo implements a simple API that takes net salary and allowances of a user and return the salary details.

## Build
Clone the project and change to the root of the project. Then run the command below to build it:
```shell
docker-compose up income-api
```

# Tests
To execute the test. Run the command below:
```shell
docker-compose up tests
```

## Endpoint
The endpoint is expose on the url `http://localhost:8000/api/salary/details`.

The documentation page for the endpoint: `http://localhost:8000` or `http://localhost:8000/api/docs`

To use the API, make a POST request to url `http://localhost:8000/api/salary/details` using the payload below:

```json
{
  "net_salary": 3000
}
```

OR

```json
{
  "net_salary": 3000,
  "allowances": [
    {
      "name": "Travel",
      "amount": "30"
    }
  ]
}
```

NOTE: The endpoint can also be tested using the documentation page.