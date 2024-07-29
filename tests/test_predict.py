from chalice_app.chalicelib.predict_price import predict_price


def predict_output():

    return predict_price(
        body={
            "locality": "PARRAMATTA",
            "postcode": "2116",
            "monthListed": "May",
            "bedrooms": 2,
            "bathrooms": 1,
            "parkingSpaces": 1,
            "propertyType": "House",
            "agencyName": "McGrath",
            "agentName": "Leasing Team",
            "landArea": 550,
            "floorArea": 200,
            "relativeMonth": 1,
        }
    )


output = predict_output()
print(output)
assert 600 <= output <= 700, f"Output {output} is not within the expected range."
