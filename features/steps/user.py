from behave import given, when, then


@given(u'the API service is running')
def flask_setup(context):
    assert context.client and context.db


@when(u'i send a post request with "{username}" and "{password}"')
def post_request(context, username, password):
    context.response = context.client.post('/users/', data=dict(username=username, password=password),
                                           follow_redirects=True)
    assert context.response


@then(u'i should see the data user response')
def step_impl(context):
    assert 'admin' in str(context.response.data)
