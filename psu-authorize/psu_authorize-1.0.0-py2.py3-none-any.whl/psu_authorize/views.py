from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden
from psu_base.classes.Log import Log
from psu_base.services import error_service, message_service
from psu_base.decorators import require_authority
from psu_authorize.services import authorization_service
from psu_base.classes.DynamicRole import DynamicRole


log = Log()

# ToDo: Error Handling/Messages

# Permission Checking
authorize_roles = DynamicRole().security_officer()


@require_authority(authorize_roles)
def index(request):
    """
    Menu of authorized applications
    """
    log.trace()
    allowed_apps = authorization_service.get_manageable_applications()
    return render(
        request, 'index.html',
        {'allowed_apps': allowed_apps}
    )


@require_authority(authorize_roles)
def app(request, app_code):
    """
    Permissions for specified app
    """
    log.trace()
    # Gather app info
    allowed_apps = authorization_service.get_manageable_applications()
    app_info = None
    for aa in allowed_apps:
        if aa.code == app_code:
            app_info = aa

    # Make sure user can authorize for this app
    if app_code not in [aa.code for aa in allowed_apps]:
        message_service.post_error(
            f"You are not authorized to manage permissions for {app_code}"
        )
        return redirect('authorize:authorize_index')

    # Generate a list of application options for the user to select from when granting
    application_options = authorization_service.get_manageable_application_options()
    has_app_options = len(application_options) > 1

    # Get permissions for this app
    app_permissions = authorization_service.get_app_permissions(app_code)

    return render(
        request, 'app.html',
        {
            'app_code': app_code,
            'app_info': app_info,
            'app_permissions': app_permissions,
            'application_options': application_options,
            'has_app_options': has_app_options,
        }
    )


@require_authority(authorize_roles)
def revoke(request, permission_id):
    """
    Revoke one assigned permission
    """
    log.trace()
    try:
        permission_instance = authorization_service.get_permission(permission_id)
        if permission_instance:
            # Make sure user can authorize for this app
            allowed_apps = authorization_service.get_manageable_application_codes()
            if permission_instance.app_code in allowed_apps:
                authorization_service.revoke_permission(permission_id)
                message_service.post_success(
                    f"Permission #{permission_id} has been revoked"
                )
                return HttpResponse('success')
            else:
                message_service.post_error(
                    f"You are not authorized to manage permissions for {permission_instance.app_code}"
                )
        else:
            message_service.post_error(
                f"Unable to find permission #{permission_id}"
            )
    except Exception as ee:
        error_service.unexpected_error("Unable to revoke permission", ee)

    return HttpResponseForbidden()


@require_authority(authorize_roles)
def grant(request):
    """
    Grant one authority to one or more users
    """
    log.trace()
    try:
        app_code = request.POST.get('app_code')
        authority_id = request.POST.get('authority_id')
        grantee = request.POST.get('grantee')

        new_permissions = authorization_service.grant_permission(app_code, authority_id, grantee)
        authority_code = new_permissions[0].authority_code if new_permissions and len(new_permissions) > 0 else None
        return render(
            request, '_app_permission_rows.html',
            {
                'permissions': {authority_code: {'new': new_permissions}}.items()
            }
        )
    except Exception as ee:
        error_service.unexpected_error("Unable to grant permission", ee)
        return HttpResponseForbidden()
