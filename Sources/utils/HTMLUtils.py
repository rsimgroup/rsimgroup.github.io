class HTMLUtils:
    @staticmethod
    def a(content='', href='', class_is=''):
        content_value = content
        url_value = ' href="' + href + '"' if href != '' else ''
        class_value = ' class="'+class_is+'"' if class_is != '' else ''
        if url_value != '':
            return '<a' + url_value+ class_value + ' target="blank">' + content_value + '</a>'
        else:
            return content_value


    @staticmethod
    def li(content='', class_is=''):

        if content == '':
            return ''
        if class_is == '':
            return '<li>'+content+'</li>'
        else:
            return '<li class="'+class_is+'">'+content+'</li>'

    @staticmethod
    def strong(content=''):
        if content == '':
            return ''
        return '<strong>'+content+'</strong>'

    @staticmethod
    def em(content=''):
        if content == '':
            return ''
        return '<em>'+content+'</em>'

    @staticmethod
    def td(content='', class_is='', style=''):
        class_value = ''
        if class_is !='':
            class_value = ' class="'+class_is+'"'
        style_value = ''
        if style != '':
            style_value = ' style="'+style+'"'
        return '<td' + class_value + style_value + '>' + content + '</td>'

    @staticmethod
    def img(alt='', height='', width='', src=''):
        if src == '':
            return '<img>'
        src_value = ' src="'+src+'"'
        alt_value = ''
        if alt != '':
            alt_value = ' alt="'+alt+'"'
        width_value = ''
        if width != '':
            width_value = ' width="'+width+'"'
        height_value = ''
        if height != '':
            height_value = ' height="'+height+'"'
        return '<img' + alt_value + width_value + height_value + src_value + '>'

    @staticmethod
    def span(content='', class_is=''):
        content_value = content
        class_value = ' class="' + class_is + '"' if class_is != '' else ''
        return '<span' + class_value + '>' + content_value + '</span>'

    @staticmethod
    def tr(content='', class_is=''):
        content_value = content
        class_value = ' class="' + class_is + '"' if class_is != '' else ''
        return '<tr' + class_value + '>' + content_value + '</tr>'

    @staticmethod
    def p(content='', class_is=''):
        content_value = content
        class_value = ' class="' + class_is + '"' if class_is != '' else ''
        return '<p' + class_value + '>' + content_value + '</p>'

    @staticmethod
    def connect_elements(*args, delimiter=', '):
        connect = [str(element)+delimiter for element in args if str(element) != '']
        return ''.join(connect).strip(delimiter).strip()

