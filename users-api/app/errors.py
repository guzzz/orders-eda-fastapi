from fastapi.responses import JSONResponse


class CustomError:

    def get_error(exc):
        try:
            errors_list = []
            for item in exc.errors():
                error = {}
                field = item.get("loc")[1]
                if item.get("type") in ("value_error.missing", "type_error.none.not_allowed"):
                    error["error"] = "Validation fails"
                    error["msg"] = f"Field {field} is required."
                else:
                    error["error"] = item.get("msg")
                    error["msg"] = f"Error on field/char {field}."
                errors_list.append(error)
            error_message = {"errors": errors_list}
        except:
            error_message = {"errors": str(exc)}
        return JSONResponse(status_code=400, content=error_message)
