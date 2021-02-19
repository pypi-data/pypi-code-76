"""API response mocks module"""

PROFILES = {
    '_embedded': {
        'profiles': [
            {
                'id': 'provider|profile-id',
                'name': 'profile name'
            }
        ]
    }
}

WORKSPACES = {
    '_embedded': {
        'workspaces': [
            {
                'id': '89969253-723d-415d-b199-bcac2aaa4cde',
                'name': 'workspace 1'
            },
            {
                'id': '9f47ec52-41da-46eb-be7e-f7ef65490081',
                'name': 'workspace 2'
            }
        ]
    },
    'page': {
        'totalElements': 2
    }
}

DATASET = {
    'id': 'b944735d-cb69-49a2-b871-3ced1fed5b02',
    'published': '2020-12-09T16:48:10.132',
    'alias': 'test1',
    'workspaceId': '8566fe13-f30b-4536-aecf-b3879bd0910f',
    'source': 'Reuben F Channel',
    'title': 'test1',
    'description': None,
    'questions': None,
    'rawData': None,
    'visualisation': None,
    'metadata': None,
    'query': None,
    'likeCount': 0,
    'likedByProfiles': [],
    'commentCount': 0,
    'viewCount': 0,
    'created': '2020-12-09T14:42:20.82',
    'score': 1.0
}

DATASETS = {
    '_embedded': {
        'datasets': [
            {
                'id': '280a2ab2-f30e-4200-b765-ed73af3d63db',
                'alias': 'dataset-1',
                'title': 'dataset 1'
            },
            {
                'id': 'c50d444f-a71d-4f29-a2cc-ee905ddc1e15',
                'alias': 'dataset-2',
                'title': 'dataset 2'
            }
        ]
    },
    'page': {
        'totalElements': 2
    }
}

DATA = {
    'google_analytics_active_user_stats.total_daily_active_users': 9,
    'google_analytics_active_user_stats.total_weekly_active_users': 26,
    'google_analytics_active_user_stats.total_14d_active_users': 75,
    'google_analytics_active_user_stats.total_28d_active_users': 201,
}

DATA_CSV = """\
"Total Daily Active Users","Total Weekly Active Users","Total 14d Active Users","Total 28d Active Users"
"9","26","75","201"
"""
