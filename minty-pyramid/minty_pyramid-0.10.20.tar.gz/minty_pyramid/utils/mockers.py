# SPDX-FileCopyrightText: 2020 Mintlab B.V.
#
# SPDX-License-Identifier: EUPL-1.2

from minty.cqrs import UserInfo
from uuid import uuid4


def mock_protected_route(view):
    def view_wrapper(request):
        user_info = UserInfo(
            user_uuid=uuid4(), permissions={"permission": True}
        )

        return view(request=request, user_info=user_info)

    return view_wrapper
