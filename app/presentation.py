from uuid import UUID

from flask import Blueprint, Response, jsonify, make_response, request

from app.infrastructure import Repository
from app.model.exceptions import UserAlreadyExistsException
from app.model.forms import UserForm
from app.model.user import User


class Controller:
    blueprint = Blueprint("app", __name__)

    def __init__(self, repository: Repository):
        self._repository = repository

    @blueprint.post("/save")
    def save_user(self) -> Response:
        form = UserForm(request.form)
        if not form.validate():
            return make_response("", 400)

        user = User(
            external_id=form.external_id.data,
            name=form.name.data,
            email=form.email.data,
            date_of_birth=form.date_of_birth.data,
        )
        try:
            self._repository.save_user(user)
        except UserAlreadyExistsException as e:
            return make_response(e, 409)
        else:
            return make_response("", 200)

    @blueprint.get("/<uuid:external_id>")
    def get_user(self, external_id: UUID) -> Response:
        user = self._repository.get_user(external_id)

        if user is not None:
            return jsonify(user)
        else:
            return make_response("", 404)
