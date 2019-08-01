def egusi_soup(category_id):
    return {
        'title':
        'Egusi soup',
        'description':
        'best local soup in nigeria for occasions',
        'ranking':
        1,
        'category':
        category_id,
        'metadata': [{
            'name': 'ingredient',
            'data_type': 'enum',
            'value': 'oil, ogiri, salt, fish'
        }, {
            'name': 'duration',
            'data_type': 'text',
            'value': '5 hours'
        }]
    }


def jellof_rice(category_id):
    return {
        'title': 'Jellof rice',
        'description': 'Best rice delicacy across west africa',
        'ranking': 1,
        'category': category_id
    }


def jellof_rice_update(category_id):
    return {
        'title': 'Jellof rice',
        'description': 'Greatest rice delicacy of all time',
        'ranking': 1,
        'category': category_id
    }


def spaghetti(category_id):
    return {
        'title': 'Spaghetti',
        'description': 'Awesome noodles for the kids',
        'ranking': 1,
        'category': category_id
    }


invalid_favourite = {
    'title':
    '90987sjfksdfsdf shdjkfhsjkdfjksdf shdjfkhsjfksdf hjskdhfjksdf hsjdkfhjsdkf hjskshdjfksdfsdf hjskdhfjksdfg ',
    'description': [],
    'ranking': 'invalid-ranking',
    'category': 'invalid-category',
    'metadata': 'invali-metadata'
}

invalid_metadata = [{'name': [], 'data_type': 'stuff', 'value': {}}]


def color_metadata(favourite_id):
    return {
        'favourite': favourite_id,
        'name': 'color',
        'value': 'red',
        'data_type': 'text'
    }


invalie_metadata_2 = {
    "name":
    "extra sdfljksdfsdf sdfkjsdkfsdf sdfsdfsdf sfsdfsdf sdfsfsf ingredients",
    "data_type": "wonderful",
    "value": [],
    "favourite": {}
}


def brite_core(category):
    return {
        'title': 'Brite Core',
        'description': 'Best company',
        'ranking': 3,
        'category': category
    }


def brite_core_update(category):
    return {
        'title': 'BriteCore',
        'description': 'Best company for insurance softwares',
        'ranking': 10,
        'category': category
    }
