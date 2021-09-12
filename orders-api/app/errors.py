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

    
    def get_integrity_error(exc):
        error = 'insert or update on table "orders" violates foreign key constraint "orders_user_id_fkey"'
        error_message = str(exc.orig)
        if error in error_message:
            body = exc.params
            user_id = body["user_id"]
            str_user_id = str(user_id)
            error_message = {"user_id": f"{str_user_id} was not found."}
        else:
            error_message = {"message": error_message}
        return JSONResponse(status_code=400, content=error_message)
