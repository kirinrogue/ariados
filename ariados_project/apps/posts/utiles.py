from ariados.models import Post


def generate_answer_title(parent_title):
    title = ''
    for i in range(1, 100):
        title = 'RE{0}: {1}'.format(i, parent_title)
        if not Post.objects.filter(title=title).exists():
            break
    return title
