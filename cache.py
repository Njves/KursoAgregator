def build_key(request):
    page = request.args.get('page')
    return f'index_{page}'