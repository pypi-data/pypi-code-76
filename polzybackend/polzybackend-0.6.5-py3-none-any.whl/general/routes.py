from flask import jsonify, request, current_app
from polzybackend.general import bp
from polzybackend.utils.import_utils import all_stages
from polzybackend import auth


@bp.route('/stages')
def stages():
    #
    # returns list of all available stages for login
    #

    try:
        # get all stages
        stages = all_stages()()
        current_app.logger.debug(f"Value of stages: {stages}")

    except Exception as e:
        current_app.logger.warning(f'Failed to get All Stages: {e}')
        stages = []

    return jsonify(stages), 200


@bp.route('/values', methods=['POST'])
@auth.login_required
def values():
    #
    # returns value list
    #

    # get post data
    data = request.get_json()

    try:
        # get parent instance from app store
        # try policies first
        instance = current_app.config['ANTRAGS'].get(data['instanceId'])
        if instance is None:
            # try antrags then
            instance = current_app.config['POLICIES'].get(data['instanceId'])
            if instance is None:
                raise Exception(f'Instance of with id {data["instanceId"]} not found in PoLZy storage. Most probably app restarted.')

        # get value list
        result = instance.getValueList(data.get('valueListName'))
        return jsonify(result), 200
    except Exception as e:
        current_app.logger.exception(f'Faild to get value-list for paylod {data}\n{e}')
    
    return jsonify({'error': f'Failed to get value-list'}), 400

