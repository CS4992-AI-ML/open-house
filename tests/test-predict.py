from src.predict_price import predict


def predict_output():

    return predict(
        body={
            "body": {
                "Street_Display": "913/58 CHURCH AVENUE",
                "Street_Name": "PACIFIC HIGHWAY",
                "Locality": "PARRAMATTA",
                "Postcode": "X2145",
                "Status": "Current",
                "Listed_Price": 0,
                "Month_Listed": "May",
                "Days_Listed": 7,
                "Bedrooms": 2,
                "Bathrooms": 1,
                "Parking": 1,
                "Property_Type": "Unit",
                "Agency_Name": "McGrath",
                "Agent": "Leasing Team",
                "Area": 0,
                "Building_Area": 0,
                "Current_Owners": "nan",
                "Current_Owners_Address": "nan",
                "PDS_Property_ID": 1513061770,
                "PDS_Listing_ID": 87192212,
                "Government_Number": "NSW4370579",
                "Parent_Government_Number": "NSW4253054",
                "Relative_Month": 1,
            }
        }
    )


predict_output()
