from decouple import config
from rest_framework import exceptions
from rest_framework.permissions import BasePermission


class OwnerPermission(BasePermission):
    message = "Only for the DeCHO Staff"

    def has_permission(self, request, view):
        user = request.META.get('OWNER_TOKEN')
        return  user == config("OWNER")

