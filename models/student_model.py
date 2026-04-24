def student_schema(data):

    student = {
        "name": data["name"],
        "email": data["email"],
        "department": data["department"],
        "semester": data["semester"]
    }

    return student