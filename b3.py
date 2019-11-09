class Tag:
    def __init__(self, tag, text,  klass = None, is_single = False,**atrr):
        self.tag = tag
        self.text = ''
        self.attributes = {}
        self.child = []
        self.is_single = is_single

        if klass is not None:
            self.attributes['class'] = ''.join(klass)

        for attribute, value in atrr.items():
            self.attributes[attribute] = value

    def __enter__(self):
        return self
    def __exit__(self, tag, text,  klass = None, is_single = False,**atrr):
        pass
    def __iadd__(self, other):
        self.child.append(other)
        return self
    def __str__(self):
        attrs = []
        for attribute, value in self.attributes.items():
            attrs.append('%s="%s"' % (attribute, value))
        attrs = " ".join(attrs)

        if len(self.child) > 0:
            opening = "<{tag} {attrs}>".format(tag=self.tag, attrs=attrs)
            if self.text:
                internal = "%s" % self.text
            else:
                internal = ""
            for child in self.child:
                internal += str(child)
            ending = "</%s>" % self.tag
            return opening + internal + ending
        else:
            if self.is_single:
                return "<{tag} {attrs}/>".format(tag=self.tag, attrs=attrs)
            else:
                return "<{tag} {attrs}>{text}</{tag}>".format(
                    tag=self.tag, attrs=attrs, text=self.text
                )


class HTML:
    def __init__(self, output=None):
        self.output = output
        self.child = []
    def __enter__(self):
        return self
    def __exit__(self, *args, **kwargs):
        if self.output is not None:
            with open(self.output, "w") as file:
                file.write(str(self))
        else:
            print(self)
    def __iadd__(self, other):
        self.child.append(other)
        return self
    def __str__(self):
        html = "<html>\n"
        for child in self.child:
            html += str(child)
        html += "\n</html>"
        return html


class TopLevelTag:
    def __init__(self, tag, **child):
        self.tag = tag
        self.child = []
    def __enter__(self):
        return self
    def __exit__(self, *args, **kwargs):
        pass
    def __iadd__(self, other):
        self.child.append(other)
        return self
    def __str__(self):
        html = "<%s>\n" % self.tag
        for child in self.child:
            html += str(child)
        html += "\n</%s>" % self.tag
        return html




def main(output=None):
    with HTML(output=output) as doc:
        with TopLevelTag("head") as head:
            with Tag("title", "hello" ) as title:
                head += title
            doc += head

        with TopLevelTag("body") as body:
            with Tag("h1", "Test", klass=("main-text")) as h1:
                body += h1

            with Tag("div", '', klass=("container", "container-fluid"), id="lead") as div:
                with Tag("p", "another test") as paragraph:
                    div += paragraph

                with Tag("img", '', is_single=True, src="/icon.png", data_image="responsive") as img:
                    div += img

                body += div

            doc += body


if __name__ == "__main__":
    main()